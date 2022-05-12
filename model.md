Zespół 13, 4-os.: Bartłomiej Krawczyk, Konrad Wojda, Mateusz Brzozowski, Mikołaj Kuranowski.

## Zbiory

- Warzywa: $ W := \lbrace ziemniak, kapusta, burak, marchew \rbrace $; $ w \in W $
- Farmy: $ F := \lbrace P1, P2, P3, P4, P5, P6 \rbrace $; $ f \in F $
- Magazyny: $ M := \lbrace M1, M2, M3 \rbrace $; $ m \in M $
- Sklepy: $ S := \lbrace S1, S2, S3, S4, S5, S6, S7, S8, S9, S10 \rbrace $; $ s \in S $
- Tygodnie: $ T := \lbrace 1, 2, ..., 51, 52 \rbrace $; $ t \in T $

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
\Large\min \normalsize
\Bigg(
    \bigg(
        \sum_{\substack{m \in M\\ f \in F}}
        \Big(
            \text{ODLEGŁOŚĆ\_FM}(f, m)
            \cdot
            \sum_{w \in W} \text{transport\_fm}(f, m, w)
        \Big)
    \bigg)
    \\\\
    + 
    \bigg(
        \sum_{\substack{m \in M\\ s \in S}}
        \Big(
            \text{ODLEGŁOŚĆ\_MS}(m, s)
            \cdot
            \sum_{\substack{w \in W \\ t \in T}} \text{transport\_ms}(m, s, t, w)
        \Big)
    \bigg)
\Bigg)
\cdot
\text{CENA\_TONO\_KILOMETRA}
$$

## Ograniczenia

### 1. W sklepie musi być tyle produktów, ile wynosi zapotrzebowanie + zapas

$$
\huge\forall \normalsize \substack{s \in S \\ t \in T \\ w \in W}:
\text{stan\_magazynu}(s, t, w) \ge (1+\text{ZAPAS\_PRODUKTÓW}) \cdot \text{ZAPOTRZEBOWANIE}(s, t, w)
$$

### 2. Magazyn przysklepowy nie jest przepełniony

$$
\huge\forall \normalsize \substack{s \in S \\ t \in T}:
\sum_{w \in W} \text{stan\_magazynu}(s, t, w)
\le \text{POJEMNOŚĆ\_MAGAZYNU\_SKLEPOWEGO}(s)
$$

### 3. Definicja zawartości magazynu

Przypadek 1 (brak resztek z poprzedniego tygodnia):
$$
\huge\forall \normalsize \substack{s \in S \\ w \in W}:
\text{stan\_magazynu}(s, 1, w) = \sum_{m \in M} \text{transport\_ms}(m, s, 1, w)
$$

Przypadek 2 (ogólny):
$$
\huge\forall \normalsize \substack{s \in S \\ w \in W \\ t \in T-\{1\}}:
\text{stan\_magazynu}(s, t, w) = \text{stan\_magazynu}(s, t-1, w)
    - \text{ZAPOTRZEBOWANIE}(s, t-1, w)
    + \sum_{m \in M} \text{transport\_ms}(m, s, t, w)
$$

### 4. Magazyn nie jest przepełniony

$$
\huge\forall \normalsize \substack{m \in M}:
\sum_{\substack{f \in F \\ w \in W}} \text{transport\_fm}(f, m ,w)
\le
\text{POJEMNOŚĆ\_MAGAZYNU}(m)
$$

### 5. Magazyn nie wysyła więcej niż ma zgromadzone

$$
\huge\forall \normalsize \substack{m \in M \\ w \in W}:
\sum_{\substack{s \in S \\ t \in T}} \text{transport\_ms}(m, s, t, w)
\le
\sum_{f \in F} \text{transport\_fm}(f, m, w)
$$

### 6. Farma nie wysyła więcej niż produkuje

$$
\huge\forall \normalsize \substack{f \in F \\ w \in W}:
\sum_{m \in M} \text{transport\_fm}(f, m, w)
\le
\text{PRODUKCJA\_FARMY}(f, w)
$$
