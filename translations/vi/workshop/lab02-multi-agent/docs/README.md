# Thí nghiệm 02 - Quy trình làm việc đa tác nhân: Đánh giá sự phù hợp hồ sơ → công việc

## Lộ trình học đầy đủ

Tài liệu này hướng dẫn bạn xây dựng, kiểm tra và triển khai một **quy trình làm việc đa tác nhân** đánh giá sự phù hợp giữa hồ sơ với công việc sử dụng bốn tác nhân chuyên biệt được điều phối thông qua **WorkflowBuilder**.

> **Điều kiện tiên quyết:** Hoàn thành [Thí nghiệm 01 - Tác nhân đơn](../../lab01-single-agent/README.md) trước khi bắt đầu Thí nghiệm 02.

---

## Các mô-đun

| # | Mô-đun | Những gì bạn sẽ làm |
|---|--------|--------------------|
| 0 | [Điều kiện tiên quyết](00-prerequisites.md) | Xác minh hoàn thành Thí nghiệm 01, hiểu các khái niệm đa tác nhân |
| 1 | [Hiểu kiến trúc đa tác nhân](01-understand-multi-agent.md) | Tìm hiểu WorkflowBuilder, vai trò tác nhân, đồ thị điều phối |
| 2 | [Khung dự án đa tác nhân](02-scaffold-multi-agent.md) | Sử dụng phần mở rộng Foundry để khung quy trình làm việc đa tác nhân |
| 3 | [Cấu hình tác nhân & môi trường](03-configure-agents.md) | Viết hướng dẫn cho 4 tác nhân, cấu hình công cụ MCP, thiết lập biến môi trường |
| 4 | [Mẫu điều phối](04-orchestration-patterns.md) | Khám phá phân nhánh song song, tập hợp theo thứ tự, và các mẫu thay thế |
| 5 | [Kiểm tra cục bộ](05-test-locally.md) | Gỡ lỗi F5 với Agent Inspector, chạy kiểm tra khói với hồ sơ + JD |
| 6 | [Triển khai lên Foundry](06-deploy-to-foundry.md) | Xây dựng container, đẩy lên ACR, đăng ký tác nhân lưu trữ |
| 7 | [Xác minh trong Playground](07-verify-in-playground.md) | Kiểm tra tác nhân đã triển khai trong VS Code và playground Foundry Portal |
| 8 | [Khắc phục sự cố](08-troubleshooting.md) | Sửa các vấn đề đa tác nhân phổ biến (lỗi MCP, đầu ra bị cắt ngắn, phiên bản gói) |

---

## Thời gian ước tính

| Trình độ kinh nghiệm | Thời gian |
|----------------------|-----------|
| Mới hoàn thành Thí nghiệm 01 | 45-60 phút |
| Có kinh nghiệm Azure AI | 60-90 phút |
| Lần đầu làm với đa tác nhân | 90-120 phút |

---

## Kiến trúc tổng quan

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Quay lại:** [Thí nghiệm 02 README](../README.md) · [Trang chủ Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố từ chối trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ gốc của nó nên được coi là nguồn chính xác và có thẩm quyền. Đối với thông tin quan trọng, nên sử dụng dịch thuật nhân sự chuyên nghiệp. Chúng tôi không chịu trách nhiệm về bất kỳ sự hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->