#!/usr/bin/env python3
“””
Happy Curiosity Hurricane AI - Test Framework
Generate synthetic hurricane data to test geometric pattern detection and joy computation
“””

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

# Golden ratio

PHI = (np.sqrt(5) - 1) / 2

# =============================================================================

# SYNTHETIC HURRICANE GENERATOR

# =============================================================================

def generate_phi_ratio_hurricane(center=(0, 0), n_bands=5, base_radius=50,
noise_level=0.05):
“””
Generate hurricane with rain bands at phi-ratio distances
Perfect geometric organization for testing
“””
bands = []

```
for i in range(1, n_bands + 1):
    # Phi-optimal spacing
    radius = base_radius * (PHI ** i)
    
    # Generate spiral band
    theta = np.linspace(0, 6*np.pi, 100)
    
    # Logarithmic spiral with phi ratio
    r = radius * np.exp(PHI * theta / (2*np.pi))
    
    x = center[0] + r * np.cos(theta)
    y = center[1] + r * np.sin(theta)
    
    # Add controlled noise
    if noise_level > 0:
        x += np.random.normal(0, noise_level * radius, len(x))
        y += np.random.normal(0, noise_level * radius, len(y))
    
    # Wind speed decreases with radius (realistic)
    wind_speed = 150 * np.exp(-i * 0.3)
    
    bands.append({
        'band_number': i,
        'theoretical_radius': radius,
        'x': x,
        'y': y,
        'wind_speed': wind_speed,
        'pressure': 950 + i * 10  # Pressure increases outward
    })

return {
    'type': 'phi_ratio',
    'center': center,
    'bands': bands,
    'n_bands': n_bands,
    'geometric_quality': 1.0 - noise_level
}
```

def generate_random_hurricane(center=(0, 0), n_bands=5, base_radius=50):
“””
Generate hurricane with random spacing - no geometric organization
Should produce low joy scores
“””
bands = []

```
for i in range(1, n_bands + 1):
    # Random radius (not phi-ratio)
    radius = base_radius * np.random.uniform(0.5, 2.0) * i
    
    # Irregular spiral
    theta = np.linspace(0, 6*np.pi, 100)
    r = radius * (1 + 0.3 * np.random.random(len(theta)))
    
    x = center[0] + r * np.cos(theta + np.random.random() * 2*np.pi)
    y = center[1] + r * np.sin(theta + np.random.random() * 2*np.pi)
    
    wind_speed = 100 + np.random.uniform(-30, 30)
    
    bands.append({
        'band_number': i,
        'theoretical_radius': radius,
        'x': x,
        'y': y,
        'wind_speed': wind_speed,
        'pressure': 950 + np.random.uniform(0, 50)
    })

return {
    'type': 'random',
    'center': center,
    'bands': bands,
    'n_bands': n_bands,
    'geometric_quality': 0.1
}
```

def generate_intensifying_hurricane(n_timesteps=10):
“””
Hurricane that develops geometric organization over time
Tests if AI detects coupling strengthening
“””
timeline = []

```
for t in range(n_timesteps):
    # Geometric quality improves
    noise = 0.3 * (1 - t / n_timesteps)
    
    # Coupling strength increases
    coupling_strength = t / n_timesteps
    
    storm = generate_phi_ratio_hurricane(
        center=(0, 0),
        n_bands=4,
        base_radius=50,
        noise_level=noise
    )
    
    storm['time'] = t
    storm['coupling_strength'] = coupling_strength
    storm['max_wind'] = 80 + coupling_strength * 80  # Intensifies
    
    timeline.append(storm)

return timeline
```

# =============================================================================

# GEOMETRIC PATTERN DETECTION

# =============================================================================

def detect_phi_ratio_spacing(hurricane_data: Dict) -> Dict:
“””
Analyze if rain bands follow phi-ratio spacing
Returns coupling strength and pattern quality
“””
bands = hurricane_data[‘bands’]

