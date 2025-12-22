"""
Tests for ABC Notation Parser
"""

import pytest
import sys
from pathlib import Path

# Add libs directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from abc_parser import parse_abc, _extract_tempo, _extract_key, _extract_time_signature, _extract_body, _parse_notes


class TestParseABC:
    """Test the main parse_abc function"""
    
    def test_empty_input(self):
        """Test parsing empty or whitespace-only input"""
        result = parse_abc("")
        assert result['notes'] == []
        assert result['tempo'] == 120
        assert result['key'] == 'C'
        assert result['time_signature'] == '4/4'
        
        result = parse_abc("   ")
        assert result['notes'] == []
    
    def test_simple_notes(self):
        """Test parsing simple note sequences"""
        result = parse_abc("CDEFG")
        assert len(result['notes']) == 5
        assert result['notes'][0]['pitch'] == 'C'
        assert result['notes'][0]['octave'] == 4
        assert result['notes'][4]['pitch'] == 'G'
    
    def test_notes_with_octaves(self):
        """Test parsing notes with explicit octave numbers"""
        result = parse_abc("C4 D4 E4 F4 G4")
        assert len(result['notes']) == 5
        assert all(note['octave'] == 4 for note in result['notes'])
    
    def test_with_headers(self):
        """Test parsing ABC notation with header fields"""
        abc_text = """Q: 140
K: D
M: 3/4
CDEFG"""
        result = parse_abc(abc_text)
        assert result['tempo'] == 140
        assert result['key'] == 'D'
        assert result['time_signature'] == '3/4'
        assert len(result['notes']) == 5
    
    def test_case_insensitive(self):
        """Test that input is case-insensitive"""
        result1 = parse_abc("CDEFG")
        result2 = parse_abc("cdefg")
        assert result1['notes'] == result2['notes']


class TestExtractTempo:
    """Test tempo extraction"""
    
    def test_extract_tempo_present(self):
        """Test extracting tempo when present"""
        assert _extract_tempo("Q: 120") == 120
        assert _extract_tempo("Q: 140") == 140
        assert _extract_tempo("Q: 60") == 60
        assert _extract_tempo("Some text Q: 100 more text") == 100
    
    def test_extract_tempo_with_spaces(self):
        """Test tempo extraction with various spacing"""
        assert _extract_tempo("Q:120") == 120
        assert _extract_tempo("Q: 120") == 120
        assert _extract_tempo("Q:  120") == 120
    
    def test_extract_tempo_case_insensitive(self):
        """Test tempo extraction is case-insensitive"""
        assert _extract_tempo("q: 120") == 120
        assert _extract_tempo("Q: 120") == 120
    
    def test_extract_tempo_default(self):
        """Test default tempo when not present"""
        assert _extract_tempo("CDEFG") == 120
        assert _extract_tempo("") == 120


class TestExtractKey:
    """Test key signature extraction"""
    
    def test_extract_key_present(self):
        """Test extracting key when present"""
        assert _extract_key("K: C") == 'C'
        assert _extract_key("K: D") == 'D'
        assert _extract_key("K: G") == 'G'
    
    def test_extract_key_with_accidentals(self):
        """Test extracting key with sharps/flats"""
        assert _extract_key("K: F#") == 'F#'
        assert _extract_key("K: Bb") == 'Bb'
        assert _extract_key("K: C#") == 'C#'
    
    def test_extract_key_with_spaces(self):
        """Test key extraction with various spacing"""
        assert _extract_key("K:C") == 'C'
        assert _extract_key("K: C") == 'C'
        assert _extract_key("K:  C") == 'C'
    
    def test_extract_key_case_insensitive(self):
        """Test key extraction is case-insensitive (matching works, but returns original case)"""
        # The regex is case-insensitive for matching, but returns the original case
        assert _extract_key("k: c") == 'c'  # Returns lowercase as found
        assert _extract_key("K: c") == 'c'  # Returns lowercase as found
        assert _extract_key("K: C") == 'C'  # Returns uppercase as found
    
    def test_extract_key_default(self):
        """Test default key when not present"""
        assert _extract_key("CDEFG") == 'C'
        assert _extract_key("") == 'C'


class TestExtractTimeSignature:
    """Test time signature extraction"""
    
    def test_extract_time_signature_present(self):
        """Test extracting time signature when present"""
        assert _extract_time_signature("M: 4/4") == '4/4'
        assert _extract_time_signature("M: 3/4") == '3/4'
        assert _extract_time_signature("M: 2/4") == '2/4'
        assert _extract_time_signature("M: 6/8") == '6/8'
    
    def test_extract_time_signature_with_spaces(self):
        """Test time signature extraction with various spacing"""
        assert _extract_time_signature("M:4/4") == '4/4'
        assert _extract_time_signature("M: 4/4") == '4/4'
        assert _extract_time_signature("M:  4/4") == '4/4'
    
    def test_extract_time_signature_case_insensitive(self):
        """Test time signature extraction is case-insensitive"""
        assert _extract_time_signature("m: 4/4") == '4/4'
        assert _extract_time_signature("M: 4/4") == '4/4'
    
    def test_extract_time_signature_default(self):
        """Test default time signature when not present"""
        assert _extract_time_signature("CDEFG") == '4/4'
        assert _extract_time_signature("") == '4/4'


