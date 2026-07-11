# Modul 5 - Nasadenie do služby Foundry Agent

⏱️ ~10 min

> ⚠️ **Používatelia cesty B:** Tento modul vyžaduje predplatné Foundry. Ak používate Foundry Local, prejdite na [Modul 07 - Zhrnutie](07-summary.md). Úspešne ste dokončili lokálny vývojársky workflow!

V tomto module nasadíte svoj lokálne otestovaný agent do Microsoft Foundry ako **Hosťovaný agent**. Nasadenie vytvorí obraz kontajnera, odošle ho do Azure Container Registry a spustí agenta v spravovanej infraštruktúre Foundry.

### Pipeline nasadenia

```mermaid
flowchart LR
    A["Dockerfile
    main.py"] -->|docker build| B["Container
    Image"]
    B -->|docker push| C["Azure Container
    Registry (ACR)"]
    C -->|zaregistrovať agenta| D["Foundry Agent
    Service"]
    D -->|spustiť kontajner| E["/responses
    endpoint ready"]

    style A fill:#9B59B6,color:#fff
    style B fill:#9B59B6,color:#fff
    style C fill:#E67E22,color:#fff
    style D fill:#3498DB,color:#fff
    style E fill:#27AE60,color:#fff
```

---

## Kontrola predpokladov

Pred nasadením si overte:

- [ ] Agent úspešne prešiel všetkými 3 lokálnymi scenármi z [Modulu 04](04-test-locally.md)
- [ ] Máte pridelenú rolu **Azure AI User** na úrovni projektu ([Modul 01, Priradenie RBAC](01-setup.md#deploy-a-model--assign-rbac))
- [ ] Ste prihlásený do Azure vo VS Code (v ikone Účty je vaše meno)

---

## Krok 1: Začnite nasadenie

### Možnosť A: Nasadenie z Agent Inspector (odporúčané)

Ak je Agent Inspector otvorený (z testovania):
1. Kliknite na tlačidlo **Deploy** v pravom hornom rohu (ikona oblaku ↑).

### Možnosť B: Nasadenie z Command Palette

1. Stlačte `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent**.

---

## Krok 2: Konfigurácia nasadenia

Sprievodca vás vyzve na:

![Projektová konfigurácia](../../../../../translated_images/sk/05-foundry-project-setup.ca6ad16a6484e054.webp)

| Výzva | Výber |
|--------|-----------|
| **Predplatné** | Vaše Azure predplatné |
| **Cieľový projekt** | Váš Foundry projekt (napr. `workshop-agents`) |

Kliknite na **ďalej** pre konfiguráciu agenta.

![Základná konfigurácia](../../../../../translated_images/sk/05-configure-basics.4d5f3d6b0d96f033.webp)

| Výzva | Výber |
|--------|-----------|
| **Metóda nasadenia** | Kontajner |
| **Registre kontajnerov** | **Predvolený ACR** (Microsoft Foundry vám vytvorí a spravuje jeden) |
| **Nasadiť do** | Nový agent (meno, `executive-summary-agent`) |

Kliknite na **ďalej** pre kontrolu a nasadenie agenta.

![Kontrola a nasadenie](../../../../../translated_images/sk/05-review-deploy.12b449d426bff886.webp)

| Výzva | Výber |
|--------|-----------|
| **CPU a pamäť** | **0.25 CPU jadra, 0.5 Gi pamäte** (postačujúce pre workshop) |

---

## Krok 3: Nasadenie a sledovanie

1. Kliknite na **Deploy**.
2. Sledujte panel **Output** (vyberte **Microsoft Foundry** z rozbaľovacieho menu).
3. Nasadenie prechádza týmito fázami:
   - **Docker build** - zostaví kontajner z vášho Dockerfile
   - **Docker push** - odošle obraz do ACR (1–3 min pri prvom nasadení)
   - **Registrácia agenta** - vytvorí hosťovaného agenta vo Foundry
   - **Štart kontajnera** - spustí sa so systémovou spravovanou identitou

4. Po dokončení sa zobrazí oznámenie:
   > **my-agent bol úspešne nasadený.** `Zobraziť logy` `Spustiť agenta`

5. Kliknite na **Spustiť agenta** pre otvorenie Agent Playground.

![Úspešné nasadenie so zobrazeným Agent Playground so stavom Running](../../../../../translated_images/sk/05-deployed-asset.b59e6a5eef31c0b1.webp)

### Hodnoty stavu nasadenia

| Stav | Význam |
|--------|---------|
| **Running** | Kontajner pripravený, agent reaguje |
| **Pending** | Kontajner sa spúšťa - počkajte 30–60 sekúnd |
| **Failed** | Skontrolujte logy (pozri riešenie problémov nižšie) |

---

## Bežné chyby pri nasadení

| Chyba | Hlavná príčina | Riešenie |
|-------|-----------|-----|
| zamietnuté oprávnenie `agents/write` | Chýba rola **Azure AI User** na úrovni projektu | [Modul 01, Priradenie RBAC](01-setup.md#deploy-a-model--assign-rbac) |
| Docker neběží | Docker Desktop nie je spustený | Spustite Docker Desktop → overte `docker info` |
| Autorizácia ACR | Spravovaná identita nemôže stiahnuť obraz | Pozrite [Modul 08 - Riešenie problémov](08-troubleshooting.md) |

---

### ✅ Kontrolný bod

- [ ] Nasadenie dokončené bez chýb
- [ ] Agent sa zobrazuje pod **Hosted Agents (Preview)** v Foundry bočnom paneli
- [ ] Stav kontajnera ukazuje **Running**
- [ ] Otvorená karta Agent Playground zobrazuje podrobnosti agenta a URL koncového bodu

---

**Predchádzajúce:** [04 - Test lokálne](04-test-locally.md) · **Nasledujúce:** [06 - Overenie v Playground →](06-verify-in-playground.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->