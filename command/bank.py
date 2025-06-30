from aiogram.filters import Command
from aiogram import Router, types, Bot
import logging

from .datebase import *
from config import TOKEN

router = Router()
bot = Bot(token=TOKEN)

@router.message(Command(commands=["ballance", "bal"]))
async def bank(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} вызвал команду /balance")    
    logging.info(f"Денег на руках у пользователя {user_id}: {get_balance(user_id)}")
    text = f"""
<b>👛На руках: {get_balance(user_id)}💸</b>\n
<b>🏦В банке: {get_balance_on_bank(user_id)}💰</b>\n
<i>/dep all (положить деньги в банк)</i>
<i>/with all (снять деньги с банка)</i>
""" 
    await message.answer(text,parse_mode="HTML")
    logging.info(f"Денег в банке у пользователя {user_id}: {get_balance_on_bank(user_id)}") 


async def get_username_by_id(bot: Bot, user_id: int):
    try:
        user = await bot.get_chat(user_id)
        return user.username or user.full_name
    except:
        return f"ID{user_id}"


@router.message(Command("pay"))
async def pay_command(message: types.Message):
    user_id = message.from_user.id
    if not message.reply_to_message:
        await message.answer("<b>❌Нужно ответить на сообщение пользователя, которому хотите перевести деньги</b>", parse_mode="HTML")
        return
    pay_user_id = message.reply_to_message.from_user.id
    balance_user_id = get_balance(user_id)
    balance_pay_user_id = get_balance(pay_user_id)
    logging.info(f"Пользователь {user_id} вызвал команду /pay для {pay_user_id}")    
    logging.info(f"{balance_user_id} на руках у пользователя {user_id}")
    logging.info(f"{balance_pay_user_id} на руках у пользователя {pay_user_id} (перевод ему): {pay_user_id}")
    if user_id == pay_user_id:
        await message.answer("<b>❌Нельзя переводить самого себя!</b>")
        return
    if len(message.text.split()) < 2:
        await message.answer("<b>❌ Введите число или all для суммы перевода</b>", parse_mode="HTML")
        return
    paystr = message.text.split()[1].lower()
    if paystr == "all":
        pay = balance_user_id
    else:
        try:
            pay = int(paystr)
        except ValueError:
            await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
            return
    if balance_user_id < int(paystr):
        await message.answer("<b>❌Недостаточно средств</b>", parse_mode="HTML")
        return
    if int(paystr) <= 0:
        await message.answer("<b>❌Укажите сумму больше нуля</b>", parse_mode="HTML")
        return
    else:
        pay = int(paystr)
        balance_pay_user_id += pay
        balance_user_id -= pay
        update_balance(user_id, balance_user_id)
        update_balance(pay_user_id, balance_pay_user_id)
        await message.answer(f"<b>✅Вы перевели {pay}💸 пользователю: @{message.reply_to_message.from_user.username}</b>", parse_mode="HTML")


@router.message(Command("dep"))
async def dep_comand(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    balance_on_bank = get_balance_on_bank(user_id)
    logging.info(f"Пользователь {user_id} вызвал команду /dep ")    
    logging.info(f"Денег на руках у пользователя {user_id}: {get_balance(user_id)}")
    if len(message.text.split()) < 2:
        await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
        return
    depstr = message.text.split()[1].lower()
    if depstr == "all":
        dep = balance
    else:
        try:
            dep = int(depstr)
        except ValueError:
            await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
            return
    if dep <= 0:
        await message.answer("<b>❌Укажите сумму больше нуля</b>", parse_mode="HTML")
    if dep > balance:
        await message.answer("<b>❌Недостаточно средств</b>", parse_mode="HTML")
    if dep <= balance and dep > 0:
        balance_on_bank += dep
        balance -= dep
        update_balance(user_id, balance)
        update_balance_on_bank(user_id, balance_on_bank)
        await message.answer(f"""
✅<b>Вы пополнили банковский счет на {dep}💸</b>
🏦<b>Сумма в банке: {balance_on_bank}💰</b>""",
parse_mode="HTML")
        logging.info(f"Денег в банке у пользователя {user_id}: {get_balance_on_bank(user_id)}")


@router.message(Command("with"))
async def with_comand(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    balance_on_bank = get_balance_on_bank(user_id)
    logging.info(f"Пользователь {user_id} вызвал команду /with ")    
    logging.info(f"Денег на руках у пользователя {user_id}: {get_balance(user_id)}")
    if len(message.text.split()) < 2:
        await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
        return
    depstr = message.text.split()[1].lower()
    if depstr == "all":
        dep = balance_on_bank
    else:
        try:
            dep = int(depstr)
        except ValueError:
            await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
            return
    if dep <= 0:
        await message.answer("<b>❌Укажите сумму больше нуля</b>", parse_mode="HTML")
    if dep > balance_on_bank:
        await message.answer("<b>❌Недостаточно средств в банке</b>", parse_mode="HTML")
    if dep <= balance_on_bank and dep > 0:
        balance += dep
        balance_on_bank -= dep
        update_balance(user_id, balance)
        update_balance_on_bank(user_id, balance_on_bank)
        await message.answer(f"""
✅<b>Вы обналичили банковский счет на {dep}💰</b>
👛<b>Сумма на руках: {balance}💸</b>""",
parse_mode="HTML")
        logging.info(f"Денег в банке у пользователя {user_id}: {get_balance_on_bank(user_id)}")