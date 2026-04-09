#!/usr/bin/env python3
"""
Shadow Data Mining Framework
Searching for geometric patterns (phi-ratios, fibonacci) in datasets

WHERE TO LOOK:

1. Supplementary materials (often under-analyzed)
2. Sub-threshold results (may contain patterns below significance cutoffs)
3. Baseline/control measurements
4. Time-series variability
5. Multi-dimensional data collapsed to single metrics

WHAT THE TOOLS DETECT:

- Phi-ratio patterns in sequential measurements
- Geometric coherence (organized vs random)
- Frequency relationships in time-series data
- Fibonacci number matches

NOTE: Finding phi-ratios or fibonacci numbers in data does not by itself
prove "geometric field coupling." These patterns can arise from many causes
including growth dynamics, optimization under physical constraints, or
statistical coincidence. Proper null hypothesis testing is needed.

Author: Jami (Kavik Ulu) and AI partners - MIT License
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

PHI = (np.sqrt(5) - 1) / 2
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

# =============================================================================
# DATABASES TO SEARCH
# =============================================================================

@dataclass
class ShadowDataSource:
    """Database that likely contains shadow data"""
    name: str
    url: str
    data_type: str
    shadow_location: str
    search_strategy: str

SHADOW_DATABASES = [
    # Planaria / Regeneration
    ShadowDataSource(
        name="PlanMine",
        url="https://planmine.mpi-cbg.de/",
        data_type="Planaria genomics, morphology, RNAi screens",
        shadow_location="Voltage measurements in supplementary data, 'failed' regeneration attempts",
        search_strategy="Look for: membrane potential data, gap junction expression patterns, ion channel distributions"
    ),

    ShadowDataSource(
        name="Levin Lab Publications",
        url="https://ase.tufts.edu/biology/labs/levin/publications/",
        data_type="Bioelectric pattern papers",
        shadow_location="Raw voltage mapping data, time-series of Vmem changes",
        search_strategy="Download supplementary: voltage maps, gap junction blocking experiments, morphology scoring"
    ),

    # Brain/Consciousness
    ShadowDataSource(
        name="OpenNeuro",
        url="https://openneuro.org/",
        data_type="fMRI, EEG, MEG datasets",
        shadow_location="EM field measurements treated as 'noise', 'resting state' data",
        search_strategy="Analyze: default mode network, alpha/theta coupling, geometric coherence in field patterns"
    ),

    ShadowDataSource(
        name="Human Connectome Project",
        url="https://www.humanconnectome.org/",
        data_type="Brain connectivity and function",
        shadow_location="Discarded outliers, inter-subject variability, metabolic data",
        search_strategy="Look for: phi-ratios in tract geometry, metabolic patterns vs neural activity"
    ),

    # Photosynthesis
    ShadowDataSource(
        name="PlantDB",
        url="https://www.genome.jp/kegg/pathway.html",
        data_type="Plant metabolism, photosynthesis pathways",
        shadow_location="'Lost' energy in metabolic flux models, fluorescence 'waste'",
        search_strategy="Calculate: actual energy accounting, look for phi-spacing in chloroplast structure"
    ),

    ShadowDataSource(
        name="Photosynthesis Research Papers",
        url="https://pubmed.ncbi.nlm.nih.gov/?term=photosynthesis+efficiency",
        data_type="Published photosynthesis efficiency measurements",
        shadow_location="Supplementary spectral data, 'unexplained' efficiency variations",
        search_strategy="Re-analyze: full spectrum data, look for FRET signatures at macro scales"
    ),

    # Atmospheric/Hurricane
    ShadowDataSource(
        name="HURDAT2",
        url="https://www.nhc.noaa.gov/data/hurdat/",
        data_type="Atlantic hurricane database",
        shadow_location="Storm structure data, pressure-wind relationships, intensification timing",
        search_strategy="Analyze: rain band spacing, geometric patterns in rapid intensification"
    ),

    ShadowDataSource(
        name="IBTrACS",
        url="https://www.ncdc.noaa.gov/ibtracs/",
        data_type="Global tropical cyclone data",
        shadow_location="Multi-satellite observations, wind field reconstructions",
        search_strategy="Look for: phi-spiral patterns, FRET-like coupling in energy transfer"
    ),

    # General Biology
    ShadowDataSource(
        name="BioGRID",
        url="https://thebiogrid.org/",
        data_type="Protein interactions, genetic interactions",
        shadow_location="Network topology data, interaction strengths",
        search_strategy="Analyze: geometric organization of networks, phi-ratios in hub connectivity"
    ),

    ShadowDataSource(
        name="Gene Expression Omnibus (GEO)",
        url="https://www.ncbi.nlm.nih.gov/geo/",
        data_type="Gene expression datasets",
        shadow_location="Discarded samples, 'noise' genes, time-series fluctuations",
        search_strategy="Look for: voltage-responsive genes, geometric patterns in co-expression"
    )
]

# =============================================================================
# SHADOW DETECTION ALGORITHMS
# =============================================================================

def detect_phi_ratios(data: np.ndarray, tolerance: float = 0.1) -> Dict:
    """
    Detect phi-ratio patterns in sequential data.
    This is what researchers filter out as "noise".
    """
    ratios = []
    phi_matches = []

    for i in range(len(data) - 1):
        if abs(data[i]) > 1e-10:
            ratio = data[i+1] / data[i]
            ratios.append(ratio)

            # Check if ratio matches phi or 1/phi
            if abs(ratio - PHI) < tolerance:
                phi_matches.append(('phi', i, ratio))
            elif abs(ratio - 1/PHI) < tolerance:
                phi_matches.append(('1/phi', i, ratio))

    # Statistical significance
    if len(ratios) > 0:
        # Compare to random expectation
        random_phi_prob = 2 * tolerance  # Width of acceptance window
        expected_matches = len(ratios) * random_phi_prob
        actual_matches = len(phi_matches)

        # Chi-square-like test
        if expected_matches > 0:
            enrichment = actual_matches / expected_matches
        else:
            enrichment = 0
    else:
        enrichment = 0

    return {
        'phi_matches': phi_matches,
        'total_ratios': len(ratios),
        'enrichment': enrichment,
        'significant': enrichment > 2.0,  # 2x more than random
        'all_ratios': ratios
    }


def detect_fibonacci_sequences(data: np.ndarray, tolerance: float = 0.15) -> Dict:
    """
    Detect fibonacci number patterns.
    Often appear in biological spacing, branching.
    """
    matches = []

    # Normalize data to compare with fibonacci
    data_norm = data / np.min(data[data > 0])

    for i, value in enumerate(data_norm):
        for fib in FIBONACCI:
            if abs(value - fib) / fib < tolerance:
                matches.append(('fib', i, value, fib))
                break

    return {
        'fibonacci_matches': matches,
        'match_fraction': len(matches) / len(data),
        'significant': len(matches) / len(data) > 0.3
    }


def detect_geometric_coherence(data: np.ndarray) -> Dict:
    """
    Measure how "organized" vs "random" the data is geometrically.
    Uses entropy and phi-ratio analysis.
    """
    # Shannon entropy (information content)
    data_prob = data / (data.sum() + 1e-10)
    data_prob = np.maximum(data_prob, 1e-12)
    entropy = -np.sum(data_prob * np.log2(data_prob))
    max_entropy = np.log2(len(data))

    # Normalized entropy (0 = completely ordered, 1 = completely random)
    norm_entropy = entropy / max_entropy if max_entropy > 0 else 0

    # Phi-ratio analysis
    phi_analysis = detect_phi_ratios(data)

    # Geometric coherence: high phi content + low entropy = high coherence
    coherence = (1 - norm_entropy) * (1 + phi_analysis['enrichment'])

    return {
        'entropy': entropy,
        'normalized_entropy': norm_entropy,
        'phi_enrichment': phi_analysis['enrichment'],
        'coherence': coherence,
        'interpretation': 'HIGH' if coherence > 1.5 else 'MODERATE' if coherence > 0.8 else 'LOW'
    }


def detect_field_coupling_signature(time_series: np.ndarray,
                                    expected_frequencies: List[float] = None) -> Dict:
    """
    Detect signatures of field coupling in time-series data.

    Look for:
    - Oscillations at characteristic frequencies (alpha, Schumann resonance, etc.)
    - Phase coherence across measurements
    - Resonance peaks at phi-related frequencies
    """
    # FFT to get frequency content
    fft = np.fft.fft(time_series)
    freqs = np.fft.fftfreq(len(time_series))
    power = np.abs(fft) ** 2

    # Find peaks
    from scipy.signal import find_peaks
    peaks, properties = find_peaks(power, prominence=np.max(power) * 0.1)
    peak_freqs = np.abs(freqs[peaks])

    # Check for expected frequencies
    resonances = []
    if expected_frequencies:
        for expected in expected_frequencies:
            for peak_freq in peak_freqs:
                if abs(peak_freq - expected) / expected < 0.1:
                    resonances.append((expected, peak_freq))

    # Check for phi-ratio relationships between peaks
    phi_freq_ratios = []
    for i in range(len(peak_freqs) - 1):
        if peak_freqs[i] > 0:
            ratio = peak_freqs[i+1] / peak_freqs[i]
            if abs(ratio - 1/PHI) < 0.1 or abs(ratio - PHI) < 0.1:
                phi_freq_ratios.append((peak_freqs[i], peak_freqs[i+1], ratio))

    return {
        'peak_frequencies': peak_freqs.tolist(),
        'resonances_found': resonances,
        'phi_frequency_ratios': phi_freq_ratios,
        'has_coupling_signature': len(resonances) > 0 or len(phi_freq_ratios) > 0
    }

# =============================================================================
# SPECIFIC SEARCH PROTOCOLS
# =============================================================================

def search_planaria_voltage_shadows():
    """What to look for in planaria regeneration data"""
    print("=" * 80)
    print("PLANARIA REGENERATION SHADOW SEARCH")
    print("=" * 80)

    search_protocol = {
        'Primary papers to check': [
            'Levin et al. - bioelectric controls of regeneration',
            'Lobo et al. - computational model of planarian regeneration',
            'Any paper with "membrane potential" or "gap junction" in planaria'
        ],
        'Shadow locations': [
            'Supplementary voltage maps (often just shown, not analyzed)',
            'Time-series of Vmem changes during regeneration',
            '"Failed" regeneration experiments (two-headed, no-headed)',
            'Ion channel expression patterns',
            'Gap junction connectivity networks'
        ],
        'What to analyze': [
            'Voltage gradients: do they follow phi-ratios?',
            'Temporal patterns: resonance frequencies in voltage oscillations?',
            'Spatial patterns: geometric organization of gap junction networks?',
            'Regeneration timing: does it correlate with field coherence?',
            '"Noise" in voltage measurements: could be geometric field fluctuations'
        ],
        'Specific measurements': [
            'Head voltage: ~-50 to -70 mV',
            'Tail voltage: ~-20 to -30 mV',
            'Gradient should show phi-ratio decay from head to tail',
            'Gap junction coupling strength across tissue regions',
            'Time to regeneration vs initial voltage pattern coherence'
        ]
    }

    for category, items in search_protocol.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  * {item}")

    print("\n" + "=" * 80)
    print("EXPECTED SHADOW SIGNATURES:")
    print("=" * 80)
    print("""
