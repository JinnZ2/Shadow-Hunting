#!/usr/bin/env python3
"""
Reverse Method of Powers and Roots
Explore how phi-ratios hide in power and root relationships

KEY INSIGHT: The golden ratio is the ONLY number where phi^2 = phi + 1
and 1/phi = phi - 1. This self-referential property means phi shows up
in power/root cascades across all scales.

Tools:
- Reverse-engineer what power/root relationships connect two numbers
- Detect phi signatures in power sequences
- Find hidden golden spirals in exponential data
- Analyze power-law distributions for geometric coupling

Author: JinnZ2 and collaborators - MIT License
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

from shadow_hunting import PHI, FIBONACCI


def reverse_power(result: float, base: float, tolerance: float = 0.01) -> Dict:
    """
    Given a result and base, find what power connects them.
    Checks if the power itself has phi-ratio significance.

    Example: reverse_power(8, 2) -> power=3.0 (fibonacci!)
    """
    if base <= 0 or base == 1 or result <= 0:
        return {'power': None, 'phi_significant': False, 'error': 'Invalid input'}

    power = np.log(result) / np.log(base)

    # Check if power is phi-related
    phi_related = False
    phi_match = None

    phi_values = {
        'phi': PHI,
        '1/phi': 1 / PHI,
        'phi^2': PHI ** 2,
        'phi^3': PHI ** 3,
        '2*phi': 2 * PHI,
        '1 + phi': 1 + PHI,
    }

    for name, val in phi_values.items():
        if abs(power - val) < tolerance:
            phi_related = True
            phi_match = name
            break

    # Check if power is a fibonacci number
    fib_match = None
    for fib in FIBONACCI:
        if abs(power - fib) < tolerance:
            fib_match = fib
            break

    return {
        'base': base,
        'result': result,
        'power': power,
        'phi_significant': phi_related,
        'phi_match': phi_match,
        'fibonacci_match': fib_match,
        'interpretation': _interpret_power(power, phi_related, fib_match)
    }


def reverse_root(result: float, value: float, tolerance: float = 0.01) -> Dict:
    """
    Given a value and its root result, find what root was taken.
    value^(1/n) = result  =>  n = log(value) / log(result)

    Example: reverse_root(3, 27) -> root=3 (fibonacci!)
    """
    if result <= 0 or result == 1 or value <= 0:
        return {'root': None, 'phi_significant': False, 'error': 'Invalid input'}

    root = np.log(value) / np.log(result)

    # Check phi relationships
    phi_related = False
    phi_match = None

    for name, val in {'phi': PHI, '1/phi': 1/PHI, 'phi^2': PHI**2}.items():
        if abs(root - val) < tolerance:
            phi_related = True
            phi_match = name
            break

    fib_match = None
    for fib in FIBONACCI:
        if abs(root - fib) < tolerance:
            fib_match = fib
            break

    return {
        'value': value,
        'result': result,
        'root': root,
        'phi_significant': phi_related,
        'phi_match': phi_match,
        'fibonacci_match': fib_match,
    }


def power_cascade(start: float, power: float, steps: int = 10) -> Dict:
    """
    Generate a cascade: start, start^power, (start^power)^power, ...
    Then analyze the cascade for phi-ratio patterns.

    The magic: cascading by phi creates self-similar patterns.
    """
    cascade = [start]
    current = start
    for _ in range(steps - 1):
        current = current ** power
        if np.isinf(current) or np.isnan(current) or current > 1e100:
            break
        cascade.append(current)

    cascade = np.array(cascade)

    # Analyze ratios between consecutive elements
    ratios = []
    phi_matches = []
    for i in range(len(cascade) - 1):
        if abs(cascade[i]) > 1e-10:
            ratio = cascade[i + 1] / cascade[i]
            ratios.append(ratio)
            if abs(ratio - PHI) < 0.05 or abs(ratio - 1/PHI) < 0.05:
                phi_matches.append((i, ratio))

    return {
        'cascade': cascade.tolist(),
        'power': power,
        'ratios': ratios,
        'phi_matches': phi_matches,
        'phi_density': len(phi_matches) / max(len(ratios), 1),
        'is_phi_cascade': abs(power - PHI) < 0.01 or abs(power - 1/PHI) < 0.01
    }


def root_cascade(start: float, root: float, steps: int = 10) -> Dict:
    """
    Generate: start, start^(1/root), (start^(1/root))^(1/root), ...
    Successive roots converge - but WHERE they converge reveals structure.
    """
    cascade = [start]
    current = start
    for _ in range(steps - 1):
        if current <= 0:
            break
        current = current ** (1.0 / root)
        cascade.append(current)

    cascade = np.array(cascade)

    # All root cascades converge to 1.0, but the PATH reveals phi
    convergence_ratios = []
    for i in range(len(cascade) - 1):
        deviation_now = abs(cascade[i] - 1.0)
        deviation_next = abs(cascade[i + 1] - 1.0)
        if deviation_now > 1e-10:
            convergence_ratios.append(deviation_next / deviation_now)

    # Check if convergence rate is phi-related
    avg_convergence = np.mean(convergence_ratios) if convergence_ratios else 0
    phi_convergence = abs(avg_convergence - PHI) < 0.05 or abs(avg_convergence - 1/PHI) < 0.05

    return {
        'cascade': cascade.tolist(),
        'root': root,
        'convergence_ratios': convergence_ratios,
        'avg_convergence_rate': avg_convergence,
        'phi_convergence': phi_convergence,
        'converges_to': cascade[-1]
    }


def scan_power_relationships(values: List[float],
                             tolerance: float = 0.05) -> Dict:
    """
    Given a set of values, find ALL power/root relationships between them
    and flag those that involve phi or fibonacci numbers.

    This is the "reverse method" - start from measurements, find hidden structure.
    """
    relationships = []
    phi_relationships = []

    for i, a in enumerate(values):
        for j, b in enumerate(values):
            if i == j or a <= 0 or b <= 0 or a == 1:
                continue

            # What power connects a to b? (a^power = b)
            power = np.log(b) / np.log(a)

            # Check phi significance
            phi_sig = False
            for name, val in [('phi', PHI), ('1/phi', 1/PHI), ('phi^2', PHI**2)]:
                if abs(power - val) < tolerance:
                    phi_sig = True
                    rel = {
                        'a': a, 'b': b,
                        'relationship': f'{a}^{name} ≈ {b}',
                        'power': power,
                        'phi_type': name,
                        'error': abs(power - val)
                    }
                    phi_relationships.append(rel)
                    break

            # Check fibonacci
            for fib in FIBONACCI[:8]:
                if abs(power - fib) < tolerance:
                    rel = {
                        'a': a, 'b': b,
                        'relationship': f'{a}^{fib} ≈ {b}',
                        'power': power,
                        'fib_value': fib,
                        'error': abs(power - fib)
                    }
                    relationships.append(rel)
                    break

    return {
        'phi_relationships': phi_relationships,
        'fibonacci_relationships': relationships,
        'total_phi': len(phi_relationships),
        'total_fibonacci': len(relationships),
        'shadow_detected': len(phi_relationships) > 0
    }


def analyze_power_spectrum(data: np.ndarray) -> Dict:
    """
    Analyze a dataset's power-law behavior and find where phi hides.

    Many natural phenomena follow power laws. The EXPONENT often encodes
    geometric coupling - and phi shows up in the exponent.
    """
    if len(data) < 3:
        return {'error': 'Need at least 3 data points'}

    data_sorted = np.sort(data[data > 0])[::-1]

    # Rank-size analysis (Zipf-like)
    ranks = np.arange(1, len(data_sorted) + 1, dtype=float)

    # Fit power law: data ~ rank^(-alpha)
    log_ranks = np.log(ranks)
    log_data = np.log(data_sorted)

    coeffs = np.polyfit(log_ranks, log_data, 1)
    alpha = -coeffs[0]  # Power law exponent

    # Check if alpha is phi-related
    phi_exponent = False
    phi_match = None
    for name, val in [('phi', PHI), ('1/phi', 1/PHI), ('phi+1', PHI+1), ('2*phi', 2*PHI)]:
        if abs(alpha - val) < 0.05:
            phi_exponent = True
            phi_match = name
            break

    # R-squared for fit quality
    predicted = np.polyval(coeffs, log_ranks)
    ss_res = np.sum((log_data - predicted) ** 2)
    ss_tot = np.sum((log_data - np.mean(log_data)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return {
        'power_law_exponent': alpha,
        'r_squared': r_squared,
        'is_power_law': r_squared > 0.9,
        'phi_exponent': phi_exponent,
        'phi_match': phi_match,
        'interpretation': (
            f"Power law with exponent {alpha:.3f}"
            + (f" ≈ {phi_match} (SHADOW FOUND!)" if phi_exponent else "")
        )
    }


def _interpret_power(power: float, phi_related: bool, fib_match) -> str:
    """Generate human-readable interpretation of a power relationship."""
    parts = [f"Power = {power:.4f}"]
    if phi_related:
        parts.append("PHI-RELATED - geometric coupling signature!")
    if fib_match:
        parts.append(f"Fibonacci number ({fib_match}) - biological growth pattern!")
    if not phi_related and not fib_match:
        parts.append("No immediate phi/fibonacci connection")
    return " | ".join(parts)


# =============================================================================
# INTERACTIVE DEMO
# =============================================================================

def demo():
    """Interactive demonstration of power/root shadow hunting."""
    print("=" * 80)
    print("REVERSE METHOD OF POWERS AND ROOTS")
    print("Finding phi-ratios hidden in exponential relationships")
    print("=" * 80)

    # Demo 1: The golden ratio's unique property
    print("\n--- PHI'S UNIQUE POWER PROPERTY ---")
    print(f"phi = {PHI:.6f}")
    print(f"phi^2 = {PHI**2:.6f}  =  phi + 1? {abs(PHI**2 - (PHI + 1)) < 1e-10}")
    print(f"1/phi = {1/PHI:.6f}  =  phi - 1? Actually 1/phi = phi + 1 = {1/PHI:.6f}")

    # Demo 2: Power cascade with phi
    print("\n--- PHI POWER CASCADE ---")
    result = power_cascade(2.0, PHI, steps=8)
    print(f"Starting at 2, raising to phi each step:")
    for i, val in enumerate(result['cascade']):
        print(f"  Step {i}: {val:.6f}")
    print(f"  Phi matches in ratios: {len(result['phi_matches'])}")

    # Demo 3: Root cascade convergence
    print("\n--- ROOT CASCADE CONVERGENCE ---")
    for root_val in [2, PHI, 1/PHI, 3]:
        result = root_cascade(100.0, root_val, steps=8)
        label = f"phi ({root_val:.3f})" if abs(root_val - PHI) < 0.01 else f"{root_val:.3f}"
        print(f"  Root={label}: converges at rate {result['avg_convergence_rate']:.4f}"
              f" {'<-- PHI!' if result['phi_convergence'] else ''}")

    # Demo 4: Scan real-world values
    print("\n--- SCANNING NATURE'S NUMBERS ---")
    nature_values = [
        1.0, 1.618, 2.618, 4.236,  # Phi sequence
        7.83,                        # Schumann resonance Hz
        13.0, 21.0, 34.0,           # Fibonacci
        137.5,                       # Golden angle (degrees)
        273.15,                      # 0 Celsius in Kelvin
    ]
    scan = scan_power_relationships(nature_values)
    print(f"  Found {scan['total_phi']} phi relationships:")
    for rel in scan['phi_relationships'][:5]:
        print(f"    {rel['relationship']}  (error: {rel['error']:.4f})")
    print(f"  Found {scan['total_fibonacci']} fibonacci relationships")

    # Demo 5: Power spectrum of fibonacci
    print("\n--- FIBONACCI POWER SPECTRUM ---")
    fib_data = np.array(FIBONACCI, dtype=float)
    spectrum = analyze_power_spectrum(fib_data)
    print(f"  Exponent: {spectrum['power_law_exponent']:.4f}")
    print(f"  R-squared: {spectrum['r_squared']:.4f}")
    print(f"  {spectrum['interpretation']}")

    print("\n" + "=" * 80)
    print("TRY IT: Feed your own data into scan_power_relationships()")
    print("The shadows hide in the exponents.")
    print("=" * 80)


if __name__ == "__main__":
    demo()
