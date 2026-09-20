import streamlit as st
import tempfile
import os
import re

# Importamos las herramientas de tus repositorios anteriores
from utils.transcriber import transcribe_audio_file
from utils.pdf_parser import extract_text_from_pdf

# Importamos el nuevo cerebro de estudio
from services.ai_tutor import generar_apuntes, generar_flashcards, generar_test

st.set_page_config(page_title="StudyBrain AI", page_icon="🧠", layout="wide")

st.title("🧠 StudyBrain AI: Tu Tutor Universitario Local")
st.markdown("Genera apuntes desde audios y material de estudio desde PDFs. 100% privado y sin coste de API.")

# Usamos pestañas para separar las dos herramientas principales
tab_audio, tab_pdf = st.tabs(["🎙️ Desgrabar Clase (Audio)", "📚 Crear Material de Estudio (PDF)"])

# ---------------------------------------------------------
# PESTAÑA 1: AUDIO A APUNTES
# ---------------------------------------------------------
with tab_audio:
    st.header("Transforma audios en apuntes estructurados")
    uploaded_audio = st.file_uploader("Sube la grabación de la clase", type=["mp3", "wav", "m4a"])
    
    if uploaded_audio and st.button("🚀 Generar Apuntes desde Audio"):
        status_box = st.status("Procesando la clase...", expanded=True)
        
        try:
            status_box.write("Guardando archivo temporal...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_audio.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_audio.read())
                tmp_path = tmp_file.name
            
            status_box.write("Transcribiendo con Whisper (esto puede tardar según la duración del audio)...")
            transcripcion = transcribe_audio_file(tmp_path)
            os.unlink(tmp_path) # Limpieza inmediata
            
            if not transcripcion.strip():
                status_box.update(label="Error en transcripción", state="error")
                st.error("No se detectó voz en el audio.")
            else:
                status_box.write("Audio transcrito. Llama 3.1 está redactando los apuntes...")
                apuntes = generar_apuntes(transcripcion)
                
                status_box.update(label="¡Apuntes generados con éxito!", state="complete")
                
                st.markdown("---")
                st.download_button("💾 Descargar Apuntes (.md)", data=apuntes, file_name="Apuntes_Clase.md", mime="text/markdown")
                st.markdown(apuntes)
                
        except Exception as e:
            status_box.update(label="Error en el proceso", state="error")
            st.error(f"Fallo técnico: {str(e)}")

# ---------------------------------------------------------
# PESTAÑA 2: PDF A FLASHCARDS / TEST
# ---------------------------------------------------------
with tab_pdf:
    st.header("Exprime los PDFs de tu profesor")
    uploaded_pdf = st.file_uploader("Sube el temario en PDF", type=["pdf"])
    
    if uploaded_pdf:
        modo_estudio = st.radio("¿Qué material quieres generar?", ["Flashcards (Memorización)", "Examen Tipo Test (Evaluación)"], horizontal=True)
        
        if st.button("🧠 Generar Material"):
            with st.status("Procesando documento...", expanded=True) as status:
                try:
                    status.write("Extrayendo texto del PDF...")
                    raw_text = extract_text_from_pdf(uploaded_pdf)
                    
                    if not raw_text.strip():
                        status.update(label="Error de lectura", state="error")
                        st.error("El PDF está vacío o es un escaneo sin OCR.")
                    else:
                        status.write("Optimizando texto para ahorrar tokens...")
                        clean_text = re.sub(r'\s+', ' ', raw_text) # Limpieza exprés
                        
                        status.write(f"Enviando a Llama 3.1 para generar {modo_estudio}...")
                        
                        if "Flashcards" in modo_estudio:
                            resultado = generar_flashcards(clean_text)
                            archivo_salida = "Flashcards_Temario.md"
                        else:
                            resultado = generar_test(clean_text)
                            archivo_salida = "Examen_Temario.md"
                            
                        status.update(label="¡Material de estudio listo!", state="complete")
                        
                        st.markdown("---")
                        st.download_button(f"💾 Descargar {modo_estudio.split()[0]} (.md)", data=resultado, file_name=archivo_salida, mime="text/markdown")
                        st.markdown(resultado)
                        
                except Exception as e:
                    status.update(label="Error en el proceso", state="error")
                    st.error(f"Fallo técnico: {str(e)}")