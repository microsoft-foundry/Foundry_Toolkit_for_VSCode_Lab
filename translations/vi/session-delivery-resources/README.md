# Cách trình bày phiên này

Cảm ơn bạn đã trình bày phiên này!

Trước khi trình bày workshop, vui lòng:

1. Đọc tài liệu này cùng tất cả các tài nguyên đi kèm một cách đầy đủ.
2. Xem bản ghi hình trình bày phiên và hướng dẫn thực hiện workshop từ đầu đến cuối.
3. Thực hiện từng lab tương tác trên máy cá nhân của bạn **ít nhất một lần** trước sự kiện.
4. Xác nhận dự án Microsoft Foundry, việc triển khai mô hình, và hạn mức của bạn.
5. Liên hệ với người duy trì nếu có bất kỳ điều gì chưa rõ.

---

## Tóm tắt file

| Tài nguyên                    | Liên kết                                                                         | Mô tả                                                                                     |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Bộ slide workshop             | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                   | Slide trình chiếu cho workshop này với ghi chú người trình bày và video demo nhúng         |
| Bản ghi hình trình bày phiên  | _Do người duy trì cung cấp_                                                      | Bản ghi hình giới thiệu workshop và hướng dẫn theo slide                                  |
| Bản ghi hình toàn bộ workshop | _Do người duy trì cung cấp_                                                      | Bản ghi toàn bộ quá trình làm hai lab từ góc nhìn người học                               |
| Tài liệu workshop             | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Kho nguồn, các README lab, các module từng bước                                         |
| Lab 01 - tác nhân đơn         | [Lab 01](../workshop/lab01-single-agent/README.md)                              | Lab tương tác: xây dựng, kiểm thử, và triển khai tác nhân *Explain Like I'm an Executive* |
| Lab 02 - quy trình đa tác nhân | [Lab 02](../workshop/lab02-multi-agent/README.md)                              | Lab tương tác: xây dựng quy trình 4 tác nhân *Resume to Job Fit Evaluator*                |
| Demo 1: Tác nhân Executive    | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                            | Demo Lab 01: dịch thuật thuật ngữ kỹ thuật thành tóm tắt dành cho lãnh đạo                |
| Demo 2: Đánh giá CV phù hợp   | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)  | Demo Lab 02: quy trình 4 tác nhân chấm điểm sự phù hợp CV-công việc và tạo đề xuất       |

