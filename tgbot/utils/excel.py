import pandas as pd
from config.loader import CARGO_TRACKING_FIELDS


DOCUMENT_PATH = '../../documents/search-documents-QCRT (18).xlsx'


def _convert_to_dict(item: list):
    return dict(zip(CARGO_TRACKING_FIELDS, item))


def get_excel_data(file_path: str):
    values = pd.read_excel(file_path).values.tolist()
    result = []
    for item in values:
        result.append(_convert_to_dict(item))
    return result



