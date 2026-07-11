# Mô-đun 9 - Tóm tắt & Các bước tiếp theo

⏱️ ~5 phút

**Chúc mừng!** Bạn đã xây dựng, thử nghiệm và (nếu theo Đường dẫn A) triển khai một quy trình làm việc đa tác nhân sử dụng Microsoft Foundry và Bộ công cụ Foundry cho VS Code.

---

## Những gì bạn đã xây dựng

**Trình đánh giá Resume → Phù hợp công việc** - một quy trình làm việc đa tác nhân được lưu trữ mà:
- Nhận một bản lý lịch + mô tả công việc qua HTTP (`POST /responses`)
- Chạy bốn tác nhân chuyên dụng trong một dãy pipeline tuần tự - mỗi tác nhân chuyển tiếp dữ liệu mà tác nhân kế tiếp cần
- Trả về điểm phù hợp (0–100 kèm phân tích chi tiết), danh sách khoảng cách kỹ năng và chứng chỉ, cùng lộ trình học tập cá nhân hóa với các liên kết Microsoft Learn thật cho từng khoảng cách
- Gọi máy chủ Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) để lấy tài nguyên học tập chính thức cho mỗi khoảng cách kỹ năng được xác định
- Chạy như một tác nhân được lưu trữ container hóa đơn lẻ trong Microsoft Foundry Agent Service

---

## Những khái niệm chính đã học

| Khái niệm | Những gì bạn đã thực hành |
|---------|-------------------|
| **Điều phối đa tác nhân** | `WorkflowBuilder` pipeline tuần tự với `add_edge()` |
| **Chuyên môn hóa tác nhân** | Bốn tác nhân tập trung vượt trội hơn một tác nhân đa năng chung |
| **Mô hình Bộ định tuyến nội dung** | ResumeParser kiêm vai trò bộ định tuyến - nó giữ nguyên văn bản JD trong phần `[JOB DESCRIPTION PASS-THROUGH]` để các tác nhân phía sau có thể truy cập (cần thiết vì `context_mode="last_agent"` nghĩa là chỉ `start_executor` xem được tin nhắn gốc của người dùng) |
| **Mô hình Chuyển tiếp nội dung** | Tác nhân JD chuyển tiếp `[PARSED RESUME PASS-THROUGH]` để MatchingAgent nhận được cả hai hồ sơ; tránh được kích hoạt đôi theo kiểu OR mà các đồ thị fan-in gây ra |
| **Tích hợp công cụ MCP** | `@tool` + `streamable_http_client` gọi máy chủ MCP ngoài |
| **Vòng đời Tác nhân được lưu trữ** | Tạo khung → Cấu hình → Thử nghiệm cục bộ → Triển khai → Xác minh trên đám mây |
| **`context_mode="last_agent"`** | Mỗi executor chỉ thấy kết quả đầu ra của người tiền nhiệm trực tiếp |
| **Quy trình Foundry Toolkit** | Trình hướng dẫn tạo khung, Kiểm tra tác nhân, Trình trực quan quy trình, triển khai một cú nhấp chuột |

---

## Những gì bạn đã hoàn thành

<details open>
<summary><strong>🅰️ Đường dẫn A - Đăng ký Foundry</strong></summary>

