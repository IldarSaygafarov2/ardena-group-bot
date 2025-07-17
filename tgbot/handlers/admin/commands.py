from aiogram import Router, types
from aiogram.filters import CommandStart



admin_commands_router = Router()


@admin_commands_router.message(CommandStart())
async def handle_admin_start_command(message: types.Message):
    await message.answer('Отправь файл с данными о доставках')


