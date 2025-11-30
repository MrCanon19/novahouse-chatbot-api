# Dashboard & Statystyki

Panel admina posiada API do pobierania kluczowych statystyk:
- Liczba rozmów, wiadomości, leadów, rezerwacji
- Współczynnik konwersji
- Timeline (wykresy dzienne/tygodniowe/miesięczne)

Endpointy:
- `/api/widgets/metrics/summary` – podsumowanie statystyk
- `/api/widgets/metrics/timeline` – dane do wykresów

Możliwości rozbudowy:
- Szybkie akcje (np. eksport leadów, reset sesji, masowe anulowanie rezerwacji)
- Wykresy w panelu admina (np. Chart.js, Plotly)
- Alerty o przekroczeniu progów (np. spadek konwersji, wzrost błędów)

Aby dodać nowe widgety lub akcje, wystarczy dodać nowy endpoint w pliku `src/routes/dashboard_widgets.py` i podpiąć go w frontendzie panelu admina.

Szczegóły i przykłady w kodzie oraz dokumentacji API.
