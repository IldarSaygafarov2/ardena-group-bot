import json


def write_to_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_complex_string_safe(input_string: str) -> tuple[str, bool]:
    """
    Форматирует строку в стандартный вид и проверяет начинается ли она с числового значения.
    Если формат не поддерживается, возвращает исходную строку.

    Args:
        input_string: Строка для форматирования

    Returns:
        tuple[str, bool]: (отформатированная строка, признак начала с числового значения)
    """
    try:
        if input_string is None:
            return "", False

        # Очищаем строку от лишних пробелов
        clean_string = ' '.join(input_string.split())

        # Проверяем, начинается ли строка с числового значения
        first_part = clean_string.split('/')[0].strip() if clean_string else ""
        starts_with_number = first_part.isdigit()

        # Разбиваем строку по слешам и очищаем от пробелов
        parts = [part.strip() for part in clean_string.split('/')]

        # Если 4 части (например: "27014 / 25 / 0705 / 0006929")
        if len(parts) == 4:
            try:
                number = parts[0]
                day = str(int(parts[1])).zfill(2)

                # Обработка месяца и года из одной части
                date_part = parts[2]
                if len(date_part) >= 4:
                    month = str(int(date_part[:2])).zfill(2)
                    year = f"20{date_part[2:]}" if len(date_part[2:]) == 2 else date_part[2:]
                else:
                    month = str(int(date_part)).zfill(2)
                    year = "2025"  # дефолтный год

                code = parts[3].zfill(6)
                return f"{number} / {day}.{month}.{year} / {code}", starts_with_number
            except (ValueError, IndexError):
                pass

        # Если строка уже в формате "число / дд.мм.гггг / код"
        if len(parts) == 3:
            try:
                number, date, code = parts
                if '.' in date:
                    # Строка уже в нужном формате
                    return f"{number} / {date} / {code.zfill(6)}", starts_with_number
            except (ValueError, IndexError):
                pass

        # Если 5 частей (формат: число/день/месяц/год/код)
        if len(parts) == 5:
            try:
                number = parts[0]
                day = str(int(parts[1])).zfill(2)
                month = str(int(parts[2])).zfill(2)
                year = parts[3]
                code = parts[4].zfill(6)
                return f"{number} / {day}.{month}.{year} / {code}", starts_with_number
            except (ValueError, IndexError):
                pass

        # Если формат не поддерживается, возвращаем исходную строку
        return clean_string, starts_with_number

    except Exception:
        return input_string, starts_with_number


incorrect_number = 'АВТО 6016GGGA80287AA'
correct_number = 'АВТО 5045НВА/5009708А'


def check_transport_number_is_correct(transport_number: str):
    _number = transport_number.split()[-1]
    if '/' in _number:
        return transport_number, True
    return transport_number, False
