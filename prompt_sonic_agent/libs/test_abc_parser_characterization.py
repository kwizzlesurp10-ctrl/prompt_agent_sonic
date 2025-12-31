"""
Characterization Tests for ABC Notation Parser

These tests capture the CURRENT BEHAVIOR of the parser, including:
- Exact output structures
- Edge cases and boundary conditions
- Input transformations
- Default values
- Regex matching behavior
- MIDI note calculations
- Duration calculations

These tests serve as a regression test suite - if any test fails after
code changes, it indicates behavior has changed.
"""

import pytest
import sys
from pathlib import Path

# Add libs directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from abc_parser import (
    parse_abc,
    _extract_tempo,
    _extract_key,
    _extract_time_signature,
    _extract_body,
    _parse_notes
)


class TestCharacterizationEmptyInputs:
    """Characterize behavior with empty/null inputs"""
    
    def test_empty_string(self):
        """Empty string returns default structure"""
        result = parse_abc("")
        assert result == {
            'notes': [],
            'tempo': 120,
            'key': 'C',
            'time_signature': '4/4'
        }
    
    def test_whitespace_only(self):
        """Whitespace-only string returns default structure"""
        result = parse_abc("   ")
        assert result == {
            'notes': [],
            'tempo': 120,
            'key': 'C',
            'time_signature': '4/4'
        }
    
    def test_newline_only(self):
        """Newline-only string returns default structure"""
        result = parse_abc("\n")
        assert result == {
            'notes': [],
            'tempo': 120,
            'key': 'C',
            'time_signature': '4/4'
        }
    
    def test_tabs_and_spaces(self):
        """Tabs and spaces return default structure"""
        result = parse_abc("\t  \t")
        assert result == {
            'notes': [],
            'tempo': 120,
            'key': 'C',
            'time_signature': '4/4'
        }


class TestCharacterizationInputTransformation:
    """Characterize input transformation behavior"""
    
    def test_lowercase_converted_to_uppercase(self):
        """Lowercase input is converted to uppercase before parsing"""
        result = parse_abc("cdefg")
        assert result['notes'][0]['pitch'] == 'C'
        assert result['notes'][1]['pitch'] == 'D'
        assert result['notes'][2]['pitch'] == 'E'
    
    def test_mixed_case_converted_to_uppercase(self):
        """Mixed case input is converted to uppercase"""
        result = parse_abc("CdEfG")
        assert all(note['pitch'] == note['pitch'].upper() for note in result['notes'])
    
    def test_leading_trailing_whitespace_stripped(self):
        """Leading and trailing whitespace is stripped"""
        result1 = parse_abc("  CDEFG  ")
        result2 = parse_abc("CDEFG")
        assert result1['notes'] == result2['notes']
    
    def test_whitespace_preserved_in_body(self):
        """Whitespace in body is preserved but doesn't affect parsing"""
        result1 = parse_abc("C D E F G")
        result2 = parse_abc("CDEFG")
        # Both should parse the same notes
        assert len(result1['notes']) == len(result2['notes'])
        assert result1['notes'][0]['pitch'] == result2['notes'][0]['pitch']


class TestCharacterizationTempoExtraction:
    """Characterize tempo extraction behavior"""
    
    def test_tempo_default_value(self):
        """Default tempo is 120 when not specified"""
        assert _extract_tempo("") == 120
        assert _extract_tempo("CDEFG") == 120
        assert _extract_tempo("K: C\nM: 4/4") == 120
    
    def test_tempo_extraction_exact_match(self):
        """Tempo is extracted from Q: field"""
        assert _extract_tempo("Q: 120") == 120
        assert _extract_tempo("Q: 60") == 60
        assert _extract_tempo("Q: 200") == 200
    
    def test_tempo_without_space(self):
        """Tempo works without space after colon"""
        assert _extract_tempo("Q:120") == 120
        assert _extract_tempo("Q:60") == 60
    
    def test_tempo_with_multiple_spaces(self):
        """Tempo works with multiple spaces"""
        assert _extract_tempo("Q:  120") == 120
        assert _extract_tempo("Q:   60") == 60
    
    def test_tempo_case_insensitive(self):
        """Tempo extraction is case-insensitive"""
        assert _extract_tempo("q: 120") == 120
        assert _extract_tempo("Q: 120") == 120
    
    def test_tempo_first_match_wins(self):
        """First tempo match is used if multiple present"""
        # Note: regex search finds first match
        assert _extract_tempo("Q: 100 Q: 200") == 100
    
    def test_tempo_in_middle_of_text(self):
        """Tempo can appear anywhere in text"""
        assert _extract_tempo("Some text Q: 150 more text") == 150
        assert _extract_tempo("CDEFG Q: 140 ABC") == 140
    
    def test_tempo_with_other_headers(self):
        """Tempo works alongside other headers"""
        text = "Q: 130\nK: C\nM: 4/4"
        assert _extract_tempo(text) == 130