> **Lưu ý dành cho người đào tạo:** Bộ slide và liên kết video sẽ được bổ sung sau khi bản ghi phát hành. Đến lúc đó, hãy liên hệ người duy trì (xem [Liên hệ](#liên-hệ)) để có tài nguyên mới nhất.

---

## Bắt đầu

Workshop này dạy các nhà phát triển cách xây dựng, kiểm thử, và triển khai tác nhân AI vào **Microsoft Foundry Agent Service** như **Tác nhân được lưu trữ** hoàn toàn từ VS Code, sử dụng tiện ích mở rộng **Microsoft Foundry Toolkit**.

Workshop được chia thành nhiều phần bao gồm slide, **2 demo trực tiếp**, và **2 lab thực hành**.

### Thời gian biểu

#### Trình bày đầy đủ (khoảng 2 giờ)

| Thời gian       | Mô tả                                                               |
|-----------------|---------------------------------------------------------------------|
| 0:00 - 10:00    | Giới thiệu: tác nhân được lưu trữ, Dịch vụ Foundry Agent, và toolkit |
| 10:00 - 20:00   | Demo: Tác nhân Executive từ đầu đến cuối                            |
| 20:00 - 60:00   | Lab 01 - tác nhân đơn (xây dựng, kiểm thử cục bộ, triển khai, playground) |
| 60:00 - 110:00  | Lab 02 - quy trình đa tác nhân (Đánh giá CV phù hợp công việc)       |
| 110:00 - 120:00 | Tổng kết, hỏi đáp, và các tài nguyên học tiếp                       |

#### Trình bày ngắn (khoảng 75 phút)

| Thời gian      | Mô tả                                                            |
|---------------|------------------------------------------------------------------|
| 0:00 - 10:00  | Giới thiệu và tổng quan                                         |
| 10:00 - 20:00 | Demo: Tác nhân Executive                                       |
| 20:00 - 70:00 | Chỉ Lab 01 (hướng dẫn người học Lab 02 tự học)                 |
| 70:00 - 75:00 | Tổng kết và hỏi đáp                                            |

### Chuẩn bị

| Tài nguyên                    | Liên kết                                                                                  | Mô tả                                                 |
|-------------------------------|-------------------------------------------------------------------------------------------|-------------------------------------------------------|
| Tài liệu workshop             | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)         | Tài liệu và mã nguồn workshop                          |
| Hướng dẫn Lab 01             | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                            | Lab tương tác: tác nhân đơn lưu trữ                    |
| Hướng dẫn Lab 02             | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                              | Lab tương tác: quy trình đa tác nhân                    |
| Danh sách kiểm tra yêu cầu    | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)            | Công cụ, tài khoản, và quyền truy cập Azure cần thiết  |
| Hướng dẫn nhanh tác nhân lưu trữ (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Hướng dẫn triển khai tác nhân lưu trữ chính thức bằng `azd` |
| Sẵn có vùng cho tác nhân lưu trữ | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Các vùng hỗ trợ tác nhân lưu trữ (bản xem trước)      |

### Yêu cầu dành cho người đào tạo

Trước khi bạn trình bày, hãy đảm bảo bạn có:

- Một **đăng ký Azure** với quyền tạo tài nguyên (Owner hoặc Contributor trên nhóm tài nguyên).
- Quyền truy cập vào **dự án Microsoft Foundry** trong [vùng hỗ trợ tác nhân lưu trữ](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Hạn mức cho **gpt-4.1** (hoặc **gpt-4.1-mini**) trong dự án Foundry của bạn.
- Các công cụ sau đã cài đặt:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Tiện ích mở rộng Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Tùy chọn)
  - Python 3.10 hoặc mới hơn

Chạy [Hướng dẫn nhanh tác nhân lưu trữ với `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) ít nhất một lần trước khi trình bày để bạn có dự án Foundry, triển khai mô hình và Azure Container Registry ổn định làm tham chiếu nếu người học bị kẹt.

---

## Hướng dẫn theo slide

Bộ slide theo luồng giống như các lab. Các điểm trình bày gợi ý cho mỗi phần:

| Phần                        | Thông điệp chính                                                                                               |
|-----------------------------|---------------------------------------------------------------------------------------------------------------|
| Tiêu đề và chương trình     | Định khung workshop như *VS Code tới Foundry* không cần chuyển đổi cổng thông tin.                             |
| Tại sao chọn tác nhân lưu trữ? | Runtime được quản lý, triển khai dựa trên ACR, API `/responses` tương thích OpenAI, phạm vi trong dự án Foundry. |
| Sơ đồ kiến trúc             | Đưa qua [README kiến trúc](../README.md#architecture): scaffold, Inspector, ACR, Dịch vụ Tác nhân.           |
| Cấu trúc một tác nhân lưu trữ | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - chức năng từng file.                             |
| Demo trực tiếp: Tác nhân Executive | Chuyển sang VS Code và chạy demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) từ đầu đến cuối (xem [Demo 1](#demo-1-tác-nhân-executive)). |
| Demo trực tiếp: Đánh giá CV phù hợp | Chuyển sang VS Code và chạy demo 4 tác nhân [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (xem [Demo 2](#demo-2-đánh-giá-cv-phù-hợp)). |
| Tóm tắt Lab 01              | Giao cho người học. Hướng dẫn tới [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Mẫu đa tác nhân             | Tuần tự, đồng thời, hoặc bàn giao - xem trước trước khi bắt đầu Lab 02.                                       |
| Tóm tắt Lab 02              | Giao cho người học. Hướng dẫn tới [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Tổng kết và tài nguyên      | Liên kết học tiếp từ phần [Tài nguyên bổ sung](#tài-nguyên-bổ-sung).                                       |

---

## Demo

Hai demo trực tiếp được bao gồm trong bài trình bày. Dự trù mỗi demo 10 phút.

| Demo              | Lab   | File                                                  | Nội dung trình bày                                         |
|-------------------|-------|-------------------------------------------------------|-----------------------------------------------------------|
| Tác nhân Executive | Lab 01| [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Tác nhân đơn lưu trữ; dịch thuật ngữ kỹ thuật sang tóm tắt lãnh đạo |
| Đánh giá CV phù hợp | Lab 02| [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Điều phối 4 tác nhân; chấm điểm phù hợp CV-công việc và tạo đề xuất |

### Demo 1: Tác nhân Executive

Một tác nhân độc lập trong [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Dùng làm demo 10 phút trước Lab 01.

1. Mở [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) và dẫn qua định nghĩa tác nhân (prompts hệ thống, mô hình, framework).
2. Nhấn `F5` để khởi chạy **Agent Inspector** cục bộ.
3. Dán prompt mẫu từ [README](../README.md#see-it-in-action) và trình bày phản hồi tóm tắt lãnh đạo.
4. Trưng bày [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) và [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) để giải thích các artefact triển khai.
5. Minh họa quy trình triển khai (xây dựng Docker, đẩy ACR, tạo tác nhân lưu trữ) mà không đợi hoàn thành.

### Demo 2: Đánh giá CV phù hợp

Quy trình 4 tác nhân trong [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Dùng làm demo 10 phút trước Lab 02.

1. Mở [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) và trình bày cách bốn tác nhân được kết nối trong trình tự điều phối.
2. Nhấn `F5` để khởi chạy **Agent Inspector** cho quy trình đa tác nhân.
3. Dán mô tả công việc ngắn và CV mẫu trong chat của Inspector.
4. Trình bày pipeline 4 tác nhân: phân tích CV, trích xuất yêu cầu công việc, chấm điểm phù hợp, và viết đề xuất.
5. Chỉ ra cách đầu ra của từng tác nhân phụ trở thành ngữ cảnh cho tác nhân kế tiếp, nhấn mạnh mẫu bàn giao.
6. Trưng bày [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) để so sánh với phiên bản tác nhân đơn trong Demo 1.

---

## Mẹo trình bày

- **Đặt kỳ vọng từ sớm.** Tác nhân lưu trữ đang trong bản xem trước - nêu rõ giới hạn vùng và hạn mức ngay từ đầu để người học không bị bất ngờ giữa chừng.
- **Chạy tác vụ kiểm tra yêu cầu đầu tiên.** Cả hai lab đều có tác vụ VS Code `Validate prerequisites` - bắt người học chạy trước khi viết code.
- **Giữ cho Agent Inspector luôn hiển thị.** Hầu hết khoảnh khắc “aha” xảy ra khi người học thấy đèn phản hồi `/responses` cục bộ sáng lên.
- **Chuẩn bị dự án dự phòng.** Nếu dự án Foundry của người học không đủ hạn mức, chia sẻ một dự án được cấp trước cho bước triển khai thay vì làm gián đoạn lớp.
- **Ghép đôi người học.** Lab 02 (đa tác nhân) dễ hơn nhiều khi người học có thể bàn luận với bạn cùng học.
- **Dùng các module docs làm mốc dừng.** Thư mục `docs/` mỗi lab chia thành 8 module đánh số - dùng đó làm điểm tạm nghỉ tự nhiên.
- **Kéo sẵn ảnh Docker cơ sở** trên máy lab chung để tránh giới hạn tốc độ registry.

---

## Xử lý sự cố trong lúc trình bày

| Triệu chứng                            | Việc đầu tiên nên thử                                                   |
|--------------------------------------|------------------------------------------------------------------------|
| Agent Inspector không kết nối được    | Xác nhận cổng `8088` đang mở và tác vụ `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` đang chạy. |
| Trình gỡ lỗi không gắn được           | Kiểm tra cổng `5679` có đang mở; khởi động lại VS Code nếu `debugpy` đã được sử dụng.                |
| `azd up` báo lỗi xác thực             | Chạy `az login` và `azd auth login`, đảm bảo chọn đúng tenant.                                    |
| Triển khai bị treo khi đẩy ACR       | Kiểm tra Docker Desktop đang chạy và người dùng có quyền `AcrPush` trên registry.                  |
| Mô hình trả về 404 / deployment-not-found | Tên triển khai mô hình trong `agent.yaml` phải trùng tên triển khai trong dự án Foundry.          |

| Đại lý lưu trữ bị kẹt ở trạng thái `Provisioning`         | Xác minh vùng dự án [hỗ trợ đại lý lưu trữ](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) và rằng còn hạn mức. |
| Playground trả về 401                       | Xác thực lại tiện ích mở rộng Foundry từ thanh hoạt động của VS Code.                                     |

Để hướng dẫn sâu hơn, mỗi phòng thí nghiệm đều cung cấp tài liệu riêng `08-troubleshooting.md` - hướng dẫn học viên tham khảo:

- Phòng thí nghiệm 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Phòng thí nghiệm 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Tùy chỉnh phiên học này

Bạn được chào đón để điều chỉnh workshop phù hợp với khán giả của bạn. Các biến thể phổ biến:

- **Đối tượng backend:** dành nhiều thời gian hơn cho `agent.yaml`, Docker, và ACR; rút ngắn phần demo playground.
- **Đối tượng phát triển dân cư:** ở lại trong giao diện tiện ích mở rộng Foundry để xây dựng cấu trúc; giảm các bước CLI.
- **Phiên 60 phút một kênh:** chỉ giới thiệu, demo, và Phòng thí nghiệm 01.
- **Định dạng chỉ workshop (không có slide):** mở cả hai README bài lab và sử dụng chúng làm kịch bản chính.

Nếu bạn mở rộng các bài lab, vui lòng đóng góp các thay đổi trở lại qua PR để các huấn luyện viên khác cùng hưởng lợi.

---

## Tài nguyên bổ sung

- [Tài liệu Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Tổng quan về đại lý lưu trữ](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Bắt đầu nhanh: triển khai đại lý lưu trữ đầu tiên của bạn (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Triển khai đại lý lưu trữ (hướng dẫn)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Bộ công cụ Microsoft Foundry cho VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Liên hệ

Nếu bạn có câu hỏi về việc trình bày phiên học này, vui lòng mở một issue trên [kho lưu trữ workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) và gắn thẻ người phụ trách duy trì.

| Vai trò                | Tên           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Người duy trì / liên hệ| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->