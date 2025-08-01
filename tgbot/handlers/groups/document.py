import json
import os

from aiogram import Router, F, types

from database.repo.requests import RequestsRepo
from utils.chat_gpt import get_response
from utils.pdf_to_image import pdf_to_image
from tgbot.utils.excel import update_filtered_data_advanced
from utils.helpers import format_complex_string_safe

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
        response_json = json.loads(response.output_text)
        print(document_name, response_json)

        # reference_number = response_json.get('7 Справочный номер')
        #
        # reference_number, is_correct = format_complex_string_safe(reference_number)
        #
        # if not is_correct:
        #     await message.answer(f"переотправьте файл с названием {document_name} еще раз")
        #
        # date = reference_number.split('/')[1].strip()
        #
        # transport_number = response_json.get('18 Транспортное средство при отправлении')
        # transport_number_list = transport_number.split()
        # number = None
        # if len(transport_number_list) == 2:
        #     second = transport_number_list[1]
        #     if '/' in second:
        #         number = second.split('/')[0]
        #     else:
        #         number = second
        # print(number)

        # number = transport_number_list[1].split('/')[0]
        # print(number)
        # gross_weight = response_json.get('Вес брутто')
        # net_weight = response_json.get('Вес нетто')
        # places_quantity = response_json.get('Количество мест')
        #
        #
        #
        #
        # df, stats = update_filtered_data_advanced(
        #     file_path=all_chemistry_files[0].file_path,
        #     filters=[
        #         ("UNI", "contains", number)
        #     ],
        #     updates={
        #         'ГТД ИМ73': reference_number,
        #         'Дата начала хранения': date
        #     },
        #     save=True,
        #     skip_existing=True
        # )
        # print(df, stats)