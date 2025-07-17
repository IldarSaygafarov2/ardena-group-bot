import pandas as pd


DOCUMENT_PATH = '../../documents/search-documents-QCRT (18).xlsx'


def _convert_to_dict(item: list, required_fields: list):
    return dict(zip(required_fields, item))


def get_excel_data(file_path: str, required_fields: list):
    values = pd.read_excel(file_path).values.tolist()
    result = []
    for item in values:
        result.append(_convert_to_dict(item, required_fields))
    return result



