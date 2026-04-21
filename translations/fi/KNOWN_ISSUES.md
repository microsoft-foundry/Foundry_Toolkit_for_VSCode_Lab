# Tunnetut ongelmat

Tämä dokumentti seuraa nykyisen repositorion tilan tunnettuja ongelmia.

> Viimeksi päivitetty: 2026-04-15. Testattu Python 3.13 / Windows käyttöympäristössä `.venv_ga_test`.

---

## Nykyiset pakettikiinnitykset (kaikki kolme agenttia)

| Paketti | Nykyinen versio |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(korjattu — katso KI-003)* |

---

## KI-001 — GA 1.0.0 -päivitys estetty: `agent-framework-azure-ai` poistettu

**Tila:** Auki | **Vakavuus:** 🔴 Korkea | **Tyyppi:** Rikkova

### Kuvaus

`agent-framework-azure-ai` -paketti (kiinnitetty versioon `1.0.0rc3`) poistettiin/vanhentui
GA-julkaisussa (1.0.0, julkaistu 2026-04-02). Sen tilalle on tullut:

- `agent-framework-foundry==1.0.0` — Foundry-isännöity agenttimalli
- `agent-framework-openai==1.0.0` — OpenAI-taustainen agenttimalli

Kaikki kolme `main.py` -tiedostoa tuovat `AzureAIAgentClient`-luokan `agent_framework.azure`-moduulista, mikä
nostaa `ImportError`-poikkeuksen GA-pakettien kanssa. `agent_framework.azure`-nimialue on edelleen olemassa
GA-julkaisussa, mutta sisältää nyt vain Azure Functions -luokat (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ei Foundryn agentteja.

### Vahvistettu virhe (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Vaikutetut tiedostot

| Tiedosto | Rivi |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` yhteensopimaton GA:n `agent-framework-core` kanssa

**Tila:** Auki | **Vakavuus:** 🔴 Korkea | **Tyyppi:** Rikkova (odottaa upstream-korjausta)

### Kuvaus

`azure-ai-agentserver-agentframework==1.0.0b17` (uusin) pakottaa
`agent-framework-core<=1.0.0rc3` -version. Sen asentaminen yhdessä `agent-framework-core==1.0.0` (GA)
kanssa pakottaa pipin **palauttamaan** `agent-framework-core`-version takaisin `rc3`:een, mikä sitten rikkoo
`agent-framework-foundry==1.0.0` ja `agent-framework-openai==1.0.0`.

Kutsua `from azure.ai.agentserver.agentframework import from_agent_framework`, jota kaikki agentit käyttävät HTTP-palvelimen sitomiseen,
ei siksi voida myöskään suorittaa.

### Vahvistettu riippuvuuskonflikti (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Vaikutetut tiedostot

Kaikki kolme `main.py`-tiedostoa — sekä ylin tuonti että toiminnon sisällä oleva tuonti `main()`-funktiossa.

---

## KI-003 — `agent-dev-cli --pre` -lipuke ei enää tarpeen

**Tila:** ✅ Korjattu (ei rikova) | **Vakavuus:** 🟢 Matala

### Kuvaus

Kaikki `requirements.txt`-tiedostot sisälsivät aiemmin `agent-dev-cli --pre`-lippua tuomaan esijulkaisun CLI:n. GA 1.0.0 -julkaisun jälkeen,
julkaistu 2026-04-02, vakaa `agent-dev-cli`-versio on saatavilla ilman `--pre`-lippua.

**Korjaus tehty:** `--pre`-lippu on poistettu kaikista kolmesta `requirements.txt`-tiedostosta.

---

## KI-004 — Dockerfilet käyttävät `python:3.14-slim` (esijulkaisuperuskuva)

**Tila:** Auki | **Vakavuus:** 🟡 Matala

### Kuvaus

Kaikki `Dockerfile`t käyttävät `FROM python:3.14-slim`, joka seuraa esijulkaisuvaiheen Python-versiota.
Tuotantoympäristöissä tulisi kiinnittää vakaaseen julkaisuun (esim. `python:3.12-slim`).

### Vaikutetut tiedostot

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Viitteet

- [agent-framework-core PyPI:ssa](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry PyPI:ssa](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:  
Tämä asiakirja on käännetty käyttämällä tekoälykäännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Pyrimme tarkkuuteen, mutta pidäthän mielessä, että automaattisissa käännöksissä saattaa esiintyä virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäiskielellä tulisi pitää virallisena lähteenä. Tärkeissä asioissa suositellaan ammattilaisen tekemää ihmiskäännöstä. Emme ole vastuussa mistään tästä käännöksestä johtuvista väärinymmärryksistä tai väärin tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->