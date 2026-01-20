from aiogram import Router, F
from aiogram.types import Message

from app.bot.modules.test.settings import settings
from app.bot.modules.test.response import get_keyboards_menu_buttons


router = Router(name=__name__)


@router.message(F.text == settings.MENU_REPLY_TEXT)
async def test(message: Message):
    await message.answer(text="ok", reply_markup=get_keyboards_menu_buttons)