# import random
# from aiogram.filters import Command
# from aiogram.types import Message
# from aiogram import Router, Bot
# from typing import Dict, List, Set
# from aiogram.exceptions import TelegramRetryAfter
# import logging
# import asyncio
# from config import TOKEN
# from .datebase import get_balance, update_balance

# router = Router()
# bot = Bot(token=TOKEN)

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
# BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

# active_games: Dict[int, Dict] = {}
# user_bets: Dict[int, Dict[int, Dict]] = {}
# users_with_active_bets: Set[int] = set()
# last_messages: Dict[tuple, str] = {}

# async def safe_edit_message(chat_id: int, message_id: int, text: str, parse_mode="HTML"):
#     try:
#         if last_messages.get((chat_id, message_id)) == text:
#             return
#         await bot.edit_message_text(
#             chat_id=chat_id,
#             message_id=message_id,
#             text=text,
#             parse_mode=parse_mode
#         )
#         last_messages[(chat_id, message_id)] = text
#     except Exception as e:
#         logger.error(f"Ошибка редактирования: {e}")

# def is_valid_bet(value: str) -> bool:
#     if value.isdigit():
#         num = int(value)
#         return 0 <= num <= 36
#     return value.lower() in {"red", "black"}

# def calculate_payout(value: str) -> int:
#     return 36 if value.isdigit() else 2

# def check_win(bet_value: str, winning_number: int) -> bool:
#     bet_value = bet_value.lower()
#     if bet_value.isdigit():
#         return int(bet_value) == winning_number
#     elif bet_value == "red":
#         return winning_number in RED_NUMBERS
#     elif bet_value == "black":
#         return winning_number in BLACK_NUMBERS
#     return False

# async def process_bet(user_id: int, amount: int) -> bool:
#     try:
#         balance = await get_balance(user_id)
#         if balance is None:
#             logger.error("Не удалось получить баланс")
#             return False
            
#         if amount > balance:
#             logger.error("Недостаточно средств")
#             return False
            
#         if not await update_balance(user_id, -amount):
#             logger.error("Ошибка списания средств")
#             return False
            
#         return True
#     except Exception as e:
#         logger.error(f"Критическая ошибка: {e}")
#         return False

# async def finish_roulette(chat_id: int):
#     if chat_id not in user_bets or not user_bets[chat_id]:
#         if chat_id in active_games:
#             try:
#                 await bot.delete_message(chat_id, active_games[chat_id]["message_id"])
#             except Exception as e:
#                 logger.error(f"Ошибка удаления: {e}")
#             del active_games[chat_id]
#         return

#     winning_number = random.randint(0, 36)
#     is_red = winning_number in RED_NUMBERS
#     winners = []
#     total_payout = 0

#     for user_id, bet in user_bets[chat_id].items():
#         try:
#             user = await bot.get_chat_member(chat_id, user_id)
#             username = f"@{user.user.username}" if user.user.username else f"ID {user.user.id}"
            
#             users_with_active_bets.discard(user_id)
            
#             if check_win(bet["value"], winning_number):
#                 payout = bet["amount"] * calculate_payout(bet["value"])
#                 if await update_balance(user_id, payout):
#                     winners.append(f"<b>🎉 {username}: +{payout} (ставка: {bet['amount']} на {bet['value']})</b>")
#                     total_payout += payout
#                 else:
#                     logger.error("Ошибка выплаты выигрыша")
#                     await update_balance(user_id, bet["amount"])
#         except Exception as e:
#             logger.error(f"Ошибка обработки ставки: {e}")
#             users_with_active_bets.discard(user_id)
#             await update_balance(user_id, bet["amount"])

#     result_text = (
#         f"🏆 <b>Результат рулетки!</b>\n\n"
#         f"<b>🎲 Выпало: {winning_number}</b>\n"
#         f"<b>🔴 Цвет: {'красное' if is_red else 'чёрное'}</b>\n\n"
#     )
    
#     if winners:
#         result_text += f"<b>💰 Победители (всего выигрыш: {total_payout}):</b>\n" + "\n".join(winners)
#     else:
#         result_text += "😢 <b>Победителей нет</b>"

#     try:
#         await bot.send_message(chat_id, result_text, parse_mode="HTML")
#     except Exception as e:
#         logger.error(f"Ошибка отправки результата: {e}")

#     if chat_id in active_games:
#         try:
#             await bot.delete_message(chat_id, active_games[chat_id]["message_id"])
#         except Exception as e:
#             logger.error(f"Ошибка удаления: {e}")
#         del active_games[chat_id]
#     if chat_id in user_bets:
#         del user_bets[chat_id]

# @router.message(Command(commands=["bet"]))
# async def bet_command(message: Message):
#     user_id = message.from_user.id
#     chat_id = message.chat.id
    
