# ---- Safe import for imghdr ----
try:
    import imghdr
except ImportError:
    import mimetypes as imghdr
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pytube import YouTube
from googletrans import Translator
import requests

TOKEN = "BOT_TOKEN"
ADMIN_CONTACT = "ADMIN_CHAT_ID"

translator = Translator()

# ---- Commands ----
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Hello! Music bot ready hai 🎵\nAdmin: {ADMIN_CONTACT}\n"
        "Use /play [YouTube link] to play music\n"
        "Use /translate [text] [target language code, e.g., hi, en]\n"
        "Use /joke, /quote, /tip for fun"
    )

def play(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Please YouTube link do: /play [link]")
        return

    link = context.args[0]
    try:
        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        file_path = audio_stream.download()
        update.message.reply_audio(open(file_path, 'rb'))
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def translate(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        update.message.reply_text("Use: /translate [text] [target language code, e.g., hi, en]")
        return
    try:
        target = context.args[-1]
        text = " ".join(context.args[:-1])
        translated = translator.translate(text, dest=target)
        update.message.reply_text(f"Translated: {translated.text}")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def joke(update: Update, context: CallbackContext):
    try:
        data = requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()
        update.message.reply_text(data.get("joke"))
    except:
        update.message.reply_text("Joke fetch karne me problem 😅")

def quote(update: Update, context: CallbackContext):
    try:
        data = requests.get("https://api.quotable.io/random").json()
        update.message.reply_text(f'"{data["content"]}" - {data["author"]}')
    except:
        update.message.reply_text("Quote fetch karne me problem 😅")

def tip(update: Update, context: CallbackContext):
    try:
        data = requests.get("https://api.adviceslip.com/advice").json()
        update.message.reply_text(f"Tip: {data['slip']['advice']}")
    except:
        update.message.reply_text("Tip fetch karne me problem 😅")

# ---- Bot Setup ----
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("play", play))
dp.add_handler(CommandHandler("translate", translate))
dp.add_handler(CommandHandler("joke", joke))
dp.add_handler(CommandHandler("quote", quote))
dp.add_handler(CommandHandler("tip", tip))

print("Bot running...")
updater.start_polling()
updater.idle()
