from uvicorn import run

from adapters import get_config


if __name__ == "__main__":
    # Запуск сервера
    config = get_config()
    run("use_cases.transcribe:app", host=config['HOST'], port=config['PORT'])

    # TODO: Добавить обработку ошибок запуска сервера