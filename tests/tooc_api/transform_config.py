import configparser


def _processing(param):
    """ Удаление лишних пробелов параметра конфигурации для метода get_config.

    :param param: Параметр для форматирования
    :type param: str

    :return: Отформатированный параметр конфигурации
    :rtype: str
    """

    res = param.replace("\n", "")
    res = res.replace(", ", ",").split(",")

    if len(res) == 1:
        res = res[0]
    return res


def get_config():
    """ Загрузка конфигурации.

    :return: Словарь параметров конфигурации
    :rtype: dict
    """

    config = configparser.ConfigParser()
    config.read("tooc_api/config.ini", encoding='utf-8')

    conf_data = {
        'CHANNELS': int(_processing(config['Audio']['channels'])),
        'SAMPLE_WIDTH': int(_processing(config['Audio']['sample_width'])),
        'FRAME_RATE': int(_processing(config['Audio']['frame_rate'])),
        "HOST": _processing(config['Server']['host']),
        "PORT": int(_processing(config['Server']['port']))
    }

    return conf_data
