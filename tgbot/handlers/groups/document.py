from aiogram import Router, F, types



group_document_router = Router()

@group_document_router.message(F.chat.type.in_({"group", "supergroup"}))
@group_document_router.message(F.document)
async def get_message_from_group(message: types.Message):
    print(message.document)

