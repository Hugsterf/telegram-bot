from aiogram import Router

from command.start import router as start_router
from command.job import router as job_router
from command.work_command import router as work_router
from command.casino import router as casino_router
from command.bank import router as bank_router
from command.different import router as different_router
from command.buy import router as buy_router
from command.support import router as support_router
from command.help import router as help_router
from command.promocode import router as promocode_router
# from command.rol import router as rol_router
# from command.premium import router as premium_router

main_router = Router()
main_router.include_router(start_router)
main_router.include_router(job_router)
main_router.include_router(work_router)
main_router.include_router(casino_router)
main_router.include_router(bank_router)
main_router.include_router(different_router)
main_router.include_router(buy_router)
main_router.include_router(support_router)
main_router.include_router(help_router)
# main_router.include_router(rol_router)
main_router.include_router(promocode_router)
# main_router.include_router(premium_router)