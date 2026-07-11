# Module 8 - Khắc phục sự cố

Mô-đun này là hướng dẫn tham khảo cho các sự cố phổ biến. Đánh dấu trang và quay lại khi có sự cố xảy ra.

---

## 1. Lỗi quyền truy cập

### 1.1 Từ chối quyền `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Nguyên nhân gốc rễ:** Thiếu vai trò `Azure AI User` ở cấp **dự án**. Đây là lỗi phổ biến nhất trong workshop.

**Cách khắc phục:**
1. Mở [portal.azure.com](https://portal.azure.com).
2. Tìm kiếm tên **dự án** Foundry của bạn → nhấp vào kết quả có loại **"Microsoft Foundry project"** (KHÔNG phải tài khoản chính).
3. **Quản lý truy cập (IAM)** → **+ Thêm** → **Thêm phân quyền vai trò**.
4. Vai trò: **Azure AI User** → Tiếp theo.
5. Thành viên: Chọn bạn → Xem lại + gán → Xem lại + gán.
6. **Chờ 1–2 phút** → thử lại.

> **Tại sao Owner/Contributor không đủ:** Các vai trò này chỉ cấp quyền thao tác *quản lý*. Hoạt động của agent cần quyền `agents/write` *hành động dữ liệu*, chỉ có trong `Azure AI User`, `Azure AI Developer`, hoặc `Azure AI Owner`. Xem thêm [tài liệu Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 Lỗi `AuthorizationFailed` trong quá trình cung cấp

**Cách khắc phục:** Yêu cầu quản trị viên gán vai trò **Contributor** trên nhóm tài nguyên, hoặc để họ tạo dự án cho bạn và cấp cho bạn **Azure AI User** trên dự án đó.

### 1.3 Lỗi `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Chờ đến khi: "Đã đăng ký"
```

---

## 2. Lỗi Docker

> Docker là **tùy chọn**. Những lỗi này chỉ áp dụng nếu Docker Desktop được cài đặt và tiện ích mở rộng cố gắng thực hiện build cục bộ.

### 2.1 Docker daemon không chạy

**Cách khắc phục:** Khởi động Docker Desktop → chờ trạng thái "đang chạy" → kiểm tra bằng lệnh `docker info` → thử lại.

### 2.2 Build thất bại do lỗi phụ thuộc

**Cách khắc phục:** Kiểm tra chính tả file `requirements.txt`, thử cài đặt cục bộ trước: `pip install -r requirements.txt`.

### 2.3 Không tương thích nền tảng (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Lỗi xác thực

### 3.1 `DefaultAzureCredential` thất bại

**Cách khắc phục (thử theo thứ tự):**
1. `az login` (đăng nhập lại)
2. `az account set --subscription "<id>"` (chọn đúng subscription)
3. VS Code → Tài khoản → Đăng xuất → Đăng nhập lại
4. Xác minh: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token hiệu quả ở cục bộ nhưng không ở môi trường lưu trữ

**Mong đợi:** Các agent lưu trữ sử dụng nhận dạng quản lý hệ thống, không dùng thông tin đăng nhập của bạn. Nếu agent lưu trữ gặp lỗi xác thực:
- Xác nhận `AZURE_AI_PROJECT_ENDPOINT` trong `agent.yaml` là chính xác
- Kiểm tra rằng nhận dạng quản lý của dự án có quyền truy cập mô hình

---

## 4. Lỗi mô hình

### 4.1 Không tìm thấy triển khai mô hình

**Cách khắc phục:** Tên phân biệt chữ hoa chữ thường. So sánh trong `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` với tên chính xác trong thanh bên Foundry → Models.

### 4.2 Kết quả mô hình không mong muốn

**Cách khắc phục:** Xem lại `AGENT_INSTRUCTIONS` trong `main.py` (không bị cắt bớt?). Thử dùng mô hình khác (`gpt-4.1` so với `gpt-4.1-mini`).

---

## 5. Lỗi triển khai

### 5.1 Không được phép kéo từ ACR

**Cách khắc phục:** Vào Azure Portal → Container Registry → Quản lý truy cập (IAM) → Thêm vai trò **AcrPull** cho nhận dạng quản lý của dự án Foundry.

### 5.2 Agent không khởi động được (ở trạng thái "Đang chờ" hoặc "Thất bại")

Kiểm tra nhật ký container trong thanh bên. Các nguyên nhân phổ biến:

| Thông báo nhật ký | Cách khắc phục |
|-------------|-----|
| `ModuleNotFoundError` | Thêm gói thiếu vào `requirements.txt`, triển khai lại |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Thêm biến môi trường vào `agent.yaml` dưới `environment_variables` |
| `Address already in use` | Đảm bảo chỉ có một tiến trình sử dụng cổng 8088 |

### 5.3 Triển khai bị timeout

**Cách khắc phục:** Kiểm tra kết nối internet. Lần đầu triển khai đẩy >100MB. Có dùng proxy không? Cấu hình proxy cho Docker Desktop.

---

## 6. Hướng B - Foundry Local

### 6.1 Foundry Local không khởi động được

| Vấn đề | Cách khắc phục |
|-------|-----|
| `foundry: command not found` | Cài lại: `winget install Microsoft.FoundryLocal` |
| Tài nguyên không đủ | Foundry Local cần ~4GB RAM trống. Đóng các ứng dụng khác. |
| Tải mô hình thất bại | Kiểm tra dung lượng đĩa (mô hình 2–8 GB). Thử lại: `foundry local models pull <name>` |

### 6.2 Lỗi mô hình Foundry Local

| Vấn đề | Cách khắc phục |
|-------|-----|
| Phản hồi chậm | Bình thường - mô hình cục bộ chạy trên CPU trừ khi bạn có GPU. Hãy kiên nhẫn. |
| Kết quả chất lượng kém | Thử mô hình lớn hơn nếu phần cứng cho phép. `phi-4-mini` là lựa chọn cân bằng tốt. |
| Kết nối bị từ chối | Xác nhận Foundry Local đang chạy: `foundry local status`. Khởi động lại nếu cần. |

---

## 7. Tham chiếu nhanh: vai trò RBAC

| Vai trò | Phạm vi | Quyền cấp |
|------|-------|--------|
| **Azure AI User** | Dự án | Hành động dữ liệu: `agents/write`, `agents/read` |
| **Azure AI Developer** | Dự án/Tài khoản | Hành động dữ liệu + tạo dự án |
| **Azure AI Owner** | Tài khoản | Toàn quyền truy cập + quản lý vai trò |
| **Contributor** | Subscription/Nhóm tài nguyên | Chỉ hành động quản lý (**không** hành động dữ liệu) |
| **Owner** | Subscription/Nhóm tài nguyên | Quản lý + gán vai trò (**không** hành động dữ liệu) |

---

## 8. Danh sách kiểm tra hoàn thành workshop

| # | Mục | Mô-đun |
|---|------|--------|
| 1 | Cài đặt và xác nhận các yêu cầu cần thiết | [00](00-prerequisites.md) |
| 2 | Cài đặt tiện ích Foundry Toolkit, kết nối dự án (hoặc cấu hình Hướng B) | [01](01-setup.md) |
| 3 | Tạo sẵn agent lưu trữ | [02](02-create-hosted-agent.md) |
| 4 | Cấu hình `.env`, viết hướng dẫn, cài đặt phụ thuộc | [03](03-configure-and-code.md) |
| 5 | Kiểm tra agent cục bộ - vượt qua 3 kịch bản chức năng | [04](04-test-locally.md) |
| 6 | Triển khai lên Foundry (chỉ Hướng A) | [05](05-deploy-to-foundry.md) |
| 7 | Kiểm tra các trường hợp biên / an toàn trên đám mây (chỉ Hướng A) | [06](06-verify-in-playground.md) |
| 8 | Đánh giá tóm tắt, xác định bước tiếp theo | [07](07-summary.md) |

---

**Trước đó:** [07 - Tóm tắt](07-summary.md) · **Trang chủ:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->