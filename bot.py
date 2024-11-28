import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Функция для команды /start
async def start(update: Update, context):
    logger.info("Команда /start была вызвана.")  # Логируем вызов команды
    # Сразу показываем кнопки "Консультация" и "Наш офис"
    keyboard = [
        [InlineKeyboardButton("Консультация", callback_data='consultation')],
        [InlineKeyboardButton("Наш офис", callback_data='office')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Чем могу помочь?', reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'consultation':  # Если выбрана консультация
        # Предлагаем выбрать одного из трех специалистов
        keyboard = [
            [InlineKeyboardButton("Руководитель представительства", callback_data='sergey')],
            [InlineKeyboardButton("Термостатика и балансировка", callback_data='evgeny')],
            [InlineKeyboardButton("Регулирующая арматура", callback_data='vadim')],
            [InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')]  # Кнопка для возврата на главную
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите, с кем вы хотите связаться:", reply_markup=reply_markup)

    elif query.data == 'sergey':  # Если выбрана консультация с руководителем
        info_text = """
        Сергей Янкун:
        Телефон: +375447534543
        Telegram: @Seregin90
        Почта: yankun@ridan.ru
        """
        keyboard = [
            [InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')]  # Кнопка для возврата на главную
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=info_text, reply_markup=reply_markup)

    elif query.data == 'evgeny':  # Если выбрана консультация по термостатике и балансировке
        info_text = """
        Евгений Эйдельман:
        Телефон: +375445999133
        Telegram: @eidelman_ridan
        Почта: eidelman@ridan.ru
        """
        keyboard = [
            [InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')]  # Кнопка для возврата на главную
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=info_text, reply_markup=reply_markup)

    elif query.data == 'vadim':  # Если выбрана консультация по регулирующей арматуре
        info_text = """
        Вадим Воронецкий:
        Телефон: +375291086353
        Почта: voronetskii@ridan.ru
        """
        keyboard = [
            [InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')]  # Кнопка для возврата на главную
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=info_text, reply_markup=reply_markup)

    elif query.data == 'office':  # Если выбрана информация о офисе
        office_info = """
        Адрес нашего офиса: Республика Беларусь,
г. Минск, ул. М. Богдановича, д.124, помещение 4Н

Координаты: 53.936730, 27.583436
На карте: [Яндекс Карты] (https://yandex.ru/maps/?pt=27.583436,53.936730&z=16)
        """
        keyboard = [
            [InlineKeyboardButton("Вернуться на главную", callback_data='back_to_main')]  # Кнопка для возврата на главную
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=office_info, reply_markup=reply_markup)

    elif query.data == 'back_to_main':  # Обработка кнопки "Вернуться на главную"
        # Возвращаем пользователя на главный экран
        keyboard = [
            [InlineKeyboardButton("Консультация", callback_data='consultation')],
            [InlineKeyboardButton("Наш офис", callback_data='office')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите, что вас интересует:", reply_markup=reply_markup)

def main():
    # Получаем токен из переменной окружения
    token = os.getenv('BOT_TOKEN')  # Используем переменную окружения, которую мы добавили в Railway
    
    if not token:
        print("Ошибка: переменная окружения BOT_TOKEN не найдена!")
        return

    # Создание приложения
    application = Application.builder().token(token).build()

    # Добавляем обработчики для команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота с polling
    application.run_polling()

if __name__ == '__main__':
    main()
