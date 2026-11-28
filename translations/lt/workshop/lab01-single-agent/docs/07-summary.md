# 7 modulis – Santrauka ir tolimesni veiksmai

⏱️ ~5 min

**Sveikiname!** Jūs sukūrėte, išbandėte ir (jei pasirinkote 1-ojo kelio variantą) įdiegėte talpinamą AI agentą naudodami Microsoft Foundry ir Foundry Toolkit skirtą VS Code.

---

## Ką jūs sukūrėte

**„Paaiškinkite, lyg būčiau vadovas“** agentą, kuris:
- Gavęs techninių incidentų ataskaitas ar veiklos atnaujinimus per HTTP (`POST /responses`)
- Išverčia juos į paprastai suprantamas vadovo santraukas
- Laikosi struktūruoto išvesties formato (Kas įvyko / Verslo poveikis / Kitas žingsnis)
- Atmeta neį temą pateiktus užklausimus ir bandymus įterpti netinkamus promptus
- Veikia kaip konteinerizuotas talpinamas agentas Microsoft Foundry Agent Service platformoje

---

## Pagrindinės išmoktos sąvokos

| Sąvoka | Ką praktikavote |
|---------|-------------------|
| **Agentų sistemos architektūra** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` dujotiekis |
| **Talpinamo agente ciklas** | Sukurti karkasą → Konfigūruoti → Išbandyti lokaliai → Diegti → Patikrinti debesyje |
| **Sisteminės užklausos inžinerija** | Vaidmuo, auditorija, išvesties formatas, taisyklės, saugumo apribojimai ir pavyzdžiai |
| **Lokalaus ir talpinamo skirtumai** | Tapatybė (asmeninis kredencialas vs. valdomoji tapatybė), galinis taškas, tinklo kelias |
| **Saugumo ribos** | Užklausų injekcijos gynimas, vaidmens laikymasis, gražus kraštutinių atvejų valdymas |
| **Foundry Toolkit darbo eiga** | Projekto kūrimas, modelio diegimas, agento karkaso kūrimas, Agent Inspector, vieno spustelėjimo diegimas |

---

## Ką įvykdėte

### 1-asis kelias (Foundry prenumerata)

- [x] Įdiegėte Foundry Toolkit ir sukūrėte Foundry projektą su įdiegtu modeliu
- [x] Sukūrėte talpinamą agentą su automatiškai sugeneruota projekto struktūra
- [x] Parašėte struktūruotas agento instrukcijas su saugumo taisyklėmis
- [x] Išbandėte lokaliai su 3 funkcionalumo scenarijais (Agent Inspector)
- [x] Įdiegėte Microsoft Foundry Agent Service (konteinerizuotą)
- [x] Patikrinote debesų žaidimų aikštelėje su 4 kraštutinių atvejų / saugumo testais

### 2-asis kelias (Foundry Local)

- [x] Įdiegėte Foundry Toolkit su lokaliu modelio galiniu tašku
- [x] Sukūrėte talpinamo agento projektą
- [x] Parašėte struktūruotas agento instrukcijas su saugumo taisyklėmis
- [x] Išbandėte lokaliai 3 funkcionalumo scenarijais
- [x] Patvirtinote agento elgseną nepriklausomai nuo debesų resursų

---

## Tolimesni veiksmai

### Toliau mokykitės

| Šaltinis | Aprašymas |
|----------|-------------|
| **[Laboratorija 02 - Multi-agentų orkestras](../../lab02-multi-agent/docs/README.md)** | Sukurkite 4 agentų darbo eigą (CV → Darbo tinkamumo vertintojas) su orkestravimo šablonais |
| **[Pridėkite įrankius savo agentui](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Prijunkite API, duomenų bazes ar savo funkcijas per Įrankių katalogą |
| **[Pridėkite žinias (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Pagrįskite agentą dokumentais, vektorinėmis saugyklomis ar Bing paieška |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Pilnas platformos nuorodų rinkinys |
| **[Agent Framework SDK nuoroda](https://learn.microsoft.com/agent-framework/)** | API dokumentacija `agent-framework` paketo |
| **[Foundry Toolkit – Kas naujo](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Pleistro naujinimo pastabos ir pokyčių žurnalas |

### Idėjos, kaip plėsti savo agentą

- **Pridėkite datų įrankį** – leiskite agentui įtraukti „šiandienos dienos“ kontekstą santraukose
- **Prijunkite prie incidentų duomenų bazės** – traukite tikras incidentų detales per įrankio funkciją
- **Pridėkite Bing pagrindimo įrankį** – leiskite agentui ieškoti naujausių naujienų papildomam kontekstui
- **Išbandykite skirtingus modelius** – palyginkite `gpt-4.1` ir `gpt-4.1-mini` išvesties kokybę
- **Įvertinkite su Foundry** – naudokite Vertinimų funkciją, kad mastu įvertintumėte agentų kokybę

### Skirtas 2-ojo kelio vartotojams: atnaujinkite į debesų diegimą

Kai būsite pasiruošę diegti debesyje:
1. Gaukite Azure prenumeratą ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Užbaikite [1 modulį, Sąranką](01-setup.md#step-2-set-up-based-on-your-access) (sukurkite projektą, įdiekite modelį, paskirkite RBAC)
3. Atnaujinkite savo `.env` su Foundry projekto galiniu tašku ir modelio diegimo pavadinimu
4. Tęskite nuo [5 modulio – Diegimas į Foundry](05-deploy-to-foundry.md)

---

## Išvalykite resursus (pasirinktinai)

Jei norite panaikinti Azure išteklius, sukurti šioje dirbtuvėje:

### 1 variantas: Ištrinkite resursų grupę (pašalina viską)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 2 variantas: Ištrinkite tik talpinamą agentą

1. Atidarykite [ai.azure.com](https://ai.azure.com) → savo projektą → **Build** → **Agents**.
2. Spustelėkite savo agentą → spustelėkite **Delete**.

### 3 variantas: Ištrinkite modelio diegimą

1. Foundry šoninė meniu srityje išplėskite savo projektą → **Models**.
2. Dešiniuoju pelės mygtuku spustelėkite modelio diegimą → **Delete**.

> **Kainos pastaba:** Talpinami agentai atsieina mokestį tik veikimo metu. Jei sustabdysite ar ištrinsite agentą, tęstinių mokesčių nėra. Modelio diegimas gali turėti nedidelį mokestį už rezervuotą talpą – trinkite, jei nebereikia.

---

**Ankstesnis:** [06 - Patikrinimas žaidimų aikštelėje](06-verify-in-playground.md) · **Sekantis:** [08 - Trikčių šalinimas (referencinė medžiaga) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba laikomas autoritetingu šaltiniu. Svarbiai informacijai rekomenduojama naudoti profesionalų žmogiškąjį vertimą. Mes neatsakome už jokius nesusipratimus ar neteisingą interpretaciją, kilusią naudojantis šiuo vertimu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->