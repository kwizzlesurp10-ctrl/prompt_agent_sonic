# 🎵 PromptSonic Agent

**Text-to-Music Generation System**

Generate custom music from text descriptions using AI-powered algorithmic composition, seeded MIDI generation, ABC notation parsing, and procedural sound effect synthesis.

## Features

- 🎹 **Seeded MIDI Generation**: Convert text prompts to deterministic, reproducible melodies
- 🎼 **ABC Notation Parsing**: Extract and parse musical notation hints from prompts
- 🎨 **Algorithmic Composition**: Apply mood-based rules for harmony, variation, and orchestration
- 🔊 **Sound Effect Synthesis**: Generate procedural sound effects from text descriptions (rain, thunder, wind, explosions, lasers, etc.)
- 🎚️ **Intelligent Parameter Inference**: Automatically extract tempo, instruments, mood, and style from prompts
- 🌐 **Streamlit Web Interface**: Interactive web app for easy music generation

## Installation

1. Clone or navigate to the project directory:
```bash
cd prompt_sonic_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Command Line

```python
from src.pipeline import generate_music

# Generate music from a text prompt
output_path = generate_music("Epic space adventure with soaring strings and laser sounds")
print(f"Generated: {output_path}")
```

### Web Interface

Run the Streamlit demo app:

```bash
streamlit run src/demo_app.py
```

Or use the provided script:

```bash
# On Unix/Mac
./run_demo.sh

# On Windows
run_demo.bat
```

Then open your browser to `http://localhost:8501`

## Usage Examples

### Basic Music Generation

```python
from src.pipeline import generate_music

# Simple prompt
generate_music("Happy upbeat tempo with guitar")

# With sound effects
generate_music("Calm ocean waves with gentle piano melody")

# With notation hints
generate_music("CDEFG major scale with thunderstorm backdrop")
```

### Advanced Usage

```python
from libs.seeded_midi import seed_to_midi
from libs.algorithmic_composer import rule_compose
from libs.sound_fx_synth import text_to_fx_wave
from src.utils import infer_params

# Step-by-step generation
prompt = "Epic cinematic music"

# 1. Generate base melody
base_midi = seed_to_midi(prompt, duration=8.0, tempo=120)

# 2. Infer parameters
params = infer_params(prompt)
# {'tempo': 120, 'instruments': ['strings', 'brass'], 'mood': 'epic', ...}

# 3. Apply composition rules
full_midi = rule_compose(base_midi, params)

# 4. Generate sound effects
fx_wave = text_to_fx_wave("thunderstorm", duration=8.0)

# 5. Render and mix (see pipeline.py for full example)
```

## Architecture

```
prompt_sonic_agent/
├── libs/
│   ├── abc_parser.py            # ABC notation parsing
│   ├── seeded_midi.py           # Deterministic MIDI generation
│   ├── algorithmic_composer.py  # Composition rules and orchestration
│   └── sound_fx_synth.py        # Procedural sound effect synthesis
├── src/
│   ├── pipeline.py              # Main generation pipeline
│   ├── agent_workflow.py        # LLM integration stub (future)
│   ├── demo_app.py              # Streamlit web interface
│   └── utils.py                 # Helper functions
└── outputs/                     # Generated WAV files
```

## How It Works

1. **Text Analysis**: Extracts musical hints, notation, instruments, mood, and sound effects from the prompt
2. **Base Melody**: Generates a deterministic melody by hashing the prompt text
3. **Notation Parsing**: If ABC notation is detected, parses and merges it into the melody
4. **Composition Rules**: Applies algorithmic transformations based on inferred mood and style
5. **Sound Effects**: Synthesizes procedural audio effects from descriptive keywords
6. **Rendering**: Converts MIDI to audio and mixes with sound effects
7. **Output**: Saves final WAV file

## Supported Sound Effects

- **Rain**: Drizzle, downpour, water drops
- **Thunder**: Thunderstorm, lightning, rumbling
- **Wind**: Breeze, gusts, air movement
- **Explosion**: Blast, boom, bang
- **Laser**: Beam, zap, sci-fi sounds
- **Ocean**: Waves, sea, surf
- **Fire**: Flame, crackling, burning

## Prompt Tips

- **Be specific**: Include mood, instruments, tempo, or style
- **Add notation**: Include note sequences like "CDEFG" for melodic hints
- **Describe FX**: Mention sound effects like "rain", "thunder", "wind", "laser"
- **Examples**:
  - "Happy upbeat tempo with guitar and strings"
  - "Epic space adventure with soaring strings and laser sounds"
  - "Calm ocean waves with gentle piano melody"
  - "CDEFG major scale with thunderstorm backdrop"

## Technical Details

### Dependencies

- **numpy**: Numerical operations and audio arrays
- **scipy**: Signal processing and filtering
- **midiutil**: MIDI file generation
- **streamlit**: Web interface

### MIDI Rendering

The system uses a simple sine-wave synthesizer by default. For better quality, you can integrate:
- **FluidSynth**: High-quality MIDI-to-audio rendering
- **pyFluidSynth**: Python bindings for FluidSynth

### Future Enhancements

- [ ] Full LangChain/CrewAI integration for advanced prompt analysis
- [ ] Support for multiple MIDI tracks and instruments
- [ ] Advanced harmony generation (chord progressions)
- [ ] Rhythm pattern generation
- [ ] Export to MIDI format
- [ ] Real-time audio preview
- [ ] Custom instrument presets

## License

This project is a reimplementation and adaptation of concepts from:
- `campoy/abc` (Go) - ABC notation parsing
- `lennrt/Csound` (Java) - Algorithmic composition rules
- `davmixcool` (Node.js) - Text-to-sound-effect synthesis

## Contributing

Contributions welcome! Areas for improvement:
- Better MIDI parsing and rendering
- More sophisticated composition algorithms
- Additional sound effect types
- LLM integration for prompt analysis
- Performance optimizations

## Acknowledgments

Inspired by various open-source music generation projects and procedural audio synthesis techniques.

