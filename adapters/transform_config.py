import configparser


def _processing(param):
    res = param.replace("\n", "")
    res = res.replace(", ", ",").split(",")

    if len(res) == 1:
        res = res[0]
    return res


def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf-8')

    conf_data = {
        "HOST": _processing(config['Server']['host']),
        "PORT": int(_processing(config['Server']['port'])),
        "MODEL_NAME": _processing(config['Model']['name']),
        "MODEL_PATH": _processing(config['Model']['path']),
        "CHANNELS": int(_processing(config['Audio']['channels'])),
        "SAMPLE_WIDTH": int(_processing(config['Audio']['sample_width'])),
        "FRAME_RATE": int(_processing(config['Audio']['frame_rate'])),
    }

    return conf_data
