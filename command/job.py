from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

from .for_job import JOBS
from .datebase import *

router = Router()

def list_job():
    text = """
═════ <b>ПЕРВЫЙ УРОВЕНЬ</b> ═════
1. {call_title}
💰 З/п: {call_salary}
<i>Чтобы устроиться: /job_call</i>

2. {seller_title}
💰 З/п: {seller_salary}
<i>Чтобы устроиться: /job_seller</i>

3. {manager_title}
💰 З/п: {manager_salary}
<i>Чтобы устроиться: /job_manager</i>

4. {waiter_title}
💰 З/п: {waiter_salary}
<i>Чтобы устроиться: /job_waiter</i>

5. {builder_title}
💰 З/п: {builder_salary}
<i>Чтобы устроиться: /job_builder</i>

6. {storekeeper_title}
💰 З/п: {storekeeper_salary}
<i>Чтобы устроиться: /job_storekeeper</i>

7. {it_title}
💰 З/п: {it_salary}
<i>Чтобы устроиться: /job_it</i>

<b>❗ Зарплата доступна каждые 3 часа</b>
""".format(
        call_title=JOBS['call'][0], call_salary=JOBS['call'][1],
        seller_title=JOBS['seller'][0], seller_salary=JOBS['seller'][1],
        manager_title=JOBS['manager'][0], manager_salary=JOBS['manager'][1],
        waiter_title=JOBS['waiter'][0], waiter_salary=JOBS['waiter'][1],
        builder_title=JOBS['builder'][0], builder_salary=JOBS['builder'][1],
        storekeeper_title=JOBS['storekeeper'][0], storekeeper_salary=JOBS['storekeeper'][1],
        it_title=JOBS['it'][0], it_salary=JOBS['it'][1]
    )
    return text

@router.message(Command("job"))
async def get_a_job(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"Пользователь {user_id} вызвал команду /job")
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Далее", callback_data="next")]
        ])
    await message.answer(
        text=list_job(),
        parse_mode="HTML",
        reply_markup=keyboard)
    

@router.message(Command(commands=[
    "job_call", "job_seller", "job_manager",
    "job_waiter", "job_builder", "job_storekeeper",
    "job_it"
]))
async def any_job(message: types.Message):
    user_id = message.from_user.id
    job_type = message.text.split('_')[1].split('@')[0]
    if job_type in JOBS:
        title, salary = JOBS[job_type]
        if get_user_job(user_id) == title:
            await message.answer(f"<b>❌Вы уже работаете на вакансии</b>:\n{title}", parse_mode="HTML")
        else:
            last_work_time = get_last_collect_time(user_id)
            current_time = time.time()
            time_diff = current_time - last_work_time
            cooldown = 3 * 60 * 60 
            if time_diff < cooldown:
                remaining_time = int(cooldown - time_diff)
                minutes = remaining_time // 60
                await message.answer(f"<b>⏳Вы сможете сменить работу через {minutes} минут.</b>", parse_mode="HTML")
                return
            else:
                update_job(user_id, title)
                update_job_type(user_id, job_type)
                await message.answer(
                f"✅ Вы теперь {title}\n"
                f"💰 Зарплата: {salary}",
                parse_mode="HTML")
                logging.info(f"Пользователь {user_id} {title}")