import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Функция для команды /start
async def start(update: Update, context):
    logger.info("Команда /start была вызвана.")
    keyboard = [
        [InlineKeyboardButton("Консультация", callback_data='consultation')],
        [InlineKeyboardButton("Наш офис", callback_data='office')],
        [InlineKeyboardButton("Дистрибьюторы", callback_data='distributors')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Чем могу помочь?', reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'consultation':
        keyboard = [
            [InlineKeyboardButton("Руководитель представительства", callback_data='sergey')],
            [InlineKeyboardButton("Термостатика и балансировка", callback_data='evgeny')],
            [InlineKeyboardButton("Регулирующая арматура", callback_data='vadim')],
 	    [InlineKeyboardButton("RidBEL SET", callback_data='artsiom')],
            [InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите, с кем вы хотите связаться:", reply_markup=reply_markup)

    elif query.data == 'sergey':
        info_text = """
        Сергей Янкун:
        Телефон: +375447534543
        Telegram: @Seregin90
        Почта: yankun@ridan.ru
        """
        await send_info(query, info_text)

    elif query.data == 'evgeny':
        info_text = """
        Евгений Эйдельман:
        Телефон: +375445999133
        Telegram: @eidelman_ridan
        Почта: eidelman@ridan.ru
        """
        await send_info(query, info_text)

    elif query.data == 'vadim':
        info_text = """
        Вадим Воронецкий:
        Телефон: +375291086353
        Почта: voronetskii@ridan.ru
        """
        await send_info(query, info_text)

    elif query.data == 'artsiom':
        info_text = """
        Артем Мартыненко:
        Телефон: +375291808002
        Почта: martynenka@ridan.ru
        """
        await send_info(query, info_text)

    elif query.data == 'office':
        office_info = """
Адрес нашего офиса: 
Республика Беларусь, г. Минск, ул. М. Богдановича, д.124, пом. 4Н

Координаты: 53.936730, 27.583436
На карте: [Яндекс Карты](https://yandex.ru/maps/?pt=27.583436,53.936730&z=16)
        """
        await send_info(query, office_info)

    elif query.data == 'distributors':
        keyboard = [
            [InlineKeyboardButton("Термоимпульс", callback_data='termoimpuls')],
            [InlineKeyboardButton("РН-Профи", callback_data='rn_profi')],
            [InlineKeyboardButton("Иста Митеринг Сервис", callback_data='ista_metering')],
            [InlineKeyboardButton("Политроника", callback_data='politronica')],
            [InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите дистрибьютора:", reply_markup=reply_markup)

    elif query.data in ['termoimpuls', 'rn_profi', 'ista_metering', 'politronica']:
        distributor_info = {
            'termoimpuls': """
Термоимпульс

Адрес: г. Минск, ул. Олешева, дом 1, пом. 310, ком. 9
Телефон: +375 (17) 282-32-82
Почта: info@termoimpuls.by
Время работы: 
Пн.–чт. 8:30–17:30, 
Пт. 8:30–16:30,
Сб.-вс. выходные
            """,
            'rn_profi': """
РН-Профи

Адрес: Боровлянский с/с, д. Копище, ул. Лопатина, дом 7А, к.1, 9 этаж
Телефон: +375 17 270-56-59
Время работы: 
Пн.–пт. 9:00–18:00, 
Сб.-вс. выходные
            """,
            'ista_metering': """
Иста Митеринг Сервис

Адрес: г. Минск, ул. Змитрока Бядули, 12
Телефон: +375 17 224-56-67
Время работы: 
Пн.–пт. 9:00–17:00, 
Сб.-вс. выходные
            """,
            'politronica': """
Политроника

Адрес: г. Минск, ул. Кульман, 2, к. 382
Телефон: +375 17 370-33-46
Почта: polytron@tut.by
Время работы:
Пн.–чт. 9:00–18:00,
Пт. 9:00–17:00,
Сб.-вс. выходные
            """
        }
        await send_info(query, distributor_info[query.data])

    elif query.data == 'back_to_main':
        keyboard = [
            [InlineKeyboardButton("Консультация", callback_data='consultation')],
            [InlineKeyboardButton("Наш офис", callback_data='office')],
            [InlineKeyboardButton("Дистрибьюторы", callback_data='distributors')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Чем могу помочь?", reply_markup=reply_markup)

async def send_info(query, info_text):
    keyboard = [[InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=info_text, reply_markup=reply_markup)

def main():
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("Ошибка: переменная окружения BOT_TOKEN не найдена!")
        return

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()
