# 9 Modulis - Santrauka ir tolesni veiksmai

⏱️ ~5 min

**Sveikiname!** Jūs sukūrėte, išbandėte ir (jei pasirinkote A kelią) diegėte daugiaagentinį darbo srautą, naudojant Microsoft Foundry ir Foundry Toolkit vietiniam VS Code.

---

## Ką sukūrėte

**CV → Darbo tinkamumo vertintojas** – daugiaagentinis talpinamas darbo srautas, kuris:
- Priima CV ir darbo aprašymą per HTTP (`POST /responses`)
- Atlieka keturių specializuotų agentų veiklą nuoseklioje eilėje – kiekvienas agentas perduoda savo sekėjui reikalingus duomenis
- Grąžina tinkamumo įvertinimą (0–100 su išskaidymu), įgūdžių ir sertifikatų spragų sąrašą bei suasmenintą mokymosi planą su realiais Microsoft Learn nuorodomis kiekvienai spragai
- Kreipiasi į Microsoft Learn MCP serverį (`https://learn.microsoft.com/api/mcp`), kad gautų oficialią mokymosi medžiagą kiekvienai nustatytai įgūdžio spragai
- Veikia kaip vienas konteineryje talpinamas agentas Microsoft Foundry agentų paslaugoje

---

## Svarbūs įgyti konceptai

| Konceptas | Ką praktikavote |
|---------|-------------------|
| **Daugiaagentinė orkestracija** | `WorkflowBuilder` nuoseklus darbo srautas su `add_edge()` |
| **Agentų specializacija** | Keturi specializuoti agentai veikia geriau nei vienas bendros paskirties agentas |
| **Turinio maršrutizatoriaus (Content Router) modelis** | ResumeParser veikia kaip maršrutizatorius – jis išsaugo JD tekstą `[JOB DESCRIPTION PASS-THROUGH]` skyriuje, kad žemiau esantys agentai prie jo galėtų prieiti (tai būtina, nes `context_mode="last_agent"` reiškia, kad žalią naudotojo žinutę mato tik `start_executor`) |
| **Turinio perdavimo (Content Relay) modelis** | JD Agent perduoda `[PARSED RESUME PASS-THROUGH]` toliau, todėl MatchingAgent gauna abu profilius; tokiu būdu išvengiama OR-semantikos dvigubo suveikimo, būdingo fan-in grafams |
| **MCP įrankio integracija** | `@tool` + `streamable_http_client`, kreipiantis į išorinį MCP serverį |
| **Talpinamo agente gyvenimo ciklas** | Sukurk → Konfigūruok → Testuok lokaliai → Įdiek → Patikrink debesyje |
| **`context_mode="last_agent"`** | Kiekvienas vykdytojas mato tik tiesioginio pirmtako išvestį |
| **Foundry Toolkit darbo srautas** | Kūrimo vedlys, Agentų inspektorius, Darbo srauto vizualizatorius, vieno paspaudimo diegimas |

---

## Ką baigėte

<details open>
<summary><strong>🅰️ A kelias - Foundry prenumerata</strong></summary>

