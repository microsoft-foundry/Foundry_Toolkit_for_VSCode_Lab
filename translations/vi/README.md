# Foundry Toolkit + Hội thảo Đại lý Hosted Foundry

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Xây dựng, kiểm thử và triển khai các đại lý AI đến **Microsoft Foundry Agent Service** dưới dạng **Đại lý Hosted** - hoàn toàn từ VS Code sử dụng **phần mở rộng Microsoft Foundry** và **Foundry Toolkit**.

> **Các Đại lý Hosted hiện đang ở giai đoạn xem trước.** Các vùng hỗ trợ bị giới hạn - xem [khu vực hỗ trợ](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Thư mục `agent/` trong mỗi bài lab được **tự động dựng sẵn** bởi phần mở rộng Foundry - bạn sau đó tùy chỉnh mã, kiểm thử tại chỗ và triển khai.

### 🌐 Hỗ trợ đa ngôn ngữ

#### Hỗ trợ qua GitHub Action (Tự động & Luôn được cập nhật)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Tiếng Ả Rập](../ar/README.md) | [Tiếng Bengal](../bn/README.md) | [Tiếng Bungari](../bg/README.md) | [Tiếng Miến Điện (Myanmar)](../my/README.md) | [Tiếng Trung (Giản thể)](../zh-CN/README.md) | [Tiếng Trung (Phồn thể, Hồng Kông)](../zh-HK/README.md) | [Tiếng Trung (Phồn thể, Macau)](../zh-MO/README.md) | [Tiếng Trung (Phồn thể, Đài Loan)](../zh-TW/README.md) | [Tiếng Croatia](../hr/README.md) | [Tiếng Séc](../cs/README.md) | [Tiếng Đan Mạch](../da/README.md) | [Tiếng Hà Lan](../nl/README.md) | [Tiếng Estonia](../et/README.md) | [Tiếng Phần Lan](../fi/README.md) | [Tiếng Pháp](../fr/README.md) | [Tiếng Đức](../de/README.md) | [Tiếng Hy Lạp](../el/README.md) | [Tiếng Do Thái](../he/README.md) | [Tiếng Hindi](../hi/README.md) | [Tiếng Hungary](../hu/README.md) | [Tiếng Indonesia](../id/README.md) | [Tiếng Ý](../it/README.md) | [Tiếng Nhật](../ja/README.md) | [Tiếng Kannada](../kn/README.md) | [Tiếng Khmer](../km/README.md) | [Tiếng Hàn](../ko/README.md) | [Tiếng Litva](../lt/README.md) | [Tiếng Malay](../ms/README.md) | [Tiếng Malayalam](../ml/README.md) | [Tiếng Marathi](../mr/README.md) | [Tiếng Nepal](../ne/README.md) | [Tiếng Pidgin Nigeria](../pcm/README.md) | [Tiếng Na Uy](../no/README.md) | [Tiếng Ba Tư (Farsi)](../fa/README.md) | [Tiếng Ba Lan](../pl/README.md) | [Tiếng Bồ Đào Nha (Brazil)](../pt-BR/README.md) | [Tiếng Bồ Đào Nha (Bồ Đào Nha)](../pt-PT/README.md) | [Tiếng Punjabi (Gurmukhi)](../pa/README.md) | [Tiếng Romania](../ro/README.md) | [Tiếng Nga](../ru/README.md) | [Tiếng Serbia (Chữ Kirin)](../sr/README.md) | [Tiếng Slovakia](../sk/README.md) | [Tiếng Slovenia](../sl/README.md) | [Tiếng Tây Ban Nha](../es/README.md) | [Tiếng Swahili](../sw/README.md) | [Tiếng Thụy Điển](../sv/README.md) | [Tiếng Tagalog (Philippines)](../tl/README.md) | [Tiếng Tamil](../ta/README.md) | [Tiếng Telugu](../te/README.md) | [Tiếng Thái](../th/README.md) | [Tiếng Thổ Nhĩ Kỳ](../tr/README.md) | [Tiếng Ukraina](../uk/README.md) | [Tiếng Urdu](../ur/README.md) | [Tiếng Việt](./README.md)

> **Ưa thích sao chép về máy?**
>
> Kho lưu trữ này gồm trên 50 bản dịch ngôn ngữ làm tăng đáng kể kích thước tải xuống. Để sao chép mà không có bản dịch, dùng sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Cách này cung cấp mọi thứ bạn cần để hoàn thành khóa học với tốc độ tải xuống nhanh hơn nhiều.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Kiến trúc

```mermaid
flowchart TB
    subgraph Local["Phát triển cục bộ (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Extension"]
        FoundryToolkit["Foundry Toolkit
        Extension"]
        Scaffold["Scaffolded Agent Code
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agent Inspector
        (Local Testing)"]
        FE -- "Create New
        Hosted Agent" --> Scaffold
        Scaffold -- "Gỡ lỗi F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Nhà máy Microsoft"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Hosted Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Khung làm sẵn
    Playground -- "Kiểm tra các lời nhắc" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Quy trình:** Phần mở rộng Foundry dựng khung đại lý → bạn tùy chỉnh mã & hướng dẫn → kiểm thử tại chỗ với Agent Inspector → triển khai lên Foundry (hình ảnh Docker đẩy lên ACR) → xác thực trên Playground.

---

## Những gì bạn sẽ xây dựng

| Lab | Mô tả | Trạng thái |
|-----|-------------|--------|
| **Lab 01 - Đại lý đơn lẻ** | Xây dựng **Đại lý "Giải thích như Tôi là Giám đốc"**, kiểm thử tại chỗ, và triển khai lên Foundry | ✅ Có sẵn |
| **Lab 02 - Quy trình đa đại lý** | Xây dựng **"Đánh giá hồ sơ → Phù hợp công việc"** - 4 đại lý phối hợp chấm điểm sự phù hợp hồ sơ và tạo lộ trình học tập | ✅ Có sẵn |

---

## Gặp gỡ Đại lý Giám đốc

Trong hội thảo này, bạn sẽ xây dựng **Đại lý "Giải thích như Tôi là Giám đốc"** - một đại lý AI biến những thuật ngữ kỹ thuật hóc búa thành những bản tóm tắt bình tĩnh, sẵn sàng cho phòng họp ban giám đốc. Bởi vì thật lòng mà nói, không ai trong ban lãnh đạo muốn nghe về "sự cạn kiệt thread pool do các gọi đồng bộ được giới thiệu trong v3.2."

Tôi xây dựng đại lý này sau quá nhiều lần sự cố khi bài báo cáo sau sự kiện được tạo hoàn hảo của tôi nhận được phản hồi: *"Vậy… trang web có bị sập không?"*

### Cách nó hoạt động

Bạn cung cấp cho nó một cập nhật kỹ thuật. Nó trả lại tóm tắt cho giám đốc - ba điểm chính, không dùng thuật ngữ chuyên ngành, không lỗi stack trace, không sợ hãi tồn tại. Chỉ có **điều đã xảy ra**, **tác động kinh doanh**, và **bước tiếp theo**.

### Xem nó hoạt động

**Bạn nói:**
> "Độ trễ API tăng do cạn kiệt thread pool bởi các gọi đồng bộ được giới thiệu trong v3.2."

**Đại lý trả lời:**

> **Tóm tắt dành cho giám đốc:**
> - **Điều đã xảy ra:** Sau bản phát hành mới nhất, hệ thống chậm lại.
> - **Tác động kinh doanh:** Một số người dùng gặp phải độ trễ khi sử dụng dịch vụ.
> - **Bước tiếp theo:** Đã hoàn tác thay đổi và đang chuẩn bị sửa lỗi trước khi triển khai lại.

### Tại sao là đại lý này?

Đây là đại lý đơn giản, chuyên dụng - hoàn hảo để học quy trình đại lý hosted từ đầu đến cuối mà không bị rối bởi chuỗi công cụ phức tạp. Và thành thật mà nói? Mỗi đội kỹ thuật đều có thể sử dụng một cái như vậy.

---

## Cấu trúc hội thảo

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-setup.md
    │   │   ├── 02-create-hosted-agent.md
    │   │   ├── 03-configure-and-code.md
    │   │   ├── 04-test-locally.md
    │   │   ├── 05-deploy-to-foundry.md
    │   │   ├── 06-verify-in-playground.md
    │   │   ├── 07-summary.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   └── 08-troubleshooting.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **Lưu ý:** Thư mục `agent/` bên trong mỗi bài lab là thứ **phần mở rộng Microsoft Foundry** tạo khi bạn chạy `Microsoft Foundry: Create a New Hosted Agent` từ Command Palette. Các tập tin sau đó được tùy chỉnh với hướng dẫn, công cụ và cấu hình của đại lý bạn. Lab 01 hướng dẫn bạn tái tạo điều này từ đầu.

---

## Bắt đầu

### 1. Sao chép kho lưu trữ

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Thiết lập môi trường ảo Python

```bash
python -m venv venv
```

Kích hoạt nó:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Cài đặt phụ thuộc

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Cấu hình biến môi trường

Sao chép tập tin `.env` mẫu trong thư mục đại lý và điền giá trị của bạn:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Chỉnh sửa `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Theo dõi các bài lab hội thảo

Mỗi bài lab là một phần riêng biệt với các module riêng. Bắt đầu với **Lab 01** để học các kiến thức cơ bản, sau đó chuyển sang **Lab 02** cho quy trình đa đại lý.

#### Lab 01 - Đại lý đơn lẻ ([hướng dẫn đầy đủ](workshop/lab01-single-agent/README.md))

| # | Module | Liên kết |
|---|--------|------|
| 1 | Đọc các yêu cầu trước | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Cài đặt Foundry Toolkit & phần mở rộng Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Tạo dự án Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Tạo đại lý hosted | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Cấu hình hướng dẫn & môi trường | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Kiểm thử tại chỗ | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Triển khai lên Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Xác thực trên playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Khắc phục sự cố | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Quy trình đa đại lý ([hướng dẫn đầy đủ](workshop/lab02-multi-agent/README.md))

| # | Module | Liên kết |
|---|--------|------|
| 1 | Yêu cầu trước (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Hiểu kiến trúc đa đại lý | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Dựng khung dự án đa đại lý | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Cấu hình đại lý & môi trường | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Mẫu mẫu phối hợp | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Kiểm thử tại chỗ (đa đại lý) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Triển khai tới Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Xác minh trong playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Xử lý sự cố (đa tác nhân) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Người duy trì

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## Quyền cần thiết (tham khảo nhanh)

| Kịch bản | Vai trò cần thiết |
|----------|---------------|
| Tạo dự án Foundry mới | **Azure AI Owner** trên tài nguyên Foundry |
| Triển khai vào dự án hiện có (tài nguyên mới) | **Azure AI Owner** + **Contributor** trên đăng ký |
| Triển khai dự án đã được cấu hình đầy đủ | **Reader** trên tài khoản + **Azure AI User** trên dự án |

> **Quan trọng:** Vai trò `Owner` và `Contributor` của Azure chỉ bao gồm quyền *quản lý*, không bao gồm quyền *phát triển* (hành động dữ liệu). Bạn cần **Azure AI User** hoặc **Azure AI Owner** để xây dựng và triển khai các tác nhân.

---

## Tham khảo

- [Bắt đầu nhanh: Triển khai tác nhân được lưu trữ đầu tiên của bạn (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Tác nhân được lưu trữ là gì?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Tạo quy trình làm việc tác nhân được lưu trữ trong VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Triển khai tác nhân được lưu trữ](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC cho Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Mẫu tác nhân đánh giá kiến trúc](https://github.com/Azure-Samples/agent-architecture-review-sample) - Tác nhân được lưu trữ thực tế với công cụ MCP, sơ đồ Excalidraw, và triển khai kép

---


## Giấy phép

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->