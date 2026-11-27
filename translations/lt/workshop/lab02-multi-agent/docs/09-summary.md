# 9 modulis – Santrauka ir tolesni žingsniai

⏱️ ~5 min

**Sveikiname!** Jūs sukūrėte, išbandėte ir (jei pasirinkote A kelią) išdiegėte daugiaagentinį darbo eigą naudodami Microsoft Foundry ir Foundry Toolkit skirtą VS Code.

---

## Ką sukūrėte

**CV → Darbo tinkamumo vertintojas** – daugiaagentinė darbo eiga, kuri:
- Gautą CV ir darbo aprašymą per HTTP (`POST /responses`)
- Paleidžia keturis specializuotus agentus seka vienas po kito – kiekvienas agentas perduoda duomenis savo įpėdiniui
- Grąžina tinkamumo balą (0–100 su detaliu suskaidymu), įgūdžių ir sertifikatų trūkumų sąrašą bei personalizuotą mokymosi planą su tikrais Microsoft Learn saitais kiekvienam trūkumui
- Kreipiasi į Microsoft Learn MCP serverį (`https://learn.microsoft.com/api/mcp`), kad gautų oficialius mokymosi išteklius kiekvienam nustatytam įgūdžių trūkumui
- Veikia kaip vienas konteinerizuotas hostintas agentas Microsoft Foundry Agent Service aplinkoje

---

## Pagrindinės įgytos sąvokos

| Sąvoka | Ką praktikuojate |
|---------|-------------------|
| **Daugiaagentinė orkestracija** | `WorkflowBuilder` sekos vamzdelis su `add_edge()` |
| **Agentų specializacija** | Keturi specializuoti agentai yra veiksmingesni už vieną bendro pobūdžio agentą |
| **Turinio maršrutizatoriaus modelis** | ResumeParser taip pat veikia kaip maršrutizatorius – jis saugo JD tekstą `[JOB DESCRIPTION PASS-THROUGH]` sekcijoje, kad tolesni agentai galėtų jį pasiekti (būtina, nes `context_mode="last_agent"` reiškia, kad tik `start_executor` mato neapdorotą naudotojo žinutę) |
| **Turinio perdavimo modelis** | JD agentas perduoda `[PARSED RESUME PASS-THROUGH]` toliau, kad MatchingAgent gautų abu profilius; taip išvengiama dvigubo aktyvavimo, kurį sukelia funlinijų grafai su OR-semantika |
| **MCP įrankio integracija** | `@tool` + `streamable_http_client` kreipimasis į išorinį MCP serverį |
| **Hostinto agento gyvavimo ciklas** | Konstravimas → Konfigūravimas → Vietinis testavimas → Diegimas → Tikrinimas debesyje |
| **`context_mode="last_agent"`** | Kiekvienas vykdytojas mato tik savo tiesioginio pirmtako rezultatą |
| **Foundry Toolkit darbo eiga** | Konstruktoriaus vedlys, Agent Inspector, darbo eigos vizualizatorius, viena spustelėjimo diegimas |

---

## Ką atlikote

<details open>
<summary><strong>🅰️ A kelias – Foundry prenumerata</strong></summary>