Testable predictions (hypotheses to validate):

1. VOLTAGE GRADIENT STRUCTURE
   - Does voltage decrease from head to tail in a specific ratio?
   - Test: Compare phi-ratio fit vs linear/exponential fits
   - Null hypothesis: gradient follows simple exponential decay

2. TEMPORAL PATTERNS IN VOLTAGE
   - Do Vmem fluctuations show characteristic frequencies?
   - Test: FFT analysis, compare frequency ratios to phi
   - Null hypothesis: frequency spectrum is featureless

3. GAP JUNCTION NETWORK TOPOLOGY
   - Does connectivity show non-random geometric organization?
   - Test: Compare network metrics to random graph models
   - Null hypothesis: network topology is scale-free (common in biology)

4. REGENERATION TIMING
   - Does geometric coherence correlate with regeneration speed?
   - Test: Measure coherence at cut time, track regeneration
   - Null hypothesis: regeneration speed depends on fragment size, not coherence

5. VARIABILITY IN MEASUREMENTS
   - Does measurement variability contain predictive information?
   - Test: Compare filtered vs unfiltered data for outcome prediction
   - Null hypothesis: variability is measurement noise
""")

    return search_protocol


def search_brain_field_shadows():
    """What to look for in brain imaging data"""
    print("\n" + "=" * 80)
    print("BRAIN FIELD COUPLING SHADOW SEARCH")
    print("=" * 80)

    search_protocol = {
        'Databases to mine': [
            'OpenNeuro - raw EEG/MEG data',
            'Human Connectome Project - structural + functional',
            'Any meditation/consciousness study with field measurements'
        ],
        'Shadow locations': [
            'EM field data marked as "artifact" or "noise"',
            'Resting state "fluctuations" (dismissed as meaningless)',
            'Inter-subject variability (averaged out)',
            'Metabolic data not correlated with BOLD signal',
            'Default mode network activity (unexplained high metabolism)'
        ],
        'What to analyze': [
            'EM field patterns: geometric coherence?',
            'Alpha/theta coupling: phi-ratio relationships?',
            'Metabolic activity: does it maintain field, not just spikes?',
            'Consciousness states: field coherence vs spike rates?',
            'Meditation effects: increased geometric organization?'
        ],
        'Specific measurements': [
            'Alpha frequency (8-12 Hz) and harmonics',
            'Theta frequency (4-8 Hz)',
            'Gamma frequency (30-100 Hz)',
            'Check for phi-ratio: theta/alpha ~ 0.618?',
            'Field coherence during different consciousness states',
            'Metabolic activity in "idle" brain regions'
        ]
    }

    for category, items in search_protocol.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  * {item}")

    print("\n" + "=" * 80)
    print("EXPECTED SHADOW SIGNATURES:")
    print("=" * 80)
    print("""