class TestCharacterizationKeyExtraction:
    """Characterize key extraction behavior"""
    
    def test_key_default_value(self):
        """Default key is 'C' when not specified"""
        assert _extract_key("") == 'C'
        assert _extract_key("CDEFG") == 'C'
        assert _extract_key("Q: 120\nM: 4/4") == 'C'
    
    def test_key_extraction_basic(self):
        """Key is extracted from K: field"""
        assert _extract_key("K: C") == 'C'
        assert _extract_key("K: D") == 'D'
        assert _extract_key("K: G") == 'G'
    
    def test_key_with_sharp(self):
        """Key with sharp is extracted"""
        assert _extract_key("K: C#") == 'C#'
        assert _extract_key("K: F#") == 'F#'
    
    def test_key_with_flat(self):
        """Key with flat is extracted"""
        assert _extract_key("K: Bb") == 'Bb'
        assert _extract_key("K: Eb") == 'Eb'
    
    def test_key_without_space(self):
        """Key works without space after colon"""
        assert _extract_key("K:C") == 'C'
        assert _extract_key("K:D") == 'D'
    
    def test_key_with_multiple_spaces(self):
        """Key works with multiple spaces"""
        assert _extract_key("K:  C") == 'C'
        assert _extract_key("K:   D") == 'D'
    
    def test_key_case_insensitive_matching(self):
        """Key matching is case-insensitive but returns original case"""
        assert _extract_key("k: c") == 'c'  # Returns lowercase as found
        assert _extract_key("K: c") == 'c'  # Returns lowercase as found
        assert _extract_key("K: C") == 'C'  # Returns uppercase as found
        assert _extract_key("K: D") == 'D'  # Returns uppercase as found
    
    def test_key_first_match_wins(self):
        """First key match is used if multiple present"""
        assert _extract_key("K: C K: D") == 'C'
    
    def test_key_in_middle_of_text(self):
        """Key can appear anywhere in text"""
        assert _extract_key("Some text K: G more text") == 'G'
    
    def test_key_regex_limitation(self):
        """Key regex only matches single accidental"""
        # The regex [A-G][#b]? only matches one accidental
        # This is current behavior - may not match all valid ABC keys
        assert _extract_key("K: C") == 'C'
        # Note: K: C#m (minor) would only match 'C#'


class TestCharacterizationTimeSignatureExtraction:
    """Characterize time signature extraction behavior"""
    
    def test_time_signature_default_value(self):
        """Default time signature is '4/4' when not specified"""
        assert _extract_time_signature("") == '4/4'
        assert _extract_time_signature("CDEFG") == '4/4'
        assert _extract_time_signature("Q: 120\nK: C") == '4/4'
    
    def test_time_signature_extraction(self):
        """Time signature is extracted from M: field"""
        assert _extract_time_signature("M: 4/4") == '4/4'
        assert _extract_time_signature("M: 3/4") == '3/4'
        assert _extract_time_signature("M: 2/4") == '2/4'
        assert _extract_time_signature("M: 6/8") == '6/8'
    
    def test_time_signature_without_space(self):
        """Time signature works without space after colon"""
        assert _extract_time_signature("M:4/4") == '4/4'
        assert _extract_time_signature("M:3/4") == '3/4'
    
    def test_time_signature_with_multiple_spaces(self):
        """Time signature works with multiple spaces"""
        assert _extract_time_signature("M:  4/4") == '4/4'
        assert _extract_time_signature("M:   3/4") == '3/4'
    
    def test_time_signature_case_insensitive(self):
        """Time signature extraction is case-insensitive"""
        assert _extract_time_signature("m: 4/4") == '4/4'
        assert _extract_time_signature("M: 4/4") == '4/4'
    
    def test_time_signature_first_match_wins(self):
        """First time signature match is used if multiple present"""
        assert _extract_time_signature("M: 4/4 M: 3/4") == '4/4'


