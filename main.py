from aiogram import Bot, executor, Dispatcher, types
from db import Database
import markyp as mrkp
from pyqiwip2p import AioQiwiP2P
import random

TOKEN = "5450001891:AAEZlazlf5COMnvj0n9reCth4hiH_iv94Jc"
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)
db = Database("database.db")
db.add_users_table()
db.add_bill_table()
SECRET_QIWIKEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImJxbDBkMS0wMCIsInVzZXJfaWQiOiI3OTc3OTk2NjA0MSIsInNlY3JldCI6IjI2OGE1MDU0Mjk5ZGE3YjdjNDUyNmExMDRjOTBhMDAxOTkyYWI1ODQ3OWM1MWRlMzU3N2VhYzAwODZmMDAwZDAifX0="
p2p = AioQiwiP2P(auth_key = SECRET_QIWIKEY)

@dp.message_handler(commands='start', chat_type=[types.ChatType.PRIVATE])
async def cmdStart(message: types.Message):  
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, text = f'Привет {message.from_user.full_name}\nЯ - бот для пополнения баланса.\nНажмите на кнопку, чтобы пополнить баланс', reply_markup=mrkp.mainMenu)
@dp.callback_query_handler(chat_type = [types.ChatType.PRIVATE])
async def platej(callback: types.CallbackQuery):
    if callback.data == "popolnitbalans":
        await bot.send_message(callback.from_user.id, 'Введите сумму, на которую вы хотите пополнить баланс')
    elif callback.data[:9] == "proverka_":
        user_bill_id = callback.data[9:]
        try:
            if ((await p2p.check(bill_id=user_bill_id)).status) == "PAID":
                db.add_user_money(db.bill_money(user_bill_id) + db.user_money(callback.from_user.id), callback.from_user.id)
                await bot.send_message(callback.from_user.id, 'Платёж прошёл👍')
                db.dell_user_bill_id(user_bill_id)
            else:
                await bot.send_message(callback.from_user.id, 'Платёж не прошёл👎')
        except:
            pass
@dp.message_handler(chat_type = [types.ChatType.PRIVATE])
async def lastMessagesText(message: types.Message):
    paymentAmount =  message.text
    if (paymentAmount.isdigit() and int(paymentAmount) > 0):
        user_bill_id = str(message.from_user.id) + str(random.randint(1000, 9999))
        while db.user_bill_id_exists(user_bill_id):
            user_bill_id = str(message.from_user.id) + str(random.randint(1000, 9999))
        db.add_user_bill_id(message.from_user.id, user_bill_id, paymentAmount)
        new_bill = await p2p.bill(bill_id=user_bill_id, amount = paymentAmount, lifetime=5)
        await bot.send_message(message.from_user.id, text = 'Платёж успешно создан', reply_markup = mrkp.billKnopki(new_bill.pay_url, user_bill_id))
    else:
        await bot.send_message(message.from_user.id, text = 'Введите сумму, на которую вы хотите пополнить баланс(целое число)')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)