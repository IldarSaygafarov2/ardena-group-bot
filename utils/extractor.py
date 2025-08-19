import re
import os
import cv2

PLATE_CHARS = "A-ZА-Я0-9"
PLATE_RE = f"[{PLATE_CHARS}]"

def extract_vehicle_number(text: str, filename: str | None = None) -> str | None:
    """
    Возвращает:
      - номер вагона (если найден «ЖД ...»),
      - ИЛИ полный номер авто вместе с частью после «/»,
      - ИЛИ None.
    Учитывает OCR-артефакты: «Ж Д», пробелы вокруг «/», кириллицу/латиницу.
    """

    if not text:
        text = ""

    T = text.upper()
    # Нормализация: убрать лишние пробелы, привести «Ж Д» -> «ЖД», слеши без пробелов
    T = re.sub(r"\s+", " ", T)
    T = T.replace("Ж Д", "ЖД")
    T = re.sub(r"\s*/\s*", "/", T)

    # --- 1) ВАГОН: ЖД <цифры> ---
    m = re.search(r"\bЖД\s*[:\-№N]*\s*([0-9]{5,12})\b", T)
    if m:
        return m.group(1)

    # --- 2) АВТО по ключевым словам ---
    # примеры: "АВТО 80K087UA/809414AA", "ABTO 60166GBA"
    m = re.search(
        rf"(?:\bАВТО(?:МОБИЛЬ)?\b|\bABTO\b)\s*({PLATE_RE}{{2,12}}(?:/{PLATE_RE}{{2,12}})?)",
        T
    )
    if m:
        # вернуть как есть (уже без пробелов вокруг /)
        return m.group(1)

    # --- 3) Fallback: любой «похожий на номер авто» токен с / ---
    # (сначала предпочитаем вариант со слэшем, чтобы вернуть полный)
    m = re.search(rf"\b[0-9]{{2,6}}[{PLATE_CHARS}]{{1,4}}/[0-9]{{2,6}}[{PLATE_CHARS}]{{1,4}}\b", T)
    if m:
        return m.group(0)

    # --- 4) Fallback: одиночный «похожий» номер без ключевых слов ---
    m = re.search(rf"\b[0-9]{{2,6}}[{PLATE_CHARS}]{{1,4}}\b", T)
    if m:
        return m.group(0)

    # --- 5) Fallback по имени файла ---
    if filename:
        name = os.path.splitext(os.path.basename(filename))[0].upper()
        name = re.sub(r"\s+", " ", name)
        # попробуем сначала со слэшем
        m = re.search(rf"\b[0-9]{{2,6}}[{PLATE_CHARS}]{{1,4}}/[0-9]{{2,6}}[{PLATE_CHARS}]{{1,4}}\b", name)
        if m:
            return m.group(0)
        m = re.search(rf"\b[0-9]{{2,6}}[{PLATE_CHARS}]{{1,4}}\b", name)
        if m:
            return m.group(0)

    return None

def normalize_text(s: str) -> str:
    """Приводим текст в удобный вид"""
    s = s.replace("\n", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def ocr_image(img_path: str) -> str:
    """OCR с предобработкой"""

    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(img_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    text = pytesseract.image_to_string(Image.fromarray(th), lang="rus+eng")
    return normalize_text(text)
    # return text


def extract_gtd(img_path: str) -> str:
    text = ocr_image(img_path)

    # GTD в формате 27014 / 01.01.2025 / 1234567
    gtd_match = re.search(r"\b(27014|12003)\s*/\s*(\d{2}\.\d{2}\.\d{4})\s*/\s*(\d{7})\b", text)
    if gtd_match:
        return f"{gtd_match.group(1)} / {gtd_match.group(2)} / {gtd_match.group(3)}"
    return "none"