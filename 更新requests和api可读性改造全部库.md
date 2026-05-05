# requests 和 API 可读性改造全部库方案

## 目标范围

本方案面向以下内部 provider：

- `voice_hub/providers/minimax`
- `voice_hub/providers/glm`
- `voice_hub/providers/aliyun/qwen_tts`
- `voice_hub/providers/aliyun/cosyvoice`

`mimo` 已经完成 `api.py + requests + MimoTTS(api=...)` 的改造，可以作为本轮全库改造的样板。

本轮目标：

- 所有手写 HTTP 请求从 `urllib` 改为 `requests`。
- 每个 provider 新增或收敛到 `api.py`，由 API 类统一管理 endpoint。
- provider 调用方只负责参数校验和 payload 构造，不再拼 URL、headers 或处理 requests 细节。
- 调用链保持单向、可调试：`调用参数 -> Request 对象 -> data/payload -> api.method(data) -> parser/bytes`。
- API 方法保持清晰写法，例如：

```python
def voice_clone(self, data: Mapping[str, object]) -> Mapping[str, Any]:
    return self.post("/voice_clone", data=data)
```

## 全局设计约定

### 统一分层

每个 provider 目录采用相同结构：

```text
provider/
  api.py        # requests 请求基类 + 业务 API 方法
  models.py     # 模型常量、endpoint 常量、Request dataclass
  payload.py    # 参数到 Request 的单向构造
  parser.py     # 响应解析和业务错误解析
  tts.py        # 对外 TTS provider，不直接处理 HTTP
  clone.py      # 如有克隆能力，只调用 api，不直接处理 HTTP
```

### API 类职责

API 层只做这些事：

- 保存 `api_key`、`base_url`、`timeout`、`requests.Session`。
- 统一设置 headers。
- 提供 `get()`、`post()`、`post_bytes()`、`stream_post()`、`post_file()`、`download_url()` 等通用方法。
- 把 `requests` 异常统一转换成 `ProviderError`。
- 暴露业务方法，例如 `t2a_v2()`、`voice_clone()`、`speech()`、`generation()`。

API 层不做：

- 不接收零散业务参数。
- 不构造 provider payload。
- 不解析音频业务结构。
- 不打印 key、token、headers、完整音频 base64/hex/data URI。

### Provider 调用方式

provider 中推荐形态：

```python
request = self.build_request(text, **overrides)
data = request.to_payload()
response = self.api.speech(data)
audio = self._parser.decode_audio(response)
```

需要流式时：

```python
request = self.build_request(text, stream=True, **overrides)
data = request.to_payload()
events = self.api.t2a_v2_stream(data)
return self._parser.iter_audio_chunks(events)
```

### 兼容策略

`mimo` 已经切换到 `api` 参数。其余 provider 建议同步切换为 `api` 参数，并对当前公开或测试依赖的 `transport` 做过渡处理：

- 内部主路径全部使用 `api`。
- 若类当前导出了 `*HTTPTransport` 或 `*SDKTransport`，保留为兼容适配器或别名，不再作为内部主实现。
- 测试从 `FakeTransport` 逐步改为 `FakeAPI`，断言接口级方法调用。
- `build_payload()`、`build_request()`、`speak()`、`bytes()`、`stream()` 等公开方法保持行为不变。

## requests 通用实现要求

普通 JSON 请求：

```python
response = self.session.request(
    method,
    self._url(path),
    headers=headers,
    json=data,
    timeout=self.timeout,
)
response.raise_for_status()
return response.json()
```

文件上传：

```python
with open(file_path, "rb") as file_obj:
    return self.post_file(
        "/files/upload",
        data={"purpose": purpose},
        files={"file": (path.name, file_obj, content_type)},
    )
```

流式 SSE：

```python
response = self.session.request(
    "POST",
    self._url(path),
    headers=headers,
    json=data,
    timeout=self.timeout,
    stream=True,
)
response.raise_for_status()
return _iter_sse_events(response)
```

二进制响应或下载：

```python
return response.content
```

错误转换：

- `requests.exceptions.HTTPError` -> `ProviderError("{prefix}: HTTP {status}: {body[:2000]}")`
- `requests.exceptions.Timeout` -> `ProviderError("{prefix}: timed out")`
- `requests.exceptions.RequestException` -> `ProviderError("{prefix}: {exc}")`
- JSON 非 mapping -> `ProviderError("{prefix}: invalid JSON response")`

## MiniMax 改造方案

### 当前问题

