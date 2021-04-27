
import logging, time, re, shutil, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from decoding import getMedia


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

smile = u' \U0001F604'
source=''
btn = 0
twitter = ''
formato = ''
url =''
chat_id = ''

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Halo, kirimkan saya tautan Instagram, Twitter atau Youtube yang akan saya cari untuk Anda!')
    update.message.reply_text('Jika Anda mengirim tautan dan tidak menerima file Anda dalam 1 menit. Silakan coba mengirim sekali lagi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/help')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

################################## Get link from Telegram/User ##################################

def getLink(update, context):
    global twitter, url, chat_id, smile
    bot = telegram.Bot(token="1757876259:AAHed09ppxaOcEQqwpVpnLfr4LyYECLc4DE")
    url = update.message.text
    chat_id = update.message.chat_id
############################################### Twitter ####################################
    if re.search('twitter', url) != None or re.search('t.co', url) != None:
        bot.send_message(chat_id=update.message.chat_id, text='Ini mungkin memakan waktu cukup lama')
        if (getSource(url, chat_id, formato) == True):
            if (twitter != 'tidak valid' and twitter != ''):
                bot.send_message(chat_id=update.message.chat_id, text='Ready ' + smile)
                print("Berhasil disimpan. Twitter")
                #print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                os.remove('/home/mateus/Documents/Python/telegram_bot/twitter.mp4')
            else:
                bot.send_message(chat_id=update.message.chat_id, text='Sepertinya Anda mengirim tautan yang tidak valid. Untuk Gambar atau GIF, Anda dapat menyimpan dari tautan yang Anda kirim tepat di atas')
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Sepertinya Anda mengirim tautan yang tidak valid. Untuk Gambar atau GIF, Anda dapat menyimpan dari tautan yang Anda kirim tepat di atas')
############################################### Instagram ####################################

    elif (re.search('instagram', url) != None):
        if(getSource(url, chat_id, formato) == True):
            if(type(source) is str):
                if (re.search('instagram', source) != None):
                    bot.send_video(chat_id=update.message.chat_id, video = source, timeout=3600)
                    bot.send_message(chat_id=update.message.chat_id, text='Ready ' + smile)
                    print("Berhasil disimpan. Instagram")
                    #print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                elif (re.search('IGTV', source) != None):
                    bot.send_message(chat_id=update.message.chat_id, text='Ready ' + smile)
                    print("Berhasil disimpan. Instagram")
                    #print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
            elif type(source) is list:
                bot.send_message(chat_id=update.message.chat_id, text='Ready ' + smile)
                print("Berhasil disimpan. Instagram")
                #print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                source.clear()
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Tidak bekerja. Pastikan akun Instagram Anda tidak bersifat pribadi / tertutup')
############################################### Youtube ####################################

    elif re.search('youtube', url) != None or re.search('youtu.be', url) != None:
        buttons = [[InlineKeyboardButton("Video - MP4", callback_data = '.mp4')],
                    [InlineKeyboardButton("Audio - MP3", callback_data ='.mp3')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        bot.send_message(chat_id=update.message.chat_id, text='Format apa yang ingin Anda simpan?', reply_markup = reply_markup)

    else:
        bot.send_message(chat_id=update.message.chat_id, text='Sepertinya Anda mengirim tautan yang tidak valid.')
############################### Get Media From User Input(URL) ##################################

def getSource(url, chat_id, formato):
    bot = telegram.Bot(token="1757876259:AAHed09ppxaOcEQqwpVpnLfr4LyYECLc4DE")
    global source, btn, twitter
######################################### Instagram Check #######################################
    if (re.search('instagram', url) != None):
        source=getMedia(url, btn, bot, chat_id, formato='')
        btn += 1
        if type(source) is str:
            if (re.search('instagram', source) != None or re.search('IGTV', source) != None):
                return True
            else:
                return False

        elif type(source) is list:
            for i in source:
                if re.search('.mp4', i) != None:
                    return True
                else:
                    return False
########################################### Twitter Check #######################################
    elif re.search('twitter', url) != None or re.search('t.co', url) != None:
        twitter = getMedia(url, btn, bot, chat_id, formato='')
        if twitter == 'tidak valid':
            return False
        elif (twitter != '' and twitter != 'tidak valid'):
            return True
######################################### Youtube Check #########################################

    elif re.search('youtube', url) != None or re.search('youtu.be', url) != None:
        source=getMedia(url, btn, bot, chat_id, formato)
        return True
################################## Button Check for Mp3/Mp4 #######################################################
def button(update, CallBackContext):
    bot = telegram.Bot(token="1757876259:AAHed09ppxaOcEQqwpVpnLfr4LyYECLc4DE")
    global url, chat_id, formato, smile
    query = update.callback_query
    query.answer()
    if (query.data == '.mp3'):
        formato = '.mp3'
    elif (query.data == '.mp4'):
        formato = '.mp4'
    bot.send_message(chat_id=chat_id, text='Ini bisa memakan waktu cukup lama. Sabar ya...')
    bot.send_message(chat_id=chat_id, text='Jika video terlalu besar maka akan dibagi menjadi beberapa bagian.')
    query.message.delete()
    if(getSource(url, chat_id, formato) == True):
        bot.send_message(chat_id=chat_id, text='Ready ' + smile)
        print("Berhasil disimpan. Youtube")
    else:
        bot.send_message(chat_id=chat_id, text='Sepertinya Anda mengirim tautan yang tidak valid.')
############################ Bot Main Function #########################################
def main():
    """Start the bot."""
    updater = Updater("1757876259:AAHed09ppxaOcEQqwpVpnLfr4LyYECLc4DE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, getLink))
    dp.add_handler(CallbackQueryHandler(button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
