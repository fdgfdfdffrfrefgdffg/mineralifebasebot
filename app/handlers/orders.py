from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.database import Order, session, delete_order_by_id, update_order_quantity
from aiogram.enums import ParseMode
from app.states import OrderState

router = Router()

# Buyurtma jarayonini faqat !order komandasi orqali boshlash
@router.message(F.text == "!order")
async def start_order(message: types.Message, state: FSMContext):
    await message.reply("👤 *Mijoz ismini kiriting:*", parse_mode="Markdown")
    await state.set_state(OrderState.name)

@router.message(OrderState.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("📞 *Telefon raqamini kiriting:*", parse_mode="Markdown")
    await state.set_state(OrderState.phone)

@router.message(OrderState.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.reply("💧 *Suv baklashkalar sonini kiriting (masalan: 2, 5):*", parse_mode="Markdown")
    await state.set_state(OrderState.quantity)

@router.message(OrderState.quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
        await state.update_data(quantity=quantity)
        btn = ReplyKeyboardBuilder()
        btn.button(text="📍 Lokatsiya yuborish", request_location=True)
        btn = btn.as_markup()
        await message.reply(
            "📍 *Iltimos, lokatsiya yuboring:*",
            reply_markup=btn,
            parse_mode="Markdown"
        )
        await state.set_state(OrderState.location)
    except ValueError:
        await message.reply("⚠️ *Iltimos, suv baklashka sonini faqat raqam bilan kiriting.*", parse_mode="Markdown")

@router.message(OrderState.location, F.location)
async def process_location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    location = message.location

    # Bazaga saqlash
    new_order = Order(
        customer_name=data["name"],
        phone_number=data["phone"],
        water_quantity=data["quantity"],  # Baklashka soni
        latitude=location.latitude,
        longitude=location.longitude
    )
    session.add(new_order)
    session.commit()

    # Buyurtma IDsi bilan javob berish
    await message.reply(
        f"✅ *Buyurtma muvaffaqiyatli qo'shildi!*\n"
        f"📦 *Buyurtma ID:* `{new_order.id}`",
        parse_mode="Markdown",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()



@router.message(F.text.startswith("!del"))
async def delete_order(message: types.Message):
    try:
        # Buyurtma ID sini olish
        order_id = int(message.text.split()[1])  # !del 1 shaklida

        # Buyurtmani o'chirish
        result = delete_order_by_id(order_id)

        # Foydalanuvchiga natijani yuborish (markdown formatda)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN)

    except (IndexError, ValueError):
        # Agar xato buyruq yoki noto'g'ri buyurtma ID bo'lsa
        await message.answer("⚠️ **Iltimos, buyurtma ID sini to'g'ri kiriting.**\nMasalan: `!del 1`", parse_mode=ParseMode.MARKDOWN)



@router.message(F.text.startswith("!edit"))
async def update_order(message: types.Message):
    try:
        # Buyurtma ID va yangi sonni olish
        parts = message.text.split()
        order_id = int(parts[1])
        new_quantity = int(parts[2])  # !update 1 10 shaklida

        # Baklashkalari sonini yangilash
        result = update_order_quantity(order_id, new_quantity)

        # Foydalanuvchiga natijani yuborish (markdown formatda)
        await message.answer(result, parse_mode=ParseMode.MARKDOWN)

    except (IndexError, ValueError):
        # Agar xato buyruq yoki noto'g'ri ma'lumot kiritilgan bo'lsa
        await message.answer("⚠️ **Iltimos, buyurtma ID va yangi sonni to'g'ri kiriting.**\nMasalan: `!update 1 10`", parse_mode=ParseMode.MARKDOWN)
