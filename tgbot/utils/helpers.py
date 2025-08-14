import os
from aiogram import types
from typing import Optional
from database.repo.requests import RequestsRepo

async def download_document(message: types.message, file_type: str, repo: RequestsRepo) -> Optional[str]:
    date = message.date.date().strftime("%d.%m.%Y")
    document = message.document

    # Example of file type validation
    allowed_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    if message.document.mime_type not in allowed_types:
        await message.answer("This file type is not allowed!")
        return None

    # File size validation (example: 10MB limit)
    if message.document.file_size > 10 * 1024 * 1024:  # 10MB in bytes
        await message.answer("File is too large!")
        return None

    os.makedirs(f'documents/{date}', exist_ok=True)
    destination = os.path.join(f'documents/{date}', document.file_name)

    await message.bot.download(
        document.file_id,
        destination=destination
    )

    await repo.chemistry_file.add_or_ignore_file(
        name=message.document.file_name,
        file_path=destination,
        file_type=file_type,
        _date=date
    )
    return destination


async def send_message_with_uni(bot, unis, chat_id):
    if not unis:
        return

    income = ['ПРИХОД:\n']
    outcome = ['РАСХОД:\n']

    for item, _number in unis:
        if _number == '73':
            income.append(f'{item}\n')
        elif _number == '40':
            outcome.append(f'{item}\n')

    income_message = ''.join(income)
    outcome_message = ''.join(outcome)

    if income_message:
        await bot.send_message(chat_id=chat_id, text=income_message)
    if outcome_message:
        await bot.send_message(chat_id=chat_id, text=outcome_message)
    # await bot.send_message(chat_id=chat_id, text=message)