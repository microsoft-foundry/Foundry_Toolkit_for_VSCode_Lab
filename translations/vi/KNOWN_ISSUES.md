# Các Vấn Đề Được Biết Đến

Tài liệu này theo dõi các vấn đề đã biết với trạng thái kho hiện tại.

> Cập nhật lần cuối: 2026-04-15. Đã kiểm tra với Python 3.13 / Windows trong `.venv_ga_test`.

---

## Các Phiên Bản Gói Hiện Tại (cả ba agent)

| Gói | Phiên Bản Hiện Tại |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(đã sửa — xem KI-003)* |

---

## KI-001 — Nâng Cấp GA 1.0.0 Bị Chặn: `agent-framework-azure-ai` Bị Loại Bỏ

**Trạng thái:** Mở | **Mức độ:** 🔴 Cao | **Loại:** Đứt gãy

### Mô Tả

Gói `agent-framework-azure-ai` (khóa ở `1.0.0rc3`) đã **bị loại bỏ/ngừng hỗ trợ**
trong bản phát hành GA (1.0.0, phát hành 2026-04-02). Nó được thay thế bởi:

- `agent-framework-foundry==1.0.0` — mô hình agent được host bởi Foundry
- `agent-framework-openai==1.0.0` — mô hình agent dựa trên OpenAI

Tất cả ba tập tin `main.py` đều nhập `AzureAIAgentClient` từ `agent_framework.azure`, điều này
gây ra lỗi `ImportError` trong các gói GA. Không gian tên `agent_framework.azure` vẫn tồn tại
trong GA nhưng hiện chỉ chứa các lớp Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — không phải các agent Foundry.

### Lỗi xác nhận (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Các tập tin bị ảnh hưởng

| Tập tin | Dòng |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Không Tương Thích với GA `agent-framework-core`

**Trạng thái:** Mở | **Mức độ:** 🔴 Cao | **Loại:** Đứt gãy (bị chặn trên phía upstream)

### Mô Tả

`azure-ai-agentserver-agentframework==1.0.0b17` (phiên bản mới nhất) khóa cứng
`agent-framework-core<=1.0.0rc3`. Việc cài đặt nó cùng với `agent-framework-core==1.0.0` (GA)
bắt buộc pip phải **hạ cấp** `agent-framework-core` về lại `rc3`, điều này làm hỏng
`agent-framework-foundry==1.0.0` và `agent-framework-openai==1.0.0`.

Gọi `from azure.ai.agentserver.agentframework import from_agent_framework` được tất cả agents sử dụng để liên kết máy chủ HTTP cũng bị chặn.

### Xung đột phụ thuộc được xác nhận (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Các tập tin bị ảnh hưởng

Cả ba tập tin `main.py` — cả nhập cấp trên và nhập trong hàm `main()`.

---

## KI-003 — Cờ `agent-dev-cli --pre` Không Còn Cần Thiết

**Trạng thái:** ✅ Đã sửa (không gây đứt gãy) | **Mức độ:** 🟢 Thấp

### Mô Tả

Tất cả các tập tin `requirements.txt` trước đây đều bao gồm `agent-dev-cli --pre` để lấy CLI phiên bản tiền phát hành. Kể từ khi bản GA 1.0.0 được phát hành vào 2026-04-02, bản phát hành ổn định của
`agent-dev-cli` giờ đã có sẵn mà không cần cờ `--pre`.

**Sửa chữa đã áp dụng:** Cờ `--pre` đã được loại bỏ khỏi cả ba tập tin `requirements.txt`.

---

## KI-004 — Dockerfiles Sử Dụng `python:3.14-slim` (Ảnh nền Phiên bản Tiền phát hành)

**Trạng thái:** Mở | **Mức độ:** 🟡 Thấp

### Mô Tả

Tất cả `Dockerfile` đều sử dụng `FROM python:3.14-slim` theo dõi bản dựng Python tiền phát hành.
Đối với triển khai thực tế nên khóa ở bản phát hành ổn định (ví dụ, `python:3.12-slim`).

### Các tập tin bị ảnh hưởng

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Tham Khảo

- [agent-framework-core trên PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry trên PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ gốc của nó nên được coi là nguồn tham khảo chính thức. Đối với những thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp của con người. Chúng tôi không chịu trách nhiệm đối với bất kỳ sự hiểu nhầm hoặc diễn giải sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->