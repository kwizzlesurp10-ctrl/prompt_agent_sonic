"""
Seeded MIDI Generator
Ported procedural seeded logic - hash prompt to deterministic notes
Converts text prompts to reproducible melody base (pitch, rhythm, length)
"""

import hashlib
from typing import List, Tuple
from midiutil import MIDIFile


def seed_to_midi(prompt: str, duration: float = 4.0, tempo: int = 120) -> MIDIFile:
    """
    Hash prompt → reproducible melody base (pitch, rhythm, length)
    
    Args:
        prompt: Text prompt to seed the melody
        duration: Duration of the melody in seconds
        tempo: Tempo in BPM
    
    Returns:
        MIDIFile object with seeded melody
    """
    # Create hash from prompt
    hash_obj = hashlib.sha256(prompt.encode('utf-8'))
    hash_bytes = hash_obj.digest()
    
    # Create MIDI file
    midi = MIDIFile(1)  # One track
    midi.addTempo(0, 0, tempo)
    
    # Extract parameters from hash
    num_notes = 8 + (hash_bytes[0] % 16)  # 8-23 notes
    base_pitch = 60 + (hash_bytes[1] % 24)  # MIDI note 60-83 (C4 to B5)
    rhythm_pattern = hash_bytes[2] % 4  # 0-3 different rhythm patterns
    
    # Generate notes deterministically
    time = 0.0
    note_durations = _get_rhythm_pattern(rhythm_pattern)
    
    for i in range(num_notes):
        if time >= duration:
            break
        
        # Use hash bytes to determine pitch variation
        pitch_variation = (hash_bytes[3 + (i % len(hash_bytes[3:]))] % 13) - 6  # -6 to +6 semitones
        pitch = max(48, min(84, base_pitch + pitch_variation))  # Clamp to reasonable range
        
        # Get duration for this note
        duration_idx = i % len(note_durations)
        note_duration = note_durations[duration_idx]
        
        # Ensure we don't exceed total duration
        if time + note_duration > duration:
            note_duration = duration - time
        
        # Add note (track 0, channel 0, pitch, time, duration, volume)
        midi.addNote(0, 0, pitch, time, note_duration, 100)
        
        time += note_duration
    
    return midi


def _get_rhythm_pattern(pattern_id: int) -> List[float]:
    """Get rhythm pattern based on pattern ID"""
    patterns = {
        0: [0.5, 0.5, 0.5, 0.5],  # Even eighth notes
        1: [1.0, 0.5, 0.5, 1.0],  # Mixed quarter/eighth
        2: [0.25, 0.25, 0.5, 1.0, 0.5],  # Syncopated
        3: [1.0, 1.0, 0.5, 0.5, 0.5, 0.5],  # Waltz-like
    }
    return patterns.get(pattern_id, patterns[0])


def hash_to_scale(hash_bytes: bytes, scale_type: str = 'major') -> List[int]:
    """
    Convert hash bytes to scale degrees
    
    Args:
        hash_bytes: Hash bytes to use
        scale_type: 'major' or 'minor'
    
    Returns:
        List of MIDI note numbers in the scale
    """
    if scale_type == 'major':
        intervals = [0, 2, 4, 5, 7, 9, 11]  # Major scale intervals
    else:
        intervals = [0, 2, 3, 5, 7, 8, 10]  # Minor scale intervals
    
    root = 60 + (hash_bytes[0] % 12)  # C4 to B4
    scale = [root + interval for interval in intervals]
    return scale

