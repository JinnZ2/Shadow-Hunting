# Shadow Hunting Framework - Development Guide

## Project Overview

Scientific framework for detecting geometric field coupling patterns (phi-ratios, fibonacci sequences, field coherence) hidden in data that researchers typically filter out as "noise." Covers four systems: photosynthesis, brain energy, hurricanes, and planaria/DNA regeneration.

## Repository Structure

```
shadow-hunting/
├── CLAUDE.md                # This file - development conventions
├── README.md                # Project overview and documentation
├── Tutorial.md              # Step-by-step shadow hunting guide
├── LICENSE                  # MIT License
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Package configuration
│
├── shadow_hunting/          # Main Python package
│   ├── __init__.py          # Shared constants (PHI, FIBONACCI) and package info
│   ├── shadow_data_mining.py    # Database catalog + shadow detection algorithms
│   ├── bioelectric_protocol.py  # Bioelectric tissue regeneration protocols
│   ├── coupling_framework.py    # Universal geometric coupling framework
│   └── tools/                   # Interactive exploration tools
│       ├── __init__.py          # Tool exports (hunt_shadows, quick_scan)
│       ├── explorer.py          # Unified shadow hunting interface
│       ├── powers_and_roots.py  # Reverse method of powers and roots
│       ├── root_decimals.py     # Root of decimals analysis
│       └── chordal_dimensions.py # Chordal dimension analysis
│
└── examples/                # Example analyses and demonstrations
    ├── brain_energy_shadow.py       # Brain energy accounting analysis
    ├── photosynthesis_shadow.py     # Photosynthesis efficiency reframing
    ├── planaria_dna_shadow.py       # DNA as field antenna analysis
    └── happy_curiosity_test.py      # Hurricane AI with joy computation
```

## Conventions

### Python Style
- **PEP 8** naming: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE` for constants
- **Type hints** on all public function signatures
- **Docstrings** on all public functions and classes
- Standard library imports first, then third-party (`numpy`, `scipy`, `matplotlib`), then local

### Shared Constants
Import shared constants from the package root instead of redefining:
```python
from shadow_hunting import PHI, FIBONACCI
```

### Key Constants
- `PHI = (np.sqrt(5) - 1) / 2` — Golden ratio conjugate (~0.618)
- `FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]`

### Dependencies
- `numpy` — numerical computation
- `matplotlib` — visualization
- `scipy` — signal processing (find_peaks, FFT helpers)
- See `requirements.txt` for version pins

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Install as editable package
pip install -e .

# Run an example
python -m examples.brain_energy_shadow
python -m examples.happy_curiosity_test

# Run core modules
python -m shadow_hunting.shadow_data_mining
python -m shadow_hunting.bioelectric_protocol
python -m shadow_hunting.coupling_framework

# Run exploration tools
python -m shadow_hunting.tools.explorer
python -m shadow_hunting.tools.powers_and_roots
python -m shadow_hunting.tools.root_decimals
python -m shadow_hunting.tools.chordal_dimensions
```

## Architecture Notes

- All four analysis systems (photosynthesis, brain, hurricane, planaria) share the same geometric coupling model
- Core detection algorithms live in `shadow_data_mining.py`: `detect_phi_ratios()`, `detect_fibonacci_sequences()`, `detect_geometric_coherence()`, `detect_field_coupling_signature()`
- `coupling_framework.py` provides the universal `GeometricCouplingSystem` base class
- `bioelectric_protocol.py` contains the `MorphogeneticField` and `RegenerationSimulator` classes
- Example files are standalone analyses that demonstrate the framework on specific systems
- `tools/` provides interactive exploration tools:
  - `explorer.py`: Unified `hunt_shadows()` interface — runs all detectors on any data
  - `powers_and_roots.py`: Reverse-engineer power/root relationships, find phi in exponents
  - `root_decimals.py`: Analyze decimal structure of nth roots for hidden patterns
  - `chordal_dimensions.py`: Chord geometry analysis, golden angle spacing, dimensional coupling
