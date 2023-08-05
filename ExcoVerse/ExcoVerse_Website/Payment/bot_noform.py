# # from telegram.ext import Updater, CommandHandler, MessageHandler
# # from telegram import ReplyKeyboardMarkup

# import os
# import telebot

# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv('API_KEY')
# bot=telebot.TeleBot(API_KEY)

# @bot.message_handler(commands=['Greet'])
# def greet(message):
#     bot.reply_to(message,"Welcome to ExcoVerse.")

# @bot.message_handler(commands=['hello'])
# def greet(message):
#     bot.reply_to(message,"Welcome to ExcoVerse.")

# #keep checking for messsages
# bot.polling()

# # def start(update, context):
# #     context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the ExcoVerse Bot!")

# # def set_receiver(update, context):
# #     receiver = update.message.text
# #     context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the receiver of payment:")

# # def main():
# #     # Create an Updater object with your bot's API token
# #     updater = Updater(token=API_KEY, use_context=True)

# #     # Get the dispatcher to register handlers
# #     dispatcher = updater.dispatcher

# #     # Register command handlers
# #     dispatcher.add_handler(CommandHandler("start", start))
# #     dispatcher.add_handler(CommandHandler("set_receiver", set_receiver))

# #     # Start the bot
# #     updater.start_polling()
# #     updater.idle()

# # if __name__ == '__main__':
# #     main()
#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""Basic example for a bot that can receive payment from user."""
import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,LabeledPrice
from aiogram.types.message import ContentType
# from aiogram.dispatcher.storage import set_state
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


#log
logging.basicConfig(level=logging.INFO)

#init
bot = Bot(token=config.TOKEN)
#process incoming msg
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)





#prices
user_states = {}
TITLE = ''
obj1 = LabeledPrice(label="Make Payment",amount = 30*100)
obj2 = LabeledPrice(label="Make Payment 2",amount = 50*100)
PRICE = [obj1,obj2]
# class State:
#     async def set(self, user=None):
#         """Option to set state for concrete user"""
#         global state
#         state = Dispatcher.get_current().current_state(user=user)
#         await state.set_state(self.state)



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: str):
    await message.reply('Welcome to the Poll Bot! Use /createpoll to create a poll.')


@dp.message_handler(commands=['createpoll'])
async def create_poll_command(message: types.Message, state:str):
    # Ask the user for the poll question
    await message.answer('Please enter the poll question:')
    # Set the state to wait for the question
    await dp.current_state().set_state('waiting_for_question')
    # user_states[message.from_user.id] = 'waiting_for_question'
    
    

# @dp.message_handler(state='waiting_for_question')
# async def process_question(message: types.Message, state: str):
#     # Get the poll question from the user's message
#     poll_question = message.text
#     user_id = message.from_user.id
#     state = user_states.get(user_id)
#     print(user_id)
#     print(state)
#     if state == 'waiting_for_question':

#     # Ask the user for the poll options
#         await message.answer('Please enter the poll options (comma-separated):')
#         # Set the poll question in the user's state
#         await state.set_data(poll_question=poll_question)
#         # Set the state to wait for the options
#         await dp.current_state().set_state(state='waiting_for_options', user=message.from_user.id)

@dp.message_handler(state='waiting_for_question')
async def process_question(message: types.Message, state: FSMContext):
    # Get the poll question from the user's message
    poll_question = message.text

    # Ask the user for the poll options
    await message.answer('Please enter the cost of the club fee:')
        # Set the poll question in the user's state
    await dp.current_state().set_state('waiting_for_options')
    user_states['poll_question'] = poll_question
    print('success2')
    
    #user_states[chatId] = {}
    # print(user_states[message.from_user.id])

@dp.message_handler(state='waiting_for_options')
#types.ChatState
async def process_options(message: types.Message, state: FSMContext):
    # Get the poll options from the user's message
    # print(user_states[message.from_user.id])
    
    # if user_states[message.from_user.id] == 'waiting_for_options':
    print('success if statement')