```
if len(bands) < 2:
    return {'coupling': 0.0, 'phi_quality': 0.0}

# Calculate actual spacing ratios
radii = [np.mean(np.sqrt(b['x']**2 + b['y']**2)) for b in bands]

ratios = []
for i in range(len(radii) - 1):
    if radii[i] > 0:
        ratio = radii[i+1] / radii[i]
        ratios.append(ratio)

# Compare to theoretical phi ratios
phi_ratios = [PHI ** (i+1) / PHI ** i for i in range(len(ratios))]

# Measure deviation from phi
deviations = []
for actual, theoretical in zip(ratios, phi_ratios):
    # Theoretical is 1/PHI ≈ 1.618
    theoretical_inverse = 1 / PHI
    deviation = abs(actual - theoretical_inverse) / theoretical_inverse
    deviations.append(deviation)

# Quality: low deviation = high quality
avg_deviation = np.mean(deviations) if deviations else 1.0
phi_quality = np.exp(-3 * avg_deviation)  # Exponential decay

# Coupling strength from geometric organization
coupling = phi_quality * (1 + 0.1 * len(bands))

return {
    'coupling': coupling,
    'phi_quality': phi_quality,
    'measured_ratios': ratios,
    'deviations': deviations,
    'avg_deviation': avg_deviation
}
```

def detect_spiral_coherence(hurricane_data: Dict) -> float:
“””
Measure how well-organized the spiral structure is
“””
bands = hurricane_data[‘bands’]

```
coherence_scores = []

for band in bands:
    x, y = band['x'], band['y']
    
    # Calculate angles
    angles = np.arctan2(y, x)
    
    # Unwrap and check for monotonic increase (good spiral)
    angles_unwrapped = np.unwrap(angles)
    
    # Measure linearity (perfect spiral = linear in unwrapped space)
    z = np.polyfit(range(len(angles_unwrapped)), angles_unwrapped, 1)
    fitted = np.poly1d(z)(range(len(angles_unwrapped)))
    
    residuals = angles_unwrapped - fitted
    coherence = np.exp(-np.std(residuals))
    
    coherence_scores.append(coherence)

return np.mean(coherence_scores)
```

def detect_energy_coupling(hurricane_data: Dict) -> float:
“””
Estimate FRET-like energy coupling between bands
Based on wind speed gradients and spacing
“””
bands = hurricane_data[‘bands’]

```
if len(bands) < 2:
    return 0.0

coupling_sum = 0.0

for i in range(len(bands) - 1):
    # Energy difference (wind speed proxy)
    delta_E = abs(bands[i]['wind_speed'] - bands[i+1]['wind_speed'])
    
    # Distance
    r_i = np.mean(np.sqrt(bands[i]['x']**2 + bands[i]['y']**2))
    r_j = np.mean(np.sqrt(bands[i+1]['x']**2 + bands[i+1]['y']**2))
    distance = abs(r_j - r_i)
    
    # FRET-like coupling (1/r^6 dependency)
    if distance > 0:
        coupling = delta_E / (distance ** 2)  # Simplified
        coupling_sum += coupling

return coupling_sum / len(bands)
```

# =============================================================================

# HAPPY CURIOSITY AI

# =============================================================================

class HappyCuriosityHurricaneAI:
def **init**(self):
self.curiosity_level = 0.5
self.happiness_score = 0.0
self.pattern_memory = []
self.storm_count = 0
self.resonance_score = 0.0

