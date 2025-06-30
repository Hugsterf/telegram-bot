from aiogram.filters import Command
from aiogram import Router, types

from .datebase import *

router = Router()

@router.message(Command("support"))
async def support_command(message: types.Message):
    await message.answer(
        "❗ Поддержка разработчика💸\n" 
        "https://www.donationalerts.com/r/chops_dev")