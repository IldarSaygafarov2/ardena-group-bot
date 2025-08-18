from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config.loader import app_config
from database.repo.requests import RequestsRepo
from tgbot.filters.admin import AdminFilter
from tgbot.misc.states import AdminChemistryFilesState
from tgbot.utils import helpers
from tgbot.utils.excel import get_filtered_excel_data, update_filtered_data_advanced

admin_commands_router = Router()
admin_commands_router.message.filter(AdminFilter())


@admin_commands_router.message(CommandStart())
async def handle_admin_start_command(message: types.Message):
    await message.answer('Отправьте файл учётки')


@admin_commands_router.message(Command('generate_report'))
async def handle_admin_generate_report_command(message: types.Message, repo: "RequestsRepo", state: "FSMContext"):
    await state.set_state(AdminChemistryFilesState.data)
    from_db = await repo.chemistry_file.get_file_by_type(file_type='учет')

    file_path = from_db[0].file_path

    filtered_data = get_filtered_excel_data(
        file_path=file_path,
        filter_column="Статус отчета",
        filter_value="отправить",
        required_columns=[
            'Станция',
            'ГТД ИМ73',
            'Рег. Номер ГТД',
            'Дата начала хранения',
            '№ вагона / авто',
            'ГТД ИМ40',
            'Рег. Номер ГТД.1',
            'Дата окончания хранения',
            'Клиент на выдачу'
        ]
    )
    await state.set_data(data={"data": filtered_data})

    await message.answer("Отправьте файлы хим составов")


@admin_commands_router.message(AdminChemistryFilesState.data)
async def get_files_from_admin_to_report(message: types.Message, repo: RequestsRepo, state: "FSMContext"):
    from_db = await repo.chemistry_file.get_file_by_type(file_type='учет')
    file_path = from_db[0].file_path

    state_data = await state.get_data()
    filtered_data = state_data.get('data')

    destination = await helpers.download_document(message, file_type='хим-состав', repo=repo)
    caption = message.caption

    first_station_filters = ['нурхает', 'нурхаёт']
    second_station_filters = ['кизилтепа', 'кызылтепа']

    station_data = []

    if caption.lower() in first_station_filters:
        station_data = [item for item in filtered_data if item['Станция'].lower() in first_station_filters]
    elif caption.lower() in second_station_filters:
        station_data = [item for item in filtered_data if item['Станция'].lower() in second_station_filters]

    unique_unis = {}

    for item in station_data:

        declaration_type_73 = item.get('ГТД ИМ73')

        _declaration_type = '73' if type(declaration_type_73) is str else '40'

        for_update = None
        if _declaration_type == '73':
            for_update = {
                'ГТД ИМ73': item.get('Рег. Номер ГТД'),
                'Дата начала хранения': item.get('Дата начала хранения')
            }
        elif _declaration_type == '40':
            for_update = {
                'Дата окончания хранения': item.get('Дата окончания хранения'),
                'Номер накладной': item.get('ГТД ИМ40'),
            }
        #
        vehicle_number = item.get('№ вагона / авто')
        updated_df, stats, unis = update_filtered_data_advanced(
            file_path=destination,
            filters=[
                ('UNI', 'contains', vehicle_number)
            ],
            updates=for_update,
            save=True,
            skip_existing=True
        )
        for uni in unis:
            if uni not in unique_unis:
                updated_df_2, stats_2, _ = update_filtered_data_advanced(
                    file_path=file_path,
                    filters=[
                        ('№ вагона / авто', 'contains', vehicle_number),
                    ],
                    updates={
                        'Статус отчета': "Отправлено"
                    },
                    save=True
                )
                print(updated_df_2, stats_2)

                unique_unis[uni] = _declaration_type

    if not unique_unis:
        return await message.answer('не найдено совпадений по номеру авто')

    chemistry_file = types.FSInputFile(path=destination)

    # отправляем измененный хим-состав
    await state.clear()

    for admin_chat_id in app_config.bot.admin_chat_id:
        await message.bot.send_document(
            chat_id=admin_chat_id,
            document=chemistry_file
        )
        await helpers.send_message_with_uni(
            bot=message.bot,
            unis=[i for i in unique_unis.items()],
            chat_id=admin_chat_id,
        )

    return None


@admin_commands_router.message(Command('get_accounting_file'))
async def get_accounting_file(message: types.Message, repo: RequestsRepo):
    from_db = await repo.chemistry_file.get_file_by_type(file_type='учет')
    file_path = from_db[0].file_path

    accounting_file = types.FSInputFile(path=file_path)
    await message.answer_document(document=accounting_file)
