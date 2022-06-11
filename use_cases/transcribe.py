import wave

from fastapi import FastAPI, UploadFile

from entities import Transcriber
from adapters import get_config

config = get_config()
trans = Transcriber(
    model_path=config['MODEL_PATH'],
    model_name=config['MODEL_NAME'],
    frame_rate=config['FRAME_RATE']
)

app = FastAPI()


@app.post("/")
async def get_transcribed_text(audio_file: UploadFile):
    with wave.open(audio_file.file, 'rb') as wave_audio:
        res = trans.recognize(wave_audio)
    return {"result": res} # FIXME: Добавить параметры.
