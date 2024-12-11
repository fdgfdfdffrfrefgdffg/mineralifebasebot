from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class IsOrderIDFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        # Foydalanuvchi hech qanday holatda bo'lmasa
        user_state = await state.get_state()
        if user_state is None:
            # Faqat raqamli xabarni tekshirish
            return message.text.isdigit()
        return False
