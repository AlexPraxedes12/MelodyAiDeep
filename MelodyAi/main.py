from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from audio_processing.pitch_correction import correct_pitch
import os

app = FastAPI()

@app.post("/correct-pitch")
async def correct_pitch_endpoint(
    file: UploadFile = File(...),
    intensity: str = "medium",
    scale: str = "C_major",
    keep_vibrato: bool = True
):
    # Validar formato
    if not file.filename.endswith((".mp3", ".wav")):
        raise HTTPException(status_code=400, detail="Solo se aceptan .mp3 o .wav")
    
    # Guardar archivo temporal
    temp_path = f"temp_audio/{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        # Corregir pitch
        output_path = correct_pitch(
            input_path=temp_path,
            intensity=intensity,
            scale=scale,
            keep_vibrato=keep_vibrato
        )
        return FileResponse(output_path, media_type="audio/wav")
    
    finally:
        # Limpieza
        os.remove(temp_path)
        if os.path.exists(output_path):
            os.remove(output_path)