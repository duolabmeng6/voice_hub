# requests 和 API 可读性改造方案

## 目标

本次先改造 `voice_hub/providers/mimo`，把 MiMo provider 中的 HTTP 请求从 `urllib` 更换为 `requests`，并把 API endpoint 统一收敛到清晰的接口管理类中。

改造后的调用链应尽量贴近 `/Users/ll/Desktop/2025/hy_sj_sdk/minimaxSDK/src/minimaxsdk/api.py` 的写法：

```python
def voice_clone(...):
    data = {...}
    return self.post("/chat/completions", data=data)
```

核心原则是：调用方参数只负责构造请求数据，请求数据只单向传给 API 方法，API 方法只负责选择 endpoint 并发起请求。这样调试时可以清楚看到“参数 -> data -> endpoint -> response”的路径。

## 当前情况

`voice_hub/providers/mimo` 当前主要文件：

- `tts.py`：provider 入口，负责配置、构造 payload、调用 `transport.post()` / `transport.stream()`、解析响应。
- `payload.py`：根据 provider 配置和 overrides 构造 `MimoRequest`。
- `models.py`：保存模型常量和 `MimoRequest`。
- `transport.py`：当前使用 `urllib.request`，并在 `_build_request()` 中硬编码 `/chat/completions`。
- `parser.py`：解析普通响应和 SSE 流式响应中的音频数据。

主要问题：

- endpoint 隐藏在 `transport.py` 的 `_build_request()` 内，调用方看不到具体接口。
- `tts.py` 直接传 `base_url/api_key/payload/timeout` 给 transport，请求语义不够明确。
- `post()` 方法不是接口级别的方法，调试时只能看到“发了一个 post”，看不到是内置 TTS、文本设计音色还是克隆音色。
- `transport.py` 同时承担 URL 拼接、headers、JSON 编码、请求发送、异常转换、SSE 解析，职责偏重。
- 项目当前 `pyproject.toml` 的 `dependencies = []`，引入 `requests` 属于新增生产依赖，实施前需要明确加入依赖。

## 目标结构

建议把 MiMo 的请求层拆成三层：

1. `MimoBaseAPI`
   - 使用 `requests.Session` 或 `requests.request` 统一处理 HTTP。
   - 管理 `base_url`、`api_key`、headers、timeout。
   - 提供 `get()`、`post()`、`stream_post()` 等通用方法。
   - 统一把 `requests` 异常转换为项目内的 `ProviderError`。

2. `MimoAPI`
   - 只管理 MiMo endpoint 和接口级方法。
   - 方法命名体现业务语义，例如 `tts()`、`voice_design()`、`voice_clone()`。
   - 方法内部保持清晰的 `return self.post("/chat/completions", data=data)` 或 `return self.stream_post("/chat/completions", data=data)`。

3. `MimoTTS`
   - 继续作为 `voice_hub` 面向用户的 provider。
   - 只负责接收调用参数、校验配置、调用 `MimoPayloadBuilder` 构造请求对象、调用 `MimoAPI`。
   - 不直接拼 URL，不直接处理 headers，不直接依赖 `requests`。

建议文件布局：

```text
voice_hub/providers/mimo/
  api.py          # 新增：MimoBaseAPI + MimoAPI
  transport.py    # 可删除或保留兼容薄壳，首轮建议保留兼容导入
  tts.py          # 改为依赖 MimoAPI
  payload.py      # 保持参数到 MimoRequest 的单向构造
  parser.py       # 保持响应解析职责
  models.py       # 补 endpoint 常量
```

## API 层设计

`models.py` 建议新增 endpoint 常量：

```python
MIMO_CHAT_COMPLETIONS_PATH = "/chat/completions"
```

`api.py` 建议结构：

```python
from __future__ import annotations

from typing import Any, Iterable, Mapping

import requests

from ...errors import ProviderError
from .models import MIMO_CHAT_COMPLETIONS_PATH


class MimoBaseAPI:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float = 60,
        session: requests.Session | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.headers = {
            "Content-Type": "application/json",
            "api-key": api_key,
        }

    def post(self, path: str, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self._request("POST", path, data=data)

    def stream_post(self, path: str, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        return self._stream_request("POST", path, data=data)

    def _request(self, method: str, path: str, data: Mapping[str, object] | None = None) -> Mapping[str, Any]:
        ...

    def _stream_request(self, method: str, path: str, data: Mapping[str, object] | None = None) -> Iterable[Mapping[str, Any]]:
        ...
```

`MimoAPI` 建议只保留接口级方法：

