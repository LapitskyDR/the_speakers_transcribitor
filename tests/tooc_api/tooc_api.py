import requests

from .audio_adaptation import get_audio
from .transform_config import get_config


def transcribition(path, amt):
    """ Отправка запроса для транскрибирования аудиофайла.

    :param path: Путь до аудиофайла
    :type path: str
    :param amt: Количество дикторов
    :type amt: int

    :return: Результат транскрибирования
    :rtype: dict
    """

    # Загрузка конфигурации и преобразование аудиофайла в поддерживаемый формат
    config = get_config()
    audio_file = get_audio(path, config['CHANNELS'],
                           config['SAMPLE_WIDTH'], config['FRAME_RATE'])

    # Формирование данных запроса
    url = f"http://{config['HOST']}:{config['PORT']}/transcribe"
    file = {'audio_file': audio_file}
    params = {'amt': amt}

    # Отправка POST-запроса
    res = requests.post(url=url, files=file, params=params)
    audio_file.close()

    return res
