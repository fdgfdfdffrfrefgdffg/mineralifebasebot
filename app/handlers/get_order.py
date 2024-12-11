from aiogram import Router, types
from app.database import Order, session
from app.filters.is_order_id import IsOrderIDFilter  # Filterni import qilamiz
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(IsOrderIDFilter())
async def get_order_by_id(message: types.Message, state: FSMContext):
    try:
        # Xabarni buyurtma ID sifatida olish
        order_id = int(message.text)

        # Bazadan buyurtmani qidirish
        order = session.query(Order).filter(Order.id == order_id).first()

        if order:
            # Buyurtma haqida ma'lumotlarni yuborish
            order_info = (
                f"📦 **Buyurtma ID:** {order.id}\n"
                f"👤 **Mijoz ismi:** {order.customer_name}\n"
                f"📞 **Telefon raqam:** {order.phone_number}\n"
                f"💧 **Suv baklashka soni:** {order.water_quantity} ta\n"
                f"📍 **Lokatsiya:** {order.latitude}, {order.longitude}"
            )

            # Lokatsiyani yuborish
            await message.bot.send_location(
                chat_id=message.chat.id,
                latitude=order.latitude,
                longitude=order.longitude
            )
            await message.reply(order_info, parse_mode="Markdown")
        else:
            await message.reply("❌ Bunday IDga ega buyurtma topilmadi.")
    except Exception as e:
        await message.reply("⚠️ Buyurtmani qidirishda xatolik yuz berdi. Keyinroq urinib ko'ring.")
