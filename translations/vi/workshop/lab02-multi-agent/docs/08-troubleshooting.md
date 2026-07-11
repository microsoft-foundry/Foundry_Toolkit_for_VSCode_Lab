# Mô-đun 8 - Xử lý sự cố

Mô-đun này trình bày các lỗi phổ biến, cách sửa và chiến lược gỡ lỗi đặc thù cho quy trình làm việc đa tác nhân.

## Vấn đề đầu ra của tác nhân

### GapAnalyzer nói “Tôi vẫn chưa có báo cáo phù hợp”

**Triệu chứng:** Phản hồi của GapAnalyzer yêu cầu bạn dán một báo cáo phù hợp có chứa “Kỹ năng còn thiếu” và “Khoảng trống chứng nhận.” Điều này xảy ra ngay cả khi bạn đã gửi cả sơ yếu lý lịch và mô tả công việc.

**Nguyên nhân:** Văn bản JD không được truyền xuống cho JD Agent. Với `context_mode="last_agent"`, `resume_executor` là thực thi viên duy nhất từng thấy tin nhắn gốc của người dùng. Nếu `RESUME_PARSER_INSTRUCTIONS` không bao gồm văn bản JD trong đầu ra, JD Agent không có JD để phân tích, MatchingAgent không thể tính điểm phù hợp, và GapAnalyzer nhận đầu vào không có ý nghĩa.

**Chẩn đoán:**

Trong nhật ký máy chủ, tìm kiếm phạm vi MatchingAgent. Nếu nó chứa:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
phần truyền qua bị thiếu hoặc hỏng.

**Sửa:** Xác nhận rằng `RESUME_PARSER_INSTRUCTIONS` trong `main.py` có phần `[JOB DESCRIPTION PASS-THROUGH]` và quy tắc:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Cũng xác nhận rằng `JOB_DESCRIPTION_INSTRUCTIONS` có quy tắc chuyển tiếp `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Nếu một trong hai khối hướng dẫn là mẫu từ trợ lý scaffold, thay thế bằng phiên bản đầy đủ từ [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent xuất ra “Không thể tính điểm phù hợp - không có JD được cung cấp”

Đây là nguyên nhân gốc như trên. MatchingAgent nhận đầu ra của JD Agent nhưng phần `[PARSED RESUME PASS-THROUGH]` bị thiếu hoặc trống, nên nó không thể so sánh hai hồ sơ. Xác nhận:
1. `JOB_DESCRIPTION_INSTRUCTIONS` bao gồm quy tắc chuyển tiếp: `Sao chép [PARSED RESUME] chính xác - Matching Agent phụ thuộc vào đó ở bước sau.`
2. `MATCHING_AGENT_INSTRUCTIONS` bảo tác nhân tìm các phần `[JD REQUIREMENTS]` và `[PARSED RESUME PASS-THROUGH]`.

Thay thế cả hai khối hướng dẫn bằng phiên bản đầy đủ từ [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Phản hồi xuất hiện hai lần

**Triệu chứng:** Đầu ra của GapAnalyzer (hoặc toàn bộ đầu ra pipeline) xuất hiện hai lần trong phản hồi của Agent Inspector.

**Nguyên nhân:** `WorkflowBuilder` sử dụng ngữ nghĩa OR cho các cạnh đầu vào - một thực thi viên phía dưới được kích hoạt ngay khi **bất kỳ** người tiền nhiệm nào hoàn thành. Nếu `matching_executor` có hai cạnh đầu vào (một từ `resume_executor` và một từ `jd_executor`), nó sẽ kích hoạt hai lần: một lần khi ResumeParser hoàn tất và một lần khi JD Agent hoàn tất. GapAnalyzer cũng chạy hai lần.

**Sửa:** Đảm bảo sơ đồ `WorkflowBuilder` là pipeline tuần tự nghiêm ngặt không có fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # KHÔNG từ resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Nếu bạn có dòng `.add_edge(resume_executor, matching_executor)` thừa, hãy xoá nó. Chuyển tiếp `[PARSED RESUME PASS-THROUGH]` trong đầu ra của JD Agent đã cung cấp cho MatchingAgent quyền truy cập vào sơ yếu lý lịch.

---

## Vấn đề môi trường và cấu hình

### Giá trị `.env` thiếu hoặc sai

File `.env` phải nằm trong thư mục `PersonalCareerCopilot/` (cùng cấp với `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Nội dung `.env` dự kiến:

**Đường dẫn A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Đường dẫn B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Cả hai đường dẫn đều sử dụng `FOUNDRY_PROJECT_ENDPOINT`. Giá trị khác nhau: cloud dùng endpoint Foundry `https://`; local dùng `http://localhost:5273/v1`. Chạy `foundry model list` để xác nhận bí danh mô hình chính xác cho Đường dẫn B.

