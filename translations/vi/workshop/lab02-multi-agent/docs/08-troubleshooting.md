# Module 8 - Khắc phục sự cố (Đa tác nhân)

Module này bao gồm các lỗi phổ biến, cách khắc phục và chiến lược gỡ lỗi dành riêng cho quy trình làm việc đa tác nhân. Đối với các vấn đề triển khai Foundry chung, cũng tham khảo [Hướng dẫn khắc phục sự cố Lab 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Tham khảo nhanh: Lỗi → Khắc phục

| Lỗi / Triệu chứng | Nguyên nhân có thể | Cách khắc phục |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Thiếu tệp `.env` hoặc giá trị chưa được thiết lập | Tạo `.env` với `PROJECT_ENDPOINT=<your-endpoint>` và `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Môi trường ảo chưa kích hoạt hoặc chưa cài đặt các phụ thuộc | Chạy `.\.venv\Scripts\Activate.ps1` rồi `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Gói MCP chưa được cài đặt (thiếu trong yêu cầu) | Chạy `pip install mcp` hoặc kiểm tra `requirements.txt` có bao gồm nó như một phụ thuộc chuyển tiếp |
| Agent khởi động nhưng trả về phản hồi trống | Không khớp `output_executors` hoặc thiếu các cạnh | Xác nhận `output_executors=[gap_analyzer]` và tất cả các cạnh tồn tại trong `create_workflow()` |
| Chỉ có 1 thẻ gap (các thẻ còn lại thiếu) | Hướng dẫn GapAnalyzer chưa đầy đủ | Thêm đoạn văn `CRITICAL:` vào `GAP_ANALYZER_INSTRUCTIONS` - xem [Module 3](03-configure-agents.md) |
| Điểm Fit là 0 hoặc không có | MatchingAgent không nhận được dữ liệu đầu vào | Xác nhận cả `add_edge(resume_parser, matching_agent)` và `add_edge(jd_agent, matching_agent)` tồn tại |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Máy chủ MCP từ chối cuộc gọi công cụ | Kiểm tra kết nối internet. Thử mở `https://learn.microsoft.com/api/mcp` trên trình duyệt. Thử lại |
| Không có URL Microsoft Learn trong đầu ra | Công cụ MCP chưa đăng ký hoặc endpoint sai | Xác nhận `tools=[search_microsoft_learn_for_plan]` trên GapAnalyzer và `MICROSOFT_LEARN_MCP_ENDPOINT` đúng |
| `Address already in use: port 8088` | Có tiến trình khác sử dụng cổng 8088 | Chạy `netstat -ano \| findstr :8088` (Windows) hoặc `lsof -i :8088` (macOS/Linux) và dừng tiến trình xung đột |
| `Address already in use: port 5679` | Xung đột cổng Debugpy | Dừng các phiên gỡ lỗi khác. Chạy `netstat -ano \| findstr :5679` để tìm và kết thúc tiến trình |
| Agent Inspector không mở được | Máy chủ chưa khởi động hoàn toàn hoặc xung đột cổng | Đợi log "Server running". Kiểm tra xem cổng 5679 có trống không |
| `azure.identity.CredentialUnavailableError` | Chưa đăng nhập Azure CLI | Chạy `az login` rồi khởi động lại máy chủ |
| `azure.core.exceptions.ResourceNotFoundError` | Triển khai mô hình không tồn tại | Kiểm tra `MODEL_DEPLOYMENT_NAME` khớp với mô hình đã triển khai trong dự án Foundry |
| Trạng thái container "Failed" sau khi triển khai | Container bị lỗi khi khởi động | Kiểm tra nhật ký container trong thanh bên Foundry. Thường là thiếu biến môi trường hoặc lỗi import |
| Triển khai hiển thị "Pending" hơn 5 phút | Container mất quá nhiều thời gian để khởi động hoặc giới hạn tài nguyên | Đợi tối đa 5 phút cho đa tác nhân (tạo 4 phiên bản agent). Nếu vẫn Pending thì kiểm tra log |
| `ValueError` từ `WorkflowBuilder` | Cấu hình đồ thị không hợp lệ | Đảm bảo `start_executor` được đặt, `output_executors` là danh sách, và không có cạnh vòng |

---

## Các vấn đề về môi trường và cấu hình

### Giá trị `.env` thiếu hoặc sai

Tệp `.env` phải nằm trong thư mục `PersonalCareerCopilot/` (cùng cấp với `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Nội dung `.env` mong đợi:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Tìm PROJECT_ENDPOINT của bạn:** 
- Mở thanh bên **Microsoft Foundry** trong VS Code → nhấp phải dự án của bạn → **Copy Project Endpoint**. 
- Hoặc vào [Azure Portal](https://portal.azure.com) → dự án Foundry của bạn → **Tổng quan** → **Project endpoint**.

> **Tìm MODEL_DEPLOYMENT_NAME của bạn:** Ở thanh bên Foundry, mở rộng dự án → **Models** → tìm tên mô hình đã triển khai (ví dụ: `gpt-4.1-mini`).

### Ưu tiên biến môi trường

`main.py` sử dụng `load_dotenv(override=False)`, nghĩa là:

| Độ ưu tiên | Nguồn | Có thắng khi cả hai được thiết lập không? |
|----------|--------|------------------------|
| 1 (cao nhất) | Biến môi trường shell | Có |
| 2 | Tệp `.env` | Chỉ khi biến shell chưa đặt |

Điều này có nghĩa biến môi trường thời gian chạy Foundry (đặt qua `agent.yaml`) ưu tiên hơn giá trị trong `.env` khi triển khai trên máy chủ.

---

## Tương thích phiên bản

### Bảng phiên bản gói

Quy trình làm việc đa tác nhân yêu cầu các phiên bản gói cụ thể. Không khớp phiên bản gây lỗi thời gian chạy.

| Gói | Phiên bản yêu cầu | Lệnh kiểm tra |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | phiên bản tiền phát hành mới nhất | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Lỗi phiên bản phổ biến

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Sửa: nâng cấp lên rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**Không tìm thấy `agent-dev-cli` hoặc Inspector không tương thích:**

```powershell
# Sửa lỗi: cài đặt với cờ --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Sửa lỗi: nâng cấp gói mcp
pip install mcp --upgrade
```

### Xác minh tất cả phiên bản cùng lúc

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Kết quả mong đợi:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## Vấn đề công cụ MCP

### Công cụ MCP không trả về kết quả

**Triệu chứng:** Thẻ gap báo "No results returned from Microsoft Learn MCP" hoặc "No direct Microsoft Learn results found".

**Nguyên nhân có thể:**

1. **Mạng có vấn đề** - Endpoint MCP (`https://learn.microsoft.com/api/mcp`) không truy cập được.
   ```powershell
   # Kiểm tra kết nối
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Nếu trả về `200`, endpoint có thể truy cập được.

2. **Truy vấn quá cụ thể** - Tên kỹ năng quá chuyên biệt đối với tìm kiếm Microsoft Learn.
   - Điều này bình thường với các kỹ năng rất chuyên ngành. Công cụ có URL dự phòng trong phản hồi.

3. **Phiên MCP hết thời gian** - Kết nối Streamable HTTP bị timeout.
   - Thử lại yêu cầu. Phiên MCP là tạm thời và có thể cần kết nối lại.

### Giải thích log MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Ý nghĩa | Hành động |
|-----|---------|--------|
| `GET → 405` | Khách hàng MCP khảo sát trong quá trình khởi tạo | Bình thường - bỏ qua |
| `POST → 200` | Cuộc gọi công cụ thành công | Mong đợi |
| `DELETE → 405` | Khách hàng MCP khảo sát trong quá trình dọn dẹp | Bình thường - bỏ qua |
| `POST → 400` | Yêu cầu sai (truy vấn sai định dạng) | Kiểm tra tham số `query` trong `search_microsoft_learn_for_plan()` |
| `POST → 429` | Bị giới hạn tốc độ | Đợi và thử lại. Giảm tham số `max_results` |
| `POST → 500` | Lỗi máy chủ MCP | Lỗi tạm thời - thử lại. Nếu kéo dài, API Microsoft Learn MCP có thể bị ngưng hoạt động |
| Kết nối timeout | Vấn đề mạng hoặc máy chủ MCP không khả dụng | Kiểm tra internet. Thử `curl https://learn.microsoft.com/api/mcp` |

---

## Vấn đề triển khai

### Container không khởi động sau khi triển khai

1. **Kiểm tra log container:**
   - Mở thanh bên **Microsoft Foundry** → mở rộng **Hosted Agents (Preview)** → nhấn vào agent của bạn → mở rộng phiên bản → **Chi tiết container** → **Nhật ký**.
   - Tìm các lỗi trace Python hoặc lỗi thiếu module.

2. **Các lỗi khởi động container phổ biến:**

   | Lỗi trong log | Nguyên nhân | Khắc phục |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` thiếu gói | Thêm gói, triển khai lại |
   | `RuntimeError: Missing required environment variable` | Các biến môi trường trong `agent.yaml` chưa đặt | Cập nhật `agent.yaml` → phần `environment_variables` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity chưa cấu hình | Foundry thiết lập tự động - đảm bảo triển khai qua extension |
   | `OSError: port 8088 already in use` | Dockerfile khai báo sai cổng hoặc xung đột cổng | Xác nhận `EXPOSE 8088` trong Dockerfile và `CMD ["python", "main.py"]` |
   | Container thoát với mã 1 | Ngoại lệ chưa xử lý trong `main()` | Test cục bộ trước ([Module 5](05-test-locally.md)) để phát hiện lỗi trước khi triển khai |

3. **Triển khai lại sau khi sửa:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → chọn cùng agent → triển khai phiên bản mới.

### Triển khai mất quá nhiều thời gian

Container đa tác nhân mất nhiều thời gian khởi động hơn vì tạo 4 phiên bản agent khi khởi động. Thời gian khởi động bình thường:

| Giai đoạn | Thời gian dự kiến |
|-------|------------------|
| Xây dựng ảnh container | 1-3 phút |
| Đẩy ảnh lên ACR | 30-60 giây |
| Khởi động container (agent đơn) | 15-30 giây |
| Khởi động container (đa tác nhân) | 30-120 giây |
| Agent sẵn sàng trong Playground | 1-2 phút sau "Started" |

> Nếu trạng thái "Pending" kéo dài quá 5 phút, kiểm tra log container để tìm lỗi.

---

## RBAC và vấn đề phân quyền

### `403 Forbidden` hoặc `AuthorizationFailed`

Bạn cần có vai trò **[Azure AI User](https://aka.ms/foundry-ext-project-role)** trong dự án Foundry của mình:

1. Vào [Azure Portal](https://portal.azure.com) → tài nguyên **dự án** Foundry của bạn.
2. Nhấp **Access control (IAM)** → **Role assignments**.
3. Tìm tên bạn → xác nhận danh sách có **Azure AI User**.
4. Nếu thiếu: **Add** → **Add role assignment** → tìm **Azure AI User** → gán cho tài khoản của bạn.

Xem tài liệu [RBAC cho Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) để biết chi tiết.

### Triển khai mô hình không truy cập được

Nếu agent trả về lỗi liên quan đến mô hình:

1. Xác nhận mô hình đã được triển khai: Thanh bên Foundry → mở rộng dự án → **Models** → kiểm tra `gpt-4.1-mini` (hoặc mô hình bạn dùng) có trạng thái **Succeeded**.
2. Xác nhận tên triển khai đúng: so sánh `MODEL_DEPLOYMENT_NAME` trong `.env` (hoặc `agent.yaml`) với tên triển khai thực tế trong thanh bên.
3. Nếu triển khai hết hạn (miễn phí): triển khai lại từ [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Vấn đề Agent Inspector

### Inspector mở nhưng hiện "Disconnected"

1. Xác nhận máy chủ đang chạy: kiểm tra log "Server running on http://localhost:8088" trong terminal.
2. Kiểm tra cổng `5679`: Inspector kết nối qua debugpy qua cổng 5679.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Khởi động lại máy chủ và mở lại Inspector.

### Inspector hiển thị phản hồi một phần

Phản hồi đa tác nhân thường dài và phát trực tiếp dần dần. Đợi phản hồi hoàn chỉnh (có thể mất 30-60 giây tùy số thẻ gap và số cuộc gọi công cụ MCP).

Nếu phản hồi bị cắt ngắn liên tục:
- Kiểm tra hướng dẫn GapAnalyzer có chứa đoạn `CRITICAL:` ngăn chặn ghép các thẻ gap.
- Kiểm tra giới hạn token của mô hình - `gpt-4.1-mini` hỗ trợ tối đa 32K token đầu ra, thường đủ dùng.

---

## Mẹo cải thiện hiệu suất

### Phản hồi chậm

Quy trình đa tác nhân vốn dĩ chậm hơn đơn tác nhân do phụ thuộc tuần tự và các cuộc gọi công cụ MCP.

| Tối ưu | Cách thực hiện | Ảnh hưởng |
|-------------|-----|--------|
| Giảm số cuộc gọi MCP | Giảm tham số `max_results` trong công cụ | Ít số lần gọi HTTP hơn |
| Đơn giản hóa hướng dẫn | Lời nhắc agent ngắn gọn, tập trung | Tăng tốc suy luận LLM |
| Sử dụng `gpt-4.1-mini` | Nhanh hơn `gpt-4.1` khi phát triển | Tăng tốc khoảng 2 lần |
| Giảm chi tiết thẻ gap | Đơn giản hóa định dạng thẻ gap trong hướng dẫn GapAnalyzer | Ít đầu ra cần tạo hơn |

### Thời gian phản hồi điển hình (cục bộ)

| Cấu hình | Thời gian dự kiến |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 thẻ gap | 30-60 giây |
| `gpt-4.1-mini`, 8+ thẻ gap | 60-120 giây |
| `gpt-4.1`, 3-5 thẻ gap | 60-120 giây |
---

## Nhận trợ giúp

Nếu bạn bị kẹt sau khi thử các cách sửa lỗi ở trên:

1. **Kiểm tra nhật ký máy chủ** - Hầu hết các lỗi đều tạo ra một stack trace Python trong terminal. Đọc toàn bộ traceback.
2. **Tìm kiếm thông báo lỗi** - Sao chép văn bản lỗi và tìm kiếm trong [Microsoft Q&A cho Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Mở một issue** - Tạo một issue trên [kho lưu trữ workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) kèm theo:
   - Thông báo lỗi hoặc ảnh chụp màn hình
   - Phiên bản gói của bạn (`pip list | Select-String "agent-framework"`)
   - Phiên bản Python của bạn (`python --version`)
   - Vấn đề xảy ra tại cục bộ hay sau khi triển khai

---

### Bảng kiểm tra

- [ ] Bạn có thể xác định và sửa các lỗi đa tác nhân phổ biến nhất bằng cách sử dụng bảng tham khảo nhanh
- [ ] Bạn biết cách kiểm tra và sửa các sự cố cấu hình `.env`
- [ ] Bạn có thể xác minh các phiên bản gói phù hợp với ma trận yêu cầu
- [ ] Bạn hiểu các mục nhật ký MCP và có thể chẩn đoán sự cố công cụ
- [ ] Bạn biết cách kiểm tra nhật ký container để phát hiện lỗi triển khai
- [ ] Bạn có thể xác minh các vai trò RBAC trong Cổng Azure

---

**Trước:** [07 - Xác minh trong Playground](07-verify-in-playground.md) · **Trang chính:** [Lab 02 README](../README.md) · [Trang chính Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố từ chối trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa các lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ nguyên bản nên được coi là nguồn tham khảo chính xác. Đối với các thông tin quan trọng, nên sử dụng dịch thuật chuyên nghiệp do con người thực hiện. Chúng tôi không chịu trách nhiệm về bất kỳ sự hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->