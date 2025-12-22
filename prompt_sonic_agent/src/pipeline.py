"""
Core fusion orchestrator
Main pipeline for generating music from text prompts
"""

import os
import numpy as np
from midiutil import MIDIFile
from scipy.io import wavfile

# Import library modules
import sys
parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, parent_dir)

from libs.seeded_midi import seed_to_midi
from libs.abc_parser import parse_abc
from libs.algorithmic_composer import rule_compose
from libs.sound_fx_synth import text_to_fx_wave
from utils import (
    extract_notation_from_prompt,
    infer_params,
    extract_fx_from_prompt,
    render_midi_to_wave,
    mix_audio,
    merge_into_midi
)


def generate_music(prompt: str, output_dir: str = "outputs") -> str:
    """
    Main music generation pipeline
    
    Args:
        prompt: Text prompt describing the music/scene/mood
        output_dir: Directory to save output WAV file
    
    Returns:
        Path to generated WAV file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎵 Generating music from prompt: '{prompt}'")
    
    # Step 1: Seed base melody from prompt text
    print("Step 1: Seeding base melody...")
    base_midi = seed_to_midi(prompt, duration=4.0)
    
    # Step 2: Extract/parse any ABC-like notation hints
    print("Step 2: Extracting notation hints...")
    abc_snippet = extract_notation_from_prompt(prompt)
    if abc_snippet:
        print(f"  Found notation: {abc_snippet}")
        structured = parse_abc(abc_snippet)
        base_midi = merge_into_midi(structured, base_midi)
    else:
        print("  No notation found, using seeded melody")
    
    # Step 3: Apply algorithmic composition rules (mood-based params)
    print("Step 3: Applying algorithmic composition...")
    params = infer_params(prompt)
    print(f"  Inferred params: {params}")
    full_midi = rule_compose(base_midi, params)
    
    # Step 4: Synthesize FX layers from descriptive text
    print("Step 4: Synthesizing sound effects...")
    fx_desc = extract_fx_from_prompt(prompt)
    if fx_desc:
        print(f"  Found FX description: {fx_desc}")
        # Estimate duration (simplified - would parse from MIDI)
        duration = 4.0
        fx_wave = text_to_fx_wave(fx_desc, duration=duration)
    else:
        print("  No FX description found")
        fx_wave = None
    
    # Step 5: Render MIDI to audio + mix FX
    print("Step 5: Rendering MIDI to audio...")
    midi_wave = render_midi_to_wave(full_midi)
    
    # Mix FX if available
    if fx_wave is not None:
        print("  Mixing sound effects...")
        mixed = mix_audio(midi_wave, fx_wave, mix_level=0.3)  # 30% FX, 70% music
    else:
        mixed = midi_wave
    
    # Save output
    output_path = os.path.join(output_dir, "generated.wav")
    print(f"Step 6: Saving to {output_path}...")
    wavfile.write(output_path, 44100, mixed)
    
    print("✅ Music generation complete!")
    return output_path


if __name__ == "__main__":
    # Test the pipeline
    test_prompt = "Epic space adventure with soaring strings and laser sounds"
    output = generate_music(test_prompt)
    print(f"\nGenerated music saved to: {output}")