class TestCharacterizationBodyExtraction:
    """Characterize body extraction behavior"""
    
    def test_body_no_headers(self):
        """Body with no headers returns input as-is (but joined with spaces)"""
        assert _extract_body("CDEFG") == "CDEFG"
        assert _extract_body("C D E F G") == "C D E F G"
    
    def test_body_removes_header_lines(self):
        """Header lines (starting with letter:) are removed"""
        text = "Q: 120\nK: C\nM: 4/4\nCDEFG"
        body = _extract_body(text)
        assert "CDEFG" in body
        assert "Q:" not in body
        assert "K:" not in body
        assert "M:" not in body
    
    def test_body_multiline_joins_with_spaces(self):
        """Multiple body lines are joined with spaces"""
        text = "Q: 120\nCDE\nFGA"
        body = _extract_body(text)
        assert body == "CDE FGA"
    
    def test_body_preserves_non_header_lines(self):
        """Non-header lines are preserved"""
        text = "Q: 120\nCDE\nXYZ\nFGA"
        body = _extract_body(text)
        assert "CDE" in body
        assert "XYZ" in body
        assert "FGA" in body
    
    def test_body_header_detection_case_insensitive(self):
        """Header detection is case-insensitive"""
        text = "q: 120\nk: c\nCDEFG"
        body = _extract_body(text)
        assert "CDEFG" in body
        assert "q:" not in body
        assert "k:" not in body
    
    def test_body_empty_lines(self):
        """Empty lines are preserved as spaces"""
        text = "Q: 120\n\nCDE\n\nFGA"
        body = _extract_body(text)
        # Empty lines become spaces when joined
        assert "CDE" in body
        assert "FGA" in body


