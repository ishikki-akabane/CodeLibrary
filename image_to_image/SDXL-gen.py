import requests
import os
import time

baseURL = "https://turbo.art"
apiURL = "https://gongy--stable-diffusion-xl-turbo-model-inference.modal.run/"

def guess_mime_type(file_bytes):
    signature = file_bytes.hex()[:8]
    if signature == "89504e47":
        return {"ext": "png", "mime": "image/png"}
    elif signature.startswith("ffd8"):
        return {"ext": "jpg", "mime": "image/jpeg"}
    else:
        return "Invalid file type"


def generate_image(prompt, image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        file_type = guess_mime_type(image_bytes)
        if isinstance(file_type, str):
            raise ValueError(file_type)
            
        headers = {
            "Origin": baseURL,
            "Referer": baseURL + "/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        files = {
            "prompt": (None, prompt),
            "image": (f"image.{file_type['ext']}", image_bytes, file_type["mime"]),
            "num_iterations": (None, "2")
        }

        response = requests.post(
            apiURL,
            files=files,
            headers=headers
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return "An error occurred while generating the image."

        file_path = f"generatedImage_{time.time()}.jpg"
        with open(file_path, "wb") as image_file:
            image_file.write(response.content)
            print("Image generated successfully.")
        return file_path
    
# Usage in Pyrogram bot
from pyrogram import Client, filters

API_ID = 7292939
API_HASH = "HSJJ72892992828BSJKSOWO"
BOT_TOKEN = "72829020:Jjshsieu920jwnbsoowyteksn"

app = Client("my_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("generate"))
async def generate_image_command(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        await message.reply_text("Processing...")
        prompt = message.text.split("/generate", 1)[-1].strip()
        image_file_id = message.reply_to_message.photo.file_id
        image_data = await client.download_media(message.reply_to_message, "generate_test.png")
        result = generate_image(prompt, "downloads/generate_test.png")
        if result.startswith("An error"):
            await message.reply_text(result)
        else:
            await message.reply_photo(result)
    else:
        await message.reply_text("Please reply to an image with the /generate command.")


print("start...")
app.run()