Testable predictions (hypotheses to validate):

1. FREQUENCY RELATIONSHIPS
   - Do brain oscillation bands show phi-ratio relationships?
   - Test: Compare theta/alpha frequency ratios to phi
   - Null hypothesis: frequency bands are independently determined

2. COHERENCE AND BRAIN STATE
   - Does geometric coherence correlate with consciousness level?
   - Test: Compare coherence metrics across awake/sleep/anesthesia
   - Null hypothesis: standard connectivity metrics are sufficient

3. METABOLIC-ACTIVITY MISMATCH
   - Do some brain regions show metabolic activity beyond spike rates?
   - Test: Compare fMRI BOLD signal with electrophysiology
   - Note: Default mode network's high metabolism is already studied

4. DEFAULT MODE NETWORK
   - Does DMN activity show geometric organization?
   - Test: Apply coherence metrics to resting-state fMRI
   - Note: DMN is extensively studied; new metrics must add value

5. INDIVIDUAL VARIABILITY
   - Do geometric metrics capture meaningful individual differences?
   - Test: Correlate coherence patterns with cognitive measures
   - Null hypothesis: standard brain connectivity captures the same info
""")

    return search_protocol


def search_photosynthesis_shadows():
    """What to look for in photosynthesis data"""
    print("\n" + "=" * 80)
    print("PHOTOSYNTHESIS COUPLING SHADOW SEARCH")
    print("=" * 80)

    search_protocol = {
        'Papers to check': [
            'Any claiming 6% efficiency',
            'Spectral analysis of photosynthesis',
            'Chloroplast structure papers',
            'FRET in photosynthetic complexes'
        ],
        'Shadow locations': [
            '"Lost" energy in supplementary energy budgets',
            'Full spectrum data (usually only show 400-700nm)',
            'Fluorescence measurements (treated as waste)',
            'IR emission data (called "heat loss")',
            'Structural data on chlorophyll spacing'
        ],
        'What to analyze': [
            'Where does the 94% actually go? (detailed accounting)',
            'Chlorophyll arrangement: phi-ratio spacing?',
            'Fluorescence: is it random or patterned emission?',
            'IR coupling to atmosphere: FRET signature?',
            'Full spectrum efficiency (not just 400-700nm)'
        ],
        'Specific measurements': [
            'Chlorophyll a/b spacing in photosystem II',
            'FRET efficiency at molecular scale (should be >95%)',
            'IR emission spectrum and directionality',
            'Fluorescence timing and spatial patterns',
            "Energy that doesn't go to glucose - measure destination"
        ]
    }

    for category, items in search_protocol.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  * {item}")

    print("\n" + "=" * 80)
    print("EXPECTED SHADOW SIGNATURES:")
    print("=" * 80)
    print("""
