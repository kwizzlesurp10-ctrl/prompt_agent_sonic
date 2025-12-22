"""
Streamlit interactive prototype
Web interface for PromptSonic Agent
"""

import streamlit as st
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.pipeline import generate_music


def main():
    st.set_page_config(
        page_title="PromptSonic Agent",
        page_icon="🎵",
        layout="wide"
    )
    
    st.title("🎵 PromptSonic Agent – Text to Custom Music")
    st.markdown("Generate custom music from text descriptions using AI-powered composition")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        output_dir = st.text_input("Output Directory", value="outputs")
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        PromptSonic Agent combines:
        - **Seeded MIDI generation** from text prompts
        - **ABC notation parsing** for musical hints
        - **Algorithmic composition** rules
        - **Sound effect synthesis** from descriptions
        
        Enter a text prompt describing your music, scene, or mood!
        """)
    
    # Main input area
    st.subheader("Describe your music/scene/mood:")
    
    # Example prompts
    example_prompts = [
        "Epic space adventure with soaring strings and laser sounds",
        "Calm ocean waves with gentle piano melody",
        "Happy upbeat tempo with guitar and strings",
        "Sad melancholy piece in C major",
        "Thunderstorm backdrop with dramatic orchestral music"
    ]
    
    selected_example = st.selectbox(
        "Or choose an example:",
        ["Custom prompt"] + example_prompts
    )
    
    if selected_example != "Custom prompt":
        default_prompt = selected_example
    else:
        default_prompt = "Epic space adventure with soaring strings and laser sounds"
    
    prompt = st.text_area(
        "Enter your prompt:",
        value=default_prompt,
        height=100,
        help="Describe the music you want to generate. Include mood, instruments, tempo, or sound effects."
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button(
            "🎹 Generate Track",
            type="primary",
            use_container_width=True
        )
    
    # Generation and output
    if generate_button:
        if not prompt.strip():
            st.warning("Please enter a prompt!")
        else:
            with st.spinner("Agent orchestrating soundwaves..."):
                try:
                    # Generate music
                    wav_path = generate_music(prompt, output_dir=output_dir)
                    
                    st.success("✅ Music generated successfully!")
                    
                    # Display audio player
                    st.subheader("Generated Music")
                    st.audio(wav_path, format="audio/wav")
                    
                    # Download button
                    with open(wav_path, "rb") as f:
                        st.download_button(
                            label="📥 Download WAV",
                            data=f.read(),
                            file_name=os.path.basename(wav_path),
                            mime="audio/wav"
                        )
                    
                    # Show file info
                    file_size = os.path.getsize(wav_path) / 1024  # KB
                    st.caption(f"File size: {file_size:.1f} KB | Path: {wav_path}")
                    
                except Exception as e:
                    st.error(f"Error generating music: {str(e)}")
                    st.exception(e)
    
    # Instructions
    with st.expander("💡 Tips for better results"):
        st.markdown("""
        - **Be specific**: Include mood, instruments, tempo, or style
        - **Add notation**: Include note sequences like "CDEFG" for melodic hints
        - **Describe FX**: Mention sound effects like "rain", "thunder", "wind", "laser"
        - **Examples**:
          - "Happy upbeat tempo with guitar and strings"
          - "Epic space adventure with soaring strings and laser sounds"
          - "Calm ocean waves with gentle piano melody"
          - "CDEFG major scale with thunderstorm backdrop"
        """)


if __name__ == "__main__":
    main()

