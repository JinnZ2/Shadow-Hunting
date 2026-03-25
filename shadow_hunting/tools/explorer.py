#!/usr/bin/env python3
"""
Shadow Hunting Explorer - Interactive Tool for Finding Hidden Patterns

This is the entry point for exploring your own data. Feed it numbers,
measurements, coordinates, or time series and it will hunt for shadows:
phi-ratios, fibonacci sequences, geometric coherence, power-law signatures,
chord relationships, and field coupling.

Usage:
    python -m shadow_hunting.tools.explorer

Or in code:
    from shadow_hunting.tools.explorer import hunt_shadows
    results = hunt_shadows(your_data)

Author: JinnZ2 and collaborators - MIT License
"""

import numpy as np
from typing import Dict, List, Union

from shadow_hunting import PHI, FIBONACCI
from shadow_hunting.shadow_data_mining import (
    detect_phi_ratios,
    detect_fibonacci_sequences,
    detect_geometric_coherence,
)
from shadow_hunting.tools.powers_and_roots import (
    scan_power_relationships,
    analyze_power_spectrum,
    power_cascade,
)
from shadow_hunting.tools.root_decimals import (
    root_decimal_analysis,
    decimal_pattern_scan,
)
from shadow_hunting.tools.chordal_dimensions import (
    analyze_chord_spectrum,
    polygon_chord_analysis,
)


def hunt_shadows(data: Union[List[float], np.ndarray],
                 verbose: bool = True) -> Dict:
    """
    Run the full shadow hunting suite on any dataset.

    Pass in any list of numbers - measurements, time series, spatial data,
    frequencies, voltages, distances, prices, anything.

    Returns a comprehensive report of all detected shadows.
    """
    data = np.array(data, dtype=float)

    if verbose:
        print("=" * 80)
        print("SHADOW HUNTER - COMPREHENSIVE PATTERN ANALYSIS")
        print(f"Analyzing {len(data)} values...")
        print("=" * 80)

    results = {}

    # 1. Phi-ratio detection
    if verbose:
        print("\n[1/6] Scanning for phi-ratio patterns...")
    phi_result = detect_phi_ratios(data)
    results['phi_ratios'] = phi_result
    if verbose:
        _print_phi_results(phi_result)

    # 2. Fibonacci sequences
    if verbose:
        print("\n[2/6] Scanning for fibonacci sequences...")
    if np.all(data > 0):
        fib_result = detect_fibonacci_sequences(data)
        results['fibonacci'] = fib_result
        if verbose:
            _print_fib_results(fib_result)
    else:
        results['fibonacci'] = {'skipped': 'Contains non-positive values'}
        if verbose:
            print("  Skipped (contains non-positive values)")

    # 3. Geometric coherence
    if verbose:
        print("\n[3/6] Measuring geometric coherence...")
    if np.all(data > 0):
        coherence_result = detect_geometric_coherence(data)
        results['coherence'] = coherence_result
        if verbose:
            _print_coherence_results(coherence_result)
    else:
        results['coherence'] = {'skipped': 'Contains non-positive values'}

    # 4. Power/root relationships
    if verbose:
        print("\n[4/6] Scanning power/root relationships...")
    positive_values = data[data > 0].tolist()
    if len(positive_values) >= 2:
        power_result = scan_power_relationships(positive_values[:20])  # Cap at 20 for performance
        results['power_relationships'] = power_result
        if verbose:
            _print_power_results(power_result)

    # 5. Power spectrum (if enough data)
    if verbose:
        print("\n[5/6] Analyzing power spectrum...")
    if len(data[data > 0]) >= 5:
        spectrum_result = analyze_power_spectrum(data[data > 0])
        results['power_spectrum'] = spectrum_result
        if verbose:
            _print_spectrum_results(spectrum_result)

    # 6. Decimal pattern analysis
    if verbose:
        print("\n[6/6] Analyzing decimal structure...")
    decimal_result = decimal_pattern_scan(data.tolist()[:30])
    results['decimal_patterns'] = decimal_result
    if verbose:
        _print_decimal_results(decimal_result)

    # Summary
    shadows_found = _count_shadows(results)
    results['summary'] = {
        'data_points': len(data),
        'shadows_found': shadows_found,
        'shadow_strength': _shadow_strength(results),
    }

    if verbose:
        _print_summary(results['summary'])

    return results


