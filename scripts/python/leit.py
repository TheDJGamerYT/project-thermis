#!/usr/bin/env python3
"""
Leit Temperature Converter (°Lt) — v1.0

Anchors:
- 0 °Lt  == 0 K
- 16 °Lt == 273.15 K (water freezes)

Constant:
- 1 °Lt = 17.071875 K

Functions and a CLI to convert between Lt, K, C, F.

Usage examples:
  python leit.py convert --from lt --to c 16
  python leit.py convert --from c  --to lt 0
  python leit.py convert --from f  --to lt 212
  python leit.py auto  "16Lt"
  python leit.py auto  "100C"
  python leit.py auto  "-40F"
  python leit.py auto  "373.15K"
  python leit.py self-test
"""

from __future__ import annotations
import argparse
import re
import sys
from typing import Literal

# ---- Core constant ----
K_PER_LT: float = 273.15 / 16.0  # 17.071875
ABSOLUTE_ZERO_K: float = 0.0

Unit = Literal["lt", "k", "c", "f"]

# ---- Conversion primitives ----
def lt_to_k(lt: float) -> float:
    return lt * K_PER_LT

def k_to_lt(k: float) -> float:
    return k / K_PER_LT

def lt_to_c(lt: float) -> float:
    return lt_to_k(lt) - 273.15

def c_to_lt(c: float) -> float:
    return (c + 273.15) / K_PER_LT

def lt_to_f(lt: float) -> float:
    return (lt_to_c(lt) * 9.0 / 5.0) + 32.0

def f_to_lt(f: float) -> float:
    return ((f - 32.0) * 5.0 / 9.0 + 273.15) / K_PER_LT

def k_to_c(k: float) -> float:
    return k - 273.15

def c_to_k(c: float) -> float:
    return c + 273.15

def k_to_f(k: float) -> float:
    return (k_to_c(k) * 9.0 / 5.0) + 32.0

def f_to_k(f: float) -> float:
    return (f - 32.0) * 5.0 / 9.0 + 273.15

# ---- Generic converter ----
def convert(value: float, from_unit: Unit, to_unit: Unit) -> float:
    if from_unit == to_unit:
        return value

    # Normalize to Kelvin as hub, then to target
    if from_unit == "lt":
        k = lt_to_k(value)
    elif from_unit == "k":
        k = value
    elif from_unit == "c":
        k = c_to_k(value)
    elif from_unit == "f":
        k = f_to_k(value)
    else:
        raise ValueError(f"Unsupported 'from' unit: {from_unit}")

    if k < ABSOLUTE_ZERO_K - 1e-9:
        raise ValueError("Temperature below absolute zero is not defined.")

    if to_unit == "lt":
        return k_to_lt(k)
    elif to_unit == "k":
        return k
    elif to_unit == "c":
        return k_to_c(k)
    elif to_unit == "f":
        return k_to_f(k)
    else:
        raise ValueError(f"Unsupported 'to' unit: {to_unit}")

# ---- Parsing helpers ----
_UNIT_ALIASES = {
    "lt": "lt", "leit": "lt", "°lt": "lt",
    "k": "k", "kelvin": "k", "°k": "k",
    "c": "c", "celcius": "c", "celsius": "c", "°c": "c",
    "f": "f", "fahrenheit": "f", "°f": "f",
}

_VALUE_UNIT_RE = re.compile(
    r"^\s*([+-]?\d+(?:\.\d+)?)\s*([a-zA-Z°]+)\s*$"
)

def normalize_unit(u: str) -> Unit:
    key = u.strip().lower()
    if key not in _UNIT_ALIASES:
        raise ValueError(f"Unknown unit '{u}'. Use one of: lt, k, c, f.")
    return _UNIT_ALIASES[key]  # type: ignore[return-value]

def parse_value_with_unit(s: str) -> tuple[float, Unit]:
    m = _VALUE_UNIT_RE.match(s)
    if not m:
        raise ValueError("Provide value with unit, e.g. '16Lt', '0 C', '373.15K', '-40F'.")
    val = float(m.group(1))
    unit = normalize_unit(m.group(2))
    return val, unit

# ---- CLI ----
def cmd_convert(args: argparse.Namespace) -> int:
    from_u = normalize_unit(args.from_unit)
    to_u = normalize_unit(args.to_unit)
    try:
        value = float(args.value)
        out = convert(value, from_u, to_u)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(format_output(value, from_u, out, to_u, decimals=args.decimals))
    return 0

def cmd_auto(args: argparse.Namespace) -> int:
    try:
        val, u = parse_value_with_unit(args.input)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    targets: list[Unit] = ["lt", "k", "c", "f"]
    targets.remove(u)

    results = []
    for t in targets:
        try:
            results.append((t, convert(val, u, t)))
        except Exception as e:
            results.append((t, f"Error: {e}"))

    print(f"Input: {val} {u.upper()}")
    for t, v in results:
        if isinstance(v, float):
            print(f"  → {round(v, args.decimals)} {t.upper()}")
        else:
            print(f"  → {v} ({t.upper()})")
    return 0

def cmd_self_test(_: argparse.Namespace) -> int:
    def approx(a, b, eps=1e-9):
        return abs(a - b) < eps

    # Core anchors
    assert approx(lt_to_k(16.0), 273.15)
    assert approx(k_to_lt(273.15), 16.0)

    # Water boiling ~21.8575874062 Lt
    assert approx(k_to_lt(373.15), 373.15 / K_PER_LT)

    # Cross-unit round trips
    for val in [0.0, 16.0, 21.8575874]:
        assert approx(convert(convert(val, "lt", "k"), "k", "lt"), val)

    for c in [-40, 0, 100]:
        assert approx(convert(convert(c, "c", "lt"), "lt", "c"), c)

    for f in [-40, 32, 212]:
        assert approx(convert(convert(f, "f", "lt"), "lt", "f"), f)

    print("All self-tests passed.")
    return 0

def format_output(inp_val: float, from_u: Unit, out_val: float, to_u: Unit, decimals: int = 2) -> str:
    return f"{round(inp_val, decimals)} {from_u.upper()} = {round(out_val, decimals)} {to_u.upper()}"

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Leit (°Lt) temperature converter.")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_conv = sub.add_parser("convert", help="Convert between units with explicit --from/--to.")
    p_conv.add_argument("--from", dest="from_unit", required=True, help="Source unit: lt|k|c|f")
    p_conv.add_argument("--to", dest="to_unit", required=True, help="Target unit: lt|k|c|f")
    p_conv.add_argument("value", help="Numeric value to convert.")
    p_conv.add_argument("--decimals", type=int, default=2, help="Decimal places for printout.")
    p_conv.set_defaults(func=cmd_convert)

    p_auto = sub.add_parser("auto", help="Auto-detect from a value+unit string (e.g., '16Lt', '0 C').")
    p_auto.add_argument("input", help="Value with unit, e.g., '16Lt', '0 C', '373.15K', '-40F'.")
    p_auto.add_argument("--decimals", type=int, default=2, help="Decimal places for printout.")
    p_auto.set_defaults(func=cmd_auto)

    p_test = sub.add_parser("self-test", help="Run internal sanity checks.")
    p_test.set_defaults(func=cmd_self_test)

    return p

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
