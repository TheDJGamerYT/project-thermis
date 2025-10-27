# Project Thermis — Leit (°Lt) Scale

## Definition

* Absolute zero = 0 °Lt = −459.67 °F = 0 K
* Water freezes = 16 °Lt = 32 °F = 273.15 K
* Water boils ≈ 22.4700209 °Lt = 212 °F = 373.15 K

## Constants

```
F_PER_LT = 491.67 / 16 = 30.729375
K_PER_LT = 273.15 / 16 = 17.071875
```

## Conversions

**Leit ↔ Fahrenheit**

```
Lt = (F + 459.67) / 30.729375
F  = (Lt × 30.729375) − 459.67
```

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
