import os

from aiogram import Router, types, F

from database.repo.requests import RequestsRepo
from aiogram.fsm.context import FSMContext
# from tgbot.utils.converters import convert_nan_to_none, convert_str_to_date
# from tgbot.utils.excel import get_excel_data
# from config.contants import CARGO_TRACKING_FIELDS

admin_text_router = Router()


@admin_text_router.message(F.document & F.chat.type.in_({"private"}))
async def get_document(message: types.Message, repo: RequestsRepo):
    document = message.document
    date = message.date.date().strftime("%d.%m.%Y")

    # Example of file type validation
    allowed_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    if document.mime_type not in allowed_types:
        await message.answer("This file type is not allowed!")
        return

    # File size validation (example: 10MB limit)
    if document.file_size > 10 * 1024 * 1024:  # 10MB in bytes
        await message.answer("File is too large!")
        return

    os.makedirs(f'documents/{date}', exist_ok=True)
    destination = os.path.join(f'documents/{date}', document.file_name)

    to_db = await repo.chemistry_file.add_or_ignore_file(
        name=document.file_name,
        file_path=destination,
        _date=date
    )
    print(to_db)

    await message.bot.download(
        document.file_id,
        destination=destination
    )

    await message.answer('Файл получен!')