class TestCharacterizationNoteParsing:
    """Characterize note parsing behavior"""
    
    def test_parse_single_note(self):
        """Single note is parsed correctly"""
        notes = _parse_notes("C")
        assert len(notes) == 1
        assert notes[0] == {
            'pitch': 'C',
            'octave': 4,
            'midi_note': 60,
            'duration': 1.0,
            'accidental': ''
        }
    
    def test_parse_all_natural_notes(self):
        """All natural notes are parsed"""
        notes = _parse_notes("CDEFGAB")
        assert len(notes) == 7
        assert [n['pitch'] for n in notes] == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        assert all(n['octave'] == 4 for n in notes)
        assert all(n['duration'] == 1.0 for n in notes)
    
    def test_parse_notes_default_octave(self):
        """Notes without octave spec default to octave 4"""
        notes = _parse_notes("CDE")
        assert all(note['octave'] == 4 for note in notes)
    
    def test_parse_notes_explicit_octave_numbers(self):
        """Explicit octave numbers are used"""
        notes = _parse_notes("C3 D4 E5 F6")
        assert notes[0]['octave'] == 3
        assert notes[1]['octave'] == 4
        assert notes[2]['octave'] == 5
        assert notes[3]['octave'] == 6
    
    def test_parse_notes_octave_up_apostrophe(self):
        """Apostrophe (') raises octave to 5"""
        notes = _parse_notes("C'")
        assert notes[0]['octave'] == 5
        assert notes[0]['pitch'] == 'C'
    
    def test_parse_notes_octave_down_comma(self):
        """Comma (,) lowers octave to 3"""
        notes = _parse_notes("C,")
        assert notes[0]['octave'] == 3
        assert notes[0]['pitch'] == 'C'
    
    def test_parse_notes_octave_number_overrides_modifier(self):
        """Explicit octave number overrides modifier"""
        notes = _parse_notes("C'4")  # Apostrophe + number
        # Current behavior: number takes precedence
        assert notes[0]['octave'] == 4
    
    def test_parse_notes_sharp(self):
        """Sharp (#) is parsed and included in pitch"""
        notes = _parse_notes("C# D# F#")
        assert notes[0]['pitch'] == 'C#'
        assert notes[0]['accidental'] == '#'
        assert notes[1]['pitch'] == 'D#'
        assert notes[2]['pitch'] == 'F#'
    
    def test_parse_notes_flat(self):
        """Flat (b) is parsed and included in pitch"""
        notes = _parse_notes("Bb Eb Ab")
        assert notes[0]['pitch'] == 'Bb'
        assert notes[0]['accidental'] == 'b'
        assert notes[1]['pitch'] == 'Eb'
        assert notes[2]['pitch'] == 'Ab'
    
    def test_parse_notes_duration_default(self):
        """Notes default to duration 1.0"""
        notes = _parse_notes("CDE")
        assert all(note['duration'] == 1.0 for note in notes)
    
    def test_parse_notes_duration_half(self):
        """Duration /2 gives 0.5"""
        notes = _parse_notes("C/2")
        assert notes[0]['duration'] == 0.5
    
    def test_parse_notes_duration_quarter(self):
        """Duration /4 gives 0.25"""
        notes = _parse_notes("C/4")
        assert notes[0]['duration'] == 0.25
    
    def test_parse_notes_duration_eighth(self):
        """Duration /8 gives 0.125"""
        notes = _parse_notes("C/8")
        assert notes[0]['duration'] == 0.125
    
    def test_parse_notes_duration_decimal(self):
        """Duration with decimal works"""
        notes = _parse_notes("C/2.5")
        assert notes[0]['duration'] == pytest.approx(1.0 / 2.5)
    
    def test_parse_notes_complex_combinations(self):
        """Complex note combinations are parsed"""
        # Note: Accidental must come immediately after note letter, not after octave
        notes = _parse_notes("C#4/2 Db'5/4 E,3/8")
        assert len(notes) == 3
        # First note: C#4/2 (accidental after note, before octave)
        assert notes[0]['pitch'] == 'C#'
        assert notes[0]['octave'] == 4
        assert notes[0]['duration'] == 0.5
        # Second note: Db'5/4 (accidental after note, octave number overrides apostrophe)
        assert notes[1]['pitch'] == 'Db'
        assert notes[1]['octave'] == 5
        assert notes[1]['duration'] == 0.25
        # Third note: E,3/8 (octave number overrides comma)
        assert notes[2]['pitch'] == 'E'
        assert notes[2]['octave'] == 3
        assert notes[2]['duration'] == 0.125
    
    def test_parse_notes_accidental_position_matters(self):
        """Accidental must come immediately after note letter"""
        # Correct: accidental after note letter
        notes1 = _parse_notes("C#4/2")
        assert notes1[0]['pitch'] == 'C#'
        assert notes1[0]['accidental'] == '#'
        # Incorrect: accidental after octave (not matched)
        notes2 = _parse_notes("C4#/2")
        assert notes2[0]['pitch'] == 'C'
        assert notes2[0]['accidental'] == ''
        # Correct: accidental with octave modifier
        notes3 = _parse_notes("C#'5/2")
        assert notes3[0]['pitch'] == 'C#'
        assert notes3[0]['octave'] == 5
    
    def test_parse_notes_midi_calculation_c4(self):
        """C4 calculates to MIDI note 60 (middle C)"""
        notes = _parse_notes("C4")
        assert notes[0]['midi_note'] == 60
        # Formula: (octave + 1) * 12 + semitone
        # (4 + 1) * 12 + 0 = 60
    
    def test_parse_notes_midi_calculation_c_sharp_4(self):
        """C#4 calculates to MIDI note 61"""
        notes = _parse_notes("C#4")
        assert notes[0]['midi_note'] == 61
        # (4 + 1) * 12 + 1 = 61
    
    def test_parse_notes_midi_calculation_b_flat_4(self):
        """Bb4 calculates to MIDI note 70"""
        notes = _parse_notes("Bb4")
        assert notes[0]['midi_note'] == 70
        # (4 + 1) * 12 + 10 = 70 (B=11, flat makes it 10)
    
    def test_parse_notes_midi_calculation_octave_range(self):
        """MIDI calculation works across octaves"""
        notes = _parse_notes("C0 C4 C8")
        assert notes[0]['midi_note'] == 12  # (0+1)*12 + 0
        assert notes[1]['midi_note'] == 60  # (4+1)*12 + 0
        assert notes[2]['midi_note'] == 108  # (8+1)*12 + 0
    
    def test_parse_notes_empty_body(self):
        """Empty body returns empty list"""
        assert _parse_notes("") == []
        assert _parse_notes("   ") == []
    
    def test_parse_notes_no_matches(self):
        """Body with no valid notes returns empty list"""
        assert _parse_notes("xyz") == []
        assert _parse_notes("123") == []
        assert _parse_notes("!@#") == []
        assert _parse_notes("xyz 123 !@#") == []
    
    def test_parse_notes_mixed_valid_invalid(self):
        """Only valid notes are parsed, invalid text is ignored"""
        notes = _parse_notes("C xyz D 123 E")
        assert len(notes) == 3
        assert [n['pitch'] for n in notes] == ['C', 'D', 'E']
    
    def test_parse_notes_regex_behavior(self):
        """Regex matches notes anywhere in string"""
        notes = _parse_notes("abcCdefDghiE")
        assert len(notes) == 3
        assert [n['pitch'] for n in notes] == ['C', 'D', 'E']
    
    def test_parse_notes_spacing_does_not_matter(self):
        """Spacing between notes doesn't affect parsing"""
        notes1 = _parse_notes("CDE")
        notes2 = _parse_notes("C D E")
        notes3 = _parse_notes("C  D  E")
        assert len(notes1) == len(notes2) == len(notes3) == 3
        assert notes1[0]['pitch'] == notes2[0]['pitch'] == notes3[0]['pitch']


