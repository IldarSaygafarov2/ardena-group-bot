from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from tgbot.misc.states import AdminChemistryFilesState

from tgbot.filters.admin import AdminFilter

admin_commands_router = Router()
admin_commands_router.message.filter(AdminFilter())



@admin_commands_router.message(CommandStart())
async def handle_admin_start_command(message: types.Message):
    await message.answer('Отправьте файл учётки')



@admin_commands_router.message(Command('generate_report'))
async def handle_admin_generate_report_command(message: types.Message, state: "FSMContext"):
    await state.set_state(AdminChemistryFilesState.files)

    await message.answer("Отправьте файлы хим составов")


@admin_commands_router.message(AdminChemistryFilesState.files)
async def get_files_from_admin_to_report(message: types.Message, state: "FSMContext"):
    document = message.document

    print(document)