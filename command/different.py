from aiogram.filters import Command
from aiogram import Router, types
import logging

from .datebase import *

router = Router()

@router.message(Command("add"))
async def crime_command(message: types.Message):
    user_id = message.from_user.id
    admins = [5225848864]
    if user_id not in admins:
        await message.answer("<b>❌Отказано в доступе</b>", parse_mode="HTML")
        return
    else:
        if len(message.text.split()) < 2:
            return
        else:
            # if len(message.text.split('_')[1].split('@')[0]) < 2:
            #     for_pay = message.text.split('_')[1].split('@')[0]
            # else:
            add = message.text.split()[1]
            logging.info(f"Пользователь {user_id} вызвал команду /add")
            balance = get_balance(user_id) 
            balance += int(add) 
            logging.info(f"Текущий баланс пользователя {user_id}: {balance}")
            update_balance(user_id, balance)

@router.message(Command("rob"))
async def rob_command(message: types.Message):
    robber_id = message.from_user.id
    robber_balance = get_balance(robber_id)
    if not message.reply_to_message:
        await message.answer("<b>❌Нужно ответить на сообщение пользователя, которого хотите ограбить</b>", parse_mode="HTML")
        return
    victim_id = message.reply_to_message.from_user.id
    ROB_COOLDOWN = 21600  
    ROB_PERCENT = 0.7
    if not message.reply_to_message:
        await message.answer("<b>❌Нужно ответить на сообщение пользователя, которого хотите ограбить</b>", parse_mode="HTML")
        return
    if robber_id == victim_id:
        await message.answer("<b>❌Нельзя грабить самого себя!</b>")
        return
    last_rob_time = get_last_rob_time(robber_id)
    current_time = time.time()
    if current_time - last_rob_time < ROB_COOLDOWN:
        remaining = int(ROB_COOLDOWN - (current_time - last_rob_time))
        await message.answer(f"<b>⏳Вы сможете грабить снова через {remaining//3600}ч {(remaining%3600)//60}м</b>", parse_mode="HTML")
        return 
    victim_balance = get_balance(victim_id)
    if victim_balance <= 0:
        await message.answer(f"<b>❌У пользователя нет наличных для кражи</b>", parse_mode="HTML")
        return
    amount = int(victim_balance * ROB_PERCENT)
    update_balance(victim_id, victim_balance - amount)
    update_balance(robber_id, robber_balance + amount)
    update_last_rob_time(robber_id, current_time)
    await message.answer(
        f"<b>✅Вы украли {amount}$ (70%) у @{message.reply_to_message.from_user.username}\n"
        f"💸Ваш новый баланс: {robber_balance + amount}$\n"
        f"⏳Следующее ограбление будет возможно через 6 часов</b>",
        parse_mode="HTML")
    

@router.message(Command("top"))
async def show_leaderboard(message: types.Message):
    try:
        cursor.execute("""
        SELECT 
            username,
            (balance + balance_on_bank) AS total_balance
        FROM users
        WHERE username IS NOT NULL
        ORDER BY total_balance DESC
        LIMIT 10
        """)
        
        top_users = cursor.fetchall()
        
        if not top_users:
            await message.answer("📊 Лидерборд пуст!")
            return
        response = "<b>🏆 ТОП-10 по балансу 🏆</b>\n\n"
        for rank, (username, balance) in enumerate(top_users, 1):
            response += f"<b>{rank}. @{username} {balance}💰</b>\n" 
        
        await message.answer(response, parse_mode="HTML")
        
    except Exception as e:
        logging.error(f"Ошибка при получении лидерборда: {e}")
        await message.answer("⚠️ Произошла ошибка при формировании лидерборда")