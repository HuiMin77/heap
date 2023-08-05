import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,LabeledPrice
from aiogram.types.message import ContentType
# from aiogram.dispatcher.storage import set_state
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import deep_linking

import os
import sys
from dotenv import load_dotenv
# from events.models import PaymentPoll
import hashlib
from importlib import import_module


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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExcoVerse_website.settings')

# Initialize Django application
import django
django.setup()

# Now you can import the PaymentPoll model
from events.models import PaymentPoll
from events.models import Event
from events.models import PaymentDetails
from events.models import Student
from events.models import Tracking_Payment
from django.core.exceptions import ObjectDoesNotExist
#log
logging.basicConfig(level=logging.INFO)

#initE
bot = Bot(token=os.environ.get('TOKEN'))
PAYMENT_TOKEN = os.environ.get('PAYMENT_TOKEN')
#process incoming msg

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

decoded_password_cache = {}

@sync_to_async
def get_event_by_name(event_name):
    all_events =  Event.objects.all()
    filtered_events = [event for event in all_events if event.name == event_name]
    return filtered_events[0]

@sync_to_async
def tele_handle():
    members = MyClubUser.objects.all()
    names = members.name
    return names

@sync_to_async
def track(student,event):
    payments = Tracking_Payment.objects.get(student=student, event=event)
    print("WHY YOU NO TRACK",payments)
    print("FIne4")
    payments.paid = True
    print("fine6")
    payments.save()

async def initiate_conversation_with_bot(chat_id, password):
    deep_link = f"https://t.me/{'excoverse_bot'}?start=" + str(password)
    await bot.send_message(chat_id, f"\nClick the link below to make payment:\n{deep_link}\n\nUse this password when prompted:\n{password}")

@dp.message_handler(commands=['create_payment_poll'])
async def start_command(message: types.Message):
     await message.reply('Welcome to the Poll Bot! Enter the password given to create your payment poll.')
     await dp.current_state().set_state('create_link_with_password')

@dp.message_handler(state='create_link_with_password')
async def process_options(message: types.Message, state: FSMContext):
    await initiate_conversation_with_bot(message.chat.id, message.text)
    await state.finish()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    password = message.get_args()
    if password:
        decoded_password = hashlib.sha256(password.encode()).hexdigest()
        user_data = await state.get_data()
        decoded_password_cache[message.chat.id] = decoded_password
        print("fortheloveofgod", decoded_password)
        print(await sync_to_async(PaymentPoll.objects.select_related('payment_event').get)(hashed_password=decoded_password))
    message_text = "If you are creating a payment poll:\n\n[/create_payment_poll]\n\nIf you are making a payment:\n\n[/make_payment]"
    await message.reply(message_text)

@dp.message_handler(commands=['make_payment'])
async def start_command(message: types.Message):
    await message.reply('Enter Payment Password')
    await dp.current_state().set_state('waiting for password')
    

@dp.message_handler(state='waiting for password')
async def process_options(message: types.Message, state: FSMContext):

    password = message.text.strip()

    # Validate the provided password against the hashed password
    # hashed_password = payment_poll.password
    decoded_password = hashlib.sha256(password.encode()).hexdigest()
    
    
    try:
        payment_poll = await sync_to_async(PaymentPoll.objects.select_related('payment_event').get)(hashed_password=decoded_password)



    # if payment_poll:

        # Password is correct; proceed with accessing the data
        # Do whatever you need to do with the data (e.g., send it to the user)

        # Example: Send the data to the user
        #await bot.send_message(message.chat.id, f"Subject: {payment_poll.subject}\nDescription: {payment_poll.description}\nPrice: {payment_poll.price}\nEvent:{payment_poll.payment_event}")
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
        await state.finish()

    except ObjectDoesNotExist:
        # Password is incorrect; inform the user
        await bot.send_message(message.chat.id, "Incorrect password. Please re-enter your password.")
        await state.finish()

    except Exception as e:
        # Handle other exceptions gracefully
        await bot.send_message(message.chat.id, "An error occurred. Please try again later.")
        await state.finish()
        logging.error(str(e))
        
    #await message.answer(f'Poll created successfully! Chat ID is ${chat_id}')
    await state.finish()


@dp.pre_checkout_query_handler(lambda query:True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id,ok=True)

#successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message:types.Message, state: FSMContext):
    user = message.from_user.username
    user_id = message.from_user.id
    chat_id = message.chat.id
    payment_id = message.successful_payment.invoice_payload
    total_amount = message.successful_payment.total_amount / 100  # Divide by 100 to get the actual amount
    currency = message.successful_payment.currency
    payment_provider = message.successful_payment.provider_payment_charge_id
    try:
        
        # Call the create method using sync_to_async
        await sync_to_async(PaymentDetails.objects.create)(
            tele_handle = user,
            user_id=user_id,
            chat_id=chat_id,
            payment_id=payment_id,
            total_amount=total_amount,
            currency=currency,
            payment_provider=payment_provider,
            is_success=True,  # You can set this to True since the payment was successful
        )

        try:
            decoded_password = decoded_password_cache.get(message.chat.id)
            print('PLSWORK', decoded_password)
            
            payment_poll = await sync_to_async(PaymentPoll.objects.select_related('payment_event').get)(hashed_password=decoded_password)
            print('Fine1')
            event = payment_poll.payment_event
            print("FINE2")
            student = await sync_to_async(Student.objects.get)(chat_id = user)
            print("Fine3")
    
            await track(student,event)
        

        except:
            await bot.send_message(message.chat.id, "Why you pay bro lmao")
        
        del decoded_password_cache[message.chat.id]

        await bot.send_message(
            message.chat.id,
            f"Payment for the amount {message.successful_payment.total_amount // 100} "
            f"{message.successful_payment.currency} was successfull!"
        )


    except Exception as e:
        # Handle other exceptions gracefully
        await bot.send_message(message.chat.id, "An error occurred. Please try again later.")
        logging.error(str(e))
        
if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)

    