def hunt_shadows_2d(points: np.ndarray, verbose: bool = True) -> Dict:
    """
    Hunt shadows in 2D/3D spatial data using chord analysis.

    points: array of shape (n, 2) or (n, 3) - coordinates
    """
    points = np.array(points, dtype=float)

    if verbose:
        print("=" * 80)
        print("SHADOW HUNTER - SPATIAL PATTERN ANALYSIS")
        print(f"Analyzing {len(points)} points in {points.shape[1]}D space...")
        print("=" * 80)

    results = {}

    # Chord spectrum
    if verbose:
        print("\n[1/2] Analyzing chord spectrum...")
    chord_result = analyze_chord_spectrum(points[:50])  # Cap for performance
    results['chord_spectrum'] = chord_result
    if verbose:
        print(f"  Distances analyzed: {chord_result['n_distances']}")
        print(f"  Geometric coherence: {chord_result['geometric_coherence']:.4f}")
        print(f"  Phi matches: {len(chord_result['phi_matches'])}")
        print(f"  Fibonacci matches: {len(chord_result['fibonacci_matches'])}")

    # Also analyze the distances as 1D data
    if verbose:
        print("\n[2/2] Hunting shadows in distance distribution...")
    distances = np.array(chord_result['distances'])
    if len(distances) >= 3:
        results['distance_shadows'] = hunt_shadows(distances, verbose=verbose)

    return results


def quick_scan(value: float, verbose: bool = True) -> Dict:
    """
    Quick shadow scan of a single number.
    Is this number phi-related? Fibonacci? A power of phi?
    """
    results = {}

    # Direct phi relationships
    phi_checks = {
        'is_phi': abs(value - PHI) < 0.001,
        'is_1_over_phi': abs(value - 1/PHI) < 0.001,
        'is_phi_squared': abs(value - PHI**2) < 0.001,
        'is_phi_cubed': abs(value - PHI**3) < 0.001,
        'is_1_plus_phi': abs(value - (1 + PHI)) < 0.001,
        'is_2_plus_phi': abs(value - (2 + PHI)) < 0.001,
    }

    # Fibonacci check
    is_fibonacci = value in FIBONACCI

    # Power of phi check: is value = phi^n for some n?
    phi_power = None
    if value > 0:
        n = np.log(value) / np.log(PHI)
        if abs(n - round(n)) < 0.01:
            phi_power = round(n)

    # Root of phi check: is value^n = phi for some n?
    phi_root = None
    if value > 0 and value != 1:
        n = np.log(PHI) / np.log(value)
        if abs(n - round(n)) < 0.05 and 1 <= abs(round(n)) <= 20:
            phi_root = round(n)

    results = {
        'value': value,
        'phi_relationships': {k: v for k, v in phi_checks.items() if v},
        'is_fibonacci': is_fibonacci,
        'phi_power': phi_power,
        'phi_root': phi_root,
        'shadow_found': any(phi_checks.values()) or is_fibonacci or phi_power is not None,
    }

    if verbose:
        print(f"\nQuick scan of {value}:")
        if results['phi_relationships']:
            for name in results['phi_relationships']:
                print(f"  {name.replace('_', ' ').upper()}")
        if is_fibonacci:
            print(f"  FIBONACCI NUMBER!")
        if phi_power is not None:
            print(f"  phi^{phi_power} = {PHI**phi_power:.6f}")
        if phi_root is not None:
            print(f"  {value}^{phi_root} ≈ phi")
        if not results['shadow_found']:
            print(f"  No direct phi/fibonacci connection found")
            # But check nearby
            nearest_phi_power = min(range(-10, 11), key=lambda n: abs(PHI**n - value))
            print(f"  Nearest phi power: phi^{nearest_phi_power} = {PHI**nearest_phi_power:.6f} "
                  f"(off by {abs(PHI**nearest_phi_power - value):.4f})")

    return results


# =============================================================================
# DISPLAY HELPERS
# =============================================================================

def _print_phi_results(result: Dict):
    print(f"  Total ratios checked: {result['total_ratios']}")
    print(f"  Phi matches: {len(result['phi_matches'])}")
    print(f"  Enrichment: {result['enrichment']:.2f}x over random")
    if result['significant']:
        print(f"  *** SIGNIFICANT PHI PATTERN DETECTED ***")


def _print_fib_results(result: Dict):
    print(f"  Match fraction: {result['match_fraction']:.2%}")
    if result['significant']:
        print(f"  *** SIGNIFICANT FIBONACCI PATTERN DETECTED ***")