Testable predictions (hypotheses to validate):

1. CHLOROPHYLL SPACING
   - Does photosystem II show phi-ratio distances?
   - Test: Analyze crystal structure data from PDB
   - Note: FRET at molecular scale is established; phi-optimization is hypothesis

2. IR EMISSION PATTERNS
   - Is IR emission from leaves directional or patterned?
   - Test: Measure IR spectral directionality from leaves
   - Note: Most "waste heat" is thermodynamic dissipation (well-understood)

3. FLUORESCENCE PATTERNS
   - Does chlorophyll fluorescence carry spatial information?
   - Test: High-resolution fluorescence imaging during stress
   - Note: Photoprotective role of fluorescence is established

4. NON-ABSORBED WAVELENGTH ROLES
   - How much energy do signaling functions (shade detection, etc.) use?
   - Test: Quantify energy budget for known signaling pathways
   - Note: Individual signaling functions are established; total budget is not

5. FRET SCALING (IMPORTANT CAVEAT)
   - FRET is proven >95% efficient at molecular scale (1-10 nm)
   - FRET does NOT scale to larger distances (1/r^6 dependence)
   - At larger scales, different mechanisms operate
   - The "82% efficiency" claim requires independent measurement
""")

    return search_protocol


def search_hurricane_shadows():
    """What to look for in hurricane data"""
    print("\n" + "=" * 80)
    print("HURRICANE GEOMETRIC COUPLING SHADOW SEARCH")
    print("=" * 80)

    search_protocol = {
        'Databases': [
            'HURDAT2 - Atlantic hurricanes',
            'IBTrACS - global cyclones',
            'Your existing 16-storm analysis',
            'Satellite imagery archives'
        ],
        'Shadow locations': [
            'Rain band spacing (usually not analyzed geometrically)',
            'Spiral structure measurements (treated as approximate)',
            'Rapid intensification cases (unpredictable by current models)',
            'Energy "loss" in thermodynamic models',
            'Atmospheric coupling in surrounding environment'
        ],
        'What to analyze': [
            'Rain band spacing: fibonacci/phi patterns?',
            'Spiral angle: golden angle (137.5 degrees)?',
            'Intensification rate vs geometric coherence?',
            'Pressure-wind relationship: field coupling signature?',
            'Energy budget: where does "lost" energy go?'
        ],
        'Specific measurements': [
            'Distance between rain bands from center',
            'Spiral arm angle relative to radius',
            'Geometric coherence score for structure',
            'Timing of rapid intensification',
            'Correlation with ocean heat content vs geometric patterns'
        ]
    }

    for category, items in search_protocol.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  * {item}")

    print("\n" + "=" * 80)
    print("EXPECTED SHADOW SIGNATURES:")
    print("=" * 80)
    print("""