class TestCharacterizationFullParseIntegration:
    """Characterize full parse_abc integration behavior"""
    
    def test_complete_abc_tune(self):
        """Complete ABC tune with all headers"""
        abc_text = """Q: 140
K: D
M: 3/4
CDEFG"""
        result = parse_abc(abc_text)
        assert result['tempo'] == 140
        assert result['key'] == 'D'
        assert result['time_signature'] == '3/4'
        assert len(result['notes']) == 5
        assert all(note['pitch'] in ['C', 'D', 'E', 'F', 'G'] for note in result['notes'])
    
    def test_abc_with_accidentals_and_durations(self):
        """ABC with accidentals and durations"""
        abc_text = """Q: 120
K: C
M: 4/4
C4/2 D#4/4 E4/8"""
        result = parse_abc(abc_text)
        assert result['tempo'] == 120
        assert result['key'] == 'C'
        assert result['time_signature'] == '4/4'
        assert len(result['notes']) == 3
        assert result['notes'][0]['duration'] == 0.5
        assert result['notes'][1]['pitch'] == 'D#'
        assert result['notes'][2]['duration'] == 0.125
    
    def test_abc_headers_case_insensitive(self):
        """Headers are case-insensitive"""
        abc_text = """q: 130
k: g
m: 2/4
CDE"""
        result = parse_abc(abc_text)
        assert result['tempo'] == 130
        assert result['key'] == 'G'  # Note: uppercase after strip().upper()
        assert result['time_signature'] == '2/4'
    
    def test_abc_notes_case_insensitive(self):
        """Notes are case-insensitive (converted to uppercase)"""
        abc_text = "cdefg"
        result = parse_abc(abc_text)
        assert [n['pitch'] for n in result['notes']] == ['C', 'D', 'E', 'F', 'G']
    
    def test_abc_multiline_body(self):
        """Multiline body is parsed correctly"""
        abc_text = """Q: 120
CDE
FGA"""
        result = parse_abc(abc_text)
        assert len(result['notes']) == 6
        assert result['notes'][0]['pitch'] == 'C'
        assert result['notes'][5]['pitch'] == 'A'
    
    def test_abc_only_notes_no_headers(self):
        """ABC with only notes, no headers"""
        result = parse_abc("CDEFG")
        assert result['tempo'] == 120  # Default
        assert result['key'] == 'C'  # Default
        assert result['time_signature'] == '4/4'  # Default
        assert len(result['notes']) == 5
    
    def test_abc_only_headers_no_notes(self):
        """ABC with only headers, no notes"""
        abc_text = """Q: 150
K: F
M: 6/8"""
        result = parse_abc(abc_text)
        assert result['tempo'] == 150
        assert result['key'] == 'F'
        assert result['time_signature'] == '6/8'
        assert result['notes'] == []
    
    def test_abc_output_structure(self):
        """Output structure is always consistent"""
        result = parse_abc("C")
        assert isinstance(result, dict)
        assert 'notes' in result
        assert 'tempo' in result
        assert 'key' in result
        assert 'time_signature' in result
        assert isinstance(result['notes'], list)
        assert isinstance(result['tempo'], int)
        assert isinstance(result['key'], str)
        assert isinstance(result['time_signature'], str)
    
    def test_abc_note_structure(self):
        """Note structure is always consistent"""
        result = parse_abc("C4#/2")
        note = result['notes'][0]
        assert isinstance(note, dict)
        assert 'pitch' in note
        assert 'octave' in note
        assert 'midi_note' in note
        assert 'duration' in note
        assert 'accidental' in note
        assert isinstance(note['pitch'], str)
        assert isinstance(note['octave'], int)
        assert isinstance(note['midi_note'], int)
        assert isinstance(note['duration'], float)
        assert isinstance(note['accidental'], str)


