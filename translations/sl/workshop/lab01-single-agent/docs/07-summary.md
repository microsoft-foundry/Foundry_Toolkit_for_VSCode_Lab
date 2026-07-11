# Modul 7 - Povzetek in nadaljnji koraki

⏱️ ~5 min

**Čestitamo!** Zgradili, preizkusili in (če ste na poti A) uvedli gostovanega AI agenta z uporabo Microsoft Foundry in Foundry orodij za VS Code.

---

## Kaj ste zgradili

**"Razloži kot da sem direktor"** agent, ki:
- Sprejema tehnična poročila o incidentih ali operativne posodobitve prek HTTP (`POST /responses`)
- Prevaja jih v preprosta, razumljiva povzetka za vodstvo
- Sledi strukturirani obliki izhoda (Kaj se je zgodilo / Poslovni vpliv / Naslednji korak)
- Zavrne zahteve, ki niso relevantne, in poskuse injiciranja v pozive
- Teče kot kontejneriziran gostovani agent v Microsoft Foundry Agent Service

---

## Ključni pojmi, ki ste se jih naučili

| Pojem | Kaj ste vadili |
|---------|-------------------|
| **Arhitektura Agent Framework** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` potek |
| **Življenjski cikel gostovanega agenta** | Scaffold → Konfiguracija → Lokalno testiranje → Uvedba → Preverjanje v oblaku |
| **Inženiring sistemskih pozivov** | Vloga, občinstvo, format izhoda, pravila, varnostne omejitve in primeri |
| **Lokalne proti gostovanim razlikam** | Identiteta (osebni poverilni podatki proti upravljani identiteti), končna točka, mrežna pot |
| **Varnostne meje** | Obramba pred injekcijo pozivov, držanje vloge, korekten odziv na robne primere |
| **Potek dela z Foundry orodji** | Ustvarjanje projekta, uvedba modela, postavitev agenta, Agent Inspector, namestitev z enim klikom |

---

## Kaj ste dokončali

### Pot A (Foundry naročnina)

- [x] Nastavili Foundry orodja in ustvarili Foundry projekt z uvedenim modelom
- [x] Postavili gostovanega agenta z avtomatsko ustvarjeno strukturo projekta
- [x] Napisali strukturirane agentove navodila z varnostnimi pravili
- [x] Testirali lokalno s 3 funkcionalnimi scenariji (Agent Inspector)
- [x] Uvedli v Foundry Agent Service (kontejnerizirano)
- [x] Preverili v oblaku z 4 robnimi/varnostnimi testi

### Pot B (Foundry lokalno)

- [x] Nastavili Foundry orodja z lokalno točko modela
- [x] Postavili projekt gostovanega agenta
- [x] Napisali strukturirane agentove navodila z varnostnimi pravili
- [x] Testirali lokalno s 3 funkcionalnimi scenariji
- [x] Potrdili vedenje agenta brez potrebe po virih v oblaku

---

## Nadaljnji koraki

### Nadaljujte z učenjem

| Vir | Opis |
|----------|-------------|
| **[Lab 02 - Orkestracija več agentov](../../lab02-multi-agent/docs/README.md)** | Zgradite potek dela s 4 agenti (Življenjepis → Ocena združljivosti za delo) z vzorci orkestracije |
| **[Dodajte orodja svojemu agentu](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Povežite API-je, baze podatkov ali prilagojene funkcije preko kataloga orodij |
| **[Dodajte znanje (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Povežite agenta z dokumenti, vektorskimi skladišči ali Bing iskanjem |
| **[Microsoft Foundry dokumentacija](https://learn.microsoft.com/azure/foundry/)** | Celoten referenčni dokument platforme |
| **[Agent Framework SDK referenca](https://learn.microsoft.com/agent-framework/)** | API dokumentacija za paket `agent-framework` |
| **[Foundry orodja - Novosti](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Zabeležke izdaj in spremembe razširitve |

### Ideje za nadgradnjo vašega agenta

- **Dodajte orodje za datum** - Naj agent v povzetkih vključuje kontekst "stanje na dan"
- **Povežite se z bazo incidentov** - Pridobivanje dejanskih podatkov o incidentih preko funkcije orodja
- **Dodajte Bing iskalno orodje** - Naj agent poišče sveže novice za dodaten kontekst
- **Preizkusite različne modele** - Primerjajte kakovost izhoda `gpt-4.1` in `gpt-4.1-mini`
- **Ocenjujte z Foundry** - Uporabite funkcijo Evaluations za merjenje kakovosti agenta na večji lestvici

### Za uporabnike poti B: Nadgradite na uvajanje v oblak

Ko ste pripravljeni za uvedbo v oblak:
1. Pridobite naročnino Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Dokončajte [Modul 01, Nastavitev](01-setup.md#step-2-set-up-based-on-your-access) (ustvarite projekt, uvedite model, dodelite RBAC)
3. Posodobite svojo `.env` datoteko s končno točko projekta Foundry in imenom uvedbe modela
4. Nadaljujte od [Modul 05 - Uvedba v Foundry](05-deploy-to-foundry.md)

---

## Počistite vire (opcijsko)

Če želite odstraniti vire Azure, ustvarjene med tem delavnim sestankom:

### Možnost 1: Izbrišite skupino virov (odstrani vse)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Možnost 2: Izbrišite samo gostovanega agenta

1. Odprite [ai.azure.com](https://ai.azure.com) → vaš projekt → **Build** → **Agents**.
2. Kliknite svojega agenta → kliknite **Delete**.

### Možnost 3: Izbrišite uvedbo modela

1. V stranski vrstici Foundry razširite svoj projekt → **Models**.
2. Z desnim klikom na uvedbo modela → **Delete**.

> **Opomba o stroških:** Gostovani agenti povzročajo stroške samo med delovanjem. Če agenta ustavite ali izbrišete, stroški ne tečejo. Uvedba modela lahko povzroči majhen strošek za rezervirano kapaciteto – izbrišite jo, če je končana.

---

**Prejšnji:** [06 - Preverjanje v igralnem polju](06-verify-in-playground.md) · **Naslednji:** [08 - Odpravljanje težav (referenca) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->