- [x] Patikrinta Laboratorinės užduoties 01 nustatymai: projektas, modelis ir RBAC aktyvūs
- [x] Sukurtas daugiaagentinis projektas naudojant Workflows šabloną
- [x] Parašytos keturių agentų instrukcijos (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Integruotas Microsoft Learn MCP įrankis su `streamable_http_client`
- [x] Sujungtas darbo srauto grafas su `WorkflowBuilder` (nuosekli linija su turinio perdavimu)
- [x] Lokaliai atlikti 3 pagrindiniai testai (Agent Inspector) – tinkamumo įvertis, spragų kortelės, MCP URL
- [x] Įdiegta Foundry Agent Service (konteineryje, su valdomu tapatumu)
- [x] Patikrinta debesų aplinkoje – rezultatai atitinka vietinius

</details>

<details open>
<summary><strong>🅱️ B kelias - Foundry Local</strong></summary>

- [x] Patikrinta Laboratorinės užduoties 01 nustatymai: Foundry Local veikia su vietiniu modeliu
- [x] Sukurtas daugiaagentinis projektas naudojant Workflows šabloną
- [x] Parašytos keturių agentų instrukcijos ir sujungtas darbo srauto grafas
- [x] Integruotas Microsoft Learn MCP įrankis
- [x] Atlikti lokaliniai 3 pagrindiniai testai
- [x] Patikrintas daugiaagentinis veikimas be debesų resursų

</details>

---

## Tolesni veiksmai

### Tęskite mokymąsi

| Išteklius | Aprašymas |
|----------|-------------|
| **[Agent Framework SDK nuoroda](https://learn.microsoft.com/agent-framework/)** | API dokumentacija `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[MCP įrankių katalogas](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Prisijunkite prie kitų MCP serverių (Bing, GitHub, specialūs) |
| **[Papildyti žinias (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Įgudinkite agentus su dokumentais, vektoriniais saugyklomis ar Bing paieška |
| **[Foundry vertinimai](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Matavimas agentų kokybės mastu su automatizuotais vertintojais |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Visa platformos nuoroda |
| **[Foundry Toolkit – Naujienos](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Praplėtimo naujinimų žurnalas |

### Idėjos praplėsti šį darbo srautą

- **Pridėti 5-ą agentą** – Pokalbių trenerį, kuris pagal spragų ataskaitą generuoja tikėtinius interviu klausimus
- **Pridėti Bing paieškos įrankį** – Leisti JD Agent ieškoti panašių darbo skelbimų reikalavimų praturtinimui
- **Prisijungti prie CV duomenų bazės** – Traukti kandidatų profilius iš duomenų bazės per specialų `@tool`
- **Išbandyti skirtingus modelius** – Palyginti `gpt-4.1` ir `gpt-4.1-mini` išvesties kokybę ir delsą
- **Vertinti su Foundry** – Naudoti Vertinimų funkciją, kad įvertintumėte tinkamumo ataskaitas pagal šabloninį duomenų rinkinį

### B kelio naudotojams: perkelti diegimą į debesis

Kai būsite pasiruošę diegti debesyje:
1. Pasiimkite Azure prenumeratą ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Atlikite [Laboratorinę užduotį 01, 1 modulį](../../lab01-single-agent/docs/01-setup.md) (sukurti projektą, įdiegti modelį, priskirti RBAC teises)
3. Atnaujinkite `.env` rinkinį su Foundry projekto galiniu tašku ir modelio diegimo pavadinimu
4. Tęskite iš [6 modulo – Diegimas į Foundry](06-deploy-to-foundry.md)

---

## Išnaikinti išteklius (pasirinktinai)

Jei norite pašalinti Azure išteklius, sukurtus šio seminaro metu:

### 1 variantas: Ištrinti išteklių grupę (pašalina viską)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 2 variantas: Ištrinti tik talpinamą agentą

1. Atidarykite [ai.azure.com](https://ai.azure.com) → savo projektą → **Build** → **Agents**.
2. Suraskite **PersonalCareerCopilot** → spustelėkite **Delete**.

### 3 variantas: Ištrinti modelio diegimą

1. Foundry šoniniame meniu išplėskite savo projektą → **Models**.
2. Dešiniuoju pelės mygtuku spustelėkite modelio diegimą → **Delete**.

> **Kainos pastaba:** Talpinami agentai sukelia išlaidas tik veikimo metu. Jei sustabdote arba ištrinate agentą, papildomų mokesčių nėra. Modelio diegimas gali sukelti nedidelį mokestį už rezervuotą pajėgumą – pašalinkite, jei baigėte.

---

**Ankstesnis:** [08 - Trikčių šalinimas](08-troubleshooting.md) · **Pagrindinis:** [Laboratorija 02 README](../README.md) · [Seminaro pradžia](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->