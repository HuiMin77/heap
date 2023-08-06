
import logging
from aiogram import Bot, Dispatcher, executor, types, helper
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,LabeledPrice
from aiogram.types.message import ContentType
# from aiogram.dispatcher.storage import set_state
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async

from aiogram.contrib.middlewares.logging import LoggingMiddleware


import os
import sys
import asyncio
from dotenv import load_dotenv
# from events.models import PaymentPoll
import hashlib
# from importlib import import_module


# Import the PaymentPoll model after initializing the Django application

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'events', '.env')
load_dotenv(dotenv_path)

# models_path = os.path.join(os.path.dirname(__file__), '..', 'events', 'models.py')

# # Get the module name from the path
# module_name = '.'.join(models_path.split(os.path.sep)[:-1]).replace('/', '.')

# # Import the models.py module
# models_module = import_module(module_name)

# Access the PaymentPoll model
# PaymentPoll = models_module.PaymentPoll


# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # Set the environment variable to point to your project's settings.py
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExcoVerse_website.settings')

# import django

# # Initialize Django application
# from django.apps import apps

# django.setup()

# # Get the model from the events app using the app registry
# PaymentPoll = apps.get_model('events', 'PaymentPoll')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)


# Set the environment variable to point to your project's settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExcoVerse_Website.settings')

# Initialize Django application
import django
from django.core.exceptions import ObjectDoesNotExist

django.setup()

# Now you can import the PaymentPoll model
from events.models import PaymentPoll, PaymentDetails
from members.models import UserProfile

#log
logging.basicConfig(level=logging.INFO)

#init
bot = Bot(token=os.environ.get('TOKEN'))
PAYMENT_TOKEN = os.environ.get('PAYMENT_TOKEN')
#process incoming msg


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: str):
    await message.reply('Welcome to the Poll Bot! Enter the password given to create your payment poll.')
    await dp.current_state().set_state('waiting_for_poll_creation')

@dp.message_handler(state='waiting_for_poll_creation')
async def process_options(message: types.Message, state: FSMContext):
    # Your existing code here...

    # Now you can use the subject, description, and price in your bot logic
    # Your bot code


    # Get the user-provided password from the message
    user_password = message.text.strip()

    # Validate the provided password against the hashed password
    # hashed_password = payment_poll.password
    decoded_password = hashlib.sha256(user_password.encode()).hexdigest()
    try:
        global payment_poll
        payment_poll = await sync_to_async(PaymentPoll.objects.select_related('payment_event').get)(hashed_password=decoded_password)



    # if payment_poll:

        # Password is correct; proceed with accessing the data
        # Do whatever you need to do with the data (e.g., send it to the user)

        # Example: Send the data to the user
        await bot.send_message(message.chat.id, f"Subject: {payment_poll.subject}\nDescription: {payment_poll.description}\nPrice: {payment_poll.price}\nEvent:{payment_poll.payment_event}")
        # Create a custom keyboard with poll options
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(str(payment_poll.price), callback_data=str(payment_poll.price)))
        PRICE = LabeledPrice(label="Make Payment", amount=int(payment_poll.price) * 100)

        # Send the poll message
        poll_message = await bot.send_invoice(
            message.chat.id,
            title=payment_poll.subject,
            description=payment_poll.description,
            provider_token=PAYMENT_TOKEN,
            currency='sgd',
            prices=[PRICE],
            start_parameter='one-year-subscription',
            payload='test_invoice_payload'
        )
        
        await state.reset_state()

    except ObjectDoesNotExist:
        # Password is incorrect; inform the user
        await bot.send_message(message.chat.id, "Incorrect password. Please re-enter your password.")

    except Exception as e:
        # Handle other exceptions gracefully
        await bot.send_message(message.chat.id, "An error occurred. Please try again later.")
        logging.error(str(e))
    


    

#precheckout
@dp.pre_checkout_query_handler(lambda query:True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id,ok=True)

#successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
# def create_stripe_transfer(total_amount, stripe_account_id):
        
