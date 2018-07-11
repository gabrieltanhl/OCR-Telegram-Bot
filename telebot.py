import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler, Filters
import visionocr
import os
from CREDENTIALS import BOT_KEY

bot = telegram.Bot(token=BOT_KEY)
updater = Updater(token=BOT_KEY)
dispatcher = updater.dispatcher

def start(bot,update):
    firstname = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, text=("Hey " + firstname + ", send me any picture containing text and I will OCR it for you!"))

def echo(bot, update):
    message = update.message.text
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text="Try sending me a picture with any text in it and I will OCR it for you!")

def receive_doc(bot, update):
    message = update.message
    file_id = message.document.file_id
    chat_id = update.message.chat_id
    ocr_file(bot,update,file_id,chat_id)

def receive_image(bot,update):
    message = update.message
    file_id = message.photo[-1].file_id
    chat_id = update.message.chat_id
    ocr_file(bot,update,file_id,chat_id)
    
def ocr_file(bot,update,file_id,chat_id):
    filepath = os.path.expanduser('~') + '/' + file_id
    print(filepath)
    bot.send_message(chat_id=chat_id, text="Please hold on...")
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    file = bot.get_file(file_id).download(filepath)
    
    ocr_text = visionocr.read_image(filepath)
    bot.send_message(chat_id=chat_id, text='Here you go:\n\n' + str(ocr_text))
    os.remove(filepath)


# handlers
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
doc_handler = MessageHandler(Filters.document, receive_doc)
image_handler = MessageHandler(Filters.photo, receive_image)

#dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(doc_handler)
dispatcher.add_handler(image_handler)

updater.start_polling()
