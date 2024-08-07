from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode  # Đảm bảo nhập ParseMode đúng cách

CHANNEL_CHAT_ID_1 = '-1002197950564'
CHANNEL_CHAT_ID_2 = '-1002200973439'

BOT_TOKEN = '7102160257:AAGVclfBkHC_8I3TZynCjqO-t1i70ymTb50'

LINK_1 = 'https://broker-qx.pro/sign-up/?lid=905982'
LINK_2 = 'https://broker-qx.pro/sign-up/?lid=897767'

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def escape_markdown_v2(text: str) -> str:
    """
    Escapes special characters in text for Markdown v2.
    """
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

# Xử lý tất cả các tin nhắn khác
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    # Escape the user message for Markdown v2
    escaped_user_message = escape_markdown_v2(user_message)

    # Lưu tin nhắn vào biến
    stored_message_channel_1 = f"{escaped_user_message}\n[REGISTER HERE]({escape_markdown_v2(LINK_1)})"
    stored_message_channel_2 = f"{escaped_user_message}\n[REGISTER HERE]({escape_markdown_v2(LINK_2)})"

    # Gửi tin nhắn vào kênh 1
    await context.bot.send_message(chat_id=CHANNEL_CHAT_ID_1, text=stored_message_channel_1, parse_mode=ParseMode.MARKDOWN_V2)

    # Gửi tin nhắn vào kênh 2
    await context.bot.send_message(chat_id=CHANNEL_CHAT_ID_2, text=stored_message_channel_2, parse_mode=ParseMode.MARKDOWN_V2)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

# Thêm bộ xử lý tin nhắn văn bản
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()