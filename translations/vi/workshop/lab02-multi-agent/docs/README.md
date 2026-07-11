# Bài Lab 02 - Quy trình làm việc đa tác nhân: Tự truyện → Đánh giá phù hợp công việc

## Lộ trình học đầy đủ

Tài liệu này hướng dẫn bạn xây dựng, kiểm tra và triển khai một **quy trình làm việc đa tác nhân** đánh giá sự phù hợp giữa hồ sơ xin việc và công việc sử dụng bốn tác nhân chuyên biệt được điều phối qua **WorkflowBuilder**.

> **Yêu cầu trước:** Hoàn thành [Lab 01 - Tác nhân đơn](../../lab01-single-agent/README.md) trước khi bắt đầu Lab 02.

---

## Các mô-đun

| # | Mô-đun | Bạn sẽ làm gì |
|---|--------|---------------|
| 0 | [Giới thiệu](00-prerequisites.md) | Những gì bạn sẽ xây dựng, xác minh Lab 01, so sánh Lab 02 với Lab 01 |
| 1 | [Hiểu kiến trúc đa tác nhân](01-understand-multi-agent.md) | Tìm hiểu WorkflowBuilder, vai trò tác nhân, đồ thị điều phối |
| 2 | [Khung dự án đa tác nhân](02-scaffold-multi-agent.md) | Sử dụng trình hướng dẫn tiện ích Foundry để khung dự án cơ bản |
| 3 | [Cấu hình tác nhân & Môi trường](03-configure-agents.md) | Viết hướng dẫn cho 4 tác nhân, cấu hình công cụ MCP, đặt biến môi trường |
| 4 | [Mẫu điều phối](04-orchestration-patterns.md) | Chuỗi tuần tự, truyền nội dung, và phép OR trong WorkflowBuilder |
| 5 | [Kiểm tra tại chỗ](05-test-locally.md) | Gỡ lỗi F5 với Agent Inspector, chạy kiểm tra nhanh với hồ sơ + mô tả công việc |
| 6 | [Triển khai lên Foundry](06-deploy-to-foundry.md) | Xây dựng container, đẩy lên ACR, đăng ký tác nhân lưu trữ |
| 7 | [Xác minh trên Playground](07-verify-in-playground.md) | Thử nghiệm tác nhân triển khai trong VS Code và cổng playground Foundry |
| 8 | [Khắc phục sự cố](08-troubleshooting.md) | Sửa lỗi đa tác nhân thường gặp (lỗi MCP, đầu ra bị cắt, phiên bản gói) |
| 9 | [Tóm tắt & Bước tiếp theo](09-summary.md) | Những gì bạn đã xây dựng, khái niệm chính đã học, dọn dẹp, và hướng đi tiếp theo |

---

**Quay lại:** [Lab 02 README](../README.md) · [Trang chủ Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->