"""
Utility functions for music generation pipeline
Helpers: extract_notation, infer_params, render_midi_to_wave, mix_audio
"""

import re
import numpy as np
from typing import Dict, List, Optional, Tuple
from midiutil import MIDIFile
from scipy.io import wavfile


def extract_notation_from_prompt(prompt: str) -> Optional[str]:
    """
    Extract ABC-like notation hints from prompt using NLP/simple regex
    
    Args:
        prompt: User prompt text
    
    Returns:
        ABC notation snippet if found, None otherwise
    """
    # Look for patterns like "CDEFG", "C D E F G", "C4 D4 E4", etc.
    # Also look for explicit ABC notation markers
    
    # Check for explicit ABC notation
    abc_match = re.search(r'ABC[:\s]+([A-G][#b]?[\s\d,/\']+)', prompt, re.IGNORECASE)
    if abc_match:
        return abc_match.group(1).strip()
    
    # Look for note sequences (C, D, E, F, G, A, B with optional numbers)
    note_pattern = r'\b([A-G][#b]?\d*[\s,]+){3,}'  # At least 3 notes
    match = re.search(note_pattern, prompt, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    
    # Look for simple note letters (CDEFG pattern)
    simple_pattern = r'\b([CDEFGAB]{3,})\b'
    match = re.search(simple_pattern, prompt, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return None


def infer_params(prompt: str) -> Dict:
    """
    Infer composition parameters from prompt text
    
    Args:
        prompt: User prompt text
    
    Returns:
        Dictionary with inferred parameters:
        {
            'tempo': int,
            'instruments': List[str],
            'mood': str,
            'harmony': str,
            'variation': str
        }
    """
    prompt_lower = prompt.lower()
    
    # Infer tempo
    tempo = 120  # Default
    tempo_match = re.search(r'\b(\d+)\s*bpm\b', prompt_lower)
    if tempo_match:
        tempo = int(tempo_match.group(1))
    elif any(word in prompt_lower for word in ['fast', 'quick', 'upbeat', 'energetic']):
        tempo = 140
    elif any(word in prompt_lower for word in ['slow', 'lazy', 'relaxed', 'calm']):
        tempo = 80
    
    # Infer instruments
    instruments = ['piano']  # Default
    instrument_keywords = {
        'piano': ['piano', 'keyboard'],
        'guitar': ['guitar', 'acoustic'],
        'strings': ['string', 'violin', 'cello', 'orchestra', 'orchestral'],
        'brass': ['brass', 'trumpet', 'horn'],
        'flute': ['flute', 'woodwind'],
        'saxophone': ['sax', 'saxophone'],
    }
    
    found_instruments = []
    for inst, keywords in instrument_keywords.items():
        if any(keyword in prompt_lower for keyword in keywords):
            found_instruments.append(inst)
    
    if found_instruments:
        instruments = found_instruments
    elif 'epic' in prompt_lower or 'orchestra' in prompt_lower:
        instruments = ['strings', 'brass', 'piano']
    
    # Infer mood
    mood = 'neutral'
    mood_keywords = {
        'happy': ['happy', 'joyful', 'cheerful', 'upbeat'],
        'sad': ['sad', 'melancholy', 'somber', 'mournful'],
        'epic': ['epic', 'grand', 'heroic', 'dramatic', 'cinematic'],
        'calm': ['calm', 'peaceful', 'serene', 'tranquil'],
        'energetic': ['energetic', 'intense', 'powerful', 'driving'],
    }
    
    for mood_type, keywords in mood_keywords.items():
        if any(keyword in prompt_lower for keyword in keywords):
            mood = mood_type
            break
    
    # Infer harmony
    harmony = 'triads'
    if 'complex' in prompt_lower or 'rich' in prompt_lower:
        harmony = 'sevenths'
    elif 'simple' in prompt_lower or 'minimal' in prompt_lower:
        harmony = 'none'
    
    # Infer variation
    variation = 'light'
    if 'varied' in prompt_lower or 'complex' in prompt_lower:
        variation = 'heavy'
    elif 'simple' in prompt_lower:
        variation = 'none'
    
    return {
        'tempo': tempo,
        'instruments': instruments,
        'mood': mood,
        'harmony': harmony,
        'variation': variation
    }


def extract_fx_from_prompt(prompt: str) -> Optional[str]:
    """
    Extract sound effect descriptions from prompt
    
    Args:
        prompt: User prompt text
    
    Returns:
        Sound effect description string, or None
    """
    # Look for common sound effect keywords
    fx_keywords = [
        'rain', 'thunder', 'wind', 'explosion', 'laser', 'ocean', 'wave',
        'fire', 'storm', 'thunderstorm', 'breeze', 'drizzle', 'blast'
    ]
    
    prompt_lower = prompt.lower()
    for keyword in fx_keywords:
        if keyword in prompt_lower:
            # Extract surrounding context (up to 5 words)
            pattern = rf'\b(?:\w+\s+){{0,2}}{keyword}(?:\s+\w+){{0,2}}\b'
            match = re.search(pattern, prompt_lower)
            if match:
                return match.group(0)
    
    return None


def render_midi_to_wave(midi: MIDIFile, sample_rate: int = 44100) -> np.ndarray:
    """
    Render MIDI file to audio waveform
    Uses simple sine-wave synthesis if fluidsynth is not available
    
    Args:
        midi: MIDIFile object
        sample_rate: Sample rate for output audio
    
    Returns:
        NumPy array of audio samples
    """
    # Calculate total duration (simplified - would need to parse MIDI events)
    # For now, estimate based on tempo and assume 4 seconds
    duration = 4.0  # Default duration
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)
    
    # Initialize output
    output = np.zeros(num_samples, dtype=np.float32)
    
    # Simple sine wave synthesis for each note
    # Note: This is a simplified version. Full implementation would:
    # 1. Parse MIDI events from the MIDIFile
    # 2. Generate sine waves for each note
    # 3. Apply ADSR envelopes
    # 4. Mix all notes together
    
    # For now, generate a simple melody
    # In a full implementation, you'd parse the MIDI file properly
    try:
        # Try to use a simple synthesis approach
        # Generate a basic melody based on common notes
        notes = [60, 64, 67, 72]  # C, E, G, C (C major chord)
        note_duration = duration / len(notes)
        
        for i, midi_note in enumerate(notes):
            start_time = i * note_duration
            end_time = (i + 1) * note_duration
            
            # Convert MIDI note to frequency
            frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
            
            # Generate sine wave for this note
            start_idx = int(start_time * sample_rate)
            end_idx = int(end_time * sample_rate)
            if end_idx > num_samples:
                end_idx = num_samples
            
            note_samples = end_idx - start_idx
            if note_samples > 0:
                note_t = np.linspace(0, note_duration, note_samples)
                note_wave = np.sin(2 * np.pi * frequency * note_t)
                
                # Apply envelope (ADSR)
                envelope = _apply_adsr_envelope(note_samples, 0.1, 0.2, 0.6, 0.2)
                note_wave *= envelope
                
                output[start_idx:end_idx] += note_wave * 0.3
        
        # Normalize
        max_val = np.max(np.abs(output))
        if max_val > 0:
            output = output / max_val * 0.8
        
    except Exception as e:
        # Fallback: generate simple tone
        frequency = 440.0
        output = np.sin(2 * np.pi * frequency * t) * 0.5
    
    return output


def _apply_adsr_envelope(num_samples: int, attack: float, decay: float, sustain: float, release: float) -> np.ndarray:
    """
    Apply ADSR envelope to audio samples
    
    Args:
        num_samples: Number of samples
        attack: Attack time (0-1)
        decay: Decay time (0-1)
        sustain: Sustain level (0-1)
        release: Release time (0-1)
    
    Returns:
        Envelope array
    """
    envelope = np.ones(num_samples)
    
    attack_samples = int(num_samples * attack)
    decay_samples = int(num_samples * decay)
    release_samples = int(num_samples * release)
    sustain_samples = num_samples - attack_samples - decay_samples - release_samples
    
    # Attack
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Decay
    if decay_samples > 0:
        decay_start = attack_samples
        decay_end = decay_start + decay_samples
        envelope[decay_start:decay_end] = np.linspace(1, sustain, decay_samples)
    
    # Sustain
    if sustain_samples > 0:
        sustain_start = attack_samples + decay_samples
        sustain_end = sustain_start + sustain_samples
        envelope[sustain_start:sustain_end] = sustain
    
    # Release
    if release_samples > 0:
        release_start = num_samples - release_samples
        envelope[release_start:] = np.linspace(sustain, 0, release_samples)
    
    return envelope


def mix_audio(audio1: np.ndarray, audio2: Optional[np.ndarray] = None, 
              mix_level: float = 0.5) -> np.ndarray:
    """
    Mix two audio arrays together
    
    Args:
        audio1: First audio array
        audio2: Second audio array (optional)
        mix_level: Mix level for audio2 (0.0 = only audio1, 1.0 = equal mix)
    
    Returns:
        Mixed audio array
    """
    if audio2 is None:
        return audio1
    
    # Ensure same length
    min_len = min(len(audio1), len(audio2))
    audio1 = audio1[:min_len]
    audio2 = audio2[:min_len]
    
    # Mix with levels
    mixed = audio1 * (1 - mix_level) + audio2 * mix_level
    
    # Normalize to prevent clipping
    max_val = np.max(np.abs(mixed))
    if max_val > 1.0:
        mixed = mixed / max_val * 0.95
    
    return mixed.astype(np.float32)


def merge_into_midi(structured: Dict, base_midi: MIDIFile) -> MIDIFile:
    """
    Merge structured ABC notation into MIDI file
    
    Args:
        structured: Dictionary from abc_parser.parse_abc()
        base_midi: Base MIDI file to merge into
    
    Returns:
        Updated MIDIFile
    """
    # This would merge the parsed ABC notes into the MIDI file
    # For now, return the base MIDI (full implementation would add notes)
    return base_midi


def simple_midi_render(midi: MIDIFile, sample_rate: int = 44100) -> np.ndarray:
    """
    Basic note → frequency → sine wave generation
    Stub simple sine-wave renderer if no fluidsynth
    """
    return render_midi_to_wave(midi, sample_rate)

