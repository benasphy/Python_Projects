import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import streamlit as st
import os

def main():
    st.title("🌐 Translation App (Deep Translator)")

    # Get supported languages
    langs = GoogleTranslator().get_supported_languages(as_dict=True)
    lang_names = list(langs.keys())

    # Input Text
    text_input = st.text_area("Enter text to translate:", height=120)

    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox("Source Language", lang_names, index=lang_names.index("english") if "english" in lang_names else 0)
    with col2:
        dest_lang = st.selectbox("Destination Language", lang_names, index=lang_names.index("amharic") if "amharic" in lang_names else 0)

    # Use session state to persist translation
    if 'translated_text' not in st.session_state:
        st.session_state['translated_text'] = ''
    if 'last_dest_lang' not in st.session_state:
        st.session_state['last_dest_lang'] = ''

    if st.button("Translate"):
        if not text_input.strip():
            st.warning("Please enter text to translate.")
        elif not src_lang or not dest_lang:
            st.warning("Please select both source and destination languages.")
        else:
            try:
                translator = GoogleTranslator(source=src_lang, target=dest_lang)
                translated_text = translator.translate(text_input.strip())
                st.session_state['translated_text'] = translated_text
                st.session_state['last_dest_lang'] = dest_lang
                st.success("Translation Result:")
                st.write(translated_text)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state['translated_text'] = ''
    
    # Show translation if present in session state
    if st.session_state['translated_text']:
        st.success("Translation Result:")
        st.write(st.session_state['translated_text'])
        if st.button("Play Translated Audio"):
            try:
                gtts_lang_code = st.session_state['last_dest_lang'][:2]
                tts = gTTS(text=st.session_state['translated_text'], lang=gtts_lang_code)
                audio_file = "temp_tts.mp3"
                tts.save(audio_file)
                audio_bytes = open(audio_file, 'rb').read()
                st.audio(audio_bytes, format='audio/mp3')
                os.remove(audio_file)
            except Exception as e:
                st.error(f"Text-to-speech Error: {str(e)}")

    st.sidebar.header("Supported Languages")
    st.sidebar.write(", ".join(lang_names))

if __name__ == "__main__":
    main()

