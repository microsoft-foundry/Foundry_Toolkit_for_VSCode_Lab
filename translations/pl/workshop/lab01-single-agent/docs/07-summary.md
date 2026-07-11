# Moduł 7 - Podsumowanie i dalsze kroki

⏱️ ~5 min

**Gratulacje!** Zbudowałeś, przetestowałeś i (jeśli na Ścieżce A) wdrożyłeś hostowanego agenta AI korzystając z Microsoft Foundry i Foundry Toolkit dla VS Code.

---

## Co zbudowałeś

Agenta **„Wyjaśnij jak dla dyrektora”** który:
- Otrzymuje techniczne raporty incydentów lub aktualizacje operacyjne przez HTTP (`POST /responses`)
- Tłumaczy je na zrozumiałe podsumowania dla zarządu
- Stosuje ustrukturyzowany format wyjściowy (Co się stało / Wpływ na biznes / Następny krok)
- Odrzuca zapytania niezwiązane z tematem oraz próby wstrzyknięcia poleceń
- Działa jako konteneryzowany hostowany agent w Microsoft Foundry Agent Service

---

## Kluczowe pojęcia, które poznałeś

| Pojęcie | Czego się nauczyłeś |
|---------|-------------------|
| **Architektura Agent Framework** | Potok `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Cykl życia hostowanego agenta** | Scaffold → Konfiguracja → Test lokalny → Wdrożenie → Weryfikacja w chmurze |
| **Inżynieria promptów systemowych** | Rola, odbiorcy, format wyjścia, zasady, ograniczenia bezpieczeństwa, przykłady |
| **Różnice lokalne vs. hostowane** | Tożsamość (poświadczenia osobiste vs. tożsamość zarządzana), punkt końcowy, ścieżka sieciowa |
| **Granice bezpieczeństwa** | Obrona przed wstrzyknięciem promptów, przestrzeganie roli, łagodne obsługiwanie przypadków granicznych |
| **Praca z Foundry Toolkit** | Tworzenie projektu, wdrażanie modelu, scaffoldowanie agenta, Agent Inspector, wdrożenie jednym kliknięciem |

---

## Co ukończyłeś

### Ścieżka A (subskrypcja Foundry)

- [x] Skonfigurowano Foundry Toolkit i utworzono projekt Foundry z wdrożonym modelem
- [x] Scaffoldowano hostowanego agenta ze strukturą projektu wygenerowaną automatycznie
- [x] Napisano ustrukturyzowane instrukcje agenta z zasadami bezpieczeństwa
- [x] Przetestowano lokalnie z 3 scenariuszami funkcyjnymi (Agent Inspector)
- [x] Wdrożono do Foundry Agent Service (konteneryzowany)
- [x] Zweryfikowano w chmurowym playground z 4 testami przypadków granicznych/bezpieczeństwa

### Ścieżka B (Foundry Local)

- [x] Skonfigurowano Foundry Toolkit z lokalnym punktem końcowym modelu
- [x] Scaffoldowano projekt hostowanego agenta
- [x] Napisano ustrukturyzowane instrukcje agenta z zasadami bezpieczeństwa
- [x] Przetestowano lokalnie z 3 scenariuszami funkcyjnymi
- [x] Zweryfikowano zachowanie agenta bez potrzeby zasobów chmurowych

---

## Kolejne kroki

### Kontynuuj naukę

| Źródło | Opis |
|----------|-------------|
| **[Lab 02 - Multi-Agent Orchestration](../../lab02-multi-agent/docs/README.md)** | Zbuduj przepływ pracy z 4 agentami (Resume → Job Fit Evaluator) z wzorcami orkiestracji |
| **[Dodaj narzędzia do swojego agenta](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Podłącz API, bazy danych lub funkcje niestandardowe przez Tool Catalog |
| **[Dodaj wiedzę (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Uzbroj agenta w dokumenty, magazyny wektorowe lub wyszukiwarkę Bing |
| **[Dokumentacja Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Pełna referencja platformy |
| **[Agent Framework SDK reference](https://learn.microsoft.com/agent-framework/)** | Dokumentacja API pakietu `agent-framework` |
| **[Foundry Toolkit - Co nowego](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Notatki o wydaniu rozszerzenia i changelog |

### Pomysły na rozszerzenie twojego agenta

- **Dodaj narzędzie daty** - Pozwól agentowi uwzględniać kontekst "na dziś" w podsumowaniach
- **Podłącz do bazy incydentów** - Pobieraj prawdziwe dane incydentów przez funkcję narzędzia
- **Dodaj narzędzie podstawienia Bing** - Pozwól agentowi wyszukiwać najnowsze wiadomości dla dodatkowego kontekstu
- **Wypróbuj różne modele** - Porównaj jakość wyjścia `gpt-4.1` vs. `gpt-4.1-mini`
- **Oceń z Foundry** - Użyj funkcji Ewaluacji do mierzenia jakości agenta na dużą skalę

### Dla użytkowników Ścieżki B: Aktualizacja do wdrożenia w chmurze

Kiedy będziesz gotowy do wdrożenia w chmurze:
1. Uzyskaj subskrypcję Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Ukończ [Moduł 01, Konfiguracja](01-setup.md#step-2-set-up-based-on-your-access) (utwórz projekt, wdroż model, przypisz RBAC)
3. Zaktualizuj swój `.env` z punktem końcowym projektu Foundry i nazwą wdrożenia modelu
4. Kontynuuj od [Moduł 05 - Wdrożenie do Foundry](05-deploy-to-foundry.md)

---

## Czyszczenie zasobów (opcjonalne)

Jeśli chcesz usunąć zasoby Azure utworzone podczas tego warsztatu:

### Opcja 1: Usuń grupę zasobów (usuwa wszystko)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opcja 2: Usuń tylko hostowanego agenta

1. Otwórz [ai.azure.com](https://ai.azure.com) → swój projekt → **Build** → **Agents**.
2. Kliknij swojego agenta → kliknij **Usuń**.

### Opcja 3: Usuń wdrożenie modelu

1. W panelu Foundry rozwiń swój projekt → **Models**.
2. Kliknij prawym przyciskiem wdrożenie modelu → **Usuń**.

> **Uwaga dotycząca kosztów:** Hostowani agenci generują koszty tylko podczas działania. Jeśli zatrzymasz lub usuniesz agenta, nie będzie dalszych opłat. Wdrożenie modelu może generować niewielką opłatę za zarezerwowaną pojemność - usuń je jeśli skończyłeś.

---

**Poprzedni:** [06 - Weryfikacja w Playground](06-verify-in-playground.md) · **Następny:** [08 - Rozwiązywanie problemów (referencja) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->