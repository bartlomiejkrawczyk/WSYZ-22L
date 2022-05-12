## Zbiory

- $ WARZYWA \coloneqq \{ ziemniak, kapusta, burak, marchew \} $  
    $ w \in WARZYWA $
- $ FARMY \coloneqq \{ P1, P2, P3, P4, P5, P6 \} $  
    $ f \in FARMY $
- $ MAGAZYNY \coloneqq \{ M1, M2, M3 \} $  
    $ m \in MAGAZYNY $
- $ SKLEPY \coloneqq \{ S1, S2, S3, S4, S5, S6, S7, S8, S9, S10 \} $  
    $ s \in SKLEPY $
- $ TYGODNIE \coloneqq \{ 1, 2, ..., 51, 52 \} $  
    $ t \in TYGODNIE $

## Parametry

- $ \text{ZAPOTRZEBOWANIE}(s, t, w) $  
- $ \text{POJEMNOŚĆ\_MAGAZYNU\_SKLEPOWEGO}(s) $  
- $ \text{POJEMNOŚĆ\_MAGAZYNU}(m) $  
- $ \text{PRODUKCJA\_FARMY}(f, w) $  
- $ \text{ODLEGŁOŚĆ\_FM}(f, m) $  
- $ \text{ODLEGŁOŚĆ\_MS}(m, s) $  
- $ \text{CENA\_TONO\_KILOMETRA} \ge 0 $
- $ \text{ZAPAS\_PRODUKTÓW} \ge 0 $

## Zmienne decyzyjne

- $ \text{transport\_fm}(f, m, w) $
- $ \text{transport\_ms}(m, s, t, w) $
- $ \text{stan\_magazynu}(s, t, w) $

## Kryterium

$$
\min \left(
    \text{CENA\_TONO\_KILOMETRA}
    \cdot
    \Bigg(
        \sum_{\substack{m \in MAGAZYNY\\ f \in FARMY}}
        \bigg(
            \text{ODLEGŁOŚĆ\_FM}(f, m)
            \cdot
            \sum_{w \in WARZYWA} \text{transport\_fm}(f, m, w)
        \bigg)
    \Bigg)
    + 
    \Bigg(
        \sum_{\substack{m \in MAGAZYNY\\ s \in SKLEPY}}
        \bigg(
            \text{ODLEGŁOŚĆ\_MS}(m, s)
            \cdot
            \sum_{\substack{w \in WARZYWA \\ t \in TYGODNIE}} \text{transport\_ms}(m, s, t, w)
        \bigg)
    \Bigg)
\right)
$$

## Ograniczenia

### 1. W sklepie musi być tyle produktów, ile wynosi zapotrzebowanie + zapas

$$
\huge\forall \normalsize \substack{s \in SKLEPY \\ t \in TYGODNIE \\ w \in WARZYWA}:
\text{stan\_magazynu}(s, t, w) \ge (1+\text{ZAPAS\_PRODUKTÓW}) \cdot ZAPOTRZEBOWANIE(s, t, w)
$$

### 2. Magazyn przysklepowy nie jest przepełniony

$$
\huge\forall \normalsize \substack{s \in SKLEPY \\ t \in TYGODNIE}:
\sum_{w \in WARZYWA} \text{stan\_magazynu}(s, t, w)
\le \text{POJEMNOŚĆ\_MAGAZYNU\_SKLEPOWEGO}(s)
$$

### 3. Definicja zawartości magazynu

Przypadek 1 (brak resztek z poprzedniego tygodnia):
$$
\huge\forall \normalsize \substack{s \in SKLEPY \\ w \in WARZYWA}:
\text{stan\_magazynu}(s, 1, w) = \sum_{m \in MAGAZYNY} \text{transport\_ms}(m, s, 1, w)
$$

Przypadek 2 (ogólny):
$$
\huge\forall \normalsize \substack{s \in SKLEPY \\ w \in WARZYWA \\ t \in TYGODNIE-\{1\}}:
\text{stan\_magazynu}(s, t, w) = \text{stan\_magazynu}(s, t-1, w)
    - ZAPOTRZEBOWANIE(s, t-1, w)
    + \sum_{m \in MAGAZYNY} \text{transport\_ms}(m, s, t, w)
$$

### 4. Magazyn nie jest przepełniony

$$
\huge\forall \normalsize \substack{m \in MAGAZYNY}:
\sum_{\substack{f \in FARMY \\ w \in WARZYWA}} \text{transport\_fm}(f, m ,w)
\le
\text{POJEMNOŚĆ\_MAGAZYNU}(m)
$$

### 5. Magazyn nie wysyła więcej niż ma zgromadzone

$$
\huge\forall \normalsize \substack{m \in MAGAZYNY \\ w \in WARZYWA}:
\sum_{\substack{s \in SKLEPY \\ t \in TYGODNIE}} \text{transport\_ms}(m, s, t, w)
\le
\sum_{f \in FARMY} \text{transport\_fm}(f, m, w)
$$

### 6. Farma nie wysyła więcej niż produkuje

$$
\huge\forall \normalsize \substack{f \in FARMY \\ w \in WARZYWA}:
\sum_{m \in MAGAZYNY} \text{transport\_fm}(f, m, w)
\le
\text{PRODUKCJA\_FARMY}(f, w)
$$
