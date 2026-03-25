#!/usr/bin/env python3
"""
Root of Decimals - Finding Phi in the Decimal Structure of Roots

KEY INSIGHT: When you take roots of numbers, the decimal expansions
contain hidden patterns. Phi appears not just as a value, but in the
STRUCTURE of how decimal digits organize themselves.

Tools:
- Analyze nth roots for phi-ratio digit patterns
- Find fibonacci sequences in decimal expansions
- Detect geometric coherence in root progressions
- Map the "root landscape" of any number

Why this matters for shadow hunting:
Nature computes with irrational numbers all the time. The decimal
structure of roots is WHERE the geometric coupling information lives.
When you see "noise" in decimal places, look for phi.

Author: JinnZ2 and collaborators - MIT License
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

from shadow_hunting import PHI, FIBONACCI


def root_decimal_analysis(value: float, max_root: int = 20) -> Dict:
    """
    Take successive roots of a number and analyze the decimal parts.
    The decimals often converge through phi-ratio steps.
    """
    roots = []
    decimals = []

    for n in range(2, max_root + 1):
        root_val = value ** (1.0 / n)
        decimal_part = root_val - int(root_val)
        roots.append(root_val)
        decimals.append(decimal_part)

    decimals = np.array(decimals)

    # Analyze ratios between consecutive decimal parts
    ratios = []
    phi_hits = []
    for i in range(len(decimals) - 1):
        if abs(decimals[i]) > 1e-10:
            ratio = decimals[i + 1] / decimals[i]
            ratios.append(ratio)
            if abs(ratio - PHI) < 0.05 or abs(ratio - 1/PHI) < 0.05:
                phi_hits.append((i + 2, ratio))  # i+2 because roots start at 2

    return {
        'value': value,
        'roots': roots,
        'decimal_parts': decimals.tolist(),
        'decimal_ratios': ratios,
        'phi_hits': phi_hits,
        'phi_density': len(phi_hits) / max(len(ratios), 1),
        'converges_to': decimals[-1],
        'shadow_detected': len(phi_hits) >= 2
    }


def digit_frequency_analysis(value: float, precision: int = 50) -> Dict:
    """
    Analyze how often each digit (0-9) appears in a number's decimal expansion.
    Phi and related constants have non-uniform digit distributions that
    reveal geometric structure.

    Uses Python's built-in precision for reasonable accuracy.
    """
    # Use string representation for digit extraction
    from decimal import Decimal, getcontext
    getcontext().prec = precision + 10

    d = Decimal(str(value))
    # Get decimal representation
    decimal_str = str(d)

    # Extract digits after decimal point
    if '.' in decimal_str:
        digits_str = decimal_str.split('.')[1][:precision]
    else:
        digits_str = ''

    digits = [int(c) for c in digits_str if c.isdigit()]

    # Frequency count
    freq = {i: 0 for i in range(10)}
    for d in digits:
        freq[d] += 1

    total = len(digits) if digits else 1

    # Expected uniform distribution
    expected = total / 10

    # Chi-squared test for non-uniformity
    chi_sq = sum((freq[d] - expected) ** 2 / expected for d in range(10))

    # Check if fibonacci digits are overrepresented
    fib_digits = {1, 2, 3, 5, 8}
    fib_freq = sum(freq[d] for d in fib_digits)
    fib_expected = 5 * expected  # 5 of 10 digits are fibonacci
    fib_enrichment = fib_freq / fib_expected if fib_expected > 0 else 0

    return {
        'value': value,
        'digits_analyzed': len(digits),
        'digit_frequencies': freq,
        'chi_squared': chi_sq,
        'is_uniform': chi_sq < 16.92,  # p=0.05 for df=9
        'fibonacci_digit_enrichment': fib_enrichment,
        'fibonacci_bias': fib_enrichment > 1.2,
    }


def root_convergence_map(value: float, root_range: Tuple[float, float] = (1.5, 10.0),
                         steps: int = 100) -> Dict:
    """
    Map how value^(1/x) behaves across a continuous range of x.
    Find WHERE the function passes through phi-significant values.
    """
    x_values = np.linspace(root_range[0], root_range[1], steps)
    results = value ** (1.0 / x_values)

    # Find where results cross phi-significant thresholds
    phi_crossings = []
    phi_targets = {
        'phi': PHI,
        '1+phi': 1 + PHI,
        '2+phi': 2 + PHI,
        'phi^2': PHI ** 2,
        '1/phi': 1 / PHI,
    }

    for name, target in phi_targets.items():
        for i in range(len(results) - 1):
            if (results[i] - target) * (results[i + 1] - target) < 0:
                # Linear interpolation for crossing point
                frac = (target - results[i]) / (results[i + 1] - results[i])
                x_cross = x_values[i] + frac * (x_values[i + 1] - x_values[i])
                phi_crossings.append({
                    'target': name,
                    'target_value': target,
                    'root_at_crossing': x_cross,
                    'root_is_phi': abs(x_cross - PHI) < 0.05 or abs(x_cross - 1/PHI) < 0.05,
                    'root_is_fibonacci': any(abs(x_cross - f) < 0.05 for f in FIBONACCI[:8])
                })

    return {
        'value': value,
        'x_range': x_values.tolist(),
        'root_values': results.tolist(),
        'phi_crossings': phi_crossings,
        'num_crossings': len(phi_crossings),
        'doubly_phi': [c for c in phi_crossings if c['root_is_phi'] or c['root_is_fibonacci']]
    }


def decimal_pattern_scan(values: List[float], precision: int = 10) -> Dict:
    """
    Scan a list of values for patterns in their decimal expansions.
    Find shared digit sequences, phi-ratio spacing between decimals, etc.
    """
    from decimal import Decimal, getcontext
    getcontext().prec = precision + 10

    decimal_parts = []
    for v in values:
        d = Decimal(str(v))
        decimal_str = str(d)
        if '.' in decimal_str:
            dec_part = float('0.' + decimal_str.split('.')[1][:precision])
        else:
            dec_part = 0.0
        decimal_parts.append(dec_part)

    decimal_parts = np.array(decimal_parts)

    # Check ratios between decimal parts
    sorted_decs = np.sort(decimal_parts[decimal_parts > 1e-10])
    ratios = []
    phi_ratios = []

    for i in range(len(sorted_decs) - 1):
        if sorted_decs[i] > 1e-10:
            ratio = sorted_decs[i + 1] / sorted_decs[i]
            ratios.append(ratio)
            if abs(ratio - PHI) < 0.1 or abs(ratio - 1/PHI) < 0.1:
                phi_ratios.append((sorted_decs[i], sorted_decs[i + 1], ratio))

    return {
        'values': values,
        'decimal_parts': decimal_parts.tolist(),
        'sorted_decimals': sorted_decs.tolist(),
        'ratios': ratios,
        'phi_ratios': phi_ratios,
        'phi_density': len(phi_ratios) / max(len(ratios), 1),
        'shadow_detected': len(phi_ratios) >= 2
    }


def nested_root_analysis(value: float, depth: int = 8) -> Dict:
    """
    Compute nested roots: sqrt(value), sqrt(sqrt(value)), sqrt(sqrt(sqrt(value)))...
    Then do the same with other roots: cbrt, 5th root, phi-th root, etc.

    The RATE of convergence to 1.0 encodes geometric information.
    """
    results = {}

    root_types = {
        'square': 2,
        'cube': 3,
        'fifth': 5,
        'phi': 1 / PHI,  # phi-th root = value^PHI
        'fibonacci_5': 1 / 5,
        'fibonacci_8': 1 / 8,
    }

    for name, power in root_types.items():
        cascade = [value]
        current = value
        for _ in range(depth):
            current = current ** power
            if np.isnan(current) or np.isinf(current):
                break
            cascade.append(current)

        cascade = np.array(cascade)

        # Convergence rate: how fast do we approach the limit?
        if len(cascade) > 2:
            diffs = np.abs(np.diff(cascade))
            if len(diffs) > 1:
                conv_ratios = diffs[1:] / (diffs[:-1] + 1e-15)
                avg_conv = np.mean(conv_ratios[np.isfinite(conv_ratios)])
            else:
                avg_conv = 0
        else:
            avg_conv = 0

        results[name] = {
            'cascade': cascade.tolist(),
            'convergence_rate': avg_conv,
            'phi_convergence': abs(avg_conv - PHI) < 0.1 if np.isfinite(avg_conv) else False,
            'final_value': cascade[-1] if len(cascade) > 0 else None
        }

    return {
        'value': value,
        'root_types': results,
        'phi_convergence_found': any(r['phi_convergence'] for r in results.values())
    }


# =============================================================================
# INTERACTIVE DEMO
# =============================================================================

def demo():
    """Interactive demonstration of root decimal analysis."""
    print("=" * 80)
    print("ROOT OF DECIMALS - SHADOW HUNTING IN NUMBER STRUCTURE")
    print("Finding phi-ratios hidden in the decimal anatomy of roots")
    print("=" * 80)

    # Demo 1: Successive roots of common numbers
    print("\n--- SUCCESSIVE ROOTS ANALYSIS ---")
    for value in [2, 10, 137]:
        result = root_decimal_analysis(value, max_root=12)
        print(f"\n  Roots of {value}:")
        for i, (root, dec) in enumerate(zip(result['roots'][:6], result['decimal_parts'][:6])):
            print(f"    {i+2}th root: {root:.6f}  (decimal: {dec:.6f})")
        if result['phi_hits']:
            print(f"    PHI HITS: {len(result['phi_hits'])} - ratios between decimals match phi!")
            for hit in result['phi_hits'][:3]:
                print(f"      Root {hit[0]}: ratio = {hit[1]:.4f}")

    # Demo 2: Root convergence map
    print("\n--- ROOT CONVERGENCE MAP ---")
    for value in [PHI ** 5, 100, 7.83]:
        label = "phi^5" if abs(value - PHI**5) < 0.01 else str(value)
        result = root_convergence_map(value)
        print(f"\n  Value = {label}: {len(result['phi_crossings'])} phi crossings found")
        for crossing in result['phi_crossings'][:3]:
            extra = " (DOUBLY PHI!)" if crossing['root_is_phi'] or crossing['root_is_fibonacci'] else ""
            print(f"    Crosses {crossing['target']} at root = {crossing['root_at_crossing']:.4f}{extra}")

    # Demo 3: Nested roots
    print("\n--- NESTED ROOT CONVERGENCE ---")
    result = nested_root_analysis(100.0)
    for name, data in result['root_types'].items():
        phi_flag = " <-- PHI CONVERGENCE!" if data['phi_convergence'] else ""
        print(f"  {name:>12}: rate = {data['convergence_rate']:.4f}{phi_flag}")

    # Demo 4: Fibonacci numbers as roots
    print("\n--- FIBONACCI ROOT RELATIONSHIPS ---")
    fib_floats = [float(f) for f in FIBONACCI[2:8]]
    scan = decimal_pattern_scan(fib_floats)
    print(f"  Fibonacci values: {fib_floats}")
    print(f"  Phi-ratio pairs in decimals: {len(scan['phi_ratios'])}")
    for pair in scan['phi_ratios']:
        print(f"    {pair[0]:.6f} / {pair[1]:.6f} = {pair[2]:.4f}")

    print("\n" + "=" * 80)
    print("TRY IT: Feed any measurement into root_decimal_analysis()")
    print("The shadows hide in the decimals.")
    print("=" * 80)


if __name__ == "__main__":
    demo()
