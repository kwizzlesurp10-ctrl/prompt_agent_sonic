"""
ABC Notation Parser
Ported from campoy/abc (Go → Python reimplementation)
Parses ABC notation snippets to structured note/duration data
"""

import re
from typing import Dict, List, Optional, Tuple


def parse_abc(abc_text: str) -> dict:
    """
    Parse ABC notation snippet to notes/duration/structure
    
    Args:
        abc_text: ABC notation string (e.g., "CDEFG" or "C4 D4 E4 F4 G4")
    
    Returns:
        Dictionary with parsed structure:
        {
            'notes': [{'pitch': 'C', 'octave': 4, 'duration': 1.0}, ...],
            'tempo': 120,
            'key': 'C',
            'time_signature': '4/4'
        }
    """
    if not abc_text or not abc_text.strip():
        return {
            'notes': [],
            'tempo': 120,
            'key': 'C',
            'time_signature': '4/4'
        }
    
    # Clean input
    abc_text = abc_text.strip().upper()
    
    # Extract header information (if present)
    tempo = _extract_tempo(abc_text)
    key = _extract_key(abc_text)
    time_sig = _extract_time_signature(abc_text)
    
    # Remove header lines for note parsing
    body = _extract_body(abc_text)
    
    # Parse notes
    notes = _parse_notes(body)
    
    return {
        'notes': notes,
        'tempo': tempo,
        'key': key,
        'time_signature': time_sig
    }


def _extract_tempo(text: str) -> int:
    """Extract tempo from ABC notation (Q: field)"""
    tempo_match = re.search(r'Q:\s*(\d+)', text, re.IGNORECASE)
    if tempo_match:
        return int(tempo_match.group(1))
    return 120  # Default tempo


def _extract_key(text: str) -> str:
    """Extract key signature from ABC notation (K: field)"""
    key_match = re.search(r'K:\s*([A-G][#b]?)', text, re.IGNORECASE)
    if key_match:
        return key_match.group(1)
    return 'C'  # Default key


def _extract_time_signature(text: str) -> str:
    """Extract time signature from ABC notation (M: field)"""
    time_match = re.search(r'M:\s*(\d+/\d+)', text, re.IGNORECASE)
    if time_match:
        return time_match.group(1)
    return '4/4'  # Default time signature


def _extract_body(text: str) -> str:
    """Remove header lines and extract body"""
    lines = text.split('\n')
    body_lines = []
    for line in lines:
        # Skip header lines (start with letter:)
        if not re.match(r'^[A-Z]:', line, re.IGNORECASE):
            body_lines.append(line)
    return ' '.join(body_lines)


def _parse_notes(body: str) -> List[Dict]:
    """
    Parse note sequence from ABC body
    Supports: C, D, E, F, G, A, B with optional octave numbers and durations
    """
    notes = []
    
    # Pattern to match notes: optional octave number, note letter, optional accidental, optional duration
    # Examples: C, C4, C' (octave up), C, (octave down), C/2 (half duration), C3/2
    note_pattern = r"([A-G])([#b]?)([',]?)(\d*)(/[\d.]+)?"
    
    matches = re.finditer(note_pattern, body)
    
    for match in matches:
        note_letter = match.group(1)
        accidental = match.group(2) or ''
        octave_mod = match.group(3) or ''
        octave_num = match.group(4)
        duration_mod = match.group(5) or ''
        
        # Determine octave
        if octave_num:
            octave = int(octave_num)
        elif octave_mod == "'":
            octave = 5  # One octave up from default
        elif octave_mod == ",":
            octave = 3  # One octave down from default
        else:
            octave = 4  # Default octave
        
        # Determine duration (default is 1.0, /2 = 0.5, /4 = 0.25, etc.)
        if duration_mod:
            duration = 1.0 / float(duration_mod[1:])
        else:
            duration = 1.0
        
        # Convert note to MIDI note number
        pitch_map = {
            'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
        }
        semitone = pitch_map[note_letter]
        if accidental == '#':
            semitone += 1
        elif accidental == 'b':
            semitone -= 1
        
        midi_note = (octave + 1) * 12 + semitone
        
        notes.append({
            'pitch': note_letter + accidental,
            'octave': octave,
            'midi_note': midi_note,
            'duration': duration,
            'accidental': accidental
        })
    
    return notes
    
