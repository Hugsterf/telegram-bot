from aiogram import Router, types
from aiogram.filters import Command
import logging

from .for_buy import BUY_SALARY, GET_SALARY
from .datebase import *

router = Router()

@router.message(Command(commands=["buy_hard", "buy_hard@buecash_bot"]))
async def buy_hard_skills(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    current_level = get_hard_level_user(user_id)
    logging.info(f"Пользователь {user_id} вызвал команду /buy_hard")
    if current_level >= 10:
        await message.answer("<b>❌ Вы уже достигли максимального уровня Hard Skills!</b>", parse_mode="HTML")
        return
    try:
        hard_cost = BUY_SALARY[current_level]
    except KeyError:
        await message.answer("<b>❌ Ошибка: неверный уровень навыка</b>", parse_mode="HTML")
        return
    if balance < hard_cost:
        await message.answer(f"<b>❌ Недостаточно средств. Нужно: {hard_cost}💸</b>", parse_mode="HTML")
        return
    new_level = current_level + 1
    salary_increase = GET_SALARY.get(new_level, 0)  
    update_balance(user_id, balance - hard_cost)
    update_hard_level_user(user_id, new_level)
    update_salary_skill_user(user_id, get_salary_skills_user(user_id) + salary_increase)
    logging.info(f"Пользователь {user_id} имеет {get_hard_level_user(user_id)} уровень Hard Skills")
    await message.answer(f"✅Ваш новый уровень Hard Skills: {get_hard_level_user(user_id)}❗", parse_mode="HTML")


@router.message(Command(commands=["buy_soft", "buy_soft@buecash_bot"]))
async def buy_soft_skills(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    current_level = get_soft_level_user(user_id)
    logging.info(f"Пользователь {user_id} вызвал команду /buy_soft")
    if current_level >= 10:
        await message.answer("<b>❌ Вы уже достигли максимального уровня Soft Skills!</b>", parse_mode="HTML")
        return
    try:
        soft_cost = BUY_SALARY[current_level]
    except KeyError:
        await message.answer("<b>❌ Ошибка: неверный уровень навыка</b>", parse_mode="HTML")
        return
    if balance < soft_cost:
        await message.answer(f"<b>❌ Недостаточно средств. Нужно: {soft_cost}💸</b>", parse_mode="HTML")
        return
    new_level = current_level + 1
    salary_increase = GET_SALARY.get(new_level, 0)  
    update_balance(user_id, balance - soft_cost)
    update_soft_level_user(user_id, new_level)
    update_salary_skill_user(user_id, get_salary_skills_user(user_id) + salary_increase)
    logging.info(f"Пользователь {user_id} имеет {get_soft_level_user(user_id)} уровень Hard Skills")
    await message.answer(f"✅Ваш новый уровень Soft Skills: {get_soft_level_user(user_id)}❗", parse_mode="HTML")


@router.message(Command("buy_menu"))
async def buy_command(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} вызвал команду /buy_menu")
    hard_level = get_hard_level_user(user_id)
    soft_level = get_soft_level_user(user_id)

    if hard_level < 1:
        hard_level = 1
        update_hard_level_user(user_id, hard_level)

    if soft_level < 1:
        soft_level = 1
        update_soft_level_user(user_id, soft_level)

    if hard_level >= 10:
        hard_cost = "Максимальный уровень!"
        hard_salary = GET_SALARY[10]
    else:
        hard_cost = f"{BUY_SALARY[hard_level]}💸"
        hard_salary = GET_SALARY[hard_level]

    if soft_level >= 10:
        soft_cost = "Максимальный уровень!"
        soft_salary = GET_SALARY[10]
    else:
        soft_cost = f"{BUY_SALARY[hard_level]}💸"
        soft_salary = GET_SALARY[hard_level]
    
    text = f"""
<b>1. 🧮 Hard Skills - прокачай свои навыки и опыт на работе!</b>
<b><i>Стоимость обучения - {hard_cost}</i></b>
<b><i>Повышение к зарплате - {hard_salary}💸</i></b>
<i>/buy_hard</i>

<b>2. 🤝 Soft Skills - прокачай свои личные качества!</b>
<b><i>Стоимость обучения - {soft_cost}</i></b>
<b><i>Повышение к зарплате - {soft_salary}💸</i></b>
<i>/buy_soft</i>
"""
    await message.answer(text, parse_mode="HTML")