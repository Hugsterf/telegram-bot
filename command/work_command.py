from aiogram.filters import Command
from aiogram import Router, types
import logging
import random
import time

from .datebase import *
from .for_job import SALARY


router = Router()

@router.message(Command("collect"))
async def collect_command(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} вызвал команду /collect")
    last_work_time = get_last_collect_time(user_id)
    salary_hard_soft = get_salary_skills_user(user_id)
    current_time = time.time()
    time_diff = current_time - last_work_time
    cooldown = 3 * 60 * 60
    if time_diff < cooldown:
        remaining_time = int(cooldown - time_diff)
        minutes = remaining_time // 60
        await message.answer(f"<b>⏳Вы сможете забрать зарплату через {minutes} минут.</b>", parse_mode="HTML")
        return
    salary = random.randint(
        (SALARY[get_job_type(user_id)]["salary_min"] + salary_hard_soft),
        (SALARY[get_job_type(user_id)]["salary_max"] + salary_hard_soft)
    )
    balance_on_bank = get_balance_on_bank(user_id)
    balance_on_bank += salary
    update_balance_on_bank(user_id, balance_on_bank)
    update_last_collect_time(user_id)
    await message.answer(f"✅<b>Вы заработали {salary}💰\n🏦В банке: {balance_on_bank}</b>💰", parse_mode="HTML")


@router.message(Command("work"))
async def work_command(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} вызвал команду /work")
    last_work_time = get_last_work_time(user_id)
    current_time = time.time()
    time_diff = current_time - last_work_time
    cooldown = 20 * 60 
    if time_diff < cooldown:
        remaining_time = int(cooldown - time_diff)
        minutes = remaining_time // 60
        await message.answer(f"⏳<b>Вы сможете снова поработать через {minutes} минут.</b>", parse_mode="HTML")
        return
    balance = get_balance(user_id)
    logging.info(f"Текущий баланс пользователя {user_id}: {balance}")
    work = random.randint(50, 100)
    balance += work
    update_balance(user_id, balance)
    update_last_work_time(user_id)
    await message.answer(f"<b>✅Вы заработали: {work}💸</b>", parse_mode="HTML")


@router.message(Command("crime"))
async def crime_command(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} вызвал команду /crime")
    last_crime_time = get_last_crime_time(user_id) 
    current_time = time.time()
    time_diff = current_time - last_crime_time
    cooldown = 30 * 60
    if time_diff < cooldown:
        remaining_time = int(cooldown - time_diff)
        minutes = remaining_time // 60
        await message.answer(f"⏳<b>Вы сможете снова совершить преступление через {minutes} минут.</b>", parse_mode="HTML")
        return
    balance = get_balance(user_id)
    balance_on_bank = get_balance_on_bank(user_id)
    logging.info(f"Текущий баланс пользователя {user_id}: {balance}")
    if random.random() < 0.8:
        crime = random.randint(100, 200)
        balance += crime
        update_balance(user_id, balance)
        await message.answer(f"✅<b>Вы заработали: {crime}💸</b>", parse_mode="HTML")
    else:
        crime = random.randint(100, 200)
        balance_on_bank -= crime
        update_balance_on_bank(user_id, balance_on_bank)
        await message.answer(f"👮‍♂️<b>Вас поймала полиция! Вы потеряли: {crime}💰</b>", parse_mode="HTML")
    update_last_crime_time(user_id)


@router.message(Command(commands=["riskywork", "rwork"]))
async def crime_command(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} вызвал команду /riskywork")
    last_riskwork_time = get_last_riskwork_time(user_id)
    current_time = time.time()
    time_diff = current_time - last_riskwork_time
    cooldown = 30 * 60
    if time_diff < cooldown:
        remaining_time = int(cooldown - time_diff)
        minutes = remaining_time // 60
        await message.answer(f"⏳<b>Вы сможете снова поработать через {minutes} минут.</b>", parse_mode="HTML")
        return
    balance = get_balance(user_id) 
    balance_on_bank = get_balance_on_bank(user_id)
    logging.info(f"Текущий баланс пользователя {user_id}: {balance}")  
    if random.random() < 0.8:
        rwork = random.randint(100, 150)
        balance += rwork
        update_balance(user_id, balance) 
        await message.answer(f"<b>✅Вы заработали: {rwork}💸</b>", parse_mode="HTML")
    else:
        rwork = random.randint(100, 200)
        balance_on_bank -= rwork
        update_balance_on_bank(user_id, balance_on_bank)  
        await message.answer(f"🏏<b>Вас избили за плохую работу... счет за восстановление в больнице: {rwork}💰</b>.", parse_mode="HTML")
    update_last_riskwork_time(user_id)