> **Tìm `FOUNDRY_PROJECT_ENDPOINT` của bạn:** 
- Mở thanh bên **Foundry Toolkit** trong VS Code → nhấp chuột phải vào dự án → **Sao chép endpoint dự án**. 
- Hoặc truy cập [Azure Portal](https://portal.azure.com) → dự án Foundry của bạn → **Tổng quan** → **Endpoint dự án**.

> **Tìm `AZURE_AI_MODEL_DEPLOYMENT_NAME` của bạn:** Trong thanh bên Foundry Toolkit, mở rộng dự án → **Models** → tìm tên mô hình đã triển khai (ví dụ, `gpt-4.1-mini`).

### Ưu tiên biến môi trường

`main.py` sử dụng `load_dotenv(override=True)`, tức là:

| Ưu tiên | Nguồn | Có thắng khi cả hai cùng đặt? |
|----------|--------|------------------------|
| 1 (cao nhất) | File `.env` | Có |
| 2 | Biến môi trường shell / container | Dùng khi không có khóa cùng tên trong `.env` |

Trong phát triển cục bộ, điều này khiến `.env` là nguồn dữ liệu chính (chỉnh sửa `.env` tác động ngay lập tức đến chạy). Trong triển khai được lưu trữ, Foundry tiêm biến môi trường ở cấp container; vì `.env` không thuộc ảnh triển khai trong cài đặt lab này, giá trị tiêm trong container được dùng.

---

## Tương thích phiên bản

### Bảng phiên bản gói

Quy trình đa tác nhân yêu cầu các phiên bản gói cụ thể. Phiên bản không khớp gây lỗi khi chạy.

| Gói | Phiên bản yêu cầu | Lệnh kiểm tra |
|---------|-----------------|---------------|
| `agent-framework-foundry` | mới nhất | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | mới nhất | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | mới nhất | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Lỗi phiên bản phổ biến

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Sửa: cài đặt lại agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Sửa: nâng cấp gói mcp
pip install mcp --upgrade
```

### Kiểm tra tất cả phiên bản một lúc

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Kết quả dự kiến:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Vấn đề triển khai

### Container không khởi động sau khi triển khai

1. **Kiểm tra nhật ký container:**
   - Mở thanh bên **Foundry Toolkit** → mở rộng **Hosted Agents (Preview)** → nhấp vào tác nhân của bạn → mở rộng phiên bản → **Chi tiết Container** → **Nhật ký**.
   - Tìm các traceback Python hoặc lỗi thiếu module.

2. **Lỗi khởi động container phổ biến:**

   | Lỗi trong nhật ký | Nguyên nhân | Cách sửa |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | file `requirements.txt` thiếu gói | Thêm gói, triển khai lại |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | biến môi trường trong `agent.yaml` hoặc `.env` chưa đặt | Cập nhật phần `environment_variables` trong `agent.yaml` (hosted) hoặc `.env` (local) |
   | `azure.identity.CredentialUnavailableError` | Chưa cấu hình Managed Identity | Foundry tự cấu hình - đảm bảo bạn triển khai qua extension |
   | `OSError: port 8088 already in use` | Dockerfile mở cổng sai hoặc xung đột cổng | Kiểm tra `EXPOSE 8088` trong Dockerfile và `CMD ["python", "main.py"]` |
   | Container thoát với mã 1 | Ngoại lệ không xử lý trong `main()` | Kiểm tra cục bộ trước ([Mô-đun 5](05-test-locally.md)) để bắt lỗi trước khi triển khai |

3. **Triển khai lại sau khi sửa:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → chọn lại tác nhân → triển khai phiên bản mới.

### Triển khai mất quá nhiều thời gian

Container đa tác nhân mất thời gian khởi động lâu hơn vì chúng tạo 4 phiên bản tác nhân khi khởi động. Thời gian khởi động bình thường:

| Giai đoạn | Thời gian dự kiến |
|-------|------------------|
| Xây dựng ảnh container | 1-3 phút |
| Đẩy ảnh lên ACR | 30-60 giây |
| Khởi động container (tác nhân đơn) | 15-30 giây |
| Khởi động container (đa tác nhân) | 30-120 giây |
| Tác nhân sẵn sàng trong Playground | 1-2 phút sau khi báo “Đã khởi động” |

> Nếu trạng thái "Đang chờ" kéo dài hơn 5 phút, kiểm tra nhật ký container để phát hiện lỗi.

---

## Vấn đề RBAC và cấp phép

### `403 Forbidden` hoặc `AuthorizationFailed`

Bạn cần vai trò **[Foundry User](https://aka.ms/foundry-ext-project-role)** trên dự án Foundry của mình (trước đây gọi là **Azure AI User** - ID vai trò không đổi):

1. Vào [Azure Portal](https://portal.azure.com) → tài nguyên **dự án** Foundry của bạn.
2. Nhấp **Access control (IAM)** → **Role assignments**.
3. Tìm tên bạn → xác nhận có danh sách **Foundry User** (hoặc nhãn cũ **Azure AI User**).
4. Nếu thiếu: **Thêm** → **Add role assignment** → tìm **Foundry User** → gán cho tài khoản của bạn.

Tham khảo tài liệu [RBAC cho Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) để biết chi tiết.

### Mô hình triển khai không truy cập được

Nếu tác nhân trả về lỗi liên quan mô hình:

1. Xác nhận mô hình đã triển khai: thanh bên Foundry → mở rộng dự án → **Models** → kiểm tra `gpt-4.1-mini` (hoặc mô hình bạn) có trạng thái **Succeeded**.
2. Xác nhận tên triển khai trùng khớp: so sánh `AZURE_AI_MODEL_DEPLOYMENT_NAME` trong `.env` (hoặc `agent.yaml`) với tên triển khai thực tế trong thanh bên.
3. Nếu triển khai hết hạn (miễn phí): triển khai lại từ [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Vấn đề Foundry Local (Đường dẫn B)

### Dịch vụ Foundry Local không chạy

```powershell
# Kiểm tra trạng thái
foundry local status

# Khởi động dịch vụ nếu nó đang dừng
foundry local start
```

| Triệu chứng | Nguyên nhân | Sửa |
|---------|-------|-----|
| Kiểm tra sức khỏe trả về `503` | Dịch vụ chưa khởi động | Chạy `foundry local start` hoặc nhấn **Start** trong thanh bên Foundry Toolkit |
| Kiểm tra sức khỏe hết thời gian chờ | Mô hình đang tải | Đợi 30-60 giây sau khi khởi động; mô hình lớn hơn mất lâu hơn |
| `StatusCode: 404` trên `/v1/health` | Cổng sai | Mặc định là `5273`. Kiểm tra `foundry local status` xem cổng thực tế |
| Tài nguyên không đủ | Foundry Local cần ~4 GB RAM trống | Đóng các ứng dụng khác |
| Tải mô hình thất bại | Không đủ dung lượng đĩa | Mô hình từ 2-8 GB. Giải phóng dung lượng, rồi `foundry model pull <name>` |

### Tên mô hình không khớp

```powershell
# Liệt kê các mô hình đã tải xuống và bí danh chính xác của chúng
foundry model list
```

Đặt `AZURE_AI_MODEL_DEPLOYMENT_NAME` trong `.env` đúng với bí danh hiển thị (ví dụ, `phi-4-mini`, không phải `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` khi chạy cục bộ (Đường dẫn B)

`main.py` của lab dùng `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local yêu cầu biến này trỏ đến dịch vụ cục bộ - **không phải** `AZURE_AI_PROJECT_ENDPOINT`. Đảm bảo `.env` của bạn chứa:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Công cụ MCP vẫn gọi ra ngoài (Đường dẫn B)

Điều này là bình thường. Công cụ `search_microsoft_learn_for_plan` lấy tài nguyên học tập từ `https://learn.microsoft.com/api/mcp`. **Chỉ truy vấn tên kỹ năng** đi qua mạng - sơ yếu lý lịch và văn bản JD xử lý hoàn toàn trên thiết bị của bạn và không bao giờ được truyền đi. Nếu cần hoạt động hoàn toàn ngoại tuyến, thêm `try/except` trong công cụ để trả về URL tĩnh `learn.microsoft.com` khi endpoint không truy cập được.

---

## Nhận trợ giúp

Nếu bạn bị mắc kẹt sau khi thử sửa lỗi ở trên:

1. **Kiểm tra nhật ký máy chủ** - Hầu hết lỗi tạo ra traceback Python trong terminal. Đọc toàn bộ traceback.
2. **Tìm kiếm thông báo lỗi** - Sao chép văn bản lỗi và tìm kiếm trong [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Mở issue** - Tạo issue trên [kho lưu trữ workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) với:
   - Thông báo lỗi hoặc ảnh chụp màn hình
   - Các phiên bản gói của bạn (`pip list | Select-String "agent-framework"`)
   - Phiên bản Python của bạn (`python --version`)
   - Vấn đề xảy ra cục bộ hay sau triển khai

---

### Điểm kiểm tra

- [ ] Bạn biết cách kiểm tra và sửa lỗi cấu hình `.env`
- [ ] Bạn có thể xác minh phiên bản gói khớp bảng yêu cầu
- [ ] Bạn biết cách kiểm tra nhật ký container khi triển khai thất bại
- [ ] Bạn có thể xác minh vai trò RBAC trong Azure Portal

---

**Trước:** [07 - Kiểm tra trong Playground](07-verify-in-playground.md) · **Tiếp:** [09 - Tóm tắt →](09-summary.md) · **Trang chủ:** [Lab 02 README](../README.md) · [Trang chủ Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->