class TestExtractBody:
    """Test body extraction (removing headers)"""
    
    def test_extract_body_no_headers(self):
        """Test body extraction when no headers present"""
        assert _extract_body("CDEFG") == "CDEFG"
        assert _extract_body("C D E F G") == "C D E F G"
    
    def test_extract_body_with_headers(self):
        """Test body extraction removes header lines"""
        text = """Q: 120
K: C
M: 4/4
CDEFG"""
        assert "CDEFG" in _extract_body(text)
        assert "Q:" not in _extract_body(text)
        assert "K:" not in _extract_body(text)
        assert "M:" not in _extract_body(text)
    
    def test_extract_body_multiline(self):
        """Test body extraction with multiline body"""
        text = """Q: 120
CDE
FGA"""
        body = _extract_body(text)
        assert "CDE" in body
        assert "FGA" in body
        assert "Q:" not in body


class TestParseNotes:
    """Test note parsing"""
    
    def test_parse_simple_notes(self):
        """Test parsing simple note letters"""
        notes = _parse_notes("CDEFGAB")
        assert len(notes) == 7
        assert notes[0]['pitch'] == 'C'
        assert notes[1]['pitch'] == 'D'
        assert notes[6]['pitch'] == 'B'
    
    def test_parse_notes_default_octave(self):
        """Test that notes default to octave 4"""
        notes = _parse_notes("CDE")
        assert all(note['octave'] == 4 for note in notes)
    
    def test_parse_notes_with_octave_numbers(self):
        """Test parsing notes with explicit octave numbers"""
        notes = _parse_notes("C4 D5 E3")
        assert notes[0]['octave'] == 4
        assert notes[1]['octave'] == 5
        assert notes[2]['octave'] == 3
    
    def test_parse_notes_octave_up(self):
        """Test parsing notes with ' (octave up)"""
        notes = _parse_notes("C'")
        assert notes[0]['octave'] == 5
    
    def test_parse_notes_octave_down(self):
        """Test parsing notes with , (octave down)"""
        notes = _parse_notes("C,")
        assert notes[0]['octave'] == 3
    
    def test_parse_notes_with_sharps(self):
        """Test parsing notes with sharps"""
        notes = _parse_notes("C# D#")
        assert notes[0]['pitch'] == 'C#'
        assert notes[0]['accidental'] == '#'
        assert notes[1]['pitch'] == 'D#'
        assert notes[1]['accidental'] == '#'
    
    def test_parse_notes_with_flats(self):
        """Test parsing notes with flats"""
        notes = _parse_notes("Bb Eb")
        assert notes[0]['pitch'] == 'Bb'
        assert notes[0]['accidental'] == 'b'
        assert notes[1]['pitch'] == 'Eb'
        assert notes[1]['accidental'] == 'b'
    
    def test_parse_notes_duration_default(self):
        """Test that notes default to duration 1.0"""
        notes = _parse_notes("CDE")
        assert all(note['duration'] == 1.0 for note in notes)
    
    def test_parse_notes_duration_half(self):
        """Test parsing notes with half duration"""
        notes = _parse_notes("C/2")
        assert notes[0]['duration'] == 0.5
    
    def test_parse_notes_duration_quarter(self):
        """Test parsing notes with quarter duration"""
        notes = _parse_notes("C/4")
        assert notes[0]['duration'] == 0.25
    
    def test_parse_notes_duration_eighth(self):
        """Test parsing notes with eighth duration"""
        notes = _parse_notes("C/8")
        assert notes[0]['duration'] == 0.125
    
    def test_parse_notes_complex(self):
        """Test parsing complex note combinations"""
        notes = _parse_notes("C4/2 D#5/4 E,3/8")
        assert len(notes) == 3
        assert notes[0]['octave'] == 4
        assert notes[0]['duration'] == 0.5
        assert notes[1]['pitch'] == 'D#'
        assert notes[1]['octave'] == 5
        assert notes[1]['duration'] == 0.25
        assert notes[2]['octave'] == 3
        assert notes[2]['duration'] == 0.125
    
    def test_parse_notes_midi_calculation(self):
        """Test MIDI note number calculation"""
        # C4 should be MIDI note 60 (middle C)
        notes = _parse_notes("C4")
        assert notes[0]['midi_note'] == 60
        
        # C#4 should be MIDI note 61
        notes = _parse_notes("C#4")
        assert notes[0]['midi_note'] == 61
        
        # Bb4 should be MIDI note 70
        notes = _parse_notes("Bb4")
        assert notes[0]['midi_note'] == 70
    
    def test_parse_notes_empty_body(self):
        """Test parsing empty body"""
        notes = _parse_notes("")
        assert notes == []
        
        notes = _parse_notes("   ")
        assert notes == []
    
    def test_parse_notes_no_matches(self):
        """Test parsing body with no valid notes"""
        notes = _parse_notes("xyz 123 !@#")
        assert notes == []


class TestIntegration:
    """Integration tests for complete ABC parsing"""
    
    def test_complete_abc_tune(self):
        """Test parsing a complete ABC tune"""
        abc_text = """Q: 120
K: C
M: 4/4
CDEF GABC"""
        result = parse_abc(abc_text)
        assert result['tempo'] == 120
        assert result['key'] == 'C'
        assert result['time_signature'] == '4/4'
        assert len(result['notes']) == 8
    
    def test_abc_with_accidentals_and_durations(self):
        """Test parsing ABC with accidentals and durations"""
        abc_text = """Q: 140
K: D
M: 3/4
C4/2 D#4/4 E4/8"""
        result = parse_abc(abc_text)
        assert result['tempo'] == 140
        assert result['key'] == 'D'
        assert result['time_signature'] == '3/4'
        assert len(result['notes']) == 3
        assert result['notes'][0]['duration'] == 0.5
        assert result['notes'][1]['pitch'] == 'D#'
        assert result['notes'][2]['duration'] == 0.125

