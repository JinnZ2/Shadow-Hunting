#!/usr/bin/env python3
"""
Chordal Dimensions - Geometric Chord Analysis for Shadow Hunting

KEY INSIGHT: When you divide a circle using the golden angle (137.5 degrees),
the chord lengths between points encode phi-ratios at EVERY scale.
This is why sunflower seeds, pine cones, and hurricanes use this geometry -
it's the mathematically optimal packing.

Tools:
- Analyze chord patterns in circular/spherical data
- Detect phi-ratio chord relationships in any geometry
- Map dimensional coupling through chord networks
- Find golden angle signatures in spatial data

Why this matters:
Chords connect distant points through interior space.
Field coupling works the same way - energy transfers through
geometric shortcuts, not along surfaces. Phi-ratio chords are
the "wormholes" of geometric coupling.

Author: JinnZ2 and collaborators - MIT License
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

from shadow_hunting import PHI, FIBONACCI


GOLDEN_ANGLE_RAD = np.pi * (3 - np.sqrt(5))  # ~137.5 degrees in radians
GOLDEN_ANGLE_DEG = 360 * (1 - PHI)  # ~137.508 degrees


def chord_length(angle_rad: float, radius: float = 1.0) -> float:
    """
    Chord length for a given central angle on a circle.
    chord = 2 * r * sin(angle/2)
    """
    return 2 * radius * np.sin(angle_rad / 2)


def golden_angle_chords(n_points: int, radius: float = 1.0) -> Dict:
    """
    Place n points on a circle using the golden angle spacing.
    Calculate ALL chord lengths between them and analyze for phi patterns.
    """
    # Place points at golden angle intervals
    angles = np.array([(i * GOLDEN_ANGLE_RAD) % (2 * np.pi) for i in range(n_points)])
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)

    # Calculate all chord lengths
    chords = []
    chord_matrix = np.zeros((n_points, n_points))

    for i in range(n_points):
        for j in range(i + 1, n_points):
            dist = np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
            chords.append(dist)
            chord_matrix[i, j] = dist
            chord_matrix[j, i] = dist

    chords = np.array(sorted(chords))

    # Analyze chord ratios
    ratios = chords[1:] / chords[:-1]
    phi_ratios = []
    for i, ratio in enumerate(ratios):
        if abs(ratio - PHI) < 0.05 or abs(ratio - 1/PHI) < 0.05:
            phi_ratios.append((chords[i], chords[i + 1], ratio))

    # Unique chord lengths (within tolerance)
    unique_chords = _cluster_values(chords, tolerance=0.01 * radius)

    return {
        'n_points': n_points,
        'angles_deg': np.degrees(angles).tolist(),
        'points': list(zip(x.tolist(), y.tolist())),
        'all_chords': chords.tolist(),
        'unique_chord_lengths': unique_chords,
        'n_unique': len(unique_chords),
        'chord_ratios': ratios.tolist(),
        'phi_ratios': phi_ratios,
        'phi_density': len(phi_ratios) / max(len(ratios), 1),
        'chord_matrix': chord_matrix
    }


def analyze_chord_spectrum(points: np.ndarray) -> Dict:
    """
    Given arbitrary 2D or 3D points, compute all pairwise distances (chords)
    and analyze the distribution for phi-ratio patterns.

    points: array of shape (n, 2) or (n, 3)
    """
    n = len(points)
    distances = []

    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(points[i] - points[j])
            distances.append(dist)

    distances = np.array(sorted(distances))

    if len(distances) < 2:
        return {'error': 'Need at least 3 points'}

    # Ratio analysis
    ratios = distances[1:] / (distances[:-1] + 1e-15)

    phi_matches = []
    fib_matches = []

    for i, ratio in enumerate(ratios):
        for name, val in [('phi', PHI), ('1/phi', 1/PHI)]:
            if abs(ratio - val) < 0.05:
                phi_matches.append({
                    'index': i,
                    'd1': distances[i],
                    'd2': distances[i + 1],
                    'ratio': ratio,
                    'type': name
                })

    # Check if distance values themselves are fibonacci-related
    min_dist = distances[0] if distances[0] > 0 else 1.0
    normalized = distances / min_dist

    for i, val in enumerate(normalized):
        for fib in FIBONACCI[:10]:
            if abs(val - fib) / fib < 0.1:
                fib_matches.append({'index': i, 'distance': distances[i], 'fibonacci': fib})
                break

    # Entropy of distance distribution (binned)
    hist, _ = np.histogram(distances, bins=20)
    hist = hist / hist.sum()
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist))
    max_entropy = np.log2(20)
    coherence = 1 - entropy / max_entropy

    return {
        'n_points': n,
        'n_distances': len(distances),
        'distances': distances.tolist(),
        'phi_matches': phi_matches,
        'fibonacci_matches': fib_matches,
        'distance_entropy': entropy,
        'geometric_coherence': coherence,
        'shadow_detected': len(phi_matches) >= 2 or coherence > 0.5
    }


def dimensional_chord_analysis(value: float, dimensions: int = 7) -> Dict:
    """
    Analyze how chord geometry changes across dimensions.

    In higher dimensions, regular polytopes have chord structures
    with phi-ratio relationships. This function computes chord
    lengths of regular simplices from 2D to nD and finds where
    phi emerges.

    The "chordal dimension" is the dimension where phi-coupling
    is strongest for a given measurement scale.
    """
    results = []

    for dim in range(2, dimensions + 1):
        # Regular simplex in n dimensions has n+1 vertices
        # Edge length for unit circumradius: sqrt(2 * (1 + 1/n))
        # But we analyze using value as the scale
        n_vertices = dim + 1
        edge_length = value * np.sqrt(2 * (1 + 1.0/dim))

        # Circumradius to inradius ratio
        circum_to_inradius = dim  # For regular simplex

        # Check phi relationships
        phi_sig = abs(edge_length - PHI * value) < 0.1 * value
        ratio_to_phi = edge_length / (PHI * value)

        # Volume of regular simplex (normalized)
        volume = (edge_length ** dim) * np.sqrt(dim + 1) / (np.math.factorial(dim) * 2 ** (dim / 2))

        # Surface-to-volume ratio (simplified)
        if volume > 0:
            sv_ratio = (n_vertices * edge_length ** (dim - 1)) / volume
        else:
            sv_ratio = 0

        results.append({
            'dimension': dim,
            'n_vertices': n_vertices,
            'edge_length': edge_length,
            'ratio_to_phi_scale': ratio_to_phi,
            'phi_significant': abs(ratio_to_phi - 1.0) < 0.1,
            'circumradius_inradius_ratio': circum_to_inradius,
            'volume': volume,
            'surface_volume_ratio': sv_ratio,
        })

    # Find the "chordal dimension" - where phi coupling is strongest
    phi_scores = [abs(1.0 - r['ratio_to_phi_scale']) for r in results]
    best_dim_idx = np.argmin(phi_scores)
    chordal_dimension = results[best_dim_idx]['dimension']

    return {
        'value': value,
        'dimensions_analyzed': results,
        'chordal_dimension': chordal_dimension,
        'phi_score_at_chordal': 1 - phi_scores[best_dim_idx],
        'interpretation': f"Strongest phi-coupling at dimension {chordal_dimension}"
    }


def polygon_chord_analysis(n_sides: int, radius: float = 1.0) -> Dict:
    """
    Analyze chord patterns in regular polygons.
    The pentagon (n=5) is special - its diagonal/side ratio IS phi.
    Find which polygons have the most phi-ratio chords.
    """
    # Vertices of regular n-gon
    angles = np.array([2 * np.pi * k / n_sides for k in range(n_sides)])
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)

    # All unique chord lengths
    chord_lengths = set()
    chord_list = []
    for i in range(n_sides):
        for j in range(i + 1, n_sides):
            dist = np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
            chord_list.append(dist)
            chord_lengths.add(round(dist, 8))

    unique = sorted(chord_lengths)

    # Check ratios between unique chord lengths
    phi_count = 0
    phi_pairs = []
    for i in range(len(unique)):
        for j in range(i + 1, len(unique)):
            if unique[i] > 1e-10:
                ratio = unique[j] / unique[i]
                if abs(ratio - PHI) < 0.02 or abs(ratio - 1/PHI) < 0.02:
                    phi_count += 1
                    phi_pairs.append((unique[i], unique[j], ratio))

    return {
        'n_sides': n_sides,
        'unique_chord_lengths': unique,
        'n_unique': len(unique),
        'phi_pairs': phi_pairs,
        'phi_count': phi_count,
        'phi_rich': phi_count >= 1,
        'is_pentagon': n_sides == 5,
    }


def _cluster_values(values: np.ndarray, tolerance: float = 0.01) -> List[float]:
    """Group similar values and return cluster centers."""
    if len(values) == 0:
        return []
    clusters = [[values[0]]]
    for v in values[1:]:
        if abs(v - clusters[-1][-1]) < tolerance:
            clusters[-1].append(v)
        else:
            clusters.append([v])
    return [np.mean(c) for c in clusters]


# =============================================================================
# INTERACTIVE DEMO
# =============================================================================

def demo():
    """Interactive demonstration of chordal dimension analysis."""
    print("=" * 80)
    print("CHORDAL DIMENSIONS - GEOMETRIC COUPLING THROUGH CHORD SPACE")
    print("Finding phi-ratios in the distances between points")
    print("=" * 80)

    # Demo 1: Golden angle chord analysis
    print("\n--- GOLDEN ANGLE CHORDS ---")
    for n in [5, 8, 13, 21]:  # Fibonacci numbers of points!
        result = golden_angle_chords(n)
        print(f"\n  {n} points (fibonacci!) at golden angle spacing:")
        print(f"    Unique chord lengths: {result['n_unique']}")
        print(f"    Phi-ratio pairs: {len(result['phi_ratios'])}")
        print(f"    Phi density: {result['phi_density']:.3f}")
        if result['phi_ratios'][:2]:
            for pair in result['phi_ratios'][:2]:
                print(f"      {pair[0]:.4f} / {pair[1]:.4f} = {pair[2]:.4f}")

    # Demo 2: Polygon comparison
    print("\n--- POLYGON CHORD ANALYSIS ---")
    print("  Which polygons have phi in their chord structure?")
    for n in [3, 4, 5, 6, 7, 8, 10, 12]:
        result = polygon_chord_analysis(n)
        phi_flag = " <-- PHI POLYGON!" if result['phi_rich'] else ""
        penta = " (PENTAGON - the phi polygon)" if result['is_pentagon'] else ""
        print(f"    {n:>2}-gon: {result['n_unique']} unique chords, "
              f"{result['phi_count']} phi pairs{phi_flag}{penta}")

    # Demo 3: Dimensional analysis
    print("\n--- DIMENSIONAL CHORD ANALYSIS ---")
    for value in [1.0, PHI, 7.83]:
        label = "phi" if abs(value - PHI) < 0.01 else str(value)
        result = dimensional_chord_analysis(value)
        print(f"\n  Scale = {label}:")
        print(f"    Chordal dimension: {result['chordal_dimension']}")
        print(f"    Phi score: {result['phi_score_at_chordal']:.4f}")
        for dim_data in result['dimensions_analyzed']:
            marker = " ***" if dim_data['phi_significant'] else ""
            print(f"      dim={dim_data['dimension']}: edge={dim_data['edge_length']:.4f}, "
                  f"phi_ratio={dim_data['ratio_to_phi_scale']:.4f}{marker}")

    # Demo 4: Random vs structured points
    print("\n--- RANDOM VS STRUCTURED POINT CLOUDS ---")

    # Structured: fibonacci spiral
    n = 50
    angles_fib = np.array([i * GOLDEN_ANGLE_RAD for i in range(n)])
    radii_fib = np.sqrt(np.arange(n))
    structured = np.column_stack([radii_fib * np.cos(angles_fib),
                                   radii_fib * np.sin(angles_fib)])

    # Random
    random_pts = np.random.randn(n, 2) * 3

    struct_result = analyze_chord_spectrum(structured[:20])
    random_result = analyze_chord_spectrum(random_pts[:20])

    print(f"\n  Fibonacci spiral (20 pts):")
    print(f"    Geometric coherence: {struct_result['geometric_coherence']:.4f}")
    print(f"    Phi matches: {len(struct_result['phi_matches'])}")
    print(f"    Fibonacci matches: {len(struct_result['fibonacci_matches'])}")
    print(f"    Shadow detected: {struct_result['shadow_detected']}")

    print(f"\n  Random points (20 pts):")
    print(f"    Geometric coherence: {random_result['geometric_coherence']:.4f}")
    print(f"    Phi matches: {len(random_result['phi_matches'])}")
    print(f"    Fibonacci matches: {len(random_result['fibonacci_matches'])}")
    print(f"    Shadow detected: {random_result['shadow_detected']}")

    print("\n" + "=" * 80)
    print("TRY IT: Feed spatial coordinates into analyze_chord_spectrum()")
    print("The shadows hide in the distances between things.")
    print("=" * 80)


if __name__ == "__main__":
    demo()
