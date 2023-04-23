from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.currency_keyboard import currency_keyboard, all_currency_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.get_currency import get_currency
from states.currency_states import CurrencyStates


async def process_start_currency(message: types.Message, state: FSMContext) -> None:
    """
    Запускается процесс после нажатия кнопки "Конвертер валюты", в основном меню.

    Создается Inline клавиатура с основными валютами и дополнительными.

    Указываем первую валюту для расчета курса.
    """
    await message.answer(text=LEXICON_RU['first_cur'],
                         reply_markup=currency_keyboard())
    await state.set_state(CurrencyStates.main_currency)


async def process_second_currency(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Указываем вторую валюту для расчета курса.
    """
    await state.update_data(main_currency=callback.data)
    await callback.message.edit_text(text=LEXICON_RU['second_cur'],
                                     reply_markup=currency_keyboard())
    await state.set_state(CurrencyStates.secondary_currency)


async def process_another_currency(callback: types.CallbackQuery) -> None:
    """
    Срабатывает при нажатии на кнопку "Другая валюта" в Inline клавиатуре.
    """
    await callback.message.edit_text(text=LEXICON_RU['all_cur'],
                                     reply_markup=all_currency_keyboard())


async def process_amount_of_currency(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Получаем от пользователя кол-во валюты, для расчета.

    Предварительно проверяем через фильтр сообщение, число там или нет.
    """
    await state.update_data(second_currency=callback.data)
    await callback.message.edit_text(text=LEXICON_RU['count_cur'])
    await state.set_state(CurrencyStates.amount_of_currency)


async def process_end_currency(message: types.Message, state: FSMContext) -> None:
    """
    Завершающий процесс ввода валюты. Подсчет и выдача результата пользователю.

    """
    await state.update_data(amount=float(message.text))
    await message.answer(text=LEXICON_RU['wait_cur'])
    user_currency = await state.get_data()
    await state.clear()
    currency_info = get_currency(main_cur=user_currency.get('second_currency'),
                                 second_cur=user_currency.get('main_currency'),
                                 amount=user_currency.get('amount'))
    await message.answer(
        text=f'{LEXICON_RU["end_cur"]}'
             f'{user_currency.get("main_currency")} ➡ {user_currency.get("second_currency")} '
             f'{round(currency_info / user_currency.get("amount"), 2)}\r\n\n'
             f'{user_currency.get("amount")} {user_currency.get("main_currency")} = '
             f'{currency_info} {user_currency.get("second_currency")}')


async def process_not_num(message: types.Message) -> None:
    """
    Срабатывает, если пользователь вместо числа отправил что-то другое.
    """
    await message.answer(text=LEXICON_RU['count_cur'])


async def process_any_message(message: types.Message) -> None:
    """
    Срабатывает на любые сообщения во время выбора валюты, пользователем.
    """
    await message.answer(text=LEXICON_RU['any_message'])


async def process_cancel_command(message: types.Message, state: FSMContext) -> None:
    """
    Срабатывает на команду /cancel, если пользователь решил прекратить ввод данных.
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(text=LEXICON_RU['nothing_cancel'])
        return
    await state.clear()
    await message.answer(text=LEXICON_RU['cancel_cur'])
