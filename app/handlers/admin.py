from aiogram import Router, types, F
from aiogram.types import FSInputFile
from app.handlers.get_orders import export_orders_to_excel

router = Router()

@router.message(F.text == "!export")
async def send_excel_file(message: types.Message):
    file_name = "orders.xlsx"
    export_orders_to_excel(file_name)  # Faylni yaratish funksiyasini chaqiramiz

    # Faylni yuborish
    await message.reply_document(document=FSInputFile(file_name), caption="📦 Buyurtmalar ro'yxati")
