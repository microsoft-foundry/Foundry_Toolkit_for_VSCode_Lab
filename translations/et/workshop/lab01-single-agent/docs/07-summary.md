# Moodul 7 - Kokkuvõte ja järgmised sammud

⏱️ ~5 minutit

**Palju õnne!** Olete loonud, testinud ja (kui valisite tee A) juurutanud majutatud tehisintellekti agendi, kasutades Microsoft Foundryt ja Foundry tööriistakomplekti VS Code jaoks.

---

## Mida te ehitasite

**„Selgita nagu juhile“** agent, mis:
- Võtab vastu tehnilisi intsidentide raporteid või tegevuse uuendusi HTTP kaudu (`POST /responses`)
- Tõlgib need lihtsas keeles juhile mõeldud kokkuvõteteks
- Järgib struktureeritud väljundvormingut (Mis juhtus / Ärimõju / Järgmine samm)
- Keeldub teemavälistest päringutest ja prompt-injektsiooni katsetest
- Jookseb konteineripõhisena majutatuna Microsoft Foundry Agent Service’is

---

## Põhikontseptsioonid, mida õppisite

| Kontseptsioon | Mida harjutasite |
|---------|-------------------|
| **Agendi raamistiku arhitektuur** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` töövoog |
| **Majutatud agendi elutsükkel** | Raamistamine → Konfigureerimine → Kohalik testimine → Juurutamine → Pilves kontrollimine |
| **Süsteemi prompti inseneritöö** | Roll, sihtrühm, väljundvorming, reeglid, turvanõuded ja näited |
| **Kohaliku ja majutatud erisused** | Identiteet (isiklik volitus vs hallatud identiteet), lõpp-punkt, võrgu rada |
| **Turvapiirid** | Prompt-injektsiooni kaitse, rolli järgimine, servajuhtumite korrapärane käsitlemine |
| **Foundry tööriistakomplekti töövoog** | Projekti loomine, mudeli juurutamine, agendi raamistamine, Agent Inspector, ühe klikiga juurutus |

---

## Mida sa tegid lõpetatuks

### Tee A (Foundry tellimus)

- [x] Seadistasin Foundry tööriistakomplekti ja lõin Foundry projekti juurutatud mudeliga
- [x] Raamistasin majutatud agendi automaatselt genereeritud projektistruktuuriga
- [x] Kirjutasin struktureeritud agendi juhised turvareeglitega
- [x] Testisin kohapeal 3 funktsionaalse stsenaariumiga (Agent Inspector)
- [x] Juurutasin Foundry Agent Servicesse (konteineripõhine)
- [x] Kontrollisin pilvekeskkonnas 4 servajuhtumi/turvatestiga

### Tee B (Foundry kohalik)

- [x] Seadistasin Foundry tööriistakomplekti kohaliku mudeli lõpp-punktiga
- [x] Raamistasin majutatud agendi projekti
- [x] Kirjutasin struktureeritud agendi juhised turvareeglitega
- [x] Testisin kohapeal 3 funktsionaalse stsenaariumiga
- [x] Kinnitasin agendi käitumise ilma pilveteenuseid kasutamata

---

## Järgmised sammud

### Õppimise jätkamine

| Ressurss | Kirjeldus |
|----------|-------------|
| **[Lab 02 - Mitme agendi orkestreerimine](../../lab02-multi-agent/docs/README.md)** | Loo 4-agendi töövoog (CV → Töö sobivuse hindaja) orkestreerimismustritega |
| **[Lisa oma agendile tööriistu](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Ühenda API-d, andmebaasid või kohandatud funktsioonid tööriistade kataloogi kaudu |
| **[Lisa teadmisi (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Põhista oma agent dokumentide, vektorpoe või Bing otsinguga |
| **[Microsoft Foundry dokumentatsioon](https://learn.microsoft.com/azure/foundry/)** | Täielik platvormi referents |
| **[Agent Frameworki SDK referents](https://learn.microsoft.com/agent-framework/)** | `agent-framework` paketi API dokumentatsioon |
| **[Foundry tööriistakomplekt - Mis uut](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Laienduste väljaannete märkmed ja muudatused |

### Ideed, kuidas oma agenti laiendada

- **Lisa kuupäevatööriist** - Lase agendil lisada "seisuga täna" kontekst kokkuvõtetesse
- **Ühenda intsidentide andmebaasiga** - Tõmba tööriistafunktsiooni kaudu tegelikud intsidentide detailid
- **Lisa Bing’i baastööriist** - Lase agendil otsida värskeid uudiseid lisakontekstiks
- **Proovi erinevaid mudeleid** - Võrdle `gpt-4.1` ja `gpt-4.1-mini` väljundite kvaliteeti
- **Hinda Foundryga** - Kasuta hinnanguid agentide kvaliteedi mõõtmiseks suurel skaalal

### Tee B kasutajatele: Täienda pilvejuurutuseks

Kui oled valmis pilve juurutamiseks:
1. Saa Azure tellimus ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Lõpeta [Moodul 01, Seadistamine](01-setup.md#step-2-set-up-based-on-your-access) (lõi projekt, juurutas mudeli, määras RBAC)
3. Uuenda oma `.env` fail Foundry projekti lõpp-punkti ja mudelijuhtumi nimega
4. Jätka [Moodul 05 - Juurutus Foundrys](05-deploy-to-foundry.md) juurest

---

## Ressursside korrastamine (valikuline)

Kui soovid selle töötuba ajal loodud Azure ressursid eemaldada:

### Variant 1: Kustuta ressursside grupp (eemaldab kõik)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Variant 2: Kustuta ainult majutatud agent

1. Ava [ai.azure.com](https://ai.azure.com) → oma projekt → **Build** → **Agents**.
2. Klõpsa oma agenti → klõpsa **Delete**.

### Variant 3: Kustuta mudelijuhtum

1. Foundry külgribal laienda oma projekt → **Models**.
2. Paremklõps mudelijuhtumil → **Delete**.

> **Kulu märkus:** Majutatud agendid tekitavad tasu ainult jooksvatel aegadel. Kui peatad või kustutad agendi, ei teki jätkuvat tasu. Mudelijuhtum võib tekitada väikese tasu reserveeritud mahutavuse eest – kustuta see, kui sul seda enam vaja pole.

---

**Eelmine:** [06 - Kontrolli playground’is](06-verify-in-playground.md) · **Järgmine:** [08 - Tõrkeotsing (viide) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Lahtiütlus**:
See dokument on tõlgitud kasutades AI tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi me püüdleme täpsuse poole, palun pange tähele, et automatiseeritud tõlgetes võib esineda vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlkega seotud eksimustest või valesti mõistmistest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->