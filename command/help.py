from aiogram.filters import Command
from aiogram import Router, types

from .datebase import *

router = Router()

@router.message(Command("help_job"))
async def help_job_command(message: types.Message):
    text = (
    "🎯 <b>РАБОТЫ И ПОДРАБОТКИ</b> 🎯\n\n"
    
    "🔹 <b>Основная работа</b>\n"
    "┣ Используйте <code>/job</code> чтобы выбрать профессию\n"
    "┗ Зарплата каждые 3 часа: <code>/collect</code>\n"
    "➖➖➖➖➖➖➖➖➖\n\n"
    
    "💰 <b>ПОДРАБОТКИ</b> 💰\n\n"
    
    "👷 <code>/work</code> - Подработка у дяди Стэна\n"
    "├ Заработок: <b>50-100</b>💸\n"
    "└ Риск: <i>Нет</i>\n\n"
    
    "🏪 <code>/crime</code> - Ограбление магазина\n"
    "├ Заработок: <b>100-200</b>💸\n"
    "└ Потери: <b>100-200</b>💰 | <i>Шанс попасть в тюрьму</i> ⚠️\n\n"
    
    "🤕 <code>/rwork</code> - Рисковая работа\n"
    "├ Заработок: <b>100-150</b>💸\n"
    "└ Потери: <b>100-200</b>💰 | <i>Шанс попасть в больницу</i> 🏥\n\n"
    
    "🔸 <i>Чем выше риск - тем больше потенциальный доход!</i> 🔸"
)
    await message.answer(text, parse_mode="HTML")


@router.message(Command("help_command"))
async def help_command(message: types.Message):
    text = (
    "🏦 <b>БАНКОВСКИЕ ОПЕРАЦИИ</b> 🏦\n\n"
    
    "💰 <u>Баланс и транзакции</u>\n"
    "┣ <code>/bal</code> - Проверить баланс\n"
    "┣ <code>/with</code> [сумма] - Снять деньги со счета\n"
    "┣ <code>/dep</code> [сумма] - Положить деньги на счет\n"
    "┗ <code>/pay</code> [сумма] (в ответ на сообщение) - Перевод игроку\n\n"
    
    "🎰 <b>АЗАРТНЫЕ ИГРЫ</b> 🎰\n\n"
    
    "🎲 <u>Игровые автоматы</u>\n"
    "┣ <code>/slot</code> [сумма] - Игра в слоты\n"
    "┃   ┗ <code>/help_slot</code> - Выигрышные комбинации\n"
    "┣ <code>/dice</code> [число] [сумма] - Ставка на кубик\n"
    "┗ <code>/foot</code> [сумма] - Футбольный пенальти\n\n"
    
    "🦹 <b>ВЗАИМОДЕЙСТВИЕ С ИГРОКАМИ</b> 🦹\n\n"
    
    "🎈 <u>Другие операции</u>\n"
    "┣ <code>/rob</code> (в ответ на сообщение) - Попытка ограбления (70% баланса)\n"
    "┗ <code>/top</code> - Топ игроков по балансу\n\n"
    
    "🔹 <i>Чем больше ставка - тем выше потенциальный выигрыш!</i>🔹\n"
    "🔸 <i>Рискуйте с умом!</i> 🔸\n\n"
    
    "💖 <b>ПОДДЕРЖКА РАЗРАБОТЧИКА</b> 💖\n"
    "┗ <code>/support</code> - Если вам нравится бот, вы можете поддержать его развитие\n"
    "   <i>Каждая помощь мотивирует на новые улучшения!</i>"
)
    await message.answer(text, parse_mode="HTML")


@router.message(Command("help_slot"))
async def help_command(message: types.Message):
    text = (
    "🏦 <b>ВЫЙГРЫШНЫЕ КОМБИНАЦИИ</b> 🏦\n\n" 

    "1. Две семерки и любой другой фрукт/bar - x2"
    "2. Три вряд - x3"
    "3. Джекпот(три семерки) - x5"
)
    await message.answer(text, parse_mode="HTML")