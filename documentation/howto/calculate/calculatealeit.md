# Project Thermis — Leit (°Lt) Scale

## Definition

* Water freezes = −10 °Lt = 32 °F = 273.15 K
* Water boils = 116 °Lt = 212 °F = 373.15 K
* Absolute zero = −(459.67 ÷ 1.428571) + 46.28571 = −276.69 °Lt ≈ 0 K

## Constants

```
F_PER_LT = 180 / 126 = 1.428571
OFFSET_F = 46.28571
```

## Conversions

**Leit ↔ Fahrenheit**

```
F  = (1.428571 × Lt) + 46.28571
Lt = (F − 46.28571) ÷ 1.428571
```

**Leit ↔ Kelvin**

```
K  = ((1.428571 × Lt) + 46.28571 − 32) × 5/9 + 273.15
Lt = (((K − 273.15) × 9/5 + 32) − 46.28571) ÷ 1.428571
```

**Leit ↔ Celsius**

```
C  = ((1.428571 × Lt) + 46.28571 − 32) × 5/9
Lt = (((C × 9/5) + 32 − 46.28571) ÷ 1.428571)
```
