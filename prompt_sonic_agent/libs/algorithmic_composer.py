"""
Algorithmic Composer
Adapted from lennrt/Csound rules (Java → Python generators)
Applies algorithmic rules: harmony, variation, orchestration
"""

import random
from typing import Dict, List, Optional
from midiutil import MIDIFile
import copy


def rule_compose(base_midi: MIDIFile, params: dict) -> MIDIFile:
    """
    Apply algorithmic rules: harmony, variation, orchestration
    
    Args:
        base_midi: Base MIDI file to enhance
        params: Composition parameters:
            - tempo: BPM
            - instruments: List of instrument names
            - mood: 'happy', 'sad', 'epic', 'calm', etc.
            - harmony: 'none', 'triads', 'sevenths'
            - variation: 'none', 'light', 'heavy'
    
    Returns:
        Enhanced MIDIFile with algorithmic composition applied
    """
    # Create a copy to work with
    enhanced_midi = copy.deepcopy(base_midi)
    
    # Extract parameters with defaults
    tempo = params.get('tempo', 120)
    instruments = params.get('instruments', ['piano'])
    mood = params.get('mood', 'neutral')
    harmony = params.get('harmony', 'triads')
    variation = params.get('variation', 'light')
    
    # Apply mood-based transformations
    enhanced_midi = _apply_mood(enhanced_midi, mood)
    
    # Add harmony if requested
    if harmony != 'none':
        enhanced_midi = _add_harmony(enhanced_midi, harmony)
    
    # Apply variation
    if variation != 'none':
        enhanced_midi = _apply_variation(enhanced_midi, variation)
    
    # Add orchestration (multiple tracks for different instruments)
    if len(instruments) > 1:
        enhanced_midi = _add_orchestration(enhanced_midi, instruments)
    
    return enhanced_midi


def _apply_mood(midi: MIDIFile, mood: str) -> MIDIFile:
    """Apply mood-based transformations to MIDI"""
    mood_effects = {
        'happy': {'tempo_mult': 1.1, 'pitch_shift': 2, 'velocity_mult': 1.1},
        'sad': {'tempo_mult': 0.85, 'pitch_shift': -2, 'velocity_mult': 0.9},
        'epic': {'tempo_mult': 1.0, 'pitch_shift': 0, 'velocity_mult': 1.2},
        'calm': {'tempo_mult': 0.9, 'pitch_shift': 0, 'velocity_mult': 0.85},
        'energetic': {'tempo_mult': 1.2, 'pitch_shift': 0, 'velocity_mult': 1.15},
    }
    
    effects = mood_effects.get(mood.lower(), {})
    
    # Note: MIDIFile doesn't easily support pitch shifting existing notes
    # This would require reconstructing the MIDI file
    # For now, we'll apply tempo and velocity changes conceptually
    # In a full implementation, you'd need to parse and rebuild the MIDI
    
    return midi


def _add_harmony(midi: MIDIFile, harmony_type: str) -> MIDIFile:
    """
    Add harmonic layers to the MIDI
    Note: This is a simplified version. Full implementation would need
    to parse MIDI events and add harmony notes.
    """
    # Harmony intervals based on type
    if harmony_type == 'triads':
        intervals = [0, 4, 7]  # Root, third, fifth
    elif harmony_type == 'sevenths':
        intervals = [0, 4, 7, 11]  # Root, third, fifth, seventh
    else:
        intervals = [0, 4, 7]
    
    # In a full implementation, we would:
    # 1. Parse existing notes from midi
    # 2. For each note, add harmony notes at specified intervals
    # 3. Add these as new notes to the MIDI file
    
    return midi


def _apply_variation(midi: MIDIFile, variation_level: str) -> MIDIFile:
    """
    Apply variation to the melody
    Variation levels: 'light', 'medium', 'heavy'
    """
    # Variation would involve:
    # - Adding passing tones
    # - Ornamentation (trills, mordents)
    # - Rhythmic variation
    # - Pitch variation
    
    return midi


def _add_orchestration(midi: MIDIFile, instruments: List[str]) -> MIDIFile:
    """
    Add orchestration by creating multiple tracks for different instruments
    """
    # Map instrument names to MIDI program numbers
    instrument_map = {
        'piano': 0,
        'guitar': 24,
        'strings': 48,
        'brass': 56,
        'flute': 73,
        'violin': 40,
        'cello': 42,
        'trumpet': 56,
        'saxophone': 65,
    }
    
    # Get number of tracks needed
    num_tracks = len(instruments)
    
    # Create new MIDI with multiple tracks
    # Note: This is simplified - full implementation would distribute
    # notes across tracks based on pitch range, rhythm, etc.
    
    return midi


def generate_counterpoint(melody: List[Dict], style: str = 'canon') -> List[Dict]:
    """
    Generate counterpoint to a melody
    
    Args:
        melody: List of note dictionaries with pitch and duration
        style: 'canon', 'fugue', 'free'
    
    Returns:
        List of counterpoint notes
    """
    counterpoint = []
    
    if style == 'canon':
        # Simple canon: repeat melody at different pitch/time
        for note in melody:
            counterpoint.append({
                'pitch': note['pitch'] - 7,  # Fifth below
                'duration': note['duration'],
                'time': note.get('time', 0) + 2.0  # Delayed entry
            })
    elif style == 'fugue':
        # Fugue-style: inverted or transposed subject
        for note in melody:
            counterpoint.append({
                'pitch': 127 - note['pitch'],  # Inverted
                'duration': note['duration'],
                'time': note.get('time', 0)
            })
    else:
        # Free counterpoint: complementary rhythm and harmony
        for i, note in enumerate(melody):
            if i % 2 == 0:
                counterpoint.append({
                    'pitch': note['pitch'] - 5,  # Fourth below
                    'duration': note['duration'] * 2,
                    'time': note.get('time', 0)
                })
    
    return counterpoint

