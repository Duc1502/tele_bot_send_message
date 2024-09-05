import os
from tempfile import NamedTemporaryFile
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

CHANNEL_CHAT_ID_1 = '-1002197950564'
CHANNEL_CHAT_ID_2 = '-1002200973439'
CHANNEL_CHAT_ID_3 = '-1002176480053'

BOT_TOKEN = '7102160257:AAGVclfBkHC_8I3TZynCjqO-t1i70ymTb50'

icon = "📲"
icon2 = "🙋"

LINK_1 = 'https://broker-qx.pro/sign-up/?lid=905982'
LINK_2 = 'https://broker-qx.pro/sign-up/?lid=986770'

LINK_TUT_1 = 'https://t.me/QuotexSignalFreeWillTurner/64'
LINK_TUT_2 = 'https://t.me/VictoryTraderQuotexSignal/55'

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def escape_markdown_v2(text: str) -> str:
    """
    Escapes special characters in text for Markdown v2.
    """
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

# Xử lý tất cả các tin nhắn văn bản và ảnh
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text:
        user_message = update.message.text

        # Escape the user message for Markdown v2
        escaped_user_message = escape_markdown_v2(user_message)

        # Lưu tin nhắn vào biến
        stored_message_channel_1 = f"{escaped_user_message}\n\n{icon} [Click here to open the broker]({escape_markdown_v2(LINK_1)}) \n{icon2} Don't know how to trade yet? [Click here]({escape_markdown_v2(LINK_TUT_1)})" 
        stored_message_channel_2 = f"{escaped_user_message}\n\n{icon} [Click here to open the broker]({escape_markdown_v2(LINK_2)}) \n{icon2} Don't know how to trade yet? [Click here]({escape_markdown_v2(LINK_TUT_2)})"
        stored_message_channel_3 = f"{escaped_user_message}"

        # Gửi tin nhắn vào kênh 1
        await context.bot.send_message(chat_id=CHANNEL_CHAT_ID_1, text=stored_message_channel_1, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

        # Gửi tin nhắn vào kênh 2
        await context.bot.send_message(chat_id=CHANNEL_CHAT_ID_2, text=stored_message_channel_2, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

        # Gửi tin nhắn vào kênh 3
        await context.bot.send_message(chat_id=CHANNEL_CHAT_ID_3, text=stored_message_channel_3, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    elif update.message.sticker:
        # Lấy thông tin sticker từ tin nhắn của người dùng
        sticker = update.message.sticker

        # Gửi sticker đến kênh 1
        await context.bot.send_sticker(chat_id=CHANNEL_CHAT_ID_1, sticker=sticker.file_id)

        # Gửi sticker đến kênh 2
        await context.bot.send_sticker(chat_id=CHANNEL_CHAT_ID_2, sticker=sticker.file_id)

        # Gửi sticker đến kênh 3
        await context.bot.send_sticker(chat_id=CHANNEL_CHAT_ID_3, sticker=sticker.file_id)
    elif update.message.photo:
        # Xử lý ảnh chụp màn hình
        photo = update.message.photo[-1]
        file = await photo.get_file()
        photo_bytes = await file.download_as_bytearray()

        # Lấy caption từ tin nhắn
        caption = update.message.caption or ""

        # Tạo tệp tạm thời để lưu ảnh
        with NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(photo_bytes)
            temp_file_path = temp_file.name

        try:
            # Gửi ảnh đến các kênh
            for channel_id in [CHANNEL_CHAT_ID_1, CHANNEL_CHAT_ID_2, CHANNEL_CHAT_ID_3]:
                with open(temp_file_path, 'rb') as image_file:
                    await context.bot.send_photo(chat_id=channel_id, photo=image_file, caption=caption)
        finally:
            # Xóa tệp tạm thời sau khi gửi
            os.remove(temp_file_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

# Thêm bộ xử lý tin nhắn văn bản
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(MessageHandler(filters.Sticker.ALL, echo))
app.add_handler(MessageHandler(filters.PHOTO, echo))

app.run_polling()
