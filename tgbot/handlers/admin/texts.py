import os
import uuid

from aiogram import Router, types, F

from database.repo.requests import RequestsRepo
from tgbot.utils.excel import get_excel_data
from tgbot.utils.converters import convert_nan_to_none, convert_str_to_date
from schemas.cargo_tracking import CargoTrackingCreateSchema, CargoTrackingSchema


admin_text_router = Router()


@admin_text_router.message(F.document)
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

    excel_data = get_excel_data(destination)
    for item in excel_data:
        _item = convert_nan_to_none(item)
        _item = convert_str_to_date(_item)
        _item = CargoTrackingCreateSchema.model_validate(_item)
        from_db = await repo.cargo_tracking.get_cargo_tracking_by_uni_in_shipment(_item.uni_in_shipment)
        from_db = [CargoTrackingSchema.model_validate(i, from_attributes=True) for i in from_db]

        # await repo.cargo_tracking.add_cargo_tracking(_item)

    await message.answer('Данные были обновлены, либо добавлены в базу!')
