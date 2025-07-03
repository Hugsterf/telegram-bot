from aiogram.filters import Command
from aiogram import Router, types
from aiogram.enums import ChatType
from aiogram.types import Message
from ctypes import cdll, c_char_p, c_int
import logging
import platform
import ctypes
import os

from .datebase import *

DLL_PATH = r"C:\Users\bogda\OneDrive\Desktop\telegram-bot\Database_promo\promo64.dll"
lib = ctypes.CDLL(DLL_PATH)

lib.add_promocode.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.find_promocode.argtypes = [c_char_p]
lib.find_promocode.restype = c_int

router = Router()

@router.message(Command("promo"))
async def promo(message: types.Message):
    user_id = message.from_user.id
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
                await message.answer("✅ Вы успешно использовали промокод!")
            else:
                await message.answer("❌ Промокод недействителен или уже использован")

        except Exception as e:
            logging.error(f"Error processing promo code: {e}")
            await message.answer("❗ Произошла ошибка при проверке промокода")


@router.message(Command("addpromo"))
async def addpromo(message: types.Message):
    promo_to_add = 's'
    lib.add_promocode(promo_to_add.encode('utf-8'), 10)
    await message.answer("!")