```python
class MimoAPI(MimoBaseAPI):
    def tts(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MIMO_CHAT_COMPLETIONS_PATH, data=data)

    def tts_stream(self, data: Mapping[str, object]) -> Iterable[Mapping[str, Any]]:
        return self.stream_post(MIMO_CHAT_COMPLETIONS_PATH, data=data)

    def voice_design(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MIMO_CHAT_COMPLETIONS_PATH, data=data)

    def voice_clone(self, data: Mapping[str, object]) -> Mapping[str, Any]:
        return self.post(MIMO_CHAT_COMPLETIONS_PATH, data=data)
```

说明：

- MiMo 当前内置音色、文本设计音色、参考音频克隆都是同一个 `/chat/completions` endpoint，通过 `model` 和 `audio` 字段区分。
- 即使 endpoint 相同，也建议保留 `tts()`、`voice_design()`、`voice_clone()` 三个业务方法，便于断点、日志和测试定位。
- 如果后续 MiMo 新增真实独立 endpoint，只需要改 `MimoAPI`，不会影响 `MimoTTS` 的参数构造逻辑。

## MimoTTS 调用链调整

`MimoTTS.__init__()` 建议把当前 `transport` 参数迁移为 `api`，同时首轮保留兼容：

```python
def __init__(
    ...,
    api: MimoAPI | None = None,
    transport: MimoHTTPTransport | None = None,
    ...
) -> None:
    if api is not None and transport is not None:
        raise ConfigurationError("MiMo api and transport cannot be used together")
    self.api = api or _api_from_transport_or_config(...)
```

首轮最小风险方案：

- 新增 `api` 参数作为推荐写法。
- 暂时保留 `transport` 参数，避免现有测试和外部用户代码立即破坏。
- `transport.py` 可以改成基于 `MimoAPI` 的兼容适配器，或者先保留但不再作为主路径。
- 文档中标记 `transport` 为兼容入口，不新增能力。

`speak()` 目标调用方式：

```python
request = self.build_request(text, stream=False, **overrides)
data = request.to_payload()
response = self._call_api(request.model, data, stream=False)
```

`_call_api()` 根据 model 选择清晰接口：

```python
def _call_api(self, model: str, data: Mapping[str, object], *, stream: bool = False):
    if stream:
        return self.api.tts_stream(data)
    if model == MIMO_VOICE_DESIGN_MODEL:
        return self.api.voice_design(data)
    if model == MIMO_VOICE_CLONE_MODEL:
        return self.api.voice_clone(data)
    return self.api.tts(data)
```

这样 `build_request()` 仍然负责参数到 payload，`MimoAPI` 负责接口选择，`parser` 负责响应解析。

## requests 处理细节

普通请求：

- 使用 `requests.Session.request(method, url, headers=..., json=data, timeout=timeout)`。
- 调用 `response.raise_for_status()`。
- JSON 解析失败时抛出 `ProviderError("MiMo API request returned invalid JSON")`。
- HTTP 错误保留响应 body 前 2000 字符以内，避免日志过大。
- 不打印 `api_key`、headers 或完整音频 data URI。

流式请求：

- 使用 `stream=True`。
- 用 `response.iter_lines(decode_unicode=False)` 读取 SSE。
- 继续复用当前 `_parse_sse_line()` 语义，`data: [DONE]` 返回 `None`。
- `with response:` 或生成器内部确保连接最终关闭。

异常转换：

- `requests.exceptions.HTTPError` -> `ProviderError("MiMo API request failed: HTTP ...")`
- `requests.exceptions.Timeout` -> `ProviderError("MiMo API request timed out")`
- `requests.exceptions.RequestException` -> `ProviderError("MiMo API request failed: ...")`
- JSON 解析错误 -> `ProviderError("MiMo API request returned invalid JSON")`

## 调试可读性要求

改造后应满足：

- `build_payload()` 不发送请求，只返回最终 data。
- `MimoAPI.voice_clone(data)` 内能明确看到 endpoint。
- `MimoTTS.speak()` 中能明确看到调用链：
  - `request = build_request(...)`
  - `data = request.to_payload()`
  - `response = api.voice_clone(data)` 或 `api.tts(data)`
  - `audio = parser.decode_message_audio(response)`
- metadata 继续保存脱敏后的 payload，克隆音频 data URI 仍需 redaction。
- 不允许 API 层反向修改 payload；如需防御，进入 API 方法时用 `dict(data)` 浅拷贝。

## 迁移步骤

### 第 1 步：增加依赖

在 `pyproject.toml` 中把：

```toml
dependencies = []
```

改为：

```toml
dependencies = [
    "requests>=2.31",
]
```

说明：这是新增生产依赖，实施前需要确认。当前只写方案，不直接修改依赖。

### 第 2 步：新增 `api.py`

新增：