`minimax` 当前 HTTP 入口集中在 `transport.py`：

- `post()` 硬编码 `/t2a_v2`
- `stream()` 硬编码 `/t2a_v2`
- `upload_file()` 手写 multipart 到 `/files/upload`
- `voice_clone()` 手写 JSON 到 `/voice_clone`
- `download_url()` 使用 `urllib`

`tts.py` 和 `clone.py` 直接传 `base_url/api_key/payload/timeout` 给 transport，接口语义不够清楚。

### 文件级改造

新增：

```text
voice_hub/providers/minimax/api.py
```

更新：

```text
voice_hub/providers/minimax/models.py
voice_hub/providers/minimax/tts.py
voice_hub/providers/minimax/clone.py
voice_hub/providers/minimax/__init__.py
tests/test_minimax.py
```

`transport.py`：

- 若不作为公开 API，可删除。
- 若考虑外部直接 import，保留为薄适配器，但内部不再使用。

### endpoint 常量

在 `models.py` 增加：

```python
MINIMAX_T2A_PATH = "/t2a_v2"
MINIMAX_FILES_UPLOAD_PATH = "/files/upload"
MINIMAX_VOICE_CLONE_PATH = "/voice_clone"
```

### API 类建议

```python
class MinimaxAPI(MinimaxBaseAPI):
    def t2a_v2(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MINIMAX_T2A_PATH, data=dict(data))

    def t2a_v2_stream(self, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        return self.stream_post(MINIMAX_T2A_PATH, data=dict(data))

    def upload_file(self, file_path: str | Path, purpose: str) -> Mapping[str, Any]:
        return self.post_file(MINIMAX_FILES_UPLOAD_PATH, file_path=file_path, data={"purpose": purpose})

    def voice_clone(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MINIMAX_VOICE_CLONE_PATH, data=dict(data))

    def download_url(self, url: str) -> bytes:
        return self.get_bytes_url(url)
```

headers：

```python
{
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
```

文件上传时不要手动设置 JSON `Content-Type`，交给 `requests` 根据 `files` 生成 multipart boundary。

### Provider 调整

`MinimaxTTS`：

- 新增 `api: MinimaxAPIClient | None = None`。
- `self.api = api or MinimaxAPI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout)`。
- `speak()` 调用 `self.api.t2a_v2(data)`。
- `stream_synthesize()` 调用 `self.api.t2a_v2_stream(data)`。
- metadata 中继续保留 `trace_id`、`extra_info`、`payload`。

`MinimaxVoiceClone`：

- 新增 `api: MinimaxVoiceCloneAPIClient | None = None`。
- `upload_clone_audio()` 调用 `self.api.upload_file(path, "voice_clone")`。
- `upload_prompt_audio()` 调用 `self.api.upload_file(path, "prompt_audio")`。
- `clone()` 调用 `self.api.voice_clone(data)`。
- `speak()` 中下载试听音频调用 `self.api.download_url(result.demo_audio_url)`。
- `build_clone_payload()` 保持不发请求。

### 测试重点

新增 `FakeMinimaxAPI`，分别记录：

- `t2a_calls`
- `stream_calls`
- `uploads`
- `voice_clone_calls`
- `downloads`

关键断言：

- 非流式 T2A 调用 `api.t2a_v2(data)`。
- 流式 T2A 调用 `api.t2a_v2_stream(data)`。
- 快速复刻只调用 `upload_file()` 和 `voice_clone()`，不调用 T2A。
- `build_payload()` 和 `build_clone_payload()` 不发请求。
- multipart 上传使用 `requests` 的 `files` 参数，不再保留自制 boundary 逻辑。

最窄验证：

```bash
python -m pytest tests/test_minimax.py -q
```

## GLM 改造方案

### 当前问题

`glm` 当前只有一个手写 HTTP 请求：

- `GLMHTTPTransport.synthesize()` 使用 `urllib` POST 到 `GLM_BASE_URL`
- 响应是二进制音频，不是 JSON

### 文件级改造

新增：

```text
voice_hub/providers/glm/api.py
```

更新：

```text
voice_hub/providers/glm/models.py
voice_hub/providers/glm/tts.py
voice_hub/providers/glm/__init__.py
tests/test_glm.py
```

`transport.py` 当前在 `__init__.py` 中导出，建议保留兼容适配器或别名，但内部主路径改为 `GLMAPI`。

### endpoint 常量

当前 `GLM_BASE_URL` 是完整 endpoint：

```python
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/audio/speech"
```

