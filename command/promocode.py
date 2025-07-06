from aiogram.filters import Command
from aiogram import Router, types
from aiogram.enums import ChatType
from aiogram.types import Message
from ctypes import cdll, c_char_p, c_int
from config import ADMINS
import logging
import platform
import ctypes
import os

from .datebase import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DLL_PATH = os.path.join(BASE_DIR, "Database_promo", "promo64.dll")
lib = ctypes.CDLL(DLL_PATH)

lib.add_promocode.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
lib.find_promocode.argtypes = [c_char_p]
lib.find_promocode.restype = c_int
lib.find_payment.argtypes = [c_char_p]
lib.find_payment.restype = c_int

router = Router()

@router.message(Command("promo"))
async def promo(message: types.Message):
    user_id = message.from_user.id
    balance_on_bank = get_balance_on_bank(user_id)    
    
    # if message.chat.type != ChatType.PRIVATE:
    #     await message.answer("❗ Функция работает только в личных сообщениях!")
    #     return
    logging.info(f"Пользователь {user_id} вызвал команду /promo")

    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("<b>❌ Введите промокод</b>", parse_mode="HTML")
        return
    else:
        promo_code = parts[1].strip()
        try:
            result = lib.find_promocode(promo_code.encode('utf-8'))
            if result == 1:
                payment = lib.find_payment(promo_code.encode('utf-8'))
                balance_on_bank += payment
                update_balance_on_bank(user_id, balance_on_bank)
                await message.answer("<b>✅ Вы успешно использовали промокод!</b>", parse_mode="HTML")
                await message.answer(f"<b>💰 Ваш баланс: {balance_on_bank}</b>", parse_mode="HTML")
            else:
                await message.answer("<b>❌ Промокод недействителен или достиг лимит использований!</b>", parse_mode="HTML")

        except Exception as e:
            logging.error(f"Error processing promo code: {e}")
            await message.answer("<b>❗ Произошла ошибка при проверке промокода</b>", parse_mode="HTML")



@router.message(Command("addpromo"))
async def addpromo(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("<b>❌ Отказано в доступе</b>", parse_mode="HTML")
        return
    try:
        _, promo, count, payment = message.text.split()
        count = int(count)
        payment = int(payment)
        lib.add_promocode(promo.encode('utf-8'), count, payment)
        await message.answer(f"{promo} \n{count} \n{payment}")
    except:
        await message.answer("<b>ERROR /addpromo PROMOCODE COUNT PAYMENT</b>", parse_mode="HTML")