- `MimoBaseAPI`
- `MimoAPI`
- `_parse_sse_line()` 或 `_iter_sse_events()` 辅助函数

这一层是后续所有 MiMo endpoint 的唯一管理位置。

### 第 3 步：补 endpoint 常量

在 `models.py` 增加：

```python
MIMO_CHAT_COMPLETIONS_PATH = "/chat/completions"
```

并在 `__init__.py` 中导出。

### 第 4 步：改造 `tts.py`

目标改动：

- `MimoTTS` 默认创建 `MimoAPI(api_key, base_url, timeout)`。
- `speak()` 改为调用 `self.api.tts()` / `self.api.voice_design()` / `self.api.voice_clone()`。
- `stream_synthesize()` 改为调用 `self.api.tts_stream()`。
- 保留 `build_payload()`、`build_request()` 行为不变。
- 保留 `_redact_payload()`。

### 第 5 步：处理 `transport.py` 兼容

首轮建议不要直接删除 `MimoHTTPTransport`，因为现有测试和用户代码可能传入 fake transport。

兼容方案二选一：

1. 保留 `MimoHTTPTransport`，内部改用 `MimoAPI` 发请求。
2. 保留当前类名但标记为兼容适配器，测试逐步切到 `FakeMimoAPI`。

建议选择方案 2，最小化公开 API 破坏。

### 第 6 步：更新测试

重点更新 `tests/test_mimo.py`：

- 新增 `FakeMimoAPI`，记录 `tts_calls`、`voice_design_calls`、`voice_clone_calls`、`stream_calls`。
- 保留 `FakeTransport` 兼容测试，确保旧入口没有立即破坏。
- 增加断言：文本设计模型调用 `api.voice_design()`。
- 增加断言：克隆模型调用 `api.voice_clone()`。
- 增加断言：内置模型调用 `api.tts()`。
- 增加 requests 错误转换测试，可用 monkeypatch 模拟 `requests.Session.request`。

建议最窄验证命令：

```bash
python -m pytest tests/test_mimo.py -q
```

如改动依赖或导出，再运行：

```bash
python -m pytest tests/test_mimo.py tests/test_my.py -q
```

## 兼容性策略

短期兼容：

- `MimoTTS(..., transport=FakeTransport())` 暂时继续支持。
- `MimoHTTPTransport` 暂时继续从 `voice_hub.providers.mimo` 导出。
- `build_payload()`、`build_request()`、`speak()`、`bytes()`、`stream()` 等公开方法保持不变。

推荐新入口：

```python
api = MimoAPI(api_key="key", base_url=MIMO_BASE_URL, timeout=60)
tts = MimoTTS(api_key="key", api=api)
```

后续清理：

- 等外部调用迁移后，再考虑移除 `transport` 参数。
- 移除前需要在文档和版本说明里明确 deprecated 周期。

## 风险和控制

风险 1：新增 `requests` 依赖影响打包。

- 控制：只新增稳定依赖 `requests>=2.31`，不更新无关依赖或工具链。

风险 2：流式响应连接未关闭。

- 控制：`stream_post()` 生成器内部使用 response 上下文，确保迭代结束或异常时释放连接。

风险 3：错误信息变化导致测试或调用方判断失败。

- 控制：保留当前 `ProviderError` 类型和主要错误前缀，例如 `MiMo API request failed`、`MiMo API stream failed`。

风险 4：克隆音频 data URI 被记录到 metadata。

- 控制：保留并测试 `_redact_payload()`。

风险 5：接口方法只是同 endpoint 包装，可能看起来重复。

- 控制：这是有意设计，用业务方法换取调试清晰度。未来 endpoint 拆分时只改 `MimoAPI`。

## 完成标准

首轮 `mimo` 改造完成后应满足：

- `voice_hub/providers/mimo/transport.py` 不再直接使用 `urllib` 作为主请求实现。
- `voice_hub/providers/mimo/api.py` 使用 `requests` 统一发起普通和流式请求。
- `MimoAPI` 中有清晰的接口方法，例如 `voice_clone()`。
- `MimoAPI` 方法中能清楚看到 `return self.post("/chat/completions", data=data)`。
- `MimoTTS` 中没有 endpoint 拼接逻辑。
- `build_payload()` 仍然不触发网络请求。
- `tests/test_mimo.py` 通过。

## 建议实施顺序

1. 先新增 `api.py` 和 endpoint 常量。
2. 再把 `MimoTTS` 主路径切到 `MimoAPI`。
3. 保留 `MimoHTTPTransport` 兼容，避免一次性破坏测试。
4. 更新 `tests/test_mimo.py`，验证接口级调用是否清晰。
5. 最后调整 `pyproject.toml` 依赖并运行最窄测试。

