import json
import os

from aiogram import Router, F, types

from database.repo.requests import RequestsRepo
from utils.chat_gpt import get_response
from utils.pdf_to_image import pdf_to_image
from tgbot.utils.excel import update_filtered_data_advanced
from utils.helpers import (
    format_complex_string_safe,
    check_transport_number_is_correct
)
from utils.claude import make_claude_request


group_document_router = Router()


@group_document_router.message(F.chat.type.in_({"group", "supergroup"}))
@group_document_router.message(F.document)
async def get_message_from_group(message: types.Message, repo: "RequestsRepo"):
    all_chemistry_files = await repo.chemistry_file.get_all_files()
    file_path = all_chemistry_files[0].file_path
    print(file_path)

    date = message.date.date().strftime("%d.%m.%Y")
    mime_type = message.document.mime_type
    if mime_type in ['application/pdf']:
        os.makedirs(f'documents/{date}', exist_ok=True)

        document = message.document
        document_name = document.file_name

        path = f'documents/{date}'
        destination = f'{path}/{document_name}'

        try:
            await message.bot.download(
                document.file_id,
                destination=destination
            )
        except TimeoutError:
            await message.answer(f'Отправьте файл {document_name} еще раз')

        output_file = document_name.split('.')[0]
        image = pdf_to_image(destination, path, output_file)

        response = get_response(image_path=image)

        print(document_name, response.output_text)

