import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

load_dotenv()

def _get_llm(temperatura=0.2):
    """Inicializa la conexión con Ollama usando un contexto amplio para clases largas."""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return Ollama(
        base_url=base_url,
        model="llama3.1",
        temperature=temperatura,
        num_ctx=16384 # Vital para que no se trunque al leer transcripciones de 2 horas
    )

def generar_apuntes(transcripcion: str) -> str:
    """Transforma la desgrabación de una clase en apuntes estructurados."""
    llm = _get_llm(temperatura=0.3)
    
    template = """
    Eres un estudiante universitario de matrícula de honor. A partir de la siguiente transcripción de una clase teórica, elabora unos apuntes definitivos en formato Markdown.

    Debes estructurar el documento en:
    1. 🎯 **Tema Principal**: De qué trata la clase en 2 líneas.
    2. 📚 **Desarrollo Teórico**: Explica los conceptos paso a paso usando títulos y subtítulos. Usa **negritas** para los términos clave.
    3. ⚠️ **Ojo al dato**: Destaca cualquier cosa que el profesor haya enfatizado mucho o haya dicho que "suele caer en exámenes". Si no hay nada, omite esta sección.
    4. 📝 **Resumen Express**: 3 bullet points con lo mínimo que hay que saber antes del examen.

    Transcripción de la clase:
    {texto}
    """
    prompt = PromptTemplate(input_variables=["texto"], template=template)
    return (prompt | llm).invoke({"texto": transcripcion})

def generar_flashcards(texto_temario: str) -> str:
    """Extrae conceptos clave y genera tarjetas de memorización."""
    llm = _get_llm(temperatura=0.2) # Temperatura más baja para evitar inventos
    
    template = """
    Eres un experto en técnicas de estudio espaciado (Anki). Lee el siguiente temario y genera una lista de Flashcards (Pregunta - Respuesta corta) con los conceptos más importantes para memorizar.
    
    Usa estrictamente este formato para cada tarjeta:
    **P:** [Pregunta conceptual y directa]
    **R:** [Respuesta de máximo 2 líneas]
    ---
    
    Genera un máximo de 10 flashcards.
    
    Temario:
    {texto}
    """
    prompt = PromptTemplate(input_variables=["texto"], template=template)
    return (prompt | llm).invoke({"texto": texto_temario})

def generar_test(texto_temario: str) -> str:
    """Crea un examen tipo test basado en el PDF para autoevaluación."""
    llm = _get_llm(temperatura=0.1) # Muy baja para asegurar precisión en las opciones
    
    template = """
    Eres un profesor universitario diseñando un examen tipo test desafiante. Basándote ÚNICAMENTE en el texto proporcionado, genera 5 preguntas de opción múltiple.
    
    Reglas:
    - Cada pregunta debe tener 4 opciones (A, B, C, D).
    - Solo una opción es correcta.
    - Las opciones incorrectas deben sonar plausibles pero ser falsas según el texto.
    - AL FINAL de todas las preguntas, incluye una sección "Plantilla de Corrección" con las respuestas correctas.

    Texto base:
    {texto}
    """
    prompt = PromptTemplate(input_variables=["texto"], template=template)
    return (prompt | llm).invoke({"texto": texto_temario})