from telegram import Bot
import asyncio

# 設定 Telegram 機器人的token
bot_token = 'YOUR_BOT_TOKEN'

# 設定要發送訊息的chat_id
chat_id = 'YOUR_CHAT_ID'

# 建立 Telegram Bot 物件
bot = Bot(token=bot_token)

# 定義發送訊息的函數
async def send_message():
    # 要發送的訊息內容
    message = f"YOUR_MESSAGE"

    # 使用機器人發送訊息到指定的聊天室
    await bot.send_message(chat_id=chat_id, text=message)

# 建立事件迴圈並執行發送訊息的函數
loop = asyncio.get_event_loop()
loop.run_until_complete(send_message())
loop.close()