#     if user_id in users_with_active_bets:
#         await message.answer("<b>❌ У вас уже есть активная ставка!</b>", parse_mode="HTML")
#         return
    
#     try:
#         balance = await get_balance(user_id)
#         if balance is None:
#             await message.answer("<b>❌ Ошибка получения баланса</b>", parse_mode="HTML")
#             return
#     except Exception as e:
#         logger.error(f"Ошибка получения баланса: {e}")
#         await message.answer("<b>❌ Ошибка получения баланса</b>", parse_mode="HTML")
#         return
    
#     if chat_id not in active_games:
#         await message.answer("<b>❌ Нет активной игры!</b>", parse_mode="HTML")
#         return
    
#     parts = message.text.split()
#     if len(parts) < 3:
#         await message.answer(
#             "<b>❌ Используйте: /bet [число/цвет] [сумма]</b>\n"
#             "<b>Пример: /bet red 100</b>",
#             parse_mode="HTML"
#         )
#         return
    
#     bet_value = parts[1]
#     amount_str = parts[2].lower()
    
#     if not is_valid_bet(bet_value):
#         await message.answer("<b>❌ Допустимо: 0-36 или red/black</b>", parse_mode="HTML")
#         return
    
#     try:
#         amount = balance if amount_str == 'all' else int(amount_str)
#         if amount <= 0:
#             await message.answer("<b>❌ Сумма должна быть > 0</b>", parse_mode="HTML")
#             return
#         if amount > balance:
#             await message.answer("<b>❌ Недостаточно средств</b>", parse_mode="HTML")
#             return
#     except ValueError:
#         await message.answer("<b>❌ Некорректная сумма</b>", parse_mode="HTML")
#         return
    
#     if not await process_bet(user_id, amount):
#         await message.answer("<b>❌ Ошибка обработки ставки</b>", parse_mode="HTML")
#         return
    
#     if chat_id not in user_bets:
#         user_bets[chat_id] = {}
#     user_bets[chat_id][user_id] = {"value": bet_value, "amount": amount}
#     users_with_active_bets.add(user_id)
    
#     await message.answer(
#         f"<b>✅ Ставка {amount} на {bet_value} принята!</b>\n"
#         f"<b>💰 Остаток: {balance - amount}</b>\n"
#         f"<b>🔮 Потенциальный выигрыш: {amount * calculate_payout(bet_value)}</b>",
#         parse_mode="HTML"
#     )

# @router.message(Command("roll"))
# async def start_roulette(message: Message):
#     chat_id = message.chat.id
    
#     if chat_id in active_games:
#         await message.answer("<b>❌ Рулетка уже запущена!</b>", parse_mode="HTML")
#         return
    
#     active_games[chat_id] = {"message_id": None, "timer": None}
#     user_bets[chat_id] = {}
    
#     msg = await message.answer(
#         "🎰 <b>Рулетка запущена!</b>\n\n"
#         "<b>⚡ Ставки: /bet [число/цвет] [сумма]</b>\n"
#         "<b>⏳ Осталось: 30 секунд</b>\n"
#         "<b>📊 Ставок: 0</b>\n"
#         "<b>⚠️ 1 ставка на игрока</b>",
#         parse_mode="HTML"
#     )
#     active_games[chat_id]["message_id"] = msg.message_id
    
#     async def countdown():
#         for counter in range(30, 0, -5):
#             bets_count = len(user_bets.get(chat_id, {}))
            
#             await safe_edit_message(
#                 chat_id,
#                 msg.message_id,
#                 f"🎰 <b>Рулетка запущена!</b>\n\n"
#                 f"<b>⚡ Ставки: /bet [число/цвет] [сумма]</b>\n"
#                 f"<b>⏳ Осталось: {counter} секунд</b>\n"
#                 f"<b>📊 Ставок: {bets_count}</b>\n"
#                 f"<b>⚠️ 1 ставка на игрока</b>",
#                 parse_mode="HTML"
#             )
#             await asyncio.sleep(5)
        
#         await finish_roulette(chat_id)
    
#     active_games[chat_id]["timer"] = asyncio.create_task(countdown())

# @router.message(Command("help_roll"))
# async def help_command(message: Message):
#     help_text = (
#         "🎰 <b>Помощь по рулетке</b>\n\n"
#         "<b>Команды:</b>\n"
#         "/roll - запустить рулетку (30 сек)\n"
#         "/bet [число/цвет] [сумма] - сделать ставку\n\n"
#         "<b>Примеры:</b>\n"
#         "/bet red 100 - на красное\n"
#         "/bet 17 50 - на число 17\n\n"
#         "<b>Выплаты:</b>\n"
#         "Число (0-36): x36\n"
#         "Цвет (red/black): x2\n\n"
#         "<b>Правила:</b>\n"
#         "- 1 ставка на игрока за игру\n"
#         "- Ставки списываются сразу"
#     )
#     await message.answer(help_text, parse_mode="HTML")