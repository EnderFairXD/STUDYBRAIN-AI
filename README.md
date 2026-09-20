# StudyBrain AI: Tutor Universitario Local

Una plataforma 100% privada y local que combina `faster-whisper` (para desgrabación de clases teóricas) y `pdfplumber` (para análisis de temarios) con modelos locales (Llama 3.1 vía Ollama) para generar material de estudio avanzado.

## Características
* **🎙️ Audio a Apuntes:** Transcribe audios de clases y los convierte en apuntes estructurados en Markdown (Temas principales, desarrollo y resumen express).
* **📚 Temario a Flashcards:** Extrae la información clave de PDFs para generar tarjetas de memorización activa espaciada.
* **📝 Temario a Test:** Diseña exámenes de autoevaluación con preguntas de opción múltiple y plantilla de corrección oculta.

## Instalación

1. Clona este repositorio: `git clone <tu-enlace-github>`
2. Crea tu entorno virtual: `python -m venv .venv`
3. Activa el entorno virtual:
   * Windows: `.venv\Scripts\activate`
   * Mac/Linux: `source .venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Copia el archivo de variables de entorno: `cp .env.example .env`
6. Asegúrate de tener [Ollama](https://ollama.com/) ejecutándose localmente con el modelo descargado (`ollama run llama3.1`).
7. Lanza la aplicación: `streamlit run src/main.py`