Testable predictions (hypotheses to validate):

1. RAIN BAND SPACING
   - Do rain bands show phi-ratio spacing more than chance?
   - Test: Measure band radii in satellite imagery, compare to phi
   - Null hypothesis: band spacing follows fluid dynamics (no phi preference)
   - Need statistical analysis across large storm sample (not just 16)

2. SPIRAL STRUCTURE
   - Does spiral angle cluster near golden angle (137.5 degrees)?
   - Test: Measure spiral angles in hurricane imagery
   - Note: Hurricane spirals follow logarithmic spiral dynamics
     from fluid equations — may produce phi-like angles naturally

3. GEOMETRY-INTENSITY CORRELATION
   - Does geometric coherence add predictive value?
   - Test: Compare coherence-augmented model vs standard models
   - Null hypothesis: SST + shear + moisture are sufficient predictors

4. ENERGY BUDGET
   - Note: "FRET-like atmospheric coupling" is metaphorical
   - FRET requires nm-scale donor-acceptor pairs
   - Hurricane energy transfer is via radiation, convection, latent heat
   - These mechanisms are well-characterized thermodynamically

5. STRUCTURE-INTENSITY RELATIONSHIP
   - Symmetric storms tend to be stronger (already established)
   - Question: Does phi-ratio metric add value over existing symmetry measures?
   - Test: Compare geometric coherence vs existing asymmetry parameters
