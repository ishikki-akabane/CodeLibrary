# Developed by @Devslab
# Author: github.com/ishikki-akabane

# we assume you already established your client and using this as a plugin 

import requests
from pyrogram import Client, filters


API_ID = 6283939
API_HASH = "72839393hswveystwiwojsbj"
BOT_TOKEN = "728292899:hsjjowutgaksooxbavsoeu"

BOT_ID = int(BOT_TOKEN.split(":")[0])
BLUE_URL = "https://blue-api.vercel.app/chatbot1"
BLUE_AI = "BLUE-AI-191939737" # Your Blue AI token / get it from @hackiabot on telegram 


app = Client("EvaChatbot", API_ID, API_HASH, BOT_TOKEN)

async def request_chatbot(query, user_id):
    params = {
        "user_id": user_id,
        "query": query,
        "BOT_ID": BOT_ID 
    }
    headers = {
        "api_key": BLUE_AI
    }

    response = requests.get(BLUE_URL, params=params, headers=headers)
    data = response.json()

    if data["status"] == 200:
        chat_reply = data["result"]["text"]
        return chat_reply
    else:
        return data["msg"]


@app.on_message()
async def eva_chatbot(client, message):
    user_id = message.from_user.id
    query = message.text
    msg = await request_chatbot(query, user_id)
    await message.reply_text(msg)


print("bot started...")
app.run()