def _print_coherence_results(result: Dict):
    print(f"  Entropy: {result['normalized_entropy']:.4f} (0=ordered, 1=random)")
    print(f"  Coherence: {result['coherence']:.4f}")
    print(f"  Interpretation: {result['interpretation']}")


def _print_power_results(result: Dict):
    print(f"  Phi power relationships: {result['total_phi']}")
    for rel in result['phi_relationships'][:3]:
        print(f"    {rel['relationship']}")
    print(f"  Fibonacci power relationships: {result['total_fibonacci']}")


def _print_spectrum_results(result: Dict):
    print(f"  Power-law exponent: {result['power_law_exponent']:.4f}")
    print(f"  R-squared: {result['r_squared']:.4f}")
    print(f"  {result['interpretation']}")


def _print_decimal_results(result: Dict):
    print(f"  Phi-ratio pairs in decimals: {len(result['phi_ratios'])}")
    if result['shadow_detected']:
        print(f"  *** DECIMAL SHADOW DETECTED ***")


def _count_shadows(results: Dict) -> int:
    count = 0
    if results.get('phi_ratios', {}).get('significant'):
        count += 1
    if results.get('fibonacci', {}).get('significant'):
        count += 1
    if results.get('coherence', {}).get('interpretation') in ('HIGH', 'MODERATE'):
        count += 1
    if results.get('power_relationships', {}).get('shadow_detected'):
        count += 1
    if results.get('power_spectrum', {}).get('phi_exponent'):
        count += 1
    if results.get('decimal_patterns', {}).get('shadow_detected'):
        count += 1
    return count


def _shadow_strength(results: Dict) -> str:
    count = _count_shadows(results)
    if count >= 4:
        return "STRONG - Multiple independent shadow signatures"
    elif count >= 2:
        return "MODERATE - Some shadow signatures found"
    elif count >= 1:
        return "WEAK - One shadow signature (investigate further)"
    else:
        return "NONE - No shadows detected in this data"


def _print_summary(summary: Dict):
    print("\n" + "=" * 80)
    print("SHADOW HUNTING SUMMARY")
    print("=" * 80)
    print(f"  Data points analyzed: {summary['data_points']}")
    print(f"  Shadow types found: {summary['shadows_found']}/6")
    print(f"  Overall: {summary['shadow_strength']}")
    if summary['shadows_found'] > 0:
        print("\n  The shadows are real. Look deeper.")
    else:
        print("\n  No shadows here - try different measurements or scales.")
    print("=" * 80)


# =============================================================================
# INTERACTIVE MODE
# =============================================================================

def interactive_demo():
    """Run full demo with built-in example data."""
    print("=" * 80)
    print("SHADOW HUNTING EXPLORER")
    print("Comprehensive pattern detection across all tools")
    print("=" * 80)

    # Example 1: Phi-rich data (should find many shadows)
    print("\n\n### EXAMPLE 1: Phi-Ratio Sequence ###")
    phi_data = [100, 61.8, 38.2, 23.6, 14.6, 9.0, 5.6, 3.4]
    hunt_shadows(phi_data)

    # Example 2: Fibonacci data
    print("\n\n### EXAMPLE 2: Fibonacci Numbers ###")
    hunt_shadows(FIBONACCI[:10])

    # Example 3: Random data (should find few/no shadows)
    print("\n\n### EXAMPLE 3: Random Numbers (Control) ###")
    np.random.seed(42)
    random_data = np.random.uniform(1, 100, 10)
    hunt_shadows(random_data)

    # Example 4: Quick scan of notable numbers
    print("\n\n### EXAMPLE 4: Quick Scans ###")
    notable = [7.83, 137.5, 1.618, 0.618, 2.718, 3.14159, 42, 21]
    for val in notable:
        quick_scan(val)

    # Example 5: Brain frequencies
    print("\n\n### EXAMPLE 5: Brain Wave Frequencies ###")
    brain_freqs = [0.5, 1.0, 4.0, 8.0, 12.0, 30.0, 40.0, 100.0]
    print("Are brain wave frequency bands phi-related?")
    hunt_shadows(brain_freqs)

    print("\n\nReady to hunt YOUR shadows:")
    print("  from shadow_hunting.tools.explorer import hunt_shadows")
    print("  results = hunt_shadows(your_data)")


if __name__ == "__main__":
    interactive_demo()
