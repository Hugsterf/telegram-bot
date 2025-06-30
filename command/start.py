from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from .datebase import *

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    balance_on_bank = get_balance_on_bank(user_id)
    update_balance_on_bank(user_id, balance_on_bank)
    update_username(user_id, message.from_user.username)
    await message.answer("это бот казино")