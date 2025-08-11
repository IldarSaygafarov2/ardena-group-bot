from aiogram import Router, types, F

from database.repo.requests import RequestsRepo
from tgbot.filters.admin import AdminFilter
from tgbot.utils import helpers

admin_text_router = Router()
admin_text_router.message.filter(AdminFilter())


@admin_text_router.message(F.document & F.chat.type.in_({"private"}))
async def get_document(message: types.Message, repo: RequestsRepo):
    await helpers.download_document(message, file_type='учет', repo=repo)
    await message.answer('Файл получен!')