为了让 API 方法清晰显示 path，建议新增：

```python
GLM_API_ROOT_URL = "https://open.bigmodel.cn/api/paas/v4"
GLM_AUDIO_SPEECH_PATH = "/audio/speech"
```

保留 `GLM_BASE_URL`，避免破坏公开常量。`GLMAPI` 初始化时兼容两种传法：

- 如果传入的是 root URL，直接拼 `GLM_AUDIO_SPEECH_PATH`。
- 如果传入的是旧的完整 `GLM_BASE_URL`，内部拆成 root + path 或直接兼容处理。

### API 类建议

```python
class GLMAPI(GLMBaseAPI):
    def speech(self, data: Mapping[str, object]) -> bytes:
        return self.post_bytes(GLM_AUDIO_SPEECH_PATH, data=dict(data))
```

headers：

```python
{
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
```

### Provider 调整

`GLMTTS`：

- 新增 `api: GLMAPIClient | None = None`。
- `speak()` 改为：

```python
request = self.build_request(text, **overrides)
data = request.to_payload()
audio = self.api.speech(data)
```

- metadata 继续保存 `model`、`voice`、`response_format`、`request_id`、`payload`。

### 测试重点

新增 `FakeGLMAPI`：

- `speech(data) -> bytes`
- 记录 `speech_calls`

关键断言：

- `GLMTTS.speak()` 调用 `api.speech(data)`。
- `build_payload()` 不发请求。
- 默认环境变量 `ZHIPUAI_API_KEY` 保持不变。
- 二进制响应不走 JSON 解析。
- `requests` HTTP 错误转换为 `ProviderError("GLM TTS request failed: HTTP ...")`。

最窄验证：

```bash
python -m pytest tests/test_glm.py -q
```

## Aliyun Qwen TTS 改造方案

### 当前问题

`aliyun/qwen_tts/transport.py` 当前包含：

- JSON POST 到 DashScope generation endpoint
- SSE 流式 POST，额外 header `X-DashScope-SSE: enable`
- 下载返回的音频 URL
- 全部使用 `urllib`

`tts.py` 直接调用 `transport.post()`、`transport.stream()`、`transport.download_url()`。

### 文件级改造

新增：

```text
voice_hub/providers/aliyun/qwen_tts/api.py
```

更新：

```text
voice_hub/providers/aliyun/qwen_tts/models.py
voice_hub/providers/aliyun/qwen_tts/tts.py
voice_hub/providers/aliyun/qwen_tts/__init__.py
voice_hub/providers/aliyun/__init__.py
tests/test_aliyun.py
```

`transport.py` 当前导出为 `AliyunHTTPTransport`，建议保留兼容适配器或别名，内部主路径改为 `AliyunQwenTTSAPI`。

### endpoint 常量

当前 `ALIYUN_BASE_URL` 是完整 endpoint。建议新增 root 和 path：

```python
ALIYUN_API_ROOT_URL = "https://dashscope.aliyuncs.com/api/v1"
ALIYUN_INTL_API_ROOT_URL = "https://dashscope-intl.aliyuncs.com/api/v1"
ALIYUN_QWEN_TTS_GENERATION_PATH = "/services/aigc/multimodal-generation/generation"
```

保留：

```python
ALIYUN_BASE_URL
ALIYUN_INTL_BASE_URL
```

兼容旧 `base_url` 传完整 endpoint 的用法。

### API 类建议

```python
class AliyunQwenTTSAPI(AliyunQwenTTSBaseAPI):
    def generation(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(ALIYUN_QWEN_TTS_GENERATION_PATH, data=dict(data))

    def generation_stream(self, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        return self.stream_post(
            ALIYUN_QWEN_TTS_GENERATION_PATH,
            data=dict(data),
            headers={"X-DashScope-SSE": "enable"},
        )

    def download_url(self, url: str) -> bytes:
        return self.get_bytes_url(url)
```

headers：

```python
{
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
```

### Provider 调整

`AliyunTTS`：

- 新增 `api: AliyunQwenTTSAPIClient | None = None`。
- `speak()` 调用 `self.api.generation(data)`，再 `self.api.download_url(audio_url)`。
- `stream()` 调用 `self.api.generation_stream(data)`。
- `build_payload()` 保持不发请求。

### 测试重点

新增 `FakeAliyunQwenTTSAPI`：

- `generation_calls`
- `stream_calls`
- `downloads`

关键断言：

