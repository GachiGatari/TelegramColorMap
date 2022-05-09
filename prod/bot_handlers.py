from telegram.ext import CallbackContext
from telegram import Update
from prod.func import send_route

def image_handler(update: Update, context: CallbackContext):
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    send_route(update, context, newFile.download(custom_path=f"media/file_{file_id}.jpg"))

def start_handler(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat.id, "Здравствуйте! Вас приветствует LaVa-бот. Как Вы себя чувствуете? Какое у Вас настроение? Давайте это проверим. Раскрасьте картинку, и я предложу Вам индивидуальный релаксационный маршрут. Let's go!")
    context.bot.send_photo(update.message.chat.id, open('prod/template.jpg', 'rb'))