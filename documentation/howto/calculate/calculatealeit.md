# Project Thermis — Leit (°Lt) Scale

## Definition

* Absolute zero = 0 °Lt = 0 K
* Water freezes = 16 °Lt = 273.15 K
* Water boils ≈ 21.8575874062 °Lt = 373.15 K

## Constant

```
K_PER_LT = 273.15 / 16 = 17.071875
```

## Conversions

**Leit ↔ Kelvin**

```
K  = Lt × 17.071875
Lt = K  ÷ 17.071875
```

**Leit ↔ Celsius**

```
C  = (Lt × 17.071875) − 273.15
Lt = (C + 273.15) ÷ 17.071875
```

**Leit ↔ Fahrenheit**

```
F  = ((Lt × 17.071875) − 273.15) × 9/5 + 32
Lt = (((F − 32) × 5/9) + 273.15) ÷ 17.071875
```
