import os
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database.repo.requests import RequestsRepo
from tgbot.filters.admin import AdminFilter
from tgbot.misc.states import AdminChemistryFilesState
from tgbot.utils.excel import get_filtered_excel_data

admin_commands_router = Router()
admin_commands_router.message.filter(AdminFilter())


@admin_commands_router.message(CommandStart())
async def handle_admin_start_command(message: types.Message):
    await message.answer('Отправьте файл учётки')


@admin_commands_router.message(Command('generate_report'))
async def handle_admin_generate_report_command(message: types.Message, repo: "RequestsRepo", state: "FSMContext"):
    await state.set_state(AdminChemistryFilesState.data)
    from_db = await repo.chemistry_file.get_all_files()
    file_path = from_db[0].file_path

    filtered_data = get_filtered_excel_data(
        file_path=file_path,
        filter_column="Статус отчета",
        filter_value="отправить",
        required_columns=[
            'Станция',
            'Рег. Номер ГТД',
            'Дата начала хранения'
        ]
    )
    await state.set_data(data={"data": filtered_data})

    await message.answer("Отправьте файлы хим составов")


@admin_commands_router.message(AdminChemistryFilesState.data)
async def get_files_from_admin_to_report(message: types.Message, state: "FSMContext"):
    state_data = await state.get_data()
    _document = message.document
    date = message.date.date().strftime("%d.%m.%Y")

    # Example of file type validation
    allowed_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    if _document.mime_type not in allowed_types:
        await message.answer("This file type is not allowed!")
        return

    # File size validation (example: 10MB limit)
    if _document.file_size > 10 * 1024 * 1024:  # 10MB in bytes
        await message.answer("File is too large!")
        return

    os.makedirs(f'documents/{date}', exist_ok=True)
    destination = os.path.join(f'documents/{date}', _document.file_name)

    caption = message.caption
    filtered_data = state_data.get('data')

    # данные для НУРХАЁТ
    station_filters = ['нурхает', 'нурхаёт']
    first_station_data = [item for item in filtered_data if item['Станция'].lower() in station_filters]






