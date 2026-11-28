# Moodul 7 - Kokkuvõte ja järgmised sammud

⏱️ ~5 min

**Õnnitlused!** Sa oled loonud, testinud ja (kui valisid tee A) juurutanud majutatud tehisintellekti agendi, kasutades Microsoft Foundryt ja Foundry tööriistakomplekti VS Code jaoks.

---

## Mida sa lõid

**"Selgita nagu ma oleksin juht"** agent, kes:
- Võtab vastu tehnilisi intsidentide aruandeid või operatiivseid uuendusi HTTP kaudu (`POST /responses`)
- Tõlgib need lihtsasti mõistetavateks juhtidele mõeldud kokkuvõteteks
- Järgib struktureeritud väljundvormingut (Mis juhtus / Äri mõju / Edasi järgmine samm)
- Keeldub teemast kõrvale kalduvatest päringutest ja promptide süstimisest
- Jookseb konteineripõhisena majutatud agendina Microsoft Foundry Agent Service’is

---

## Peamised omandatud kontseptsioonid

| Kontseptsioon | Mida sa harjutasid |
|---------|-------------------|
| **Agendi raamistikupositsiooni arhitektuur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` torujuhe |
| **Majutatud agendi elutsükkel** | Alus → Konfigureeri → Testi lokaalselt → Juuruta → Kontrolli pilves |
| **Süsteemi promptide seadistamine** | Roll, sihtrühm, väljundvorming, reeglid, ohutuspiirangud ja näited |
| **Lokaalse ja majutatud vaheline erinevus** | Identiteet (isiklik mandarv vs hallatav identiteet), lõpp-punkt, võrgu tee |
| **Ohutuspiirid** | Promptide süstimise kaitse, rolli järgimine, tagavarade ja servjuhtumite väärikas käsitlemine |
| **Foundry tööriistakomplekti töövoog** | Projekti loomine, mudeli juurutamine, agendi scaffolding, Agent Inspector, ühe klikiga juurutamine |

---

## Mida sa lõpetasid

### Tee A (Foundry tellimus)

- [x] Seadistasid Foundry tööriistakomplekti ja lõid Foundry projekti koos juurutatud mudeliga
- [x] Scaffolding majutatud agendi automaatselt genereeritud projekti struktuuriga
- [x] Kirjutasid struktureeritud agendi juhised ohutusreeglitega
- [x] Testisid lokaalselt 3 funktsionaalse stsenaariumiga (Agent Inspector)
- [x] Juurtasid Foundry Agent Service’i (konteineripõhiselt)
- [x] Kontrollisid pilves mänguväljakul 4 äärmus- ja ohutest’iga

### Tee B (Foundry lokaalne)

- [x] Seadistasid Foundry tööriistakomplekti kohaliku mudeli lõpp-punktiga
- [x] Scaffolding majutatud agendi projekt
- [x] Kirjutasid struktureeritud agendi juhised koos ohutusreeglitega
- [x] Testisid lokaalselt 3 funktsionaalse stsenaariumiga
- [x] Kontrollisid agendi käitumist ilma pilveressurssideta

---

## Järgmised sammud

### Jätka õppimist

| Ressurss | Kirjeldus |
|----------|-------------|
| **[Lab 02 - Mitme agendi orkestreerimine](../../lab02-multi-agent/docs/README.md)** | Ehita 4-agendi töövoog (CV → Töö sobivuse hindaja) orkestreerimismustritega |
| **[Lisa oma agendile tööriistad](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Ühenda API-d, andmebaasid või kohandatud funktsioonid tööriistade kataloogi kaudu |
| **[Lisa teadmisi (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Põhista agent dokumentide, vektoripoe või Bing otsingu kaudu |
| **[Microsoft Foundry dokumentatsioon](https://learn.microsoft.com/azure/foundry/)** | Platvormi täielik viide |
| **[Agent Framework SDK viide](https://learn.microsoft.com/agent-framework/)** | API dokumentatsioon `agent-framework` paketi kohta |
| **[Foundry tööriistakomplekti uuendused](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Laienduste väljalasete ja muudatuste logi |

### Ideed agendi laiendamiseks

- **Lisa kuupäeva tööriist** - Luba agendil lisada kokkuvõttesse "seisuga tänasest" kontekst
- **Ühenda intsidentide andmebaasiga** - Tõmba reaalsete intsidentide detailid tööriista funktsiooni kaudu
- **Lisa Bing põlistamise tööriist** - Luba agendil otsida viimaseid uudiseid lisakontekstiks
- **Proovi erinevaid mudeleid** - Võrdle `gpt-4.1` ja `gpt-4.1-mini` väljundi kvaliteeti
- **Hinda Foundryga** - Kasuta hindamisfunktsiooni agentide kvaliteedi mõõtmiseks suurelt

### Tee B kasutajatele: uuenda pilve juurutuseks

Kui oled valmis juurutama pilve:
1. Hangi Azure tellimus ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Lõpeta [Moodul 01, Seadistamine](01-setup.md#step-2-set-up-based-on-your-access) (loo projekt, juuruta mudel, määra RBAC)
3. Uuenda oma `.env` Foundry projekti lõpp-punkti ja mudeli juurutuse nimega
4. Jätka [Moodul 05 - Juuruta Foundrys](05-deploy-to-foundry.md)

---

## Ressursside koristamine (valikuline)

Kui soovid eemaldada selle töötoa jooksul loodud Azure ressursid:

### Variant 1: Kustuta ressursigrupp (eemaldab kõik)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Variant 2: Kustuta ainult majutatud agent

1. Ava [ai.azure.com](https://ai.azure.com) → oma projekt → **Build** → **Agents**.
2. Klõpsa oma agendil → klõpsa **Kustuta**.

### Variant 3: Kustuta mudeli juurutus

1. Foundry külgribal ava oma projekt → **Models**.
2. Paremklõps mudeli juurutusel → **Kustuta**.

> **Kulu märkus:** Majutatud agendid toovad kulusid ainult töötamise ajal. Kui peatad või kustutad agendi, ei kaasne edasisi kulusid. Mudeli juurutus võib põhjustada väikese tasu eraldatud võimsuse eest — kustuta see, kui oled lõpetanud.

---

**Eelmine:** [06 - Kontroll mänguväljakul](06-verify-in-playground.md) · **Järgmine:** [08 - Tõrkeotsing (Viide) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->