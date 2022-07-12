def response_format(speakers):
    """ Сформировать ответ из результата транскрибирования.

    :param speakers: Обработанный список дикторов
    :type speakers: list

    :return: Результат транскрибирования
    :rtype: dict
    """

    # Формирование словаря с результатом транскрибирования
    res = {"speakers": []}
    for spk in speakers:
        res['speakers'].append({
            'id': spk.id,
            'timecodes': spk.timecodes,
            'sequences': spk.sequences,
            'text': spk.text
        })

    return res

    # TODO: Добавить доп. параметры
