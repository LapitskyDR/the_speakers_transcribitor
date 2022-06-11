import json

from vosk import Model, KaldiRecognizer


class Transcriber:
    def __init__(self, model_path, model_name, frame_rate):
        self.model = Model(model_path + model_name)
        self.frame_rate = frame_rate
        self.rec = KaldiRecognizer(self.model, self.frame_rate)

    def recognize(self, audio_file):
        res = ''

        frames = audio_file.readframes(self.frame_rate)
        while frames != b'':
            if self.rec.AcceptWaveform(frames):
                res += json.loads(self.rec.Result())['text'] + " "
            frames = audio_file.readframes(self.frame_rate)
        res += json.loads(self.rec.FinalResult())['text']
        res.replace("  ", " ").strip()

        return res

    # TODO: Добавить функцию распознавания участников.
    # TODO: Добавить функцию привязки к тайм-кодам.