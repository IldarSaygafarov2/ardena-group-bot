import os

from aiogram import Router, types, F

from database.repo.requests import RequestsRepo
from schemas.cargo_tracking import CargoTrackingCreateSchema, CargoTrackingSchema
from tgbot.utils.converters import convert_nan_to_none, convert_str_to_date
from tgbot.utils.excel import get_excel_data
from config.contants import CARGO_TRACKING_FIELDS

admin_text_router = Router()


@admin_text_router.message(F.document & F.chat.type.in_({"private"}))
async def get_document(message: types.Message, repo: RequestsRepo):
    document = message.document

    # Example of file type validation
    allowed_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    if document.mime_type not in allowed_types:
        await message.answer("This file type is not allowed!")
        return

    # File size validation (example: 10MB limit)
    if document.file_size > 10 * 1024 * 1024:  # 10MB in bytes
        await message.answer("File is too large!")
        return

    os.makedirs('documents', exist_ok=True)
    destination = os.path.join('documents', document.file_name)

    await message.bot.download(
        document.file_id,
        destination=destination
    )

    excel_data = get_excel_data(destination, CARGO_TRACKING_FIELDS)

    await message.answer('Данные были обновлены, либо добавлены в базу!')
