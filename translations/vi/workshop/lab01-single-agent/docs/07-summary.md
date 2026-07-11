# Module 7 - Tóm tắt & Các bước tiếp theo

⏱️ ~5 phút

**Chúc mừng!** Bạn đã xây dựng, kiểm thử, và (nếu theo Lộ trình A) triển khai một đại lý AI được lưu trữ sử dụng Microsoft Foundry và Bộ công cụ Foundry cho VS Code.

---

## Những gì bạn đã xây dựng

Một đại lý **"Giải thích Như Tôi Là Giám đốc"** mà:
- Nhận báo cáo sự cố kỹ thuật hoặc cập nhật vận hành qua HTTP (`POST /responses`)
- Dịch chúng thành tóm tắt ngôn ngữ đơn giản dành cho giám đốc
- Tuân theo định dạng đầu ra có cấu trúc (Chuyện đã xảy ra / Tác động kinh doanh / Bước tiếp theo)
- Từ chối các yêu cầu ngoài chủ đề và các cố gắng tiêm lệnh nhắc
- Chạy như một đại lý lưu trữ trong container trên Dịch vụ Đại lý Foundry của Microsoft

---

## Các khái niệm chính đã học

| Khái niệm | Những gì bạn đã thực hành |
|---------|-------------------|
| **Kiến trúc Agent Framework** | Pipeline `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Vòng đời Đại lý lưu trữ** | Scaffold → Cấu hình → Kiểm thử cục bộ → Triển khai → Xác minh trên đám mây |
| **Kỹ thuật prompt cho hệ thống** | Vai trò, đối tượng, định dạng đầu ra, quy tắc, giới hạn an toàn, và ví dụ |
| **Khác biệt giữa cục bộ và lưu trữ** | Định danh (chứng chỉ cá nhân so với định danh quản lý), điểm cuối, đường mạng |
| **Ranh giới an toàn** | Phòng chống tiêm prompt, tuân thủ vai trò, xử lý uyển chuyển các trường hợp cạnh |
| **Quy trình làm việc Foundry Toolkit** | Tạo dự án, triển khai mô hình, scaffold đại lý, Agent Inspector, triển khai một lần nhấp |

---

## Những gì bạn đã hoàn thành

### Lộ trình A (Đăng ký Foundry)

- [x] Thiết lập Foundry Toolkit và tạo dự án Foundry với mô hình đã triển khai
- [x] Scaffold đại lý lưu trữ với cấu trúc dự án tự động tạo
- [x] Viết hướng dẫn đại lý có cấu trúc với các quy tắc an toàn
- [x] Kiểm thử cục bộ với 3 kịch bản chức năng (Agent Inspector)
- [x] Triển khai lên Dịch vụ Đại lý Foundry (containerized)
- [x] Xác minh trên playground đám mây với 4 bài kiểm tra trường hợp cạnh / an toàn

### Lộ trình B (Foundry Local)

- [x] Thiết lập Foundry Toolkit với điểm cuối mô hình cục bộ
- [x] Scaffold dự án đại lý lưu trữ
- [x] Viết hướng dẫn đại lý có cấu trúc với các quy tắc an toàn
- [x] Kiểm thử cục bộ với 3 kịch bản chức năng
- [x] Xác thực hành vi đại lý mà không cần tài nguyên đám mây

---

## Các bước tiếp theo

### Tiếp tục học

| Tài nguyên | Mô tả |
|----------|-------------|
| **[Lab 02 - Điều phối đa đại lý](../../lab02-multi-agent/docs/README.md)** | Xây dựng quy trình 4 đại lý (Resume → Đánh giá phù hợp công việc) với các mẫu điều phối |
| **[Thêm công cụ vào đại lý của bạn](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Kết nối API, cơ sở dữ liệu, hoặc hàm tùy chỉnh qua Công cụ Catalog |
| **[Thêm kiến thức (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Nền tảng cho đại lý với tài liệu, kho vector, hoặc tìm kiếm Bing |
| **[Tài liệu Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Tham khảo đầy đủ nền tảng |
| **[Tham khảo SDK Agent Framework](https://learn.microsoft.com/agent-framework/)** | Tài liệu API cho gói `agent-framework` |
| **[Foundry Toolkit - Những cập nhật mới](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Ghi chú phát hành và nhật ký thay đổi tiện ích mở rộng |

### Ý tưởng mở rộng đại lý của bạn

- **Thêm công cụ ngày tháng** - Cho phép đại lý bao gồm ngữ cảnh "tính đến hôm nay" trong tóm tắt
- **Kết nối với cơ sở dữ liệu sự cố** - Lấy thông tin sự cố thực tế qua hàm công cụ
- **Thêm công cụ nguồn Bing** - Cho phép đại lý tra cứu tin tức gần đây để bổ sung ngữ cảnh
- **Thử mô hình khác nhau** - So sánh chất lượng đầu ra `gpt-4.1` và `gpt-4.1-mini`
- **Đánh giá với Foundry** - Dùng tính năng Đánh giá để đo lường chất lượng đại lý ở quy mô lớn

### Dành cho người dùng Lộ trình B: Nâng cấp lên triển khai đám mây

Khi bạn sẵn sàng triển khai lên đám mây:
1. Đăng ký Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Hoàn thành [Module 01, Thiết lập](01-setup.md#step-2-set-up-based-on-your-access) (tạo dự án, triển khai mô hình, gán RBAC)
3. Cập nhật `.env` với điểm cuối dự án Foundry và tên triển khai mô hình
4. Tiếp tục từ [Module 05 - Triển khai lên Foundry](05-deploy-to-foundry.md)

---

## Dọn dẹp tài nguyên (tuỳ chọn)

Nếu bạn muốn xóa các tài nguyên Azure đã tạo trong khóa học này:

### Tuỳ chọn 1: Xóa nhóm tài nguyên (xóa mọi thứ)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Tuỳ chọn 2: Xóa chỉ đại lý lưu trữ

1. Mở [ai.azure.com](https://ai.azure.com) → dự án của bạn → **Xây dựng** → **Các đại lý**.
2. Nhấp vào đại lý của bạn → nhấp **Xóa**.

### Tuỳ chọn 3: Xóa triển khai mô hình

1. Trong thanh bên Foundry, mở rộng dự án của bạn → **Mô hình**.
2. Nhấp phải vào triển khai mô hình → **Xóa**.

> **Lưu ý chi phí:** Đại lý lưu trữ chỉ phát sinh chi phí khi đang chạy. Nếu bạn dừng hoặc xóa đại lý, sẽ không còn phí phát sinh. Việc triển khai mô hình có thể phát sinh phí nhỏ cho dung lượng đặt trước - hãy xóa nếu bạn đã hoàn tất.

---

**Trước đó:** [06 - Xác minh trên Playground](06-verify-in-playground.md) · **Tiếp theo:** [08 - Khắc phục sự cố (Tham khảo) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->