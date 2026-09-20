import os
from faster_whisper import WhisperModel

def transcribe_audio_file(file_path: str) -> str:
    """
    Carga el modelo Whisper localmente en la CPU, procesa el archivo 
    de audio y devuelve la transcripción con marcas de tiempo.
    """
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(file_path, beam_size=5, language="es")
    
    transcript_text = ""
    for segment in segments:
        start_min = int(segment.start // 60)
        start_sec = int(segment.start % 60)
        end_min = int(segment.end // 60)
        end_sec = int(segment.end % 60)
        
        transcript_text += f"[{start_min:02d}:{start_sec:02d} -> {end_min:02d}:{end_sec:02d}]: {segment.text}\n"
        
    return transcript_text