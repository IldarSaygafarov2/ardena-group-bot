import json


def write_to_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Версия с дополнительными проверками
def format_complex_string_safe(input_string: str) -> str:
    try:
        clean_string = ' '.join(input_string.split())

        parts = [part.strip() for part in clean_string.split('/')]

        if len(parts) != 5:
            raise ValueError("Строка должна содержать 5 частей, разделенных '/'")

        if not parts[0].isdigit():
            raise ValueError("Первая часть должна быть числом")
        number = parts[0]

        day = int(parts[1])
        if not (1 <= day <= 31):
            raise ValueError("День должен быть от 1 до 31")
        day = str(day).zfill(2)

        month = int(parts[2])
        if not (1 <= month <= 12):
            raise ValueError("Месяц должен быть от 1 до 12")
        month = str(month).zfill(2)

        year = parts[3]
        if not (len(year) == 4 and year.isdigit()):
            raise ValueError("Год должен быть 4-значным числом")

        if not parts[4].isdigit():
            raise ValueError("Код должен содержать только цифры")
        code = parts[4].zfill(6)

        result = f"{number} / {day}.{month}.{year} / {code}"

        return result

    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"Непредвиденная ошибка при форматировании: {str(e)}")