- [x] Xác minh cài đặt Lab 01: dự án, mô hình, và RBAC vẫn hoạt động
- [x] Tạo khung dự án đa tác nhân sử dụng mẫu Workflows
- [x] Viết bốn bộ hướng dẫn cho tác nhân (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Tích hợp công cụ Microsoft Learn MCP với `streamable_http_client`
- [x] Kết nối sơ đồ quy trình làm việc bằng `WorkflowBuilder` (pipeline tuần tự với chuyển tiếp nội dung)
- [x] Thử nghiệm cục bộ với 3 bài kiểm tra khói (Agent Inspector) - điểm phù hợp, thẻ khoảng cách, và URL MCP
- [x] Triển khai lên Foundry Agent Service (container hóa, định danh quản lý)
- [x] Xác minh trên đám mây playground - độ nhất quán cấu trúc với kết quả cục bộ

</details>

<details open>
<summary><strong>🅱️ Đường dẫn B - Foundry Local</strong></summary>

- [x] Xác minh cài đặt Lab 01: Foundry Local đang chạy với mô hình cục bộ
- [x] Tạo khung dự án đa tác nhân sử dụng mẫu Workflows
- [x] Viết bốn bộ hướng dẫn cho tác nhân và kết nối sơ đồ quy trình làm việc
- [x] Tích hợp công cụ Microsoft Learn MCP
- [x] Thử nghiệm cục bộ với 3 bài kiểm tra khói
- [x] Xác thực hành vi đa tác nhân mà không cần tài nguyên đám mây

</details>

---

## Các bước tiếp theo

### Tiếp tục học tập

| Tài nguyên | Mô tả |
|----------|-------------|
| **[Tài liệu tham khảo Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Tài liệu API cho `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Danh mục công cụ MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Kết nối các tác nhân tới các máy chủ MCP khác (Bing, GitHub, tùy chỉnh) |
| **[Thêm kiến thức (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Cung cấp nền tảng cho tác nhân dựa trên tài liệu, kho vector hoặc tìm kiếm Bing |
| **[Các đánh giá Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Đo lường chất lượng tác nhân ở quy mô lớn với các bộ đánh giá tự động |
| **[Tài liệu Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Tài liệu tham khảo toàn diện về nền tảng |
| **[Foundry Toolkit - Có gì mới](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Ghi chú phát hành tiện ích mở rộng và nhật ký thay đổi |

### Ý tưởng mở rộng quy trình làm việc này

- **Thêm tác nhân thứ 5** - Một huấn luyện viên phỏng vấn tạo ra các câu hỏi phỏng vấn khả dĩ dựa trên báo cáo khoảng cách
- **Thêm công cụ nền Bing** - Cho phép tác nhân JD tìm kiếm các việc làm tương tự để bổ sung yêu cầu
- **Kết nối với cơ sở dữ liệu lý lịch** - Lấy hồ sơ ứng viên từ cơ sở dữ liệu qua một `@tool` tùy chỉnh
- **Thử các mô hình khác nhau** - So sánh chất lượng và độ trễ đầu ra giữa `gpt-4.1` và `gpt-4.1-mini`
- **Đánh giá với Foundry** - Sử dụng tính năng Evaluations để chấm điểm các báo cáo phù hợp với bộ dữ liệu chuẩn

### Dành cho người dùng Đường dẫn B: Nâng cấp lên triển khai đám mây

Khi bạn sẵn sàng triển khai lên đám mây:
1. Lấy đăng ký Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Hoàn thành [Lab 01, Mô-đun 01](../../lab01-single-agent/docs/01-setup.md) (tạo dự án, triển khai mô hình, gán RBAC)
3. Cập nhật `.env` của bạn với điểm cuối dự án Foundry và tên triển khai mô hình
4. Tiếp tục từ [Mô-đun 06 - Triển khai đến Foundry](06-deploy-to-foundry.md)

---

## Dọn dẹp tài nguyên (tùy chọn)

Nếu bạn muốn xóa các tài nguyên Azure được tạo trong quá trình workshop này:

### Lựa chọn 1: Xóa nhóm tài nguyên (xóa hết tất cả)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Lựa chọn 2: Xóa chỉ tác nhân được lưu trữ

1. Mở [ai.azure.com](https://ai.azure.com) → dự án của bạn → **Xây dựng** → **Tác nhân**.
2. Tìm **PersonalCareerCopilot** → nhấp **Xóa**.

### Lựa chọn 3: Xóa triển khai mô hình

1. Trong thanh bên Foundry, mở rộng dự án của bạn → **Mô hình**.
2. Nhấp chuột phải vào triển khai mô hình → **Xóa**.

> **Lưu ý chi phí:** Tác nhân được lưu trữ chỉ phát sinh chi phí khi đang chạy. Nếu bạn dừng hoặc xóa tác nhân, không có chi phí liên tục. Triển khai mô hình có thể phát sinh một khoản phí nhỏ cho dung lượng dự trữ - hãy xóa nếu bạn đã hoàn tất.

---

**Trước:** [08 - Khắc phục sự cố](08-troubleshooting.md) · **Trang chủ:** [README Lab 02](../README.md) · [Trang chủ Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->