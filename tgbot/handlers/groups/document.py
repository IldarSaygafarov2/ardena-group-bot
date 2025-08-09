import json
import os

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from config.loader import app_config
from database.repo.requests import RequestsRepo
from tgbot.utils.excel import update_filtered_data_advanced
from utils.chat_gpt import get_response
from utils.helpers import split_gtd
from utils.pdf_to_image import pdf_to_image
from tgbot.utils.excel import fill_excel_with_variables

group_document_router = Router()


FIELDS = [
    "Дата отправки",
    "№ вагона / авто",
    "Вес брутто, мт",
    "Вес нетто, мт",
    "Количество грузовых мест",
    "Дата прибытия:",
    "ГТД ИМ73",
    "Рег. Номер ГТД",
    "Дата начала хранения",
    "Сумма ГТД",
    "Курс валют ГТД",
]


async def _send_message(bot, unis, chat_id, declaration_type):
    if not unis:
        return
    message = "ПРИХОД\n" if declaration_type == '73' else "РАСХОД\n"
    for item in unis:
        message += f'{item}\n'
    await bot.send_message(chat_id=chat_id, text=message)


@group_document_router.message(F.chat.type.in_({"group", "supergroup"}))
@group_document_router.message(F.document)
async def get_message_from_group(message: types.Message, repo: "RequestsRepo", state: "FSMContext"):

    all_chemistry_files = await repo.chemistry_file.get_all_files()
    file_path = all_chemistry_files[0].file_path

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

        try:
            response_json = json.loads(response.output_text)
            print(response_json)

            gtd = response_json.get('GTD')

            gtd_number = split_gtd(gtd)[0]
            gtd_date = split_gtd(gtd)[1]

            print(f'{gtd_number=}')

            declaration_type = response_json.get('declaration_type')
            vehicle_id = response_json.get('vehicleId')
            declaration_number = response_json.get('declaration_number')
            weight_b = response_json.get('weightB')
            weight_n = response_json.get('weightN')
            currency_total = response_json.get('currency_total')
            currency_rate = response_json.get('currency_rate')
            count = response_json.get('count')
            if gtd_number == '27014':
                station = 'НУРХАЁТ'
            elif gtd_number == '12003':
                station = 'КЫЗЫЛТЕПА'
            else:
                station = ''

            _, result = fill_excel_with_variables(
                file_path, 
                output_path=file_path,
                dispatch_date=None,
                vehicle_number=vehicle_id,
                gross_weight=weight_b,
                net_weight=weight_n,
                cargo_places_count=count,
                arrival_date=gtd_date,
                gtd_im73=declaration_number,
                gtd_registration_number=gtd,
                storage_start_date=gtd_date,
                gtd_amount=currency_total,
                gtd_currency_rate=currency_rate,
                station=station
            )
            
            print(result)
            



        except Exception as e:
            response_json = {}
            print(e)

        # vehicle_id = response_json.get('vehicleId')

        # try:
        #     gtd = response_json.get('GTD')
        #     date = gtd.split('/')[1].strip()
        # except Exception as e:
        #     gtd = ''
        #     date = ''
        #     print(e)
        #
        # declaration_type = response_json.get('declaration_type')
        # print(document_name, f'{declaration_type=}')

        #
        # if declaration_type == '73':
        #     df, stats, unis = update_filtered_data_advanced(
        #         file_path=file_path,
        #         filters=[
        #             ('UNI', 'contains', vehicle_id),
        #         ],
        #         updates={
        #             'ГТД ИМ73': gtd,
        #             'Дата начала хранения': date
        #         }
        #     )
        #     print('ИМ 73', document_name, stats, unis)
        #     await _send_message(
        #         bot=message.bot,
        #         unis=unis,
        #         chat_id=app_config.bot.admin_chat_id,
        #         declaration_type="73",
        #     )
        #
        # elif declaration_type == '40':
        #     df, stats, unis = update_filtered_data_advanced(
        #         file_path=file_path,
        #         filters=[
        #             ('UNI', 'contains', vehicle_id),
        #         ],
        #         updates={
        #             'Номер накладной': gtd,
        #             'Дата окончания хранения': date
        #         }
        #     )
        #     print('ИМ 40', document_name, stats, unis)
        #     await _send_message(
        #         bot=message.bot,
        #         unis=unis,
        #         chat_id=app_config.bot.admin_chat_id,
        #         declaration_type="40",
        #     )

    # file = types.FSInputFile(file_path)
    # if not is_sent:
    #     await message.bot.send_document(
    #         chat_id=app_config.bot.admin_chat_id,
    #         document=file
    #     )