#     transfer = stripe.Transfer.create(
#         amount=int(total_amount*100),
#         currency="sgd",
#         destination=stripe_account_id
#     )
#     return transfer
async def successful_payment(message:types.Message):
    
    print("Successfully paid to bot")
    payment_info = message.successful_payment.to_python()
    for key,value in payment_info.items():
        print(f"{key}:{value}")
    
    user_id = message.from_user.id
    chat_id = message.chat.id
    payment_id = message.successful_payment.invoice_payload
    total_amount = message.successful_payment.total_amount / 100  # Divide by 100 to get the actual amount
    currency = message.successful_payment.currency
    payment_provider = message.successful_payment.provider_payment_charge_id

    # Save the payment details to the database
    # payment_details = PaymentDetails.objects.create(
    #     user_id=user_id,
    #     chat_id=chat_id,
    #     payment_id=payment_id,
    #     total_amount=total_amount,
    #     currency=currency,
    #     payment_provider=payment_provider,
    #     is_success=True,  # You can set this to True since the payment was successful
    # )

    # await bot.send_message(message.chat.id, f"Payment for the amount {message.successful_payment.total_amount //100} {message.successful_payment.currency} passed successfully!")
    try:
        print("my payment poll",payment_poll.id)
        poll_id = payment_poll.id
        # creator_user = await sync_to_async(PaymentPoll.objects.get)()
        # creator_user_profile = await sync_to_async(payment_poll.user_profile)  # Adjust field name accordingly
        # creator_user_profile = await sync_to_async(PaymentPoll.objects.select_related('stripe_account_id').get)(user=creator_user)
        # print("userprofile",creator_user_profile)
        # Now you can use creator_user_profile.stripe_account_id to direct the payment to their Stripe account
        # stripe_account_id = payment_poll.stripe_account_id
        # print(stripe_account_id)
        
        # loop = asyncio.get_event_loop()
        # result = await loop.run_in_executor(None, create_stripe_transfer, total_amount, stripe_account_id)
            
        # print("successfully paid back to user")

        
        # Call the create method using sync_to_async
        await sync_to_async(PaymentDetails.objects.create)(
            poll_id=payment_poll,
            user_id=user_id,
            chat_id=chat_id,
            payment_id=payment_id,
            total_amount=total_amount,
            currency=currency,
            payment_provider=payment_provider,
            # You can set this to True since the payment was successful to the bot
            is_success_excoverse=True,
            # poll_creator=creator_user,
        )
            
        

        await bot.send_message(
            message.chat.id,
            f"Payment for the amount {message.successful_payment.total_amount // 100} "
            f"{message.successful_payment.currency} passed successfully!"
        )


    except Exception as e:
        # Handle other exceptions gracefully
        await bot.send_message(message.chat.id, "An error occurred. Please try again later.")
        logging.error(str(e))

#     async def create_stripe_transfer(total_amount, stripe_account_id):
        
#         transfer = await sync_to_async(stripe.Transfer.create(
#             amount=total_amount,
#             currency="sgd",
#             destination=stripe_account_id
#         ))
#         return transfer
# # def start_telegram_bot():

    #create new event loop for a thread
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # executor.start_polling(dp, skip_updates=True)
# if __name__=="__main__":
#     executor.start_polling(dp, skip_updates=True)

# async def start_telegram_bot_async():
#     await executor.start_polling(dp,skip_updates=True)

# def start_telegram_bot():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     # loop.run_until_complete(start_telegram_bot_async())
#     # loop = asyncio.get_event_loop()
#     loop.run_until_complete(start_telegram_bot_async())

if __name__ == "__main__":
    #  loop = asyncio.get_event_loop()
     executor.start_polling(dp, skip_updates=True)
    

# async def start_telegram_bot():
#     # This will start the polling of updates for your Telegram bot
#     await executor.start_polling(dp, skip_updates=True)

# def start_telegram_bot(loop):
#     # Create a new event loop for the Telegram bot
#     # loop = asyncio.get_event_loop()
#     # Run the bot as a coroutine using asyncio
#     asyncio.run(start_telegram_bot_async(loop))