# Set the poll question in the user's state
    
    poll_option = message.text
    user_states['poll_options'] = poll_option

# Create a custom keyboard with poll options
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    # for option in poll_options:
    keyboard.add(types.InlineKeyboardButton(int(poll_option), callback_data=int(poll_option)))
    print(int(poll_option)*100)
    PRICE = LabeledPrice(label="Make Payment",amount = int(poll_option)*100)
    
#state.get_data().get('poll_question')
# Send the poll message
    # poll_message = await message.reply_poll(
    #     question=user_states['poll_question'],
    #     options=poll_options,
    #     is_anonymous=False,
    #     reply_markup=keyboard
    # )

    # if config.PAYMENT_TOKEN.split(":")[1] == 'TEST':
    #     await bot.send_message(message.chat.id,"test payment")
    #     # print(PRICE)

    poll_message = await bot.send_invoice(
        message.chat.id,
        title=user_states['poll_question'],
        description="hi",
        provider_token = config.PAYMENT_TOKEN,
        currency='sgd',
        prices=[PRICE],
        start_parameter='one-year-subscription',
        payload='test_invoice_payload'
    )

    # Store the poll message ID for later reference
    poll_message_id = poll_message.message_id
    user_states['poll_message_id'] = poll_message_id
    chat_id = message.chat.id

    # # Reset the user's state
    await state.reset_state()
    
    await message.answer(f'Poll created successfully! Chat ID is ${chat_id}')


# @dp.callback_query_handler(text=user_states['poll_options'])
# async def process_callback_query(callback_query: types.CallbackQuery):
#     # Get the selected option from the callback data
#     selected_option = callback_query.data

#     # Get the poll message ID from the user's state
#     user_data = await callback_query.bot.get_user_data(callback_query.from_user.id)
#     poll_message_id = user_data.get('poll_message_id')

#     if poll_message_id:
#         # Forward the poll to other people
#         await callback_query.bot.forward_message(
#             chat_id=callback_query.from_user.id,
#             from_chat_id=callback_query.message.chat.id,
#             message_id=poll_message_id,
#             caption=f"You selected: {selected_option}"
#         )

#     # Answer the callback query
#     await callback_query.answer()


# if __name__ == '__main__':
#     # Start the bot
#     dp.loop.run_until_complete(dp.start_polling())





#buy 
@dp.message_handler(commands=['pay'])
async def pay(message:types.Message):
    # if not has_started(message.chat.id):
    #     await bot.send_message(message.chat.id, "Please start the conversation with /start command first.")
    #     return
    
    # if config.PAYMENT_TOKEN.split(":")[1] == 'TEST':
    #     await bot.send_message(message.chat.id,"test payment")

    await bot.send_invoice(
        message.chat.id,
        title=user_states['poll_question'],
        description="hi",
        provider_token = config.PAYMENT_TOKEN,
        currency='sgd',
        prices=[PRICE],
        start_parameter='one-year-subscription',
        payload='test_invoice_payload'
    )

#precheckout
@dp.pre_checkout_query_handler(lambda query:True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id,ok=True)

#successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message:types.Message):
    print("Success")
    payment_info = message.successful_payment.to_python()
    for key,value in payment_info.items():
        print(f"{key}:{value}")

    await bot.send_message(message.chat.id, f"Payment for the amount {message.successful_payment.total_amount //100} {message.successful_payment.currency} passed successfully!")

# transfer = stripe.Transfer.create(
#     amount=1000,  # Amount in cents
#     currency='usd',
#     destination='payment_method_id' --> received when exco registers a card
# )

# if transfer.status == 'paid':
#     # The transfer was successful
#     print('Transfer successful!')
# else:
#     # The transfer failed
#     print('Transfer failed. Reason:', transfer.failure_message)

# import stripe.error

# try:
#     transfer = stripe.Transfer.create(...)
# except stripe.error.StripeError as e:
#     # Handle the error
#     print('Transfer error:', str(e))


#run long-polling
if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)
