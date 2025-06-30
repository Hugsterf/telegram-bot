from aiogram.filters import Command
from aiogram import Router, types

router = Router()

@router.message(Command("premium"))
async def premium_command(message: types.Message):
    user_id = message.from_user.id
    text= (
        f"<b>👑Купить премиум👑</b>\n\n"
        f"<b>❗ Зарплата больше на 25% </b>\n<i>(/collect)💰</i>\n"
        f"<b>❗ Ежедневные бонусы </b>\n<i>(/bonus)🎁</i>\n"
        f"<b>❗ Персональная копилка </b>\n<i>(/invest_info)💵</i>\n"
    )
    await message.answer(text, parse_mode="HTML")