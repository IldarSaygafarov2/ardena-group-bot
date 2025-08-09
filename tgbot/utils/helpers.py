import os
from aiogram import types
from typing import Optional

async def download_document(message: types.message) -> Optional[str]:
    date = message.date.date().strftime("%d.%m.%Y")

    # Example of file type validation
    allowed_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    if message.document.mime_type not in allowed_types:
        await message.answer("This file type is not allowed!")
        return

    # File size validation (example: 10MB limit)
    if message.document.file_size > 10 * 1024 * 1024:  # 10MB in bytes
        await message.answer("File is too large!")
        return

    os.makedirs(f'documents/{date}', exist_ok=True)
    destination = os.path.join(f'documents/{date}', message.document.file_name)
    return destination