- 非流式调用 `generation()` 并下载 audio URL。
- 流式调用 `generation_stream()`。
- `ALIYUN_INTL_BASE_URL` 兼容。
- 指令模型校验保持在 payload 层。
- `build_payload()` 不发请求。

最窄验证：

```bash
python -m pytest tests/test_aliyun.py -q
```

## Aliyun CosyVoice 改造方案

### 当前情况

`aliyun/cosyvoice` 不完全是手写 HTTP：

- `synthesize()`、`query_voice()`、`list_voices()`、`delete_voice()` 当前通过 DashScope SDK 调用。
- `create_voice()` 当前手写 HTTP POST 到 `/services/audio/tts/customization`。
- `upload_file()` 当前手写 multipart 到 `/files`。
- `get_file()` 当前手写 GET 到 `/files/{file_id}`。

本轮要求是把代码中的手写 HTTP 请求替换为 `requests`，同时把外部接口统一管理起来。因此：

- 手写 HTTP 的 `create_voice()`、`upload_file()`、`get_file()` 必须迁移到 requests API 层。
- SDK 调用不属于本项目手写 HTTP，可保留 SDK 实现，但建议也包进 `AliyunCosyVoiceAPI` 的业务方法，保持调用入口统一。
- 如果后续要求连 SDK 合成和音色管理也完全改成 requests，需要单独确认 DashScope WebSocket/HTTP 协议和鉴权细节，不能在本轮用猜测替换。

### 文件级改造

新增：

```text
voice_hub/providers/aliyun/cosyvoice/api.py
```

更新：

```text
voice_hub/providers/aliyun/cosyvoice/models.py
voice_hub/providers/aliyun/cosyvoice/tts.py
voice_hub/providers/aliyun/cosyvoice/clone.py
voice_hub/providers/aliyun/cosyvoice/__init__.py
voice_hub/providers/aliyun/__init__.py
tests/test_aliyun_cosyvoice.py
```

`transport.py`：

- 可拆分为 SDK 辅助模块，或保留为兼容适配器。
- 内部主路径改为 `AliyunCosyVoiceAPI`。
- 手写 `urllib` 逻辑全部移除。

### endpoint 常量

已有：

```python
ALIYUN_COSYVOICE_HTTP_BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
ALIYUN_COSYVOICE_CUSTOMIZATION_PATH = "/services/audio/tts/customization"
```

建议新增：

```python
ALIYUN_COSYVOICE_FILES_PATH = "/files"
```

文件查询 path 可由 API 方法构造：

```python
f"{ALIYUN_COSYVOICE_FILES_PATH}/{file_id}"
```

### API 类建议

```python
class AliyunCosyVoiceAPI(AliyunCosyVoiceBaseAPI):
    def synthesize(self, data: Mapping[str, object]) -> tuple[bytes, str | None]:
        return self._sdk_synthesize(data)

    def create_voice(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(ALIYUN_COSYVOICE_CUSTOMIZATION_PATH, data=dict(data))

    def query_voice(self, voice_id: str) -> Mapping[str, Any]:
        return self._sdk_query_voice(voice_id)

    def list_voices(self, data: Mapping[str, object]) -> list[Mapping[str, Any]]:
        return self._sdk_list_voices(data)

    def delete_voice(self, voice_id: str) -> str | None:
        return self._sdk_delete_voice(voice_id)

    def upload_file(self, file_path: str | Path, purpose: str) -> Mapping[str, Any]:
        return self.post_file(ALIYUN_COSYVOICE_FILES_PATH, file_path=file_path, data={"purpose": purpose})

    def get_file(self, file_id: str) -> Mapping[str, Any]:
        return self.get(f"{ALIYUN_COSYVOICE_FILES_PATH}/{file_id}")
```

`create_voice()` 的调用方先构造清晰 data：

```python
data = {
    "model": ALIYUN_COSYVOICE_ENROLLMENT_MODEL,
    "input": {
        "action": "create_voice",
        "target_model": self.target_model,
        "prefix": final_prefix,
        "url": audio_url,
    },
}
return self.api.create_voice(data)
```

### Provider 调整

`AliyunCosyVoiceTTS`：

- 新增 `api: AliyunCosyVoiceAPIClient | None = None`。
- `speak()` 改为：

```python
request = self.build_request(text, **overrides)
data = request.to_payload()
audio, request_id = self.api.synthesize(data)
```

`AliyunCosyVoiceClone`：