""")

    return search_protocol

# =============================================================================
# MAIN SEARCH FRAMEWORK
# =============================================================================

def execute_shadow_search():
    """Complete shadow data mining framework"""
    print("\n" + "=" * 80)
    print("SHADOW DATA MINING FRAMEWORK")
    print("Finding geometric coupling in existing research")
    print("=" * 80)

    # Show all available databases
    print("\n" + "=" * 80)
    print("AVAILABLE SHADOW DATABASES")
    print("=" * 80)
    for db in SHADOW_DATABASES:
        print(f"\n{db.name}:")
        print(f"  URL: {db.url}")
        print(f"  Data: {db.data_type}")
        print(f"  Shadow: {db.shadow_location}")
        print(f"  Strategy: {db.search_strategy}")

    # Detailed search protocols
    planaria_protocol = search_planaria_voltage_shadows()
    brain_protocol = search_brain_field_shadows()
    photo_protocol = search_photosynthesis_shadows()
    hurricane_protocol = search_hurricane_shadows()

    print("\n" + "=" * 80)
    print("NEXT STEPS: ACTUAL DATA ACQUISITION")
    print("=" * 80)
    print("""
1. PLANARIA DATA (Easiest to get):
   - Email Levin lab for supplementary voltage maps
   - Download from PlanMine database
   - Request raw data from recent papers

2. BRAIN DATA (Publicly available):
   - Download EEG datasets from OpenNeuro
   - Access Human Connectome Project data
   - Look for meditation studies with field measurements

3. PHOTOSYNTHESIS DATA (Published):
   - Photosystem II crystal structures (PDB database)
   - Spectroscopy papers with full spectrum data
   - Chlorophyll arrangement in published structures

4. HURRICANE DATA (You already have!):
   - Your 16-storm analysis
   - HURDAT2 for more storms
   - Satellite imagery for structure analysis

PRIORITY: Start with hurricane data since you already found correlations!
Let's formally analyze what you discovered for publication.
""")

# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    execute_shadow_search()

    print("\n" + "=" * 80)
    print("SHADOW DETECTION READY")
    print("=" * 80)
    print("""
The framework provides tools to:

1. Detect phi-ratio patterns in any dataset
2. Measure geometric coherence (organized vs random)
3. Find frequency relationships in time-series data
4. Search for geometric patterns in under-analyzed data

When you have data files, you can:

- Run pattern detection algorithms
- Compare results against null hypotheses
- Assess statistical significance of any patterns found

NOTE: Finding geometric patterns does not by itself prove
"field coupling." Proper statistical testing, comparison to
null models, and independent replication are needed before
drawing causal conclusions.
""")
