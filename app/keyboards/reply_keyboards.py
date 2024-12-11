from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_btn = ReplyKeyboardBuilder()
start_btn.button(text="Buyurtma berish")
start_btn.button(text="Buyurtmalarni ko'rish")
start_btn = start_btn.as_markup()
