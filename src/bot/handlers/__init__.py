from aiogram import Router
from src.bot.handlers.start import start_router
from src.bot.handlers.draws import draws_router

main_router = Router()

main_router.include_routers(
    start_router,
    draws_router
)

