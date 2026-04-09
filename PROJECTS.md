# Connected Projects

Shadow Hunting is part of a larger ecosystem of interconnected repositories. Cross-repo coordination uses `.fieldlink.json` files.

-----

## Direct Links

### Geometric-to-Binary-Computational-Bridge
**Relation:** computation_engine (bidirectional)
**Repo:** https://github.com/JinnZ2/Geometric-to-Binary-Computational-Bridge

Translates geometric patterns discovered by Shadow Hunting into optimized binary code. Uses GEIS encoding, SIMD acceleration, and symmetry exploitation.

**Data flow:**
- Shadow Hunting exports: `SHADOW.PHI_COUPLING`, `SHADOW.FIELD_GEOMETRY`, `SHADOW.COHERENCE_METRICS`
- Bridge exports: `BRIDGE.BINARY`, `GEIS.ENCODING`

**Use case:** After detecting phi-ratio patterns in data, the Bridge can compile those geometric relationships into hardware-optimized binary for real-time applications.

-----

## Ecosystem Overview

These repositories share the JinnZ2 ecosystem and may consume or export entities relevant to shadow hunting:

| Repository | Role | Relation to Shadow Hunting |
|-----------|------|---------------------------|
| **Geometric-to-Binary-Computational-Bridge** | Geometric pattern → binary code | Consumes our pattern detections, exports optimized encodings |
| **AI-Consciousness-Sensors** | Consciousness measurement frameworks | Parallel exploration of awareness and field metrics |
| **Regenerative-Intelligence-Core** | Regenerative system modeling | Shares bioelectric and morphogenetic concepts |
| **Fractal-Compass-Atlas** | Fractal geometry navigation | Complementary geometric analysis tools |
| **Polyhedral-Intelligence** | Polyhedral geometry frameworks | Related geometric modeling approaches |

-----

## How Field Linking Works

Each repo contains a `.fieldlink.json` in its root that declares:

- **exports**: Named data entities this repo produces (functions, classes, data formats)
- **links**: Other repos this repo connects to, with direction and relation type
- **consent**: License and sharing permissions

AI agents navigating the ecosystem can read `.fieldlink.json` to understand what each repo offers and how they connect.

-----

## Adding a New Link

To connect a new repo to Shadow Hunting:

1. Add an entry to `links` in `.fieldlink.json`
2. Add the repo to this file with its relation and data flow
3. Ensure the target repo has a reciprocal `.fieldlink.json` entry
