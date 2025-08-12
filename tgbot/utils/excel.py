import typing

import pandas as pd

DOCUMENT_PATH = '../../documents/search-documents-QCRT (18).xlsx'
TEST_PATH = '../../documents/29.07.2025/Chemistry file - 28.07.2025_0007654793.xlsx'


def get_excel_data(file_path: str, required_fields: list):
    values = pd.read_excel(file_path).values.tolist()
    result = []
    for item in values:
        result.append(_convert_to_dict(item, required_fields))
    return result


def get_filtered_data(file_path: str, column_name: str, filter_value: any):
    df = pd.read_excel(file_path)
    filtered_df = df[df[column_name] == filter_value]
    return filtered_df


# Более сложный вариант с дополнительными параметрами
def get_filtered_excel_data(
        file_path: str,
        filter_column: str,
        filter_value: any,
        required_columns: list[str] = None,
        operation: str = 'equals'
):
    """
    Получение отфильтрованных данных из Excel файла

    Args:
        file_path (str): Путь к Excel файлу
        filter_column (str): Название столбца для фильтрации
        filter_value (any): Значение для фильтрации
        required_columns (list[str], optional): Список нужных столбцов
        operation (str): Тип операции фильтрации ('equals', 'contains', 'greater', 'less')
    """
    df = pd.read_excel(file_path)

    if operation == 'equals':
        filtered_df = df[df[filter_column] == filter_value]
    elif operation == 'contains':
        filtered_df = df[df[filter_column].str.contains(filter_value, na=False)]
    elif operation == 'greater':
        filtered_df = df[df[filter_column] > filter_value]
    elif operation == 'less':
        filtered_df = df[df[filter_column] < filter_value]
    else:
        raise ValueError("Неподдерживаемая операция фильтрации")
    if required_columns:
        filtered_df = filtered_df[required_columns]

    result = filtered_df.to_dict('records')

    return result


# res = get_filtered_excel_data(
#     file_path=TEST_PATH,
#     filter_column='UNI',
#     filter_value='80W648WA',
#     operation='contains'
# )


# Версия с поддержкой различных операторов сравнения
def update_filtered_data_advanced(
        file_path: str,
        filters: list[tuple[str, str, typing.Any]],  # [(column, operator, value), ...]
        updates: dict[str, typing.Any],
        skip_existing: bool = True,
        save: bool = True
) -> tuple[pd.DataFrame, dict[str, int], list]:
    """
    Обновляет данные с поддержкой различных операторов сравнения и пропуском существующих значений

    Args:
        file_path (str): Путь к файлу
        filters (list): Список кортежей (столбец, оператор, значение)
        updates (dict): Словарь с обновлениями
        skip_existing (bool): Пропускать записи, где значение уже совпадает с обновляемым
        save (bool): Сохранить изменения

    Returns:
        tuple[pd.DataFrame, dict[str, int], list]: DataFrame, статистика обновлений и список UNI обновленных записей
    """
    df = pd.read_excel(file_path)
    stats = {
        'total_matching_rows': 0,
        'updated_rows': 0,
        'skipped_rows': 0
    }
    updated_unis = []  # Список для хранения UNI обновленных записей

    operators = {
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y,
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y,
        'contains': lambda x, y: x.str.contains(y, na=False),
        'startswith': lambda x, y: x.str.startswith(y, na=False),
        'endswith': lambda x, y: x.str.endswith(y, na=False)
    }

    mask = pd.Series(True, index=df.index)
    for column, operator, value in filters:
        if operator not in operators:
            raise ValueError(f"Неподдерживаемый оператор: {operator}")
        mask &= operators[operator](df[column], value)

    stats['total_matching_rows'] = mask.sum()
    final_update_mask = pd.Series(False, index=df.index)

    for column, new_value in updates.items():
        if column not in df.columns:
            raise ValueError(f"Столбец '{column}' не найден в файле")

        if skip_existing:
            value_differs_mask = df[column] != new_value
            update_mask = mask & value_differs_mask

            rows_to_update = update_mask.sum()
            stats['updated_rows'] += rows_to_update
            stats['skipped_rows'] += mask.sum() - rows_to_update

            df.loc[update_mask, column] = new_value
            final_update_mask |= update_mask
        else:
            df.loc[mask, column] = new_value
            stats['updated_rows'] += mask.sum()
            final_update_mask |= mask

    # Получаем UNI обновленных записей
    if 'UNI' in df.columns:
        updated_unis = df.loc[final_update_mask, 'UNI'].tolist()

    if save:
        df.to_excel(file_path, index=False)

    return df, stats, updated_unis


# updated_df, stats, unis = update_filtered_data_advanced(
#     file_path=TEST_PATH,
#     filters=[
#         ('UNI', 'contains', '50N782UA')
#     ],
#     updates={
#         'ГТД ИМ73': '27014 / 25.07.2025 / 0009559',
#         'Дата начала хранения': '25.07.2025'
#     },
#     save=True,
#     skip_existing=True
# )
# print(stats)
# print(unis)
#
# print(updated_df)

def fill_excel_with_variables(
        file_path: str,
        output_path: str,
        declaration_type,
        dispatch_date,
        vehicle_number,
        gross_weight,
        net_weight,
        cargo_places_count,
        arrival_date,
        gtd_number,
        gtd_registration_number,
        storage_start_date,
        gtd_amount,
        gtd_currency_rate,
        station,
        recipient

) -> tuple:
    """
    Добавляет строку в Excel-файл, если такой записи ещё нет.
    Уникальность определяется по: '№ вагона / авто' + 'Вес нетто, мт'.
    """

    # Загрузка файла
    df = pd.read_excel(file_path)

    # Проверка на дубликат
    exists = (
            (df['№ вагона / авто'] == vehicle_number) &
            (df['Вес нетто, мт'] == net_weight)
    ).any()

    if exists:
        return 0, []

    # Новая строка — ключи на русском языке, как в файле
    new_row = {
        "Дата отправки": dispatch_date,
        "№ вагона / авто": vehicle_number,
        "Вес брутто, мт": gross_weight,
        "Вес нетто, мт": net_weight,
        "Количество грузовых мест": cargo_places_count,
        "Дата начала хранения": storage_start_date,
        "Сумма ГТД": gtd_amount,
        "Курс валют ГТД": gtd_currency_rate,
        "Станция": station,
        "Статус отчета": "отправить"
    }

    if declaration_type == '73':
        new_row.update({
            "Дата прибытия:": arrival_date,
            "ГТД ИМ73": gtd_number,
            "Рег. Номер ГТД": gtd_registration_number,
        })

    if declaration_type == '40':
        new_row.update({
            'ГТД ИМ40': gtd_number,
            'Рег. Номер ГТД.1': gtd_registration_number,
            'Дата окончания хранения': arrival_date,
            'Клиент на выдачу': recipient,
        })


    # Добавление и сохранение
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(output_path, index=False)

    return 1, [vehicle_number]
