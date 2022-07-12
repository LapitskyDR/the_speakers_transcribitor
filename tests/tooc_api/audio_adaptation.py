import wave

from pydub import AudioSegment


def get_audio(path, channels, sample_width, frame_rate):
    """ Преобразование аудиофайла в поддерживаемый формат.

    :param path: Путь к аудиофайлу
    :type path: str
    :param channels: Количество каналов (1)
    :type channels: int
    :param sample_width: Размер сэмпла (2 байта)
    :type sample_width: int
    :param frame_rate: Частота дискретизации (16000 Гц)
    :type frame_rate: int

    :return: Открытый аудиофайл.
    :rtype: class '_io.BufferedReader'
    """

    data = AudioSegment.from_wav(path)
    data = data. \
        set_channels(channels). \
        set_sample_width(sample_width). \
        set_frame_rate(frame_rate)

    with wave.open(path, "wb") as audio_file:
        audio_file.setnchannels(data.channels)
        audio_file.setsampwidth(data.sample_width)
        audio_file.setframerate(data.frame_rate)
        audio_file.setnframes(int(data.frame_count()))
        audio_file.writeframesraw(data._data)

    return open(path, "rb")