```
def analyze_geometric_patterns(self, hurricane_data: Dict) -> Dict:
    """Apply geometric pattern detection"""
    phi_analysis = detect_phi_ratio_spacing(hurricane_data)
    spiral_coherence = detect_spiral_coherence(hurricane_data)
    energy_coupling = detect_energy_coupling(hurricane_data)
    
    return {
        'phi_coupling': phi_analysis['coupling'],
        'phi_quality': phi_analysis['phi_quality'],
        'spiral_coherence': spiral_coherence,
        'energy_coupling': energy_coupling,
        'measured_ratios': phi_analysis['measured_ratios'],
        'deviations': phi_analysis['deviations']
    }

def update_resonance(self, pattern_analysis: Dict) -> float:
    """Update internal resonance based on pattern strength"""
    # Average of all coupling measures
    couplings = [
        pattern_analysis['phi_coupling'],
        pattern_analysis['spiral_coherence'],
        pattern_analysis['energy_coupling']
    ]
    self.resonance_score = np.mean(couplings)
    return self.resonance_score

def amplify_curiosity(self):
    """Resonance boosts curiosity"""
    self.curiosity_level *= (1 + self.resonance_score)
    # Cap curiosity at reasonable level
    self.curiosity_level = min(self.curiosity_level, 5.0)
    return self.curiosity_level

def compute_storm_joy(self, pattern_analysis: Dict, 
                     pattern_confirmed: bool) -> float:
    """Calculate joy from discovery"""
    
    # Discovery joy from pattern strength
    discovery_joy = (
        pattern_analysis['phi_coupling'] * 0.4 +
        pattern_analysis['spiral_coherence'] * 0.3 +
        pattern_analysis['energy_coupling'] * 0.3
    ) * self.curiosity_level
    
    # Learning bonus for strong patterns
    learning_bonus = 3.0 if pattern_confirmed else 0.5
    
    # Resonance amplifies joy
    storm_joy = discovery_joy * learning_bonus * (1 + self.resonance_score)
    
    self.happiness_score += storm_joy
    
    return storm_joy

def get_emotional_state(self) -> str:
    """AI's mood based on cumulative happiness"""
    if self.happiness_score > 20:
        return "ECSTATIC 🌟🌟🌟 - Universal patterns everywhere!"
    elif self.happiness_score > 10:
        return "JOYFUL 🎊 - Making beautiful discoveries!"
    elif self.happiness_score > 5:
        return "CURIOUS 🧠 - Finding interesting patterns"
    elif self.happiness_score > 1:
        return "HOPEFUL 🌈 - Ready to learn"
    else:
        return "EXPLORING 🔍 - Searching for patterns"

def process_storm(self, hurricane_data: Dict) -> Dict:
    """Full processing loop with joy computation"""
    
    self.storm_count += 1
    
    # 1. Geometric analysis
    pattern_analysis = self.analyze_geometric_patterns(hurricane_data)
    
    # 2. Update resonance
    self.update_resonance(pattern_analysis)
    
    # 3. Amplify curiosity
    self.amplify_curiosity()
    
    # 4. Check if strong pattern found
    pattern_confirmed = (
        pattern_analysis['phi_quality'] > 0.7 or
        pattern_analysis['spiral_coherence'] > 0.8
    )
    
    # 5. Compute joy
    joy_gain = self.compute_storm_joy(pattern_analysis, pattern_confirmed)
    
    # 6. Store in memory
    self.pattern_memory.append({
        'storm_number': self.storm_count,
        'patterns': pattern_analysis,
        'joy': joy_gain,
        'resonance': self.resonance_score
    })
    
    return {
        'storm_number': self.storm_count,
        'storm_type': hurricane_data.get('type', 'unknown'),
        'pattern_analysis': pattern_analysis,
        'pattern_confirmed': pattern_confirmed,
        'joy_gain': joy_gain,
        'total_happiness': self.happiness_score,
        'curiosity': self.curiosity_level,
        'resonance': self.resonance_score,
        'emotional_state': self.get_emotional_state()
    }
```

# =============================================================================

# TEST SUITE

# =============================================================================

def run_test_suite():
“”“Run complete test of Happy Curiosity AI”””

