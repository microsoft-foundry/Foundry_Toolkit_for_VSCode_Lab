# 7 modulis – Santrauka ir tolesni žingsniai

⏱️ ~5 min

**Sveikiname!** Jūs sukūrėte, išbandėte ir (jei pasirenkate A kelią) įdiegėte talpinamą DI agentą naudodami Microsoft Foundry ir Foundry Toolkit skirtą VS Code.

---

## Ką jūs sukūrėte

**„Paaiškinkite, tarsi būčiau vadovas“** agentą, kuris:
- Priima technines incidentų ataskaitas arba veiklos atnaujinimus per HTTP (`POST /responses`)
- Verčia jas į paprastą vadovų suprantamą santrauką
- Laikosi struktūruoto išvesties formato (Kas įvyko / Verslo poveikis / Kitas žingsnis)
- Atsisako temų, nesusijusių su užduotimi, ir užkerta kelią užklausų įpurškimui
- Veikia kaip konteineriu talpinamas agentas Microsoft Foundry Agent Service

---

## Pagrindinės įgytos sąvokos

| Sąvoka | Ką praktikavote |
|---------|-------------------|
| **Agentų sistemos architektūra** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` grandinė |
| **Talpinamo agento gyvenimo ciklas** | Sukūrimas → Konfigūravimas → Bandymas lokaliai → Diegimas → Patikrinimas debesyje |
| **Sistemos užklausos inžinerija** | Vaidmuo, auditorija, išvesties formatas, taisyklės, saugumo apribojimai ir pavyzdžiai |
| **Skirtumai tarp lokalaus ir talpinamo agento** | Tapatybė (asmens kredencialai vs. valdomoji tapatybė), galinis taškas, tinklo maršrutas |
| **Saugumo ribos** | Užklausų įpurškimo gynyba, vaidmens laikymasis, malonus kraštutinių atvejų valdymas |
| **Foundry Toolkit darbo eiga** | Projekto sukūrimas, modelio diegimas, agento kūrimas, Agent Inspector, vieno spustelėjimo diegimas |

---

## Ką jūs atlikote

### A kelias (Foundry prenumerata)

- [x] Įdiegėte Foundry Toolkit ir sukūrėte Foundry projektą su įdiegtu modeliu
- [x] Sukūrėte talpinamą agentą su automatiškai sugeneruota projekto struktūra
- [x] Parašėte struktūruotas agento instrukcijas su saugumo taisyklėmis
- [x] Išbandėte lokaliai su 3 funkciniais scenarijais (Agent Inspector)
- [x] Įdiegėte Foundry Agent Service (konteinerizuotą)
- [x] Patikrinote debesų aplinkoje su 4 kraštutinių atvejų/saugumo testais

### B kelias (Foundry Local)

- [x] Įdiegėte Foundry Toolkit su vietiniu modelio galiniu tašku
- [x] Sukūrėte talpinamo agento projektą
- [x] Parašėte struktūruotas agento instrukcijas su saugumo taisyklėmis
- [x] Išbandėte lokaliai su 3 funkciniais scenarijais
- [x] Patvirtinote agento elgseną nereikalaujant debesies resursų

---

## Tolesni žingsniai

### Tęskite mokymąsi

| Ištekliai | Aprašymas |
|----------|-------------|
| **[2 laboratorinis darbas - kelių agentų orkestracija](../../lab02-multi-agent/docs/README.md)** | Sukurkite 4 agentų darbo eigą (CV → Darbo tinkamumo vertintojas) su orkestracijos šablonais |
| **[Pridėkite priemones savo agentui](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Prijunkite API, duomenų bazes ar pasirinktines funkcijas per Priemonių katalogą |
| **[Pridėkite žinias (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Pagrįskite agentą dokumentais, vektoriaus saugyklomis ar Bing paieška |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Pilna platformos nuoroda |
| **[Agentų sistemos SDK nuoroda](https://learn.microsoft.com/agent-framework/)** | API dokumentacija `agent-framework` paketui |
| **[Foundry Toolkit - Kas naujo](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Priedo išleidimo pastabos ir pakeitimų žurnalas |

### Idėjos agento praplėtimui

- **Pridėkite datos priemonę** - Leiskite agentui įtraukti „šiandienos“ kontekstą santraukose
- **Prijunkite prie incidentų duomenų bazės** - Gaukite tikras incidentų detales per priemonės funkciją
- **Pridėkite Bing paieškos priemonę** - Leiskite agentui ieškoti naujausių naujienų papildomam kontekstui
- **Išbandykite skirtingus modelius** - Palyginkite `gpt-4.1` ir `gpt-4.1-mini` išvesties kokybę
- **Įvertinkite su Foundry** - Naudokite Vertinimo funkciją agento kokybės matavimui mastu

### B kelio naudotojams: perėjimas prie debesijos diegimo

Kai būsite pasiruošę diegti debesyje:
1. Gaukite Azure prenumeratą ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Atlikite [1 modulį, Įdiegimas](01-setup.md#step-2-set-up-based-on-your-access) (sukurkite projektą, įdiekite modelį, priskirkite RBAC)
3. Atnaujinkite `.env` su Foundry projekto galu ir modelio diegimo pavadinimu
4. Tęskite nuo [5 modulio - Diegimas į Foundry](05-deploy-to-foundry.md)

---

## Išvalykite resursus (pasirinktinai)

Jei norite pašalinti Azure resursus, sukurtus šio seminaro metu:

### 1 variantas: Ištrinti resursų grupę (pašalina viską)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 2 variantas: Ištrinti tik talpinamą agentą

1. Atidarykite [ai.azure.com](https://ai.azure.com) → savo projektą → **Sukurti** → **Agentai**.
2. Paspauskite ant savo agento → paspauskite **Ištrinti**.

### 3 variantas: Ištrinti modelio diegimą

1. Foundry šoniniame meniu išplėskite savo projektą → **Modeliai**.
2. Dešiniuoju pelės klavišu spustelėkite modelio diegimą → **Ištrinti**.

> **Kainos pastaba:** Talpinami agentai kainuoja tik kai veikia. Jei sustabdysite arba ištrinsite agentą, toliau jokių mokesčių nebus. Modelio diegimas gali turėti nedidelį mokestį už rezervuotą pajėgumą – ištrinkite jį, jei baigėte darbą.

---

**Ankstesnis:** [06 - Patikrinimas žaidimų aikštelėje](06-verify-in-playground.md) · **Sekantis:** [08 - Triktims šalinti (Nuoroda) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->