- 新增 `api: AliyunCosyVoiceAPIClient | None = None`。
- `create_voice()` 中构造 data 后调用 `self.api.create_voice(data)`。
- `upload_file()` 调用 `self.api.upload_file(file_path, purpose)`。
- `get_file()` 调用 `self.api.get_file(file_id)`。
- `query_voice()`、`list_voices()`、`delete_voice()` 也通过 `api` 入口调用，即使内部仍走 SDK。
- `tts()` 创建 `AliyunCosyVoiceTTS` 时传同一个 `api`，避免克隆和合成走两套客户端。

### 测试重点

新增 `FakeAliyunCosyVoiceAPI`：

- `syntheses`
- `created`
- `queries`
- `lists`
- `deleted`
- `uploads`
- `files`

关键断言：

- 系统音色合成调用 `api.synthesize(data)`。
- `build_payload()` 不发请求。
- 克隆创建调用 `api.create_voice(data)`，data 中能直接看到 `"action": "create_voice"`。
- 文件上传调用 `api.upload_file(path, purpose)`。
- 文件查询调用 `api.get_file(file_id)`。
- `tts_from_voice()` 传递同一个 API 实例。
- 不再出现手写 multipart boundary。

最窄验证：

```bash
python -m pytest tests/test_aliyun_cosyvoice.py -q
```

## 导出和命名建议

新增导出：

- `MinimaxAPI`
- `GLMAPI`
- `AliyunQwenTTSAPI`
- `AliyunCosyVoiceAPI`

保留兼容导出：

- `GLMHTTPTransport`
- `AliyunHTTPTransport`
- `AliyunCosyVoiceSDKTransport`

兼容导出可以作为 adapter，但新文档和测试应优先使用 `api`。

## 全库实施顺序

建议按复杂度和风险排序：

1. `glm`
   - 单 endpoint、二进制响应，最容易先建立 `post_bytes()` 模式。
2. `aliyun/qwen_tts`
   - 覆盖 JSON、SSE、URL 下载，适合沉淀通用 requests 辅助函数。
3. `minimax`
   - 覆盖 JSON、SSE、multipart、下载、voice clone，接口最多但结构清晰。
4. `aliyun/cosyvoice`
   - 同时涉及 SDK 和 HTTP，最后改，避免和前面通用 API 设计反复冲突。
5. 更新 `__init__.py` 导出和文档示例。
6. 删除或适配旧 transport 测试。

## 验证计划

分 provider 最窄验证：

```bash
python -m pytest tests/test_glm.py -q
python -m pytest tests/test_aliyun.py -q
python -m pytest tests/test_minimax.py -q
python -m pytest tests/test_aliyun_cosyvoice.py -q
```

全库回归：

```bash
python -m pytest tests/test_mimo.py tests/test_glm.py tests/test_aliyun.py tests/test_minimax.py tests/test_aliyun_cosyvoice.py -q
```

最终检查手写 HTTP 是否清理干净：

```bash
rg -n "urllib" voice_hub/providers/minimax voice_hub/providers/glm voice_hub/providers/aliyun
```

完成后该命令在目标目录中不应再命中手写 HTTP 请求代码。若 `urllib` 只出现在兼容注释或历史说明中，应评估是否移除。

## 完成标准

全部库改造完成后应满足：

- `minimax`、`glm`、`aliyun/qwen_tts`、`aliyun/cosyvoice` 的手写 HTTP 请求均使用 `requests`。
- 每个 provider 都有清晰的 `api.py`。
- API 方法中能直接看到 endpoint，例如 `return self.post("/voice_clone", data=data)`。
- provider 不再直接拼 URL、headers、multipart body 或调用 `urllib`。
- `build_payload()` / `build_request()` 全部不发请求。
- 流式请求使用 `requests` 的 `stream=True` 和 `iter_lines()`。
- 文件上传使用 `requests` 的 `files` 参数。
- 音频下载和二进制响应使用 `response.content`。
- 公开 provider 行为和 metadata 尽量保持不变。
- 相关测试全部通过。

## 剩余风险

- `AliyunCosyVoice` 的 DashScope SDK 调用不是手写 HTTP。本轮建议只统一入口，不强行替换 SDK 协议。
- 旧 `transport` 参数如果外部用户直接使用，删除会造成破坏。建议至少保留一个版本周期的兼容适配。
- 错误信息前缀可能因 requests 改造发生轻微变化，测试应断言 `ProviderError` 类型和核心业务信息，不要过度绑定完整字符串。
- 文件上传改用 requests 后 multipart boundary 会变化，测试不要断言 boundary，只断言 path、purpose、文件名和 API 方法调用。

