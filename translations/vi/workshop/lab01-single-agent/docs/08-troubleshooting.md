# Module 8 - Khắc phục sự cố

Module này là hướng dẫn tham khảo cho mọi vấn đề thường gặp trong suốt buổi học. Hãy đánh dấu trang này - bạn sẽ quay lại đây mỗi khi có sự cố xảy ra.

---

## 1. Lỗi phân quyền

### 1.1 Từ chối quyền `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Nguyên nhân chính:** Bạn không có vai trò `Azure AI User` ở cấp **dự án**. Đây là lỗi phổ biến nhất trong buổi học.

**Cách khắc phục - theo từng bước:**

1. Mở [https://portal.azure.com](https://portal.azure.com).
2. Trong thanh tìm kiếm phía trên, nhập tên **dự án Foundry** của bạn (ví dụ `workshop-agents`).
3. **Quan trọng:** Nhấp vào kết quả có loại **"Microsoft Foundry project"**, KHÔNG phải tài khoản cha hoặc tài nguyên hub. Đây là các tài nguyên khác nhau với phạm vi RBAC khác nhau.
4. Ở thanh điều hướng bên trái của trang dự án, nhấp **Access control (IAM)**.
5. Nhấp tab **Role assignments** để kiểm tra bạn đã có vai trò này chưa:
   - Tìm tên hoặc email của bạn.
   - Nếu `Azure AI User` đã có → lỗi có nguyên nhân khác (xem Bước 8 bên dưới).
   - Nếu chưa có → tiếp tục thêm vai trò.
6. Nhấp **+ Add** → **Add role assignment**.
7. Ở tab **Role**:
   - Tìm [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Chọn nó trong danh sách.
   - Nhấp **Next**.
8. Ở tab **Members**:
   - Chọn **User, group, or service principal**.
   - Nhấp **+ Select members**.
   - Tìm tên hoặc email của bạn.
   - Chọn bản thân.
   - Nhấp **Select**.
9. Nhấp **Review + assign** → nhấp **Review + assign** lần nữa.
10. **Chờ 1-2 phút** - thay đổi RBAC cần thời gian lan truyền.
11. Thử lại thao tác bị lỗi.

> **Tại sao Owner/Contributor không đủ:** Azure RBAC có hai loại quyền - *hành động quản lý* và *hành động dữ liệu*. Owner và Contributor cho phép các hành động quản lý (tạo tài nguyên, thay đổi cài đặt), nhưng thao tác với agent yêu cầu quyền dữ liệu `agents/write`, chỉ có trong các vai trò `Azure AI User`, `Azure AI Developer` hoặc `Azure AI Owner`. Xem thêm [tài liệu Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` trong quá trình tạo tài nguyên

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Nguyên nhân chính:** Bạn không có quyền tạo hoặc sửa đổi tài nguyên Azure trong subscription/nhóm tài nguyên này.

**Cách khắc phục:**
1. Hỏi quản trị viên subscription cấp cho bạn vai trò **Contributor** trên nhóm tài nguyên nơi dự án Foundry đang nằm.
2. Hoặc nhờ họ tạo dự án Foundry cho bạn và cấp quyền **Azure AI User** trên dự án.

### 1.3 `SubscriptionNotRegistered` với [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Nguyên nhân chính:** Subscription Azure chưa đăng ký nhà cung cấp tài nguyên cần cho Foundry.

**Cách khắc phục:**

1. Mở terminal và chạy:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Chờ đăng ký xong (từ 1 đến 5 phút):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Kết quả mong đợi: `"Registered"`
3. Thử lại thao tác.

---

## 2. Lỗi Docker (chỉ khi đã cài Docker)

> Docker là **tùy chọn** cho buổi học này. Các lỗi này chỉ xảy ra nếu bạn đã cài Docker Desktop và extension Foundry cố xây dựng container cục bộ.

### 2.1 Docker daemon không chạy

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Cách khắc phục - từng bước:**

1. **Tìm Docker Desktop** trong menu Start (Windows) hoặc Applications (macOS) và khởi động nó.
2. Đợi cửa sổ Docker Desktop hiển thị **"Docker Desktop is running"** - thường mất 30-60 giây.
3. Tìm biểu tượng cá voi Docker ở system tray (Windows) hoặc thanh menu (macOS). Di chuột qua để xem trạng thái.
4. Kiểm tra trong terminal:
   ```powershell
   docker info
   ```
   Nếu in ra thông tin hệ thống Docker (Phiên bản Server, Storage Driver, v.v.), Docker đang chạy.
5. **Riêng Windows:** Nếu Docker vẫn không khởi động:
   - Mở Docker Desktop → **Settings** (biểu tượng bánh răng) → **General**.
   - Đảm bảo **Use the WSL 2 based engine** đã được tích.
   - Nhấn **Apply & restart**.
   - Nếu chưa cài WSL 2, chạy `wsl --install` trong PowerShell với quyền admin và khởi động lại máy.
6. Thử lại triển khai.

### 2.2 Docker build lỗi phụ thuộc

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Cách khắc phục:**
1. Mở `requirements.txt` và kiểm tra tên các package chính xác.
2. Đảm bảo việc cố định phiên bản đúng:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Thử cài ở máy local trước:
   ```bash
   pip install -r requirements.txt
   ```
4. Nếu dùng kho package riêng tư, đảm bảo Docker có kết nối mạng tới đó.

### 2.3 Không tương thích nền tảng container (Apple Silicon)

Nếu triển khai từ Mac Apple Silicon (M1/M2/M3/M4), container phải được build cho `linux/amd64` vì runtime container của Foundry dùng AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Lệnh deploy của extension Foundry thường xử lý tự động. Nếu bạn gặp lỗi liên quan kiến trúc, hãy build thủ công với cờ `--platform` và liên hệ đội Foundry.

---

## 3. Lỗi xác thực

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) không lấy được token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Nguyên nhân chính:** Không có nguồn credential nào trong chuỗi `DefaultAzureCredential` có token hợp lệ.

**Cách khắc phục - thử từng bước theo thứ tự:**

1. **Đăng nhập lại qua Azure CLI** (cách phổ biến nhất):
   ```bash
   az login
   ```
   Một cửa sổ trình duyệt mở ra. Đăng nhập rồi quay lại VS Code.

2. **Chọn đúng subscription:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Nếu đây không phải subscription đúng:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Đăng nhập lại qua VS Code:**
   - Nhấp biểu tượng **Accounts** (biểu tượng người) ở góc dưới bên trái VS Code.
   - Nhấp tên tài khoản → **Sign Out**.
   - Nhấp lại biểu tượng Accounts → **Sign in to Microsoft**.
   - Hoàn tất quy trình đăng nhập qua trình duyệt.

4. **Service principal (chỉ cho kịch bản CI/CD):**
   - Đặt các biến môi trường này trong `.env`:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Sau đó khởi động lại tiến trình agent.

5. **Kiểm tra cache token:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Nếu lỗi, token CLI của bạn đã hết hạn. Chạy lại `az login`.

### 3.2 Token hoạt động ở local nhưng lỗi ở triển khai hosted

**Nguyên nhân chính:** Agent hosted dùng identity quản lý hệ thống, khác với credential cá nhân của bạn.

**Cách khắc phục:** Đây là hành vi dự kiến - identity quản lý được cấp tự động khi triển khai. Nếu agent hosted vẫn báo lỗi auth:
1. Kiểm tra xem managed identity của dự án Foundry có quyền truy cập tài nguyên Azure OpenAI không.
2. Xác nhận `PROJECT_ENDPOINT` trong `agent.yaml` đúng.

---

## 4. Lỗi với mô hình

### 4.1 Không tìm thấy deployment mô hình

```
Error: Model deployment not found / The specified deployment does not exist
```

**Cách khắc phục - từng bước:**

1. Mở file `.env` và ghi chú giá trị `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Mở thanh bên **Microsoft Foundry** trong VS Code.
3. Mở rộng dự án của bạn → **Model Deployments**.
4. So sánh tên deployment liệt kê với giá trị trong `.env`.
5. Tên phân biệt chữ hoa chữ thường - ví dụ `gpt-4o` khác `GPT-4o`.
6. Nếu không khớp, cập nhật `.env` dùng đúng tên trong sidebar.
7. Với triển khai hosted, đồng thời cập nhật `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Mô hình trả về nội dung không mong muốn

**Cách khắc phục:**
1. Xem lại hằng `EXECUTIVE_AGENT_INSTRUCTIONS` trong `main.py`. Đảm bảo không bị cắt bớt hoặc hỏng.
2. Kiểm tra tham số nhiệt độ mô hình (nếu có thể cấu hình) - giá trị thấp cho kết quả chắc chắn hơn.
3. So sánh mô hình được deploy (ví dụ `gpt-4o` và `gpt-4o-mini`) - các mô hình khác nhau có năng lực khác nhau.

---

## 5. Lỗi triển khai

### 5.1 Phân quyền kéo hình ACR

```
Error: AcrPullUnauthorized
```

**Nguyên nhân chính:** Managed identity của dự án Foundry không thể kéo image container từ Azure Container Registry.

**Cách khắc phục - từng bước:**

1. Mở [https://portal.azure.com](https://portal.azure.com).
2. Tìm **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** trong thanh tìm kiếm trên cùng.
3. Nhấp vào registry liên quan tới dự án Foundry của bạn (thường ở cùng nhóm tài nguyên).
4. Trong điều hướng bên trái, nhấp **Access control (IAM)**.
5. Nhấp **+ Add** → **Add role assignment**.
6. Tìm và chọn vai trò **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)**. Nhấn **Next**.
7. Chọn **Managed identity** → nhấp **+ Select members**.
8. Tìm và chọn managed identity của dự án Foundry.
9. Nhấp **Select** → **Review + assign** → **Review + assign**.

> Phân quyền này thường do extension Foundry tự thiết lập. Nếu bạn thấy lỗi này, việc thiết lập tự động có thể đã thất bại. Bạn cũng có thể thử triển khai lại - extension có thể thử thiết lập lại.

### 5.2 Agent không khởi động sau triển khai

**Triệu chứng:** Trạng thái container giữ ở "Pending" hơn 5 phút hoặc hiện "Failed".

**Cách khắc phục - từng bước:**

1. Mở thanh bên **Microsoft Foundry** trong VS Code.
2. Nhấp vào agent hosted của bạn → chọn phiên bản.
3. Trong bảng chi tiết, kiểm tra phần **Container Details** → tìm phần **Logs** hoặc link.
4. Đọc log khởi động container. Nguyên nhân phổ biến:

| Thông báo log | Nguyên nhân | Cách khắc phục |
|-------------|-------------|---------------|
| `ModuleNotFoundError: No module named 'xxx'` | Thiếu phụ thuộc | Thêm vào `requirements.txt` và triển khai lại |
| `KeyError: 'PROJECT_ENDPOINT'` | Thiếu biến môi trường | Thêm biến env vào `agent.yaml` dưới phần `env:` |
| `OSError: [Errno 98] Address already in use` | Xung đột cổng | Đảm bảo `agent.yaml` có `port: 8088` và chỉ một tiến trình dùng cổng này |
| `ConnectionRefusedError` | Agent không bắt đầu lắng nghe | Kiểm tra `main.py` - lệnh `from_agent_framework()` phải chạy lúc khởi động |

5. Sửa lỗi, rồi triển khai lại theo [Module 6](06-deploy-to-foundry.md).

### 5.3 Triển khai hết thời gian chờ

**Cách khắc phục:**
1. Kiểm tra kết nối internet - thao tác Docker push có thể lớn (>100MB lần đầu).
2. Nếu dùng proxy công ty, đảm bảo cấu hình proxy trong Docker Desktop: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Thử lại - sự cố mạng tạm thời có thể gây lỗi ngắt quãng.

---

## 6. Tham khảo nhanh: Các vai trò RBAC

| Vai trò | Phạm vi thường dùng | Quyền cấp |
|---------|---------------------|-----------|
| **Azure AI User** | Dự án | Hành động dữ liệu: build, deploy, gọi agent (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Dự án hoặc Tài khoản | Hành động dữ liệu + tạo dự án |
| **Azure AI Owner** | Tài khoản | Toàn quyền + quản lý phân quyền |
| **Azure AI Project Manager** | Dự án | Hành động dữ liệu + có thể phân vai Azure AI User cho người khác |
| **Contributor** | Subscription/RG | Hành động quản lý (tạo/xóa tài nguyên). **KHÔNG BAO GỒM hành động dữ liệu** |
| **Owner** | Subscription/RG | Hành động quản lý + phân quyền. **KHÔNG BAO GỒM hành động dữ liệu** |
| **Reader** | Bất kỳ | Quyền đọc quản lý |

> **Điểm chính:** Vai trò `Owner` và `Contributor` KHÔNG BAO GỒM hành động dữ liệu. Bạn luôn cần vai trò `Azure AI *` để thao tác với agent. Vai trò tối thiểu cho buổi học là **Azure AI User** ở phạm vi **dự án**.

---

## 7. Bảng kiểm tra hoàn thành workshop

Dùng bảng này để xác nhận cuối cùng bạn đã hoàn thành tất cả:

| # | Mục | Module | Đã xong? |
|---|------|--------|---------|
| 1 | Đã cài và kiểm tra tất cả điều kiện tiên quyết | [00](00-prerequisites.md) | |
| 2 | Đã cài Foundry Toolkit và extension Foundry | [01](01-install-foundry-toolkit.md) | |
| 3 | Đã tạo dự án Foundry (hoặc chọn dự án có sẵn) | [02](02-create-foundry-project.md) | |
| 4 | Mô hình đã triển khai (ví dụ: gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Vai trò Người dùng Azure AI được gán ở phạm vi dự án | [02](02-create-foundry-project.md) | |
| 6 | Dự án tác nhân lưu trữ được khung sườn (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` được cấu hình với PROJECT_ENDPOINT và MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Hướng dẫn tác nhân tùy chỉnh trong main.py | [04](04-configure-and-code.md) | |
| 9 | Môi trường ảo được tạo và các phụ thuộc được cài đặt | [04](04-configure-and-code.md) | |
| 10 | Tác nhân được thử nghiệm cục bộ với F5 hoặc terminal (4 bài kiểm tra khói vượt qua) | [05](05-test-locally.md) | |
| 11 | Đã triển khai tới Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Trạng thái container hiển thị "Started" hoặc "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Đã xác minh trong VS Code Playground (4 bài kiểm tra khói vượt qua) | [07](07-verify-in-playground.md) | |
| 14 | Đã xác minh trong Foundry Portal Playground (4 bài kiểm tra khói vượt qua) | [07](07-verify-in-playground.md) | |

> **Chúc mừng bạn!** Nếu tất cả các mục đều được đánh dấu, bạn đã hoàn thành toàn bộ hội thảo. Bạn đã xây dựng một tác nhân lưu trữ từ đầu, thử nghiệm nó cục bộ, triển khai nó lên Microsoft Foundry, và xác thực nó trong môi trường thực tế.

---

**Trước:** [07 - Xác minh trong Playground](07-verify-in-playground.md) · **Trang chủ:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ bản địa nên được coi là nguồn tham khảo chính thức. Đối với thông tin quan trọng, khuyến nghị sử dụng dịch thuật chuyên nghiệp do con người thực hiện. Chúng tôi không chịu trách nhiệm về bất kỳ sự hiểu nhầm hay giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->