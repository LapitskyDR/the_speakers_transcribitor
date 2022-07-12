import os
import json

import numpy as np
from sklearn.cluster import KMeans
from vosk import Model, SpkModel, KaldiRecognizer

from .speaker import Speaker


class Transcriber:
    """ Создание транскрибатора для транскрибирования аудиофайла."""

    def __init__(self, model_path, model_rec_name, model_spk_name, frame_rate):
        """ Инициализация транскрибатора.

        :param model_path: Путь к папке с моделями
        :type model_path: str
        :param model_rec_name: Название модели распознавания речи
        :type model_rec_name: str
        :param model_spk_name: Название модели диаризации
        :type model_spk_name: str
        :param frame_rate: Частота дискретизации
        :type frame_rate: int
        """

        self.model = Model(os.path.join(model_path, model_rec_name))
        self.spk_model = SpkModel(os.path.join(model_path, model_spk_name))
        self.frame_rate = frame_rate

    def recognize(self, audio_file):
        """ Распознавание речи, с определением тайм-кода для фразы.

        :param audio_file: Открытый с помощью библиотеки wave, аудиофайл
        :type audio_file: class 'wave.Wave_read'

        :return: Список созданных дикторов
        :rtype: list
        """

        # Инициализация распознавателя и включение определения тайм-кодов
        rec = KaldiRecognizer(self.model, self.frame_rate, self.spk_model)
        rec.SetWords(True)

        # Распознавание речи
        speeches = []
        while (frames := audio_file.readframes(self.frame_rate)) != b'':
            if rec.AcceptWaveform(frames):
                rec_result = json.loads(rec.Result())

                # Проверка на обнаружение диктора
                if 'spk' in rec_result:
                    speeches.append({'sequence': len(speeches)+1,
                                     'signal': rec_result['spk'],
                                     'timecode': [
                                         rec_result['result'][0]['start'],
                                         rec_result['result'][-1]['end']
                                     ],
                                     'text': rec_result['text']})

        # Последняя распознанная фраза
        rec_result = json.loads(rec.FinalResult())
        if 'spk' in rec_result:
            speeches.append({'sequence': len(speeches)+1,
                             'signal': rec_result['spk'],
                             'timecode': [
                                 rec_result['result'][0]['start'],
                                 rec_result['result'][-1]['end']
                             ],
                             'text': rec_result['text']})

        return speeches

    def diarize(self, speeches, amt):
        """ Поиск схожести сигналов фраз, для распределения по дикторам.

        :param speeches: Список созданных дикторов
        :type speeches: list
        :param amt: Количество дикторов
        :type amt: int

        :return: Обработанный список дикторов
        :rtype: list
        """

        # Создание "пустых" дикторов и массива всех сигналов
        speakers = [Speaker(i) for i in range(amt)]
        signals_ = [speech['signal'] for speech in speeches]

        # Кластеризация сигналов методом k-средних
        kmeans = KMeans(n_clusters=amt, random_state=0).fit_predict(
            np.array(signals_)
        )

        # Распределение параметров по дикторам
        for i, id_ in enumerate(kmeans):
            speakers[id_].sequences.append(speeches[i]['sequence'])
            speakers[id_].signals.append(speeches[i]['signal'])
            speakers[id_].timecodes.append(speeches[i]['timecode'])
            speakers[id_].text.append(speeches[i]['text'])

        return speakers

        # TODO: Добавить обработку ошибок дизаризации
        # TODO: Добавить расстановку пунктуации
