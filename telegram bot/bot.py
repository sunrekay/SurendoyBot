from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from State import Test


@dp.message_handler(Command("start"))
async def enter_start(message: types.Message):
    if check_sub_member(await bot.get_chat_member(chat_id='@surendoy_boost', user_id=message.from_user.id)):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["/comeback", "/help"]
        keyboard.add(*buttons)

        await message.answer("Доступные команды:\n" 
                             "/comeback - расчет следующей ставки.\n"
                             "/help", reply_markup=keyboard)
    else:
        await message.answer("Для доступа к функционалу бота подпишитесь на "
                             "<a href='https://t.me/surendoy_boost'>канал</a>")


def check_sub_member(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(Command("help"))
async def enter_help(message: types.Message):
    if check_sub_member(await bot.get_chat_member(chat_id='@surendoy_boost', user_id=message.from_user.id)):
        await message.answer("Почта для сотрудничества: moderator.surendoybot@mail.ru")
    else:
        await message.answer("Для доступа к функционалу бота подпишитесь на "
                             "<a href='https://t.me/surendoy_boost'>канал</a>")


@dp.message_handler(Command("comeback"), state=None)
async def enter_test(message: types.Message):
    if check_sub_member(await bot.get_chat_member(chat_id='@surendoy_boost', user_id=message.from_user.id)):
        await message.answer("Введите сумму проигрыша:")
        await Test.Q1.set()
    else:
        await message.answer("Для доступа к функционалу бота подпишитесь на "
                             "<a href='https://t.me/surendoy_boost'>канал</a>")


@dp.message_handler(state=Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.replace(',', '', 1).isdigit() or answer.replace('.', '', 1).isdigit():

        check_num = float(answer.replace(',', '.', 1))
        if (check_num >= 0) and (check_num <= 10000000):

            await state.update_data({"lose_money": answer})
            await message.answer("На сколько вы хотите выйти в плюс:")
            await Test.next()
        else:
            await message.answer("Введите, пожалуйста, число в диапозоне от 0 до 1кк.")

    else:
        await message.answer("Введите пожалуйста число.")


@dp.message_handler(state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.replace(',', '', 1).isdigit() or answer.replace('.', '', 1).isdigit():

        check_num = float(answer.replace(',', '.', 1))
        if (check_num >= 0) and (check_num <= 10000000):

            await state.update_data({"plus_money": answer})
            await message.answer("Коэффициент следующей ставки:")
            await Test.next()
        else:
            await message.answer("Введите, пожалуйста, число в диапозоне от 0 до 10кк.")
    else:
        await message.answer("Введите пожалуйста только число.")


@dp.message_handler(state=Test.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.replace(',', '', 1).isdigit() or answer.replace('.', '', 1).isdigit():

        check_num = float(answer.replace(',', '.', 1))
        if (check_num > 1) and (check_num <= 100):
            await state.update_data({"percent": answer})

            data = await state.get_data()

            lose_money = float(data.get("lose_money").replace(',', '.', 1))
            plus_money = float(data.get("plus_money").replace(',', '.', 1))
            percent = float(data.get("percent").replace(',', '.', 1))

            for bet in range(1, 100000000):
                if bet*percent >= bet + lose_money + plus_money:
                    bet = str(bet)
                    await message.answer("Для возвращения проигрыша, в размере " + data.get("lose_money") + " руб. " +
                                         " и выхода в плюс на " + data.get("plus_money") + " руб. "
                                         " необходимо поставить: <u>" + bet + " руб. </u>")
                    break

            await state.finish()
        else:
            await message.answer("Введите, пожалуйста, число в диапозоне от 1,1 до 100.")
    else:
        await message.answer("Введите пожалуйста число.")


@dp.message_handler()
async def trash_message(message: types.Message):
    await message.answer("Я не понимаю.")


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
