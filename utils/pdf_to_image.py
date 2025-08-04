import os

from pdf2image import convert_from_path


def pdf_to_image(pdf_path: str, output_path: str, output_file: str):
    images = convert_from_path(
        pdf_path,
        first_page=1,
        last_page=1,
        dpi=300
    )[0]

    if not images:
        return None

    # Сохраняем изображение сразу с нужным именем
    image_path = f"{output_path}/{output_file}.jpg"
    images.save(image_path, "JPEG")

    return image_path


