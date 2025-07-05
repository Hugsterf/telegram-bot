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

lib.add_promocode.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.find_promocode.argtypes = [c_char_p]
lib.find_promocode.restype = c_int

router = Router()

@router.message(Command("promo"))
async def promo(message: types.Message):
    user_id = message.from_user.id    
    
    if message.chat.type != ChatType.PRIVATE:
        await message.answer("❗ Функция работает только в личных сообщениях!")
        return
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
                await message.answer("<b>✅ Вы успешно использовали промокод!</b>", parse_mode="HTML")
            else:
                await message.answer("<b>❌ Промокод недействителен или уже использован</b>", parse_mode="HTML")

        except Exception as e:
            logging.error(f"Error processing promo code: {e}")
            await message.answer("<b>❗ Произошла ошибка при проверке промокода</b>", parse_mode="HTML")



@router.message(Command("addpromo"))
async def addpromo(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("<b>❌ Отказано в доступе</b>", parse_mode="HTML")
        return
    try:
        _, promo, count = message.text.split()
        count = int(count)
        lib.add_promocode(promo.encode('utf-8'), count)
        await message.answer(f"<b>✅ Промокод {promo} добавлен!</b>", parse_mode="HTML")
    except:
        await message.answer("<b>Использование: /addpromo PROMOCODE COUNT</b>", parse_mode="HTML")