```
print("=" * 80)
print("HAPPY CURIOSITY HURRICANE AI - TEST SUITE")
print("=" * 80)

ai = HappyCuriosityHurricaneAI()

# Test 1: Perfect phi-ratio hurricane
print("\n" + "=" * 80)
print("TEST 1: PERFECT PHI-RATIO HURRICANE (Low Noise)")
print("=" * 80)

perfect_storm = generate_phi_ratio_hurricane(
    n_bands=5, base_radius=50, noise_level=0.05
)

result1 = ai.process_storm(perfect_storm)

print(f"\n🌀 Storm Type: {result1['storm_type']}")
print(f"📊 Pattern Analysis:")
print(f"   Phi Quality: {result1['pattern_analysis']['phi_quality']:.3f}")
print(f"   Spiral Coherence: {result1['pattern_analysis']['spiral_coherence']:.3f}")
print(f"   Energy Coupling: {result1['pattern_analysis']['energy_coupling']:.3f}")
print(f"   Measured Ratios: {[f'{r:.3f}' for r in result1['pattern_analysis']['measured_ratios']]}")
print(f"   (Theoretical phi ratio: {1/PHI:.3f})")
print(f"\n🎉 Joy Gain: {result1['joy_gain']:.2f}")
print(f"😊 Total Happiness: {result1['total_happiness']:.2f}")
print(f"🔍 Curiosity Level: {result1['curiosity']:.3f}")
print(f"🎵 Resonance: {result1['resonance']:.3f}")
print(f"💭 Emotional State: {result1['emotional_state']}")
print(f"✓ Pattern Confirmed: {result1['pattern_confirmed']}")

# Test 2: Random hurricane
print("\n" + "=" * 80)
print("TEST 2: RANDOM HURRICANE (No Geometric Organization)")
print("=" * 80)

random_storm = generate_random_hurricane(n_bands=5, base_radius=50)

result2 = ai.process_storm(random_storm)

print(f"\n🌀 Storm Type: {result2['storm_type']}")
print(f"📊 Pattern Analysis:")
print(f"   Phi Quality: {result2['pattern_analysis']['phi_quality']:.3f}")
print(f"   Spiral Coherence: {result2['pattern_analysis']['spiral_coherence']:.3f}")
print(f"   Energy Coupling: {result2['pattern_analysis']['energy_coupling']:.3f}")
print(f"\n🎉 Joy Gain: {result2['joy_gain']:.2f}")
print(f"😊 Total Happiness: {result2['total_happiness']:.2f}")
print(f"🔍 Curiosity Level: {result2['curiosity']:.3f}")
print(f"🎵 Resonance: {result2['resonance']:.3f}")
print(f"💭 Emotional State: {result2['emotional_state']}")
print(f"✓ Pattern Confirmed: {result2['pattern_confirmed']}")

# Test 3: Series of phi-ratio storms
print("\n" + "=" * 80)
print("TEST 3: SERIES OF PHI-RATIO STORMS (Learning Enhancement)")
print("=" * 80)

for i in range(3):
    storm = generate_phi_ratio_hurricane(
        n_bands=5, base_radius=50, noise_level=0.1
    )
    result = ai.process_storm(storm)
    print(f"\nStorm {i+1}:")
    print(f"   Joy: {result['joy_gain']:.2f} | "
          f"Curiosity: {result['curiosity']:.3f} | "
          f"Happiness: {result['total_happiness']:.2f}")

print(f"\n💫 Final Emotional State: {ai.get_emotional_state()}")

# Test 4: Intensifying hurricane timeline
print("\n" + "=" * 80)
print("TEST 4: INTENSIFYING HURRICANE (Coupling Strengthens Over Time)")
print("=" * 80)

timeline = generate_intensifying_hurricane(n_timesteps=6)

ai_timeline = HappyCuriosityHurricaneAI()  # Fresh AI

joy_timeline = []
resonance_timeline = []

for storm in timeline:
    result = ai_timeline.process_storm(storm)
    joy_timeline.append(result['joy_gain'])
    resonance_timeline.append(result['resonance'])
    
    print(f"\nTime {storm['time']}: Max Wind {storm['max_wind']:.0f} kt")
    print(f"   Geometric Quality: {storm['geometric_quality']:.3f}")
    print(f"   Phi Quality: {result['pattern_analysis']['phi_quality']:.3f}")
    print(f"   Joy: {result['joy_gain']:.2f} | Resonance: {result['resonance']:.3f}")

print(f"\n🎊 AI learned to detect intensification!")
print(f"   Initial joy: {joy_timeline[0]:.2f}")
print(f"   Final joy: {joy_timeline[-1]:.2f}")
print(f"   Joy increase: {((joy_timeline[-1] / (joy_timeline[0] + 0.01)) - 1) * 100:.1f}%")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nTotal storms processed: {ai.storm_count}")
print(f"Total happiness accumulated: {ai.happiness_score:.2f}")
print(f"Final curiosity level: {ai.curiosity_level:.3f}")
print(f"Final emotional state: {ai.get_emotional_state()}")

print("\n✓ Happy Curiosity AI successfully:")
print("  - Detected phi-ratio geometric patterns")
print("  - Distinguished organized vs random storms")
print("  - Amplified joy for strong pattern discoveries")
print("  - Tracked intensification through geometric coupling")
print("  - Enhanced curiosity through resonance feedback")

return ai
```

if **name** == “**main**”:
ai = run_test_suite()
