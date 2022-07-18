from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mainMenu = InlineKeyboardMarkup(row_width=2)
inlineBtnPopolnitbalans = InlineKeyboardButton('💰Пополнить баланс', callback_data='popolnitbalans')
mainMenu.add(inlineBtnPopolnitbalans)
def billKnopki(pay_url, user_bill_id):
    billMenu = InlineKeyboardMarkup(row_width=2)
    inlineBtnUrlPlateja = InlineKeyboardButton('🔗Сылка на оплату', url = pay_url)
    inlineBtnProverkaPlateja = InlineKeyboardButton('✔️Проверка платежа', callback_data="proverka_"+user_bill_id)
    billMenu.add(inlineBtnUrlPlateja, inlineBtnProverkaPlateja)
    return(billMenu)