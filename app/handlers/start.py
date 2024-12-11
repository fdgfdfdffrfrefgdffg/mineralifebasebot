from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.keyboards.reply_keyboards import start_btn
router = Router()

@router.message(F.text == "/start")
async def start_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Assalomu alaykum! Xush kelibsiz!")
