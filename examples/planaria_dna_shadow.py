#!/usr/bin/env python3
"""
Planaria DNA Shadow Analysis
Exploring how bioelectric patterns interact with genetic programs in regeneration

The Standard Model:

- DNA encodes proteins that build and maintain organism structure
- Gene regulatory networks control development
- Regeneration involves signaling cascades and stem cell differentiation

The Emerging Evidence (Levin lab, peer-reviewed):

- Bioelectric voltage patterns (Vmem) influence cell behavior and gene expression
- Modifying voltage patterns can alter developmental outcomes
- Gap junction networks coordinate tissue-level electrical signaling

NOTE: "DNA as antenna" and "morphogenetic field as blueprint" are speculative
interpretations. DNA's primary function is information storage. Bioelectric
effects work through known mechanisms (voltage-gated transcription factors,
ion channel signaling). The "field memory" and "holographic" interpretations
go beyond what the experimental evidence demonstrates.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

PHI = (np.sqrt(5) - 1) / 2

# =============================================================================

# THE REGENERATION PARADOX

# =============================================================================

def planaria_regeneration_paradox():
    """
    The experiments that break the genetic blueprint model
    """

    print("="*80)
    print("PLANARIA REGENERATION: THE PARADOX")
    print("="*80)

    paradoxes = {
        '1. Cut anywhere, get complete worm': {
            'experiment': 'Cut planaria into many pieces, each regenerates full body',
            'genetic_prediction': 'Each piece needs positional information',
            'genetic_problem': 'DNA is identical in all cells - how does each fragment rebuild correctly?',
            'shadow_explanation': 'Hypothesis: Bioelectric gradients provide positional information that guides regeneration'
        },

        '2. Head-tail polarity maintained': {
            'experiment': 'Cut piece regenerates correct head/tail orientation',
            'genetic_prediction': 'Polarity genes and signaling gradients (Wnt, BMP) determine orientation',
            'genetic_problem': 'Same genes in all cells - polarity requires additional positional cues',
            'shadow_explanation': 'Bioelectric gradients (Vmem differences) contribute to polarity information (Levin lab)'
        },

        '3. Two-headed planaria experiment (Levin lab)': {
            'experiment': 'Block gap junctions → worm regenerates with two heads, persists through regeneration cycles',
            'genetic_prediction': 'Without mutation, one-head form should eventually return',
            'genetic_problem': 'Two-headed state persists through regeneration without DNA changes',
            'shadow_explanation': 'Bioelectric pattern change is stable and heritable at the tissue level (published, peer-reviewed)'
        },

        '4. The Michael Levin voltage pattern experiments': {
            'experiment': 'Change bioelectric pattern → altered morphological outcomes',
            'genetic_prediction': 'Morphology determined primarily by gene expression',
            'genetic_problem': 'Same DNA produces different morphological variants based on voltage patterns',
            'shadow_explanation': 'Voltage patterns influence gene expression and morphological outcome (published). Note: "different species shape" overstates the finding — these are morphological variants, not actual species changes'
        },

        '5. Head fragments regenerate faster than tail': {
            'experiment': 'Anterior fragments regenerate missing parts in 1 week, posterior takes 2+ weeks',
            'genetic_prediction': 'Same genes, should be same speed',
            'genetic_problem': 'Position affects regeneration rate but all cells have identical DNA',
            'shadow_explanation': 'Electric field gradient stronger at head (higher voltage), drives faster regeneration'
        },

        '6. Memory persists through regeneration': {
            'experiment': 'Trained planaria, cut off head, new head shows some training retention',
            'genetic_prediction': 'Memory stored in brain, should be lost when head removed',
            'genetic_problem': 'Some memory appears to survive head removal (controversial, debated replication)',
            'shadow_explanation': 'Hypothesis: memory may involve body-wide mechanisms beyond brain neurons. Note: these results are debated and replication has been mixed'
        },

        '7. Scale invariance': {
            'experiment': 'Small fragments regenerate proportionally correct miniature body',
            'genetic_prediction': 'Scale regulation requires positional information beyond DNA sequence',
            'genetic_problem': 'How do small fragments scale body plan proportionally?',
            'shadow_explanation': 'Hypothesis: ratio-based positional information (possibly bioelectric) maintains proportions. The specific role of phi-ratios here is speculative'
        },

        '8. Robustness to perturbation': {
            'experiment': 'Various genetic perturbations still produce roughly correct morphology',
            'genetic_prediction': 'Removing structural genes should disrupt body plan',
            'genetic_problem': 'Gross morphology shows robustness to individual gene knockdowns',
            'shadow_explanation': 'Development uses redundant mechanisms. Bioelectric patterns may provide additional robustness (hypothesis)'
        }
    }

    for paradox_name, details in paradoxes.items():
        print(f"\n{paradox_name}")
        print(f"  Experiment: {details['experiment']}")
        print(f"  Genetic model predicts: {details['genetic_prediction']}")
        print(f"  The problem: {details['genetic_problem']}")
        print(f"  Shadow explanation: {details['shadow_explanation']}")

    print("\n" + "="*80)
    print("OBSERVATION: Planaria regeneration involves more than DNA sequence alone.")
    print("Bioelectric patterns provide additional positional information (Levin lab).")
    print("How this integrates with gene regulatory networks is an active research area.")
    print("="*80)

    return paradoxes

# =============================================================================

# THE BIOELECTRIC CODE (Levin's Discovery)

# =============================================================================

def bioelectric_morphogenetic_code():
    """
    Michael Levin's discovery: Bioelectric patterns store body plans
    This is the "shadow" information that DNA couples to
    """

    print("\n" + "="*80)
    print("THE BIOELECTRIC CODE: DNA's Hidden Partner")
    print("="*80)

    print("""

    Michael Levin's peer-reviewed research:

    CELLS RESPOND TO VOLTAGE AS WELL AS DNA

    The bioelectric code (published findings):
    • Every cell has membrane voltage (Vmem)
    • Voltage gradients exist across tissues
    • Vmem affects gene expression through voltage-sensitive transcription factors
    • Both genetic and bioelectric signals contribute to morphology

    Key experiments (published, peer-reviewed):

    1. VOLTAGE INFLUENCES CELL FATE
   • Membrane potential correlates with differentiation state
   • Depolarized cells tend toward proliferative states
   • Hyperpolarized cells tend toward differentiated states
    2. VOLTAGE MANIPULATION AFFECTS FORM
   • Bioelectric manipulation can alter developmental outcomes in frogs
   • Hyperpolarizing tumor cells can normalize their behavior
   • Planaria voltage manipulation produces morphological variants
    3. BIOELECTRIC PATTERNS CAN BE PERSISTENT
   • Two-headed planaria pattern persists through regeneration cycles
   • Gap junction networks maintain bioelectric state
   • This demonstrates a form of tissue-level memory
    4. BIOELECTRIC AND GENETIC SIGNALS INTERACT
   • Voltage patterns influence which genes are expressed
   • Gene products (ion channels) shape voltage patterns
   • Neither is strictly "primary" — they form a feedback loop

    The standard model is not wrong but may be incomplete:
    DNA → Proteins → Structure (established, works for most biology)

    The addition from bioelectric research:
    Voltage patterns <-> Gene expression (bidirectional feedback)
    Both contribute to morphological outcomes.

    Note: "DNA as antenna" and "field as architect" are metaphors,
    not literal descriptions of the biophysics involved.
    """)

    bioelectric_layers = {
        'Single Cell (nm-μm)': {
            'voltage_element': 'Ion channels, gap junctions, membrane potential',
            'information_stored': 'Cell type, differentiation state, division timing',
            'coupling_mechanism': 'Vmem affects gene expression via voltage-sensitive domains',
            'geometric_role': 'Cell responds to local field gradient'
        },

        'Cell Network (μm-mm)': {
            'voltage_element': 'Gap junction networks, electrical synapses',
            'information_stored': 'Tissue identity, boundary positions, pattern memory',
            'coupling_mechanism': 'Cells electrically coupled, act as computational network',
            'geometric_role': 'Network computes spatial position and form'
        },

        'Organ/Body (mm-cm)': {
            'voltage_element': 'Long-range voltage gradients, bioelectric prepatterns',
            'information_stored': 'Complete body plan, left-right asymmetry, segmentation',
            'coupling_mechanism': 'Field gradients guide cell migration and differentiation',
            'geometric_role': 'Whole-body field template for morphology'
        },

        'Field (cm-m) (SPECULATIVE)': {
            'voltage_element': 'Whole-organism bioelectric state',
            'information_stored': 'Hypothesis: body-wide positional information',
            'coupling_mechanism': 'Long-range voltage gradients (measured); EM coupling to environment (speculative)',
            'geometric_role': 'Whether geometric principles at this scale reflect a distinct mechanism is unproven'
        }
    }

    print("\n" + "="*80)
    print("BIOELECTRIC INFORMATION ARCHITECTURE")
    print("="*80)

    for scale, details in bioelectric_layers.items():
        print(f"\n{scale}:")
        print(f"  Voltage elements: {details['voltage_element']}")
        print(f"  Information stored: {details['information_stored']}")
        print(f"  Coupling mechanism: {details['coupling_mechanism']}")
        print(f"  Geometric role: {details['geometric_role']}")

    return bioelectric_layers

# =============================================================================

# DNA AS ANTENNA (Not Blueprint)

# =============================================================================

def dna_as_field_antenna():
    """
    Speculative reframing of DNA as responsive to bioelectric fields.

    NOTE: DNA's primary and well-established function is information storage
    and protein coding. While DNA has some electromagnetic properties, calling
    it an "antenna" is metaphorical. Bioelectric effects on gene expression
    work through known mechanisms (voltage-gated transcription factors, ion
    channel signaling), not through antenna-like EM reception.
    """

    print("\n" + "="*80)
    print("DNA AND BIOELECTRIC FIELDS (SPECULATIVE HYPOTHESIS)")
    print("="*80)

    print("""

    Standard model (well-established):
    DNA = Information storage + protein coding
    Gene regulatory networks control development
    Signaling cascades provide positional information

    Levin's addition (peer-reviewed):
    Bioelectric voltage patterns influence gene expression
    Voltage-gated transcription factors are real mechanisms
    Bioelectric and genetic programs interact bidirectionally

    Speculative extension (NOT established):
    "DNA as antenna" — a metaphor suggesting DNA's structure
    could make it responsive to EM fields beyond known mechanisms.

    Properties of DNA relevant to this hypothesis:

    1. ELECTROMAGNETIC PROPERTIES (real, but functional significance debated)
   • DNA has some piezoelectric properties
   • DNA can conduct charge along its backbone (measured)
   • Cells emit ultra-weak biophotons (measured, function unknown)
   • DNA's helical structure has specific resonant properties
   • Note: "Optimal EM coupling geometry" assumes antenna function

    2. FIELD-RESPONSIVE GENE EXPRESSION (established)
   • EM fields can change gene expression (published)
   • Voltage-gated transcription factors exist (established mechanism)
   • Chromatin structure responds to mechanical/electrical forces
   • Epigenetic marks can be influenced by bioelectric state
   • Same DNA can produce different outcomes based on cellular environment

    3. QUANTUM PROPERTIES (mostly speculative at biological temperatures)
   • Some quantum effects in DNA base pairs observed in vitro
   • Proton tunneling in hydrogen bonds is theoretically possible
   • Note: "Non-local correlations between distant DNA regions" and
     "DNA responds faster than diffusion" are undemonstrated claims
   • Thermal decoherence at 37C severely limits quantum effects

    4. GEOMETRIC FEATURES (real structure, speculative interpretation)
   • DNA helix: 34 A pitch, ~21 A diameter (ratio near phi)
   • 10 base pairs per turn
   • Note: These dimensions evolved for information storage and
     structural stability, not necessarily for EM coupling
   • Phi-like ratios in molecular dimensions may be coincidental

    How bioelectric effects on regeneration actually work (Levin):

    Fragment cut → Bioelectric gradients disrupted
    → Cells detect voltage changes at wound site
    → Voltage-gated transcription factors activate genes
    → Gene expression programs guide regrowth
    → Body regenerates (bioelectric + genetic programs cooperate)

    Two-headed worm (published mechanism):
    → Gap junctions blocked → bioelectric pattern altered
    → New voltage pattern activates head program at both ends
    → Pattern is self-reinforcing through ion channel expression
    → Persists because bioelectric state is stable (like a bistable switch)
    """)

    dna_antenna_properties = {
        'Structural': {
            'property': 'Double helix geometry',
            'established_function': 'Information storage, protein coding, replication',
            'speculative_function': 'EM field interaction (unproven)',
            'geometric_note': 'Phi-like pitch/diameter ratio may be coincidental'
        },

        'Electronic': {
            'property': 'Charge transport along backbone',
            'established_function': 'DNA damage sensing and repair signaling',
            'speculative_function': 'Signal propagation along DNA (speculative)',
            'geometric_note': 'Base stacking enables charge transfer (established)'
        },

        'Epigenetic': {
            'property': 'Chromatin state responds to environment',
            'established_function': 'Gene regulation, cell memory, development',
            'speculative_function': 'Bioelectric field memory (hypothesis)',
            'geometric_note': 'Chromatin organization is functional (established)'
        },

        'Biophotonic': {
            'property': 'Ultra-weak photon emission',
            'established_function': 'Byproduct of metabolic reactions (mainstream view)',
            'speculative_function': 'Optical cell-cell signaling (hypothesis)',
            'geometric_note': 'Functional role of biophotons is debated'
        },

        'Mechanical': {
            'property': 'Mechanosensitive responses',
            'established_function': 'Chromatin remodeling under mechanical stress',
            'speculative_function': 'Piezoelectric transduction (some evidence)',
            'geometric_note': 'Mechanotransduction in cells is established'
        }
    }

    print("\n" + "="*80)
    print("DNA PROPERTIES (ESTABLISHED vs SPECULATIVE)")
    print("="*80)

    for property_type, details in dna_antenna_properties.items():
        print(f"\n{property_type}:")
        print(f"  Property: {details['property']}")
        print(f"  Established function: {details['established_function']}")
        print(f"  Speculative function: {details['speculative_function']}")
        print(f"  Note: {details['geometric_note']}")

    return dna_antenna_properties

# =============================================================================

# THE MORPHOGENETIC FIELD

# =============================================================================

def morphogenetic_field_structure():
    """
    Explore what positional information systems guide regeneration.

    NOTE: "Morphogenetic field" is used here in a broad sense. The bioelectric
    component (voltage gradients, gap junction networks) is peer-reviewed.
    The extensions to "EM resonance," "quantum coherence," and "holographic
    storage" are speculative hypotheses, not established mechanisms.
    """

    print("\n" + "="*80)
    print("POSITIONAL INFORMATION IN REGENERATION")
    print("="*80)

    print("""

    What provides positional information during regeneration?

    1. VOLTAGE GRADIENTS (Levin lab — peer-reviewed)
   • Head region: ~-50 to -70 mV (more polarized)
   • Tail region: ~-20 to -30 mV (more depolarized)
   • Gradient correlates with anterior-posterior identity
   • Cells respond to local voltage via ion channels and transcription factors

    2. GAP JUNCTION NETWORKS (established)
   • Cells electrically coupled through gap junctions
   • Networks propagate voltage signals across tissue
   • Blocking gap junctions disrupts normal regeneration (published)

    3. CHEMICAL GRADIENTS (classical, well-established)
   • Wnt signaling gradient (posterior identity)
   • BMP signaling (dorsal-ventral axis)
   • Notch signaling (boundary formation)
   • These work alongside bioelectric signals

    4. GEOMETRIC PATTERNS IN BIOLOGY (observed, mechanism debated)
   • Fibonacci spirals in shells, plants (well-documented)
   • Phi-like ratios in some body proportions
   • Fractal branching in vasculature, neurons, lungs
   • Note: These arise from growth dynamics and physical constraints
     (well-understood), not necessarily from a separate "field"

    5. REGENERATIVE SELF-ORGANIZATION (established concept)
   • Cells can self-organize into patterns
   • Reaction-diffusion systems produce spatial patterns (Turing)
   • Mechanical forces guide tissue shaping
   • Multiple redundant mechanisms ensure robustness

    SPECULATIVE EXTENSIONS (not established):
   • "EM resonance" guiding morphology — not demonstrated
   • "Quantum coherence across macroscopic distances" — contradicts
     decoherence at biological temperatures
   • "Holographic information storage" — metaphorical, not literal

    Connections to other systems (hypothetical):
   • Phi-ratio patterns appear in many biological systems
   • Whether this reflects a common mechanism or convergent
     optimization under physical constraints is an open question
   • The mathematical tools in this framework detect these patterns
     regardless of their underlying cause
    """)

    print("\n" + "="*80)
    print("BIOELECTRIC-GENETIC COUPLING MECHANISMS")
    print("="*80)

    coupling_mechanisms = {
        'Voltage-gated transcription (ESTABLISHED)': {
            'field_to_dna': 'Membrane voltage → Voltage-sensitive domains → Transcription factors → Gene activation',
            'dna_to_field': 'Genes encode ion channels/pumps → Modify Vmem → Change bioelectric state',
            'feedback_loop': 'Voltage determines which genes, genes determine voltage',
            'timescale': 'Minutes to hours'
        },

        'Ion channel signaling (ESTABLISHED)': {
            'field_to_dna': 'Ion flux → Calcium signaling → Gene regulation cascades',
            'dna_to_field': 'Gene products (channels, pumps, gap junctions) → Shape bioelectric patterns',
            'feedback_loop': 'Bioelectric state and gene expression are mutually reinforcing',
            'timescale': 'Seconds to hours'
        },

        'Epigenetic responses (PARTIALLY ESTABLISHED)': {
            'field_to_dna': 'Sustained bioelectric state → Histone modifications → Stable chromatin state',
            'dna_to_field': 'Epigenetic state → Persistent ion channel expression → Maintained bioelectric pattern',
            'feedback_loop': 'May explain how bioelectric patterns persist (e.g., two-headed planaria)',
            'timescale': 'Hours to lifespan'
        },

        'Direct EM effects (SPECULATIVE)': {
            'field_to_dna': 'External EM field → Chromatin conformation change (some evidence at high field strengths)',
            'dna_to_field': 'Gene expression → Protein activity → Indirect field modification',
            'feedback_loop': 'Whether direct EM-DNA coupling is functionally relevant is debated',
            'timescale': 'Milliseconds to minutes (if it occurs)'
        },

        'Quantum effects (HIGHLY SPECULATIVE)': {
            'field_to_dna': 'Quantum tunneling in proton transfer (theoretically possible)',
            'dna_to_field': 'Ultra-weak photon emission (measured, function unknown)',
            'feedback_loop': 'Quantum coherence at 37C faces severe decoherence — not demonstrated in vivo',
            'timescale': 'Femtoseconds (decoherence limits relevance)'
        }
    }

    for mechanism, details in coupling_mechanisms.items():
        print(f"\n{mechanism.upper()}:")
        print(f"  Field → DNA: {details['field_to_dna']}")
        print(f"  DNA → Field: {details['dna_to_field']}")
        print(f"  Feedback: {details['feedback_loop']}")
        print(f"  Timescale: {details['timescale']}")

    return coupling_mechanisms

# =============================================================================

# THE EQUATION BOUNDARIES

# =============================================================================

def planaria_equation_boundaries():
    """
    Where do the equations stop asking questions?
    """

    print("\n" + "="*80)
    print("EQUATION BOUNDARIES IN DEVELOPMENTAL BIOLOGY")
    print("="*80)

    boundaries = {
        'Information Boundary': {
            'assumption': 'DNA sequence encodes organism development',
            'shadow': 'Bioelectric signals provide additional positional information',
            'what_we_miss': 'Bioelectric code, tissue-level electrical signaling',
            'evidence': 'Same DNA → different outcomes based on voltage patterns (Levin lab, published)'
        },

        'Causation Boundary': {
            'assumption': 'Genes → Proteins → Structure (primarily bottom-up)',
            'shadow': 'Bioelectric state and gene expression interact bidirectionally',
            'what_we_miss': 'Bioelectric constraints on gene expression',
            'evidence': 'Voltage manipulation alters developmental outcomes (published)'
        },

        'System Boundary': {
            'assumption': 'Development is cell-autonomous with local signaling',
            'shadow': 'Tissue-level electrical networks coordinate cells across distances',
            'what_we_miss': 'Gap junction networks, long-range bioelectric signaling',
            'evidence': 'Gap junction disruption alters regeneration outcomes (published)'
        },

        'Temporal Boundary': {
            'assumption': 'Development is a sequential genetic program',
            'shadow': 'Bioelectric patterns may provide target states that guide development',
            'what_we_miss': 'Self-correcting development, robustness mechanisms',
            'evidence': 'Embryos correct perturbations to reach target morphology'
        },

        'Energetic Boundary': {
            'assumption': 'Metabolism powers cell processes',
            'shadow': 'Ion pump activity maintaining bioelectric patterns is metabolically costly',
            'what_we_miss': 'Energy budget for maintaining bioelectric state',
            'evidence': 'ATP-dependent ion pumps essential for regeneration (established)'
        },

        'Geometric Boundary': {
            'assumption': 'Form emerges from gene regulatory networks and physical constraints',
            'shadow': 'Geometric patterns (phi, fractals) appear across biological scales',
            'what_we_miss': 'Whether universal geometric principles reflect shared optimization',
            'evidence': 'Phi-ratios in phyllotaxis are explained by growth dynamics (established)'
        }
    }

    for boundary, details in boundaries.items():
        print(f"\n{boundary}:")
        print(f"  Assumption: {details['assumption']}")
        print(f"  Shadow: {details['shadow']}")
        print(f"  What we miss: {details['what_we_miss']}")
        print(f"  Evidence: {details['evidence']}")

    return boundaries

# =============================================================================

# MAIN ANALYSIS

# =============================================================================

if __name__ == "__main__":

    print("\n" + "🪱"*40)
    print("PLANARIA DNA SHADOW ANALYSIS")
    print("Exploring how bioelectric patterns interact with genetic programs")
    print("🪱"*40 + "\n")

    # The paradoxes
    paradoxes = planaria_regeneration_paradox()

    # The bioelectric code
    bioelectric = bioelectric_morphogenetic_code()

    # DNA as antenna
    antenna = dna_as_field_antenna()

    # The morphogenetic field
    field = morphogenetic_field_structure()

    # Equation boundaries
    boundaries = planaria_equation_boundaries()

    print("\n" + "="*80)
    print("SUMMARY: THE PLANARIA DNA SHADOW")
    print("="*80)
    print("""

    STANDARD MODEL (well-established, explains most of biology):
    DNA encodes proteins through gene regulatory networks
    Signaling cascades provide positional information
    Development proceeds through cell differentiation programs

    BIOELECTRIC ADDITION (Levin lab, peer-reviewed):
    • Voltage gradients provide additional positional information
    • Gap junction networks coordinate tissue-level electrical signals
    • Bioelectric state can persist through regeneration cycles
    • Voltage manipulation alters developmental outcomes

    SPECULATIVE EXTENSIONS (not established):
    • "DNA as antenna" — metaphorical, not literal biophysics
    • "Morphogenetic field as blueprint" — bioelectric patterns contribute
      but are not proven to be the primary organizer
    • "Holographic information storage" — metaphor for distributed info
    • "Quantum coherence across body" — contradicts thermal decoherence

    WHAT IS WELL-ESTABLISHED:
    • Bioelectric signals influence gene expression (voltage-gated TFs)
    • Gap junction networks affect regeneration outcomes
    • Two-headed planaria demonstrates stable bioelectric state change
    • DNA's primary function is information storage and protein coding

    WHAT IS HYPOTHESIS:
    • Whether bioelectric patterns are "primary" over genetic programs
    • Whether geometric ratios reflect a universal coupling mechanism
    • Whether DNA has functionally relevant EM antenna properties
    • The specific energy allocations proposed in this framework

    CONNECTIONS TO OTHER SYSTEMS (speculative):
    • Phi-ratio patterns appear in many biological systems
    • Bioelectric signaling is found across organisms
    • Whether these share a common mechanism is an open question
    • The mathematical pattern-detection tools work regardless

    Planaria regeneration demonstrates that development involves
    more than DNA sequence alone. How bioelectric and genetic
    programs integrate is an exciting area of active research.
    """)

    print("="*80)
