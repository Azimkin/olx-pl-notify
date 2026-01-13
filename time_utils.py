from datetime import datetime, timedelta
import locale
import re


def parse_polish_datetime(date_str: str) -> datetime:
    """
    Конвертирует строку с датой/временем в формате польского языка в объект datetime.

    Поддерживает форматы:
    - "Dzisiaj o HH:MM" (сегодня в HH:MM)
    - "Wczoraj o HH:MM" (вчера в HH:MM)
    - "DD месяц YYYY" (например: "07 stycznia 2026")
    - "DD месяц YYYY o HH:MM" (например: "07 stycznia 2026 o 22:01")

    Args:
        date_str (str): Строка с датой/временем на польском языке

    Returns:
        datetime: Объект datetime

    Raises:
        ValueError: Если строка не соответствует поддерживаемым форматам
    """
    # Устанавливаем польскую локаль для парсинга названий месяцев
    try:
        locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Polish_Poland.1250')
        except locale.Error:
            # Если не удалось установить польскую локаль, используем словарь для перевода
            pass

    # Приводим к нижнему регистру для удобства обработки
    date_str_lower = date_str.lower().replace('odświeżono dnia ', '').replace('odświeżono ', '').strip()

    # Словарь для перевода польских названий месяцев (если локаль не поддерживается)
    polish_months = {
        'stycznia': 1, 'styczen': 1, 'styczeń': 1,
        'lutego': 2, 'luty': 2,
        'marca': 3, 'marzec': 3,
        'kwietnia': 4, 'kwiecien': 4, 'kwiecień': 4,
        'maja': 5, 'maj': 5,
        'czerwca': 6, 'czerwiec': 6,
        'lipca': 7, 'lipiec': 7,
        'sierpnia': 8, 'sierpien': 8, 'sierpień': 8,
        'wrzesnia': 9, 'wrzesien': 9, 'wrzesień': 9,
        'pazdziernika': 10, 'października': 10, 'pazdziernik': 10, 'październik': 10,
        'listopada': 11, 'listopad': 11,
        'grudnia': 12, 'grudzien': 12, 'grudzień': 12
    }

    # Паттерны для распознавания форматов
    patterns = [
        # Формат "Dzisiaj o HH:MM"
        (r'^dzisiaj\s+o\s+(\d{1,2}):(\d{2})$',
         lambda m: datetime.now().replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0, microsecond=0)),

        # Формат "Wczoraj o HH:MM"
        (r'^wczoraj\s+o\s+(\d{1,2}):(\d{2})$',
         lambda m: (datetime.now() - timedelta(days=1)).replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0,
                                                                microsecond=0)),

        # Формат "DD месяц YYYY o HH:MM"
        (r'^(\d{1,2})\s+([a-ząćęłńóśźż]+)\s+(\d{4})\s+o\s+(\d{1,2}):(\d{2})$',
         lambda m: datetime(int(m.group(3)), polish_months.get(m.group(2), 1), int(m.group(1)), int(m.group(4)),
                            int(m.group(5)))),

        # Формат "DD месяц YYYY" (без времени)
        (r'^(\d{1,2})\s+([a-ząćęłńóśźż]+)\s+(\d{4})$',
         lambda m: datetime(int(m.group(3)), polish_months.get(m.group(2), 1), int(m.group(1)))),
    ]

    # Пробуем каждый паттерн
    for pattern, converter in patterns:
        match = re.match(pattern, date_str_lower, re.IGNORECASE)
        if match:
            return converter(match)

    # Если ни один паттерн не подошел, пробуем парсить стандартными средствами с польской локалью
    try:
        # Пробуем различные форматы
        formats_to_try = [
            '%d %B %Y o %H:%M',  # 07 stycznia 2026 o 22:01
            '%d %B %Y',  # 07 stycznia 2026
            '%d %b %Y o %H:%M',  # 07 sty 2026 o 22:01
            '%d %b %Y',  # 07 sty 2026
        ]

        for fmt in formats_to_try:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
    except:
        pass

    # Если ничего не помогло
    raise ValueError(f"Не удалось распознать формат даты: {date_str}")


# Тестирование функции с примерами из задания
if __name__ == "__main__":
    test_cases = [
        "Dzisiaj o 22:01",
        "Dzisiaj o 00:01",
        "07 stycznia 2026",
        "07 stycznia 2026 o 22:01",
        "Wczoraj o 15:30",  # дополнительный пример
    ]

    for test in test_cases:
        try:
            result = parse_polish_datetime(test)
            print(f"'{test}' -> {result}")
        except ValueError as e:
            print(f"'{test}' -> Ошибка: {e}")

    # Дополнительный пример использования
    print("\nПример использования в коде:")
    date_str = "Dzisiaj o 14:30"
    dt_object = parse_polish_datetime(date_str)
    print(f"Строка '{date_str}' преобразована в: {dt_object}")
    print(f"Форматированный вывод: {dt_object.strftime('%Y-%m-%d %H:%M:%S')}")