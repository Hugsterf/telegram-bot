from aiogram.filters import Command
from aiogram import Router, types
import logging
import asyncio

from .datebase import *


router = Router()

def get_combo_text(dice_value: int) -> str:
    #       бар(0)      виноград(1)        лимон(2)       семь(3)
    values = ["0", "1", "2", "3"]

    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(values[dice_value % 4])
        dice_value //= 4
    return " ".join(result)


@router.message(Command("slot"))
async def roll_dice(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    logging.info(f"Пользователь {user_id} вызвал команду /slot")
    logging.info(f"Деньги на руках у пользователя {user_id}  {balance}")
    if len(message.text.split()) < 2:
        await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
        return
    dicestr = message.text.split()[1].lower()
    win_combinations = {
    "0 0 0": 3,
    "1 1 1": 3,
    "2 2 2": 3,
    "3 3 3": 5,
    "3 3 0": 2,
    "3 3 1": 2,
    "3 3 2": 2,
    "0 3 3": 2,
    "1 3 3": 2,
    "2 3 3": 2,
    "3 0 3": 2,
    "3 1 3": 2,
    "3 2 3": 2,
}
    if dicestr == "all":
        dicee = balance
    else:
        try:
            dicee = int(dicestr)
        except ValueError:
            await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
            return
    if dicee <= 0:
        await message.answer("<b>❌Укажите сумму больше нуля</b>", parse_mode="HTML")
    if dicee > balance:
        await message.answer("<b>❌Недостаточно средств</b>", parse_mode="HTML")
    if dicee <= balance and dicee > 0:
        data = await message.bot.send_dice(message.chat.id, emoji='🎰')
        str_value = get_combo_text(data.dice.value)
        await asyncio.sleep(2,5)
        if str_value in win_combinations:
            multiplier = win_combinations[str_value]
            win_amount = dicee * multiplier
            balance += win_amount
            await message.answer(f"✅<b>Вы выиграли:</b> {win_amount}💸", parse_mode="HTML")
        else:
            await message.answer(f"❌<b>К сожалению, вы проиграли: {dicee}💸</b>", parse_mode="HTML")
            balance -= dicee
            logging.info(f"Пользователь {user_id} проиграл {dicee}")
        update_balance(user_id, balance)


@router.message(Command("dice"))
async def roll_dice(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    logging.info(f"Пользователь {user_id} вызвал команду /dice")
    parts = message.text.split()

    if len(parts) < 3:
        await message.answer("<b>❌Нужно ввести два числа через пробел</b>", parse_mode="HTML")
        return
    if not parts[1].isdigit() or int(parts[1]) < 1 or int(parts[1]) > 6:
        await message.answer("<b>❌Первое число должно быть от 1 до 6</b>", parse_mode="HTML")
        return
    
    if parts[2].lower() == 'all':
        bet = balance
    elif parts[2].isdigit():
        bet = int(parts[2])
    else:
        await message.answer("<b>❌Второе число должно быть цифрой или all</b>", parse_mode="HTML")
        return
    
    if bet <= 0:
        await message.answer("<b>❌Ставка должна быть больше нуля</b>", parse_mode="HTML")
        return
    if bet > balance:
        await message.answer("<b>❌Недостаточно средств</b>", parse_mode="HTML")
        return
    
    kef = 4
    logging.info(f"Деньги на руках у пользователя {user_id}  {balance}")
    dice_message = await message.answer_dice(emoji='🎲')
    await asyncio.sleep(4)
    dice_result = dice_message.dice.value
    if dice_result == int(parts[1]):
        balance += bet * kef
        await message.answer(f"<b>✅Вы выйграли: {bet * kef}💸</b>", parse_mode="HTML")
        logging.info(f"Пользователь {user_id} выиграл {bet * kef}")
    else:
        balance -= bet
        await message.answer(f"<b>❌К сожалению, вы проиграл: {bet}💸</b>", parse_mode="HTML")
        logging.info(f"Пользователь {user_id} проиграл {bet}")
    update_balance(user_id, balance)


@router.message(Command("foot"))
async def send_dice_cmd(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    if len(message.text.split()) < 2:
        await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
        return
    betstr = message.text.split()[1].lower()
    if betstr == "all":
        bet = balance
    else:
        try:
            bet = int(betstr)
        except ValueError:
            await message.answer("<b>❌ Введите число или all</b>", parse_mode="HTML")
            return
    if bet <= 0:
        await message.answer("<b>❌Ставка должна быть больше нуля</b>", parse_mode="HTML")
        return
    if bet > balance:
        await message.answer("<b>❌Недостаточно средств</b>", parse_mode="HTML")
        return
    dice_msg = await message.answer_dice(emoji="⚽")
    dice_result = dice_msg.dice.value
    await asyncio.sleep(4)
    if dice_result in {3, 4, 5}:
        balance += int(bet * 1.5)
        await message.answer(f"<b>✅Вы выйграли: {int(bet * 1.5)}</b>", parse_mode="HTML")
    else:
        balance -= bet
        await message.answer(f"<b>❌Вы проиграли: {bet}</b>", parse_mode="HTML")
    update_balance(user_id, balance)