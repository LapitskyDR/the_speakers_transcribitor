import wave

from fastapi import FastAPI, UploadFile

from entities import Transcriber
from adapters import get_config, response_format


# Загрузка конфигурации и инициализация транскрибатора
config = get_config()
trans = Transcriber(
    model_path=config['MODEL_PATH'],
    model_rec_name=config['MODEL_REC_NAME'],
    model_spk_name=config['MODEL_SPK_NAME'],
    frame_rate=config['FRAME_RATE']
)

app = FastAPI()  # Инициализация API

# Обработка POST-запроса
@app.post("/transcribe")
async def get_transcribed_text(audio_file: UploadFile, amt: int):
    """ Транскрибирование аудиофайла (Распознавание речи, определение
    тайм-кодов и распределение распознанных фраз по дикторам).

    :param audio_file: Аудиофайл, который нужно транскрибировать
    :type audio_file: UploadFile
    :param amt: Количество дикторов в аудиофайле
    :type amt: int

    :return: список дикторов (id диктора, его тайм-коды,
    порядковые номера фраз, фразы)
    :rtype: str
    """

    # Распознавание речи и создание тайм-кодов
    with wave.open(audio_file.file, 'rb') as wave_audio:
        speeches = trans.recognize(wave_audio)

    # Распределение распознанных фраз по дикторам
    speakers = trans.diarize(speeches, amt)

    return response_format(speakers)

    # TODO: Добавить доп. методы обработки
    # TODO: Добавить поддержку ассинхронности
