class Speaker:
    """ Создание диктора для записи параметров распознанной речи."""

    def __init__(self, id):
        """ Инициализация диктора.

        :param id: Идентификатор диктора
        :type id: int
        """

        self.id = id
        self.sequences = []
        self.signals = []
        self.timecodes = []
        self.text = []
