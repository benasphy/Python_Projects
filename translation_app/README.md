# Translation App (Streamlit + Deep Translator)

**Repository:** [https://github.com/benasphy/Python_Projects](https://github.com/benasphy/Python_Projects)

A simple, modern translation app built with [Streamlit](https://streamlit.io/) and [deep-translator](https://github.com/nidhaloff/deep-translator), supporting text-to-speech (TTS) with [gTTS](https://pypi.org/project/gTTS/).

## Features
- Translate text between 100+ languages (Google Translate backend)
- Clean web UI with Streamlit
- Text-to-speech for translated output (where supported)
- Instant language dropdowns populated from GoogleTranslator

## Usage

1. **Install dependencies** (in this folder):
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```bash
   streamlit run app.py
   ```
3. **How to use:**
   - Enter text, select source and destination languages, and click "Translate"
   - Click "Play Translated Audio" to hear the result (if supported)

## Requirements
- Python 3.8+
- See `requirements.txt` in this folder

## Dependencies
- streamlit
- deep-translator
- gtts

## License
MIT
