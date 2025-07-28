import json
import os


from aiogram import Router, F, types

from utils.chat_gpt import get_response
from utils.pdf_to_image import pdf_to_image
from utils.helpers import write_to_json, read_json


group_document_router = Router()

@group_document_router.message(F.chat.type.in_({"group", "supergroup"}))
@group_document_router.message(F.document)
async def get_message_from_group(message: types.Message):
    date = message.date.date().strftime("%d.%m.%Y")
    mime_type = message.document.mime_type
    if mime_type in ['application/pdf']:
        os.makedirs(f'documents/{date}', exist_ok=True)

        document = message.document
        document_name = document.file_name
        path = f'documents/{date}'
        destination = f'{path}/{document_name}'

        await message.bot.download(
            document.file_id,
            destination=destination
        )

        output_file = document_name.split('.')[0]
        image = pdf_to_image(destination, path, output_file)
        image_name = image.split('/')[-1]

        response = get_response(image_path=image)
        response_json = json.loads(response.output_text)
        write_to_json(response_json, f'documents/{date}/{image_name}.json')




