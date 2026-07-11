# Modul 7 - Verifiera i Playground

⏱️ ~10 min

I den här modulen testar du ditt distribuerade multi-agent-flöde i VS Code och Foundry Portal, för att bekräfta att agenten beter sig likadant som vid lokal testning.

---

## Varför testa igen efter distribution?

Den hostade miljön skiljer sig från lokal på några viktiga sätt:

| | Lokal | Hostad |
|--|-------|--------|
| **Identitet** | Din personliga inloggning (`DefaultAzureCredential`) | Dedikerad per-agent Entra-identitet (auto-provisionerad vid distribution) |
| **Endpoint** | `http://localhost:8088/responses` | Foundry Agent Service hanterad URL |
| **Nätverk** | Din maskin → Azure OpenAI + MCP | Azure ryggrad (lägre latens) |

En felkonfigurerad miljövariabel, RBAC-problem eller blockerad MCP-utgående anrop skulle visa sig här först.

---

## Alternativ A: Testa i VS Code Playground (rekommenderas först)

### Steg 1: Navigera till din hostade agent

1. Klicka på **Foundry Toolkit**-ikonen i aktivitetsfältet.
2. Expandera ditt projekt → **Hosted Agents (Preview)** → hitta din agent.

![Foundry Toolkit sidebar showing Hosted Agents (Preview) with resume-job-fit-evaluator and its deployed versions](../../../../../translated_images/sv/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### Steg 2: Välj en version

1. Klicka på agenten för att expandera dess versioner.
2. Klicka på `v1` → verifiera att status är **aktiv** (sidofältet kan visa "Running" eller "Started" - båda indikerar samma redo-status).

### Steg 3: Öppna Playground

1. Klicka på **Playground** (eller högerklicka på versionen → **Open in Playground**).
2. Ett chattfönster öppnas i en VS Code-flik.

### Steg 4: Kör dina röktester

Använd samma 3 tester från [Modul 5](05-test-locally.md). Skriv varje meddelande i input-rutan i Playground och tryck på **Send** (eller **Enter**).

#### Test 1 - Fullständigt CV + JD (standardflöde)

Klistra in hela resume + JD-prompten från Modul 5, Test 1 (Jane Doe + Senior Cloud Engineer på Contoso Ltd).

**Förväntat:**
- Passningspoäng med uppdelningsberäkning (100-poängsskala)
- Matched Skills-sektion
- Missing Skills-sektion
- **Ett gapkort per saknad kompetens** med Microsoft Learn-URL:er
- Läroplan med tidslinje

#### Test 2 - Snabbt kort test (minimalt input)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Förväntat:**
- Lägre passningspoäng (< 40)
- Ärlig bedömning med stegvis inlärningsväg
- Flera gapkort (AWS, Kubernetes, Terraform, CI/CD, erfarenhetsbrist)

#### Test 3 - Hög-passande kandidat

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Förväntat:**
- Hög passningspoäng (≥ 80)
- Fokus på intervjuförberedelser och finslipning
- Få eller inga gapkort
- Kort tidslinje med fokus på förberedelse

### Steg 5: Jämför med lokala resultat

Öppna dina anteckningar eller webbläsarflik från Modul 5 där du sparade lokala svar. För varje test:

- Har svaret **samma struktur** (passningspoäng, gapkort, läroplan)?
- Följer det **samma poängsättningskriterier** (100-poängs uppdelning)?
- Finns **Microsoft Learn-URL:er** fortfarande i gapkorten?
- Finns det **ett gapkort per saknad kompetens** (inte trunkerat)?

> **Mindre ordalydelse-förändringar är normala** - modellen är icke-deterministisk. Fokusera på struktur, poängkonsekvens och MCP-verktygsanvändning.

---

## Alternativ B: Testa i Foundry Portal

[Foundry Portal](https://ai.azure.com) erbjuder en webbaserad playground som är användbar för att dela med lagkamrater eller intressenter.

### Steg 1: Öppna Foundry Portal

1. Öppna din webbläsare och gå till [https://ai.azure.com](https://ai.azure.com).
2. Logga in med samma Azure-konto som du använt genom hela workshopen.

### Steg 2: Navigera till ditt projekt

1. På startsidan, leta efter **Recent projects** i vänstra sidofältet.
2. Klicka på ditt projektnamn (t.ex. `workshop-agents`).
3. Om du inte ser det, klicka på **All projects** och sök efter det.

### Steg 3: Hitta din distribuerade agent

1. I projektets vänstra navigering klickar du på **Build** → **Agents** (eller leta efter sektionen **Agents**).
2. Du bör se en lista över agenter. Hitta din distribuerade agent (t.ex. `resume-job-fit-evaluator`).
3. Klicka på agentens namn för att öppna dess detaljsida.

### Steg 4: Öppna Playground

1. På agentens detaljsida, titta på den övre verktygslisten.
2. Klicka på **Open in playground** (eller **Try in playground**).
3. Ett chattgränssnitt öppnas.

### Steg 5: Kör samma röktester

Upprepa alla 3 tester från VS Code Playground-sektionen ovan. Jämför varje svar med både lokala resultat (Modul 5) och VS Code Playground-resultat (Alternativ A ovan).

---

## Multi-agent-specifik verifiering

Utöver grundläggande korrekthet, verifiera dessa multi-agent-specifika beteenden:

### MCP-verktygsexekvering

| Kontroll | Hur man verifierar | Godkänd villkor |
|-------|---------------|----------------|
| MCP-anrop lyckas | Gapkorten innehåller `learn.microsoft.com`-URL:er | Riktiga URL:er, inte fallback-meddelanden |
| Flera MCP-anrop | Varje High/Medium prioriterad brist har resurser | Inte bara det första gapkortet |
| MCP-fallback fungerar | Om URL:er saknas, kontrollera fallback-text | Agenten producerar fortsatt gapkort (med eller utan URL:er) |

### Agentkoordinering

| Kontroll | Hur man verifierar | Godkänd villkor |
|-------|---------------|----------------|
| Alla 4 agenter kördes | Utdata innehåller passningspoäng OCH gapkort | Poängen kommer från MatchingAgent, korten från GapAnalyzer |
| Sekventiell exekvering | Svarstiden är rimlig (< 2 min) | Om > 3 min, kontrollera för fel i terminalloggen |
| Dataintegritet | Gapkorten refererar till färdigheter från matchningsrapporten | Inga hallucinerade färdigheter som inte finns i JD |

---

## Valideringskriterier

Använd denna rubrik för att utvärdera ditt multi-agent-flödes hostade beteende:

| # | Kriterium | Godkänd villkor | Godkänd? |
|---|----------|---------------|-------|
| 1 | **Funktionell korrekthet** | Agent svarar på CV + JD med passningspoäng och bristanalys | |
| 2 | **Poängsättningskonsekvens** | Passningspoäng använder 100-poängsskala med uppdelningsberäkning | |
| 3 | **Gapkortens fullständighet** | Ett kort per saknad kompetens (inte trunkerat eller kombinerat) | |
| 4 | **MCP-verktygsintegration** | Gapkort innehåller riktiga Microsoft Learn-URL:er | |
| 5 | **Strukturell konsekvens** | Utdata-strukturen matchar mellan lokal och hostad körning | |
| 6 | **Svarstid** | Hostad agent svarar inom 2 minuter för fullständig bedömning | |
| 7 | **Inga fel** | Inga HTTP 500-fel, timeout eller tomma svar | |

> Ett ”godkänt” innebär att alla 7 kriterier uppfylls för alla 3 röktester i minst en playground (VS Code eller Portal).

---

## Felsökning av playground-problem

| Symtom | Trolig orsak | Åtgärd |
|---------|-------------|-----|
| Playground laddas inte | Container är inte i `aktiv`-status | Gå tillbaka till [Modul 6](06-deploy-to-foundry.md), verifiera distributionsstatus. Vänta om `skapar` |
| Agent returnerar tomt svar | Modellens distributionsnamn matchar inte | Kontrollera `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` matchar din distribuerade modell |
| Agent returnerar felmeddelande | [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) behörighet saknas | Tilldela **[Foundry User](https://aka.ms/foundry-ext-project-role)** (tidigare Azure AI User) på projektnivå |
| Inga Microsoft Learn-URL:er i gapkort | MCP utgående anrop blockerat eller MCP-server otillgänglig | Kontrollera att containern kan nå `learn.microsoft.com`. Se [Modul 8](08-troubleshooting.md) |
| Endast 1 gapkort (trunkerat) | GapAnalyzer-instruktioner saknar "CRITICAL" block | Granska [Modul 3, Steg 2.4](03-configure-agents.md) |
| Passningspoäng skiljer sig kraftigt från lokal | Olika modell eller instruktioner distribuerade | Jämför `agent.yaml` miljövariabler med lokal `.env`. Distribuera om nödvändigt |
| "Agent not found" i Portalen | Distributionen håller på att spridas eller misslyckades | Vänta 2 minuter, uppdatera. Om saknas, distribuera om från [Modul 6](06-deploy-to-foundry.md) |

---

### Kontrollpunkt

- [ ] Testade agent i VS Code Playground - alla 3 röktester godkända
- [ ] Testade agent i [Foundry Portal](https://ai.azure.com) Playground - alla 3 röktester godkända
- [ ] Svaren är strukturellt konsekventa med lokal testning (passningspoäng, gapkort, läroplan)
- [ ] Microsoft Learn-URL:er finns i gapkort (MCP-verktyget fungerar i hostad miljö)
- [ ] Ett gapkort per saknad kompetens (ingen trunkering)
- [ ] Inga fel eller timeout under testningen
- [ ] Färdigställd valideringsrubrik (alla 7 kriterier godkända)

---

**Föregående:** [06 - Distribuera till Foundry](06-deploy-to-foundry.md) · **Nästa:** [08 - Felsökning →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->