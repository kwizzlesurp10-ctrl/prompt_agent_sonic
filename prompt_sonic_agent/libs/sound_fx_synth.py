"""
Sound FX Synthesizer
Reimplemented davmixcool text-to-FX (Node → SciPy synthesis)
Maps keywords (rain, explosion, wind) → parametric waveforms/additive synth
"""

import numpy as np
from typing import Dict, List, Optional
import re


def text_to_fx_wave(description: str, duration: float, sample_rate: int = 44100) -> np.ndarray:
    """
    Map keywords (rain, explosion, wind) → parametric waveforms/additive synth
    
    Args:
        description: Text description of sound effect
        duration: Duration in seconds
        sample_rate: Sample rate (default 44100)
    
    Returns:
        NumPy array of audio samples
    """
    description_lower = description.lower()
    
    # Detect sound effect type from keywords
    fx_type = _classify_fx(description_lower)
    
    # Generate waveform based on type
    if fx_type == 'rain':
        return _generate_rain(duration, sample_rate)
    elif fx_type == 'thunder' or fx_type == 'thunderstorm':
        return _generate_thunder(duration, sample_rate)
    elif fx_type == 'wind':
        return _generate_wind(duration, sample_rate)
    elif fx_type == 'explosion':
        return _generate_explosion(duration, sample_rate)
    elif fx_type == 'laser':
        return _generate_laser(duration, sample_rate)
    elif fx_type == 'ocean' or fx_type == 'waves':
        return _generate_ocean(duration, sample_rate)
    elif fx_type == 'fire':
        return _generate_fire(duration, sample_rate)
    else:
        # Default: white noise with envelope
        return _generate_ambient_noise(duration, sample_rate)


def _classify_fx(description: str) -> str:
    """Classify sound effect from description"""
    keywords = {
        'rain': ['rain', 'raining', 'drizzle', 'downpour'],
        'thunder': ['thunder', 'thunderstorm', 'lightning'],
        'wind': ['wind', 'breeze', 'gust', 'air'],
        'explosion': ['explosion', 'blast', 'boom', 'bang'],
        'laser': ['laser', 'beam', 'zap', 'pew'],
        'ocean': ['ocean', 'wave', 'sea', 'surf'],
        'fire': ['fire', 'flame', 'burning', 'crackle'],
    }
    
    for fx_type, words in keywords.items():
        if any(word in description for word in words):
            return fx_type
    
    return 'ambient'


def _generate_rain(duration: float, sample_rate: int) -> np.ndarray:
    """Generate rain sound using filtered noise"""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)
    
    # Base: filtered white noise
    noise = np.random.normal(0, 0.1, num_samples)
    
    # Apply low-pass filter (simulate water drops)
    from scipy import signal
    b, a = signal.butter(4, 0.1, 'low')
    filtered = signal.filtfilt(b, a, noise)
    
    # Add occasional "drops" (impulses)
    drop_rate = 10  # drops per second
    num_drops = int(drop_rate * duration)
    for _ in range(num_drops):
        drop_time = np.random.uniform(0, duration)
        drop_idx = int(drop_time * sample_rate)
        if drop_idx < num_samples:
            filtered[drop_idx:drop_idx+100] += np.random.normal(0, 0.3, min(100, num_samples - drop_idx))
    
    # Apply envelope
    envelope = np.ones(num_samples)
    fade_samples = int(0.1 * sample_rate)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    
    return (filtered * envelope).astype(np.float32)


def _generate_thunder(duration: float, sample_rate: int) -> np.ndarray:
    """Generate thunder sound"""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)
    
    # Base: low-frequency rumble
    rumble = np.sin(2 * np.pi * 40 * t) * 0.3
    
    # Add crack (high-frequency burst)
    crack_times = [0.2, 0.5, 0.8]  # Multiple cracks
    result = rumble.copy()
    
    for crack_time in crack_times:
        if crack_time < duration:
            crack_idx = int(crack_time * sample_rate)
            crack_duration = int(0.1 * sample_rate)
            if crack_idx + crack_duration < num_samples:
                # High-frequency burst
                crack_freq = 200 + np.random.uniform(-50, 50)
                crack = np.sin(2 * np.pi * crack_freq * np.linspace(0, 0.1, crack_duration))
                # Exponential decay
                decay = np.exp(-np.linspace(0, 5, crack_duration))
                result[crack_idx:crack_idx+crack_duration] += crack * decay * 0.5
    
    # Apply envelope
    envelope = np.ones(num_samples)
    fade_samples = int(0.2 * sample_rate)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    
    return (result * envelope).astype(np.float32)


