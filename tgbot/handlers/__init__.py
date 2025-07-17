from tgbot.handlers.admin.commands import admin_commands_router
from tgbot.handlers.admin.texts import admin_text_router


routers_list = [
    admin_commands_router,
    admin_text_router
]

__all__ = ["routers_list"]