- [x] Patvirtinote 01 laboratorijos nustatymus: projektas, modelis ir RBAC vis dar aktyvūs
- [x] Sukūrėte daugiaagentinį projektą naudodami Workflows šabloną
- [x] Parašėte keturias agentų instrukcijas (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integravote Microsoft Learn MCP įrankį su `streamable_http_client`
- [x] Susiejote darbo eigos grafiką su `WorkflowBuilder` (sekos vamzdelis su turinio perdavimu)
- [x] Vietoje atlikote du pagrindinius testus (Agent Inspector) – tinkamumo balas, trūkumų kortelės, MCP saitai
- [x] Išdiegėte Foundry Agent Service (konteinerizuotas, valdomas identitetas)
- [x] Patikrinta debesies aplinkoje – struktūrinis suderinamumas su vietiniais rezultatais

</details>

<details open>
<summary><strong>🅱️ B kelias – Foundry Local</strong></summary>

- [x] Patvirtinote 01 laboratorijos nustatymus: Foundry Local veikia su vietiniu modeliu
- [x] Sukūrėte daugiaagentinį projektą naudodami Workflows šabloną
- [x] Parašėte keturias agentų instrukcijas ir susiejote darbo eigos grafiką
- [x] Integravote Microsoft Learn MCP įrankį
- [x] Vietoje atlikote du pagrindinius testus
- [x] Patvirtinote daugiaagentinį elgesį nenaudodami debesies išteklių

</details>

---

## Tolesni žingsniai

### Tęskite mokymąsi

| Išteklius | Aprašymas |
|----------|-------------|
| **[Agent Framework SDK nuoroda](https://learn.microsoft.com/agent-framework/)** | API dokumentacija `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP įrankių katalogas](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Prijunkite agentus prie kitų MCP serverių (Bing, GitHub, naudotojo) |
| **[Pridėti žinias (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Įtvirtinkite agentus dokumentais, vektorinių duomenų saugyklomis arba Bing paieška |
| **[Foundry vertinimai](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Matavimas agentų kokybės mastu su automatizuotais vertintojais |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Visapusiška platformos nuoroda |
| **[Foundry Toolkit – Kas naujo](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Priedų išleidimo pastabos ir pakeitimų žurnalas |

### Idėjos darbo eigai išplėsti

- **Pridėti 5-ą agentą** – Pokalbio trenerį, kuris pagal trūkumų ataskaitą generuoja tikėtinas interviu klausimų temas
- **Pridėti Bing įtvirtinimo įrankį** – Leisti JD agentui ieškoti panašių darbo skelbimų, kad praturtintų reikalavimus
- **Prijungti prie CV duomenų bazės** – Gauti kandidatų profilius iš duomenų bazės per naudotojo modifikuotą `@tool`
- **Išbandyti skirtingus modelius** – Palyginti `gpt-4.1` ir `gpt-4.1-mini` išvesties kokybę ir delsą
- **Vertinti su Foundry** – Naudoti Vertinimų funkciją tinkamumo ataskaitų balams įvertinti pagal pagrindinį duomenų rinkinį

### B kelio naudotojams: pereikite prie debesies diegimo

Kai būsite pasirengę diegti debesyje:
1. Gaukite Azure prenumeratą ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Baikite [01 laboratoriją, 01 modulį](../../lab01-single-agent/docs/01-setup.md) (sukurkite projektą, išdiekite modelį, priskirkite RBAC)
3. Atnaujinkite savo `.env` su Foundry projekto pabaigos punktu ir modelio diegimo pavadinimu
4. Tęskite iš [06 modulio – Diegimas Foundry](06-deploy-to-foundry.md)

---

## Išvalyti išteklius (pasirinktinai)

Jei norite pašalinti Azure išteklius, sukurtus šio seminaro metu:

### 1 variantas: Ištrinti išteklių grupę (pašalina viską)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 2 variantas: Ištrinti tik hostintą agentą

1. Atidarykite [ai.azure.com](https://ai.azure.com) → savo projektą → **Build** → **Agents**.
2. Suraskite **PersonalCareerCopilot** → spustelėkite **Delete**.

### 3 variantas: Ištrinti modelio diegimą

1. Foundry šoniniame meniu išskleiskite savo projektą → **Models**.
2. Dešiniuoju pelės klavišu spustelėkite modelio diegimą → **Delete**.

> **Išlaidų pastaba:** Hostinti agentai generuoja išlaidas tik vykdant. Jei sustabdote arba ištrinate agentą, mokestis neskaičiuojamas. Modelio diegimas gali turėti nedidelį rezervuotos talpos mokestį – ištrinkite jį, jei baigėte.

---

**Ankstesnis:** [08 – Probleminių situacijų sprendimas](08-troubleshooting.md) · **Pagrindinis:** [02 laboratorijos README](../README.md) · [Seminaro pagrindinis puslapis](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->