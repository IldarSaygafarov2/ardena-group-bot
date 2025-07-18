from pdf2image import convert_from_path

document_path = "../documents/70F505EA.pdf"
output_path = "../documents/pdf_images"

convert_from_path(document_path, output_folder=output_path, fmt="jpg")
