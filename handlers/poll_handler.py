from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.main_keyboard import main_keyboard
from keyboards.poll_keyboard import poll_keyboard, list_poll_keyboard, group_chat_keyboard
from database.saved_polls import saved_polls
from lexicon.lexicon_ru import LEXICON_RU
from states.poll_states import PollStates


async def process_main_menu_poll(message: types.Message, state: FSMContext) -> None:
    """
    Создаем клавиатуру с меню для Опроса.

    Для группового чата создается клавиатура с кнопками: Отправить опрос и Выйти.
    Для личного чата с ботом создается клавиатура с кнопками: Создать опрос, Список опросов и Выйти.
    Разделение клавиатур идет из-за отсутствия возможности создавать опросы в групповых чатах через бота.
    """
    await state.set_state(PollStates.menu)
    if message.chat.type == 'group':
        await message.answer(text=f'{message.from_user.first_name}, {LEXICON_RU["start_group"]}',
                             reply_markup=group_chat_keyboard())
    else:
        await message.answer(text=f'{message.from_user.first_name}, {LEXICON_RU["start_private"]}',
                             reply_markup=poll_keyboard())


async def process_get_list_poll(message: types.Message) -> None:
    """
    Получаем список всех сохраненных опросов.
    """
    if message.from_user.id not in saved_polls:
        await message.answer(text=LEXICON_RU['empty_list_poll'],
                             reply_markup=poll_keyboard())
    else:
        await message.answer(text=f'{LEXICON_RU["saved_polls"]}'
                                  f'{", ".join([ _ for _ in saved_polls[message.from_user.id]])}',
                             reply_markup=poll_keyboard())


async def process_save_poll(message: types.Message, state: FSMContext) -> None:
    """
    Процесс срабатывает, когда пользователь завершает создание опроса.

    Для процесса настроен специальный фильтр, что бы отлавливать опросы и сохранять их в database/saved_polls.
    """
    poll_data = await state.update_data(
        question=message.poll.question,
        options=[i.text for i in message.poll.options],
        is_anonymous=message.poll.is_anonymous,
        type=message.poll.type,
        allows_multiple_answers=message.poll.allows_multiple_answers,
        open_period=message.poll.open_period,
        close_date=message.poll.close_date
    )
    if message.from_user.id not in saved_polls:
        saved_polls[message.from_user.id] = {poll_data['question']: poll_data}
    else:
        saved_polls[message.from_user.id][poll_data['question']] = poll_data
    await message.answer(text=LEXICON_RU['save_success'],
                         reply_markup=poll_keyboard())


async def process_enter_poll(message: types.Message, state: FSMContext) -> None:
    """
    Процесс работает только в групповом чате.

    Позволяет выбрать опрос для отправки в групповой чат.
    """
    if message.from_user.id not in saved_polls:
        await message.answer(text=LEXICON_RU['empty_list_poll_group'],
                             reply_markup=group_chat_keyboard())
    else:
        await state.set_state(PollStates.send_poll)
        await message.answer(text=LEXICON_RU['choose_poll'],
                             reply_markup=list_poll_keyboard(list(saved_polls[message.from_user.id])))


async def process_send_poll(callback: types.CallbackQuery) -> None:
    """
    Процесс работает только в групповом чате, отправляет выбранный на предыдущем шаге опрос в групповой чат.
    """
    await callback.message.edit_text(text='Опрос: ')
    await callback.message.answer_poll(
        question=saved_polls.get(callback.from_user.id).get(callback.data).get('question'),
        options=saved_polls.get(callback.from_user.id).get(callback.data)['options'],
        is_anonymous=saved_polls.get(callback.from_user.id).get(callback.data).get('is_anonymous'),
        type=saved_polls.get(callback.from_user.id).get(callback.data).get('type'),
        allows_multiple_answers=saved_polls.get(callback.from_user.id).get(callback.data).get('allows_multiple_answers'),
        open_period=saved_polls.get(callback.from_user.id).get(callback.data).get('open_period'),
        close_date=saved_polls.get(callback.from_user.id).get(callback.data).get('close_date')
    )


async def process_echo_poll(message: types.Message) -> None:
    """
    Отвечает на все сообщения от пользователя, пока он находится в меню Опрос.

    """
    await message.answer(text=LEXICON_RU['any_message_poll'])


async def process_end_poll(message: types.Message, state: FSMContext) -> None:
    """
    Процесс срабатывает при нажатии на кнопку "Выйти" клавиатуры.

    """
    await state.clear()
    await message.answer(text=LEXICON_RU['exit_polls'],
                         reply_markup=main_keyboard())