class TestCharacterizationEdgeCases:
    """Characterize edge cases and boundary conditions"""
    
    def test_very_long_note_sequence(self):
        """Very long sequence of notes"""
        notes_str = "CDEFGAB" * 100
        result = parse_abc(notes_str)
        assert len(result['notes']) == 700
    
    def test_single_character_input(self):
        """Single character input"""
        result = parse_abc("C")
        assert len(result['notes']) == 1
        assert result['notes'][0]['pitch'] == 'C'
    
    def test_extreme_tempo_values(self):
        """Extreme tempo values"""
        assert _extract_tempo("Q: 1") == 1
        assert _extract_tempo("Q: 9999") == 9999
    
    def test_octave_boundaries(self):
        """Octave boundary values"""
        notes = _parse_notes("C0 C9")
        assert notes[0]['octave'] == 0
        assert notes[1]['octave'] == 9
    
    def test_duration_very_small(self):
        """Very small duration values"""
        notes = _parse_notes("C/100")
        assert notes[0]['duration'] == 0.01
    
    def test_duration_very_large(self):
        """Very large duration values"""
        notes = _parse_notes("C/0.5")
        assert notes[0]['duration'] == 2.0
    
    def test_multiple_headers_same_type(self):
        """Multiple headers of same type (first wins)"""
        text = "Q: 100\nQ: 200\nQ: 300"
        assert _extract_tempo(text) == 100
    
    def test_headers_in_wrong_order(self):
        """Headers in any order work"""
        text = "M: 3/4\nK: D\nQ: 120\nCDE"
        result = parse_abc(text)
        assert result['tempo'] == 120
        assert result['key'] == 'D'
        assert result['time_signature'] == '3/4'
    
    def test_notes_with_whitespace_characters(self):
        """Notes with various whitespace characters"""
        notes = _parse_notes("C\tD\nE F")
        assert len(notes) == 4
        assert [n['pitch'] for n in notes] == ['C', 'D', 'E', 'F']
    
    def test_special_characters_in_body(self):
        """Special characters in body don't break parsing"""
        notes = _parse_notes("C!D@E#F$G")
        # Only E# is parsed as a note (E with sharp)
        # Others are ignored or parsed as separate notes
        assert len(notes) >= 1  # At least E# is parsed
        assert any(n['pitch'] == 'E#' for n in notes)