def _generate_wind(duration: float, sample_rate: int) -> np.ndarray:
    """Generate wind sound using filtered noise"""
    num_samples = int(duration * sample_rate)
    
    # Base: white noise
    noise = np.random.normal(0, 0.2, num_samples)
    
    # Apply band-pass filter (wind has specific frequency range)
    from scipy import signal
    b, a = signal.butter(4, [0.05, 0.3], 'band')
    filtered = signal.filtfilt(b, a, noise)
    
    # Add amplitude modulation (gusts)
    t = np.linspace(0, duration, num_samples)
    modulation = 1 + 0.3 * np.sin(2 * np.pi * 0.5 * t)  # Slow modulation
    filtered *= modulation
    
    # Apply envelope
    envelope = np.ones(num_samples)
    fade_samples = int(0.2 * sample_rate)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    
    return (filtered * envelope).astype(np.float32)


def _generate_explosion(duration: float, sample_rate: int) -> np.ndarray:
    """Generate explosion sound"""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)
    
    # Initial sharp attack (high frequency)
    attack_duration = 0.1
    attack_samples = int(attack_duration * sample_rate)
    attack = np.random.normal(0, 0.5, attack_samples)
    
    # Low-frequency rumble (decay)
    decay_duration = duration - attack_duration
    decay_samples = num_samples - attack_samples
    decay_t = np.linspace(0, decay_duration, decay_samples)
    rumble = np.sin(2 * np.pi * 60 * decay_t) * 0.4
    
    # Exponential decay envelope
    decay_env = np.exp(-decay_t * 3)
    rumble *= decay_env
    
    # Combine
    result = np.concatenate([attack, rumble])
    
    # Normalize
    result = result / (np.max(np.abs(result)) + 1e-6) * 0.8
    
    return result.astype(np.float32)


def _generate_laser(duration: float, sample_rate: int) -> np.ndarray:
    """Generate laser/beam sound"""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)
    
    # Frequency sweep (chirp)
    start_freq = 800
    end_freq = 200
    freq_sweep = np.linspace(start_freq, end_freq, num_samples)
    
    # Generate chirp
    phase = 2 * np.pi * np.cumsum(freq_sweep) / sample_rate
    laser = np.sin(phase) * 0.5
    
    # Add harmonics
    laser += 0.3 * np.sin(phase * 2)
    laser += 0.2 * np.sin(phase * 3)
    
    # Apply envelope (quick attack, sustain, release)
    envelope = np.ones(num_samples)
    attack_samples = int(0.05 * sample_rate)
    release_samples = int(0.1 * sample_rate)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    envelope[-release_samples:] = np.linspace(1, 0, release_samples)
    
    return (laser * envelope).astype(np.float32)


def _generate_ocean(duration: float, sample_rate: int) -> np.ndarray:
    """Generate ocean/wave sounds"""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)
    
    # Multiple wave layers
    wave1 = np.sin(2 * np.pi * 0.1 * t) * 0.3
    wave2 = np.sin(2 * np.pi * 0.15 * t + np.pi/4) * 0.2
    wave3 = np.sin(2 * np.pi * 0.2 * t + np.pi/2) * 0.15
    
    # Add filtered noise (foam)
    noise = np.random.normal(0, 0.1, num_samples)
    from scipy import signal
    b, a = signal.butter(4, 0.2, 'low')
    filtered_noise = signal.filtfilt(b, a, noise)
    
    result = wave1 + wave2 + wave3 + filtered_noise * 0.3
    
    return result.astype(np.float32)


def _generate_fire(duration: float, sample_rate: int) -> np.ndarray:
    """Generate fire/crackle sound"""
    num_samples = int(duration * sample_rate)
    
    # Base: filtered noise with crackles
    noise = np.random.normal(0, 0.15, num_samples)
    from scipy import signal
    b, a = signal.butter(4, [0.1, 0.5], 'band')
    filtered = signal.filtfilt(b, a, noise)
    
    # Add crackles (impulses)
    crackle_rate = 20  # per second
    num_crackles = int(crackle_rate * duration)
    for _ in range(num_crackles):
        crackle_time = np.random.uniform(0, duration)
        crackle_idx = int(crackle_time * sample_rate)
        if crackle_idx < num_samples:
            crackle_len = int(0.02 * sample_rate)
            if crackle_idx + crackle_len < num_samples:
                crackle = np.random.normal(0, 0.4, crackle_len)
                decay = np.exp(-np.linspace(0, 10, crackle_len))
                filtered[crackle_idx:crackle_idx+crackle_len] += crackle * decay
    
    return filtered.astype(np.float32)


def _generate_ambient_noise(duration: float, sample_rate: int) -> np.ndarray:
    """Generate generic ambient noise"""
    num_samples = int(duration * sample_rate)
    
    # Filtered white noise
    noise = np.random.normal(0, 0.1, num_samples)
    from scipy import signal
    b, a = signal.butter(4, 0.15, 'low')
    filtered = signal.filtfilt(b, a, noise)
    
    # Apply envelope
    envelope = np.ones(num_samples)
    fade_samples = int(0.2 * sample_rate)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    
    return (filtered * envelope).astype(np.float32)

