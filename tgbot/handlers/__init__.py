from tgbot.handlers.admin.commands import admin_commands_router
from tgbot.handlers.admin.texts import admin_text_router
from tgbot.handlers.groups.document import group_document_router


routers_list = [
    # admin router
    admin_commands_router,
    admin_text_router,

    # group router
    group_document_router
]

__all__ = ["routers_list"]
