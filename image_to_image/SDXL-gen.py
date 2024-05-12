import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
from datetime import datetime

base_url = "https://turbo.art"
api_url = "https://gongy--stable-diffusion-xl-turbo-model-inference.modal.run/"

def generate_image(prompt, image_data):
    headers = {
        "Origin": base_url,
        "Referer": base_url + "/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    form_data = MultipartEncoder(
        fields={
            "prompt": prompt,
            "image": ("image", image_data, f"image.png"),
            "num_iterations": "2"
        }
    )

    response = requests.post(
        api_url,
        data=form_data,
        headers={"Content-Type": form_data.content_type},
        timeout=30
    )

    if response.status_code != 200:
        print(response.status_code, response.text)
        return "An error occurred while generating the image."

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"generatedImage_{now}.jpg"

    with open(file_name, "wb") as f:
        f.write(response.content)

    print("Image generated successfully:", file_name)
    return file_name
    
# Usage in Pyrogram bot
from pyrogram import Client, filters

app = Client("my_bot", 14681826, "add59ab14dbbccf3c92c65ca4477f2fa")

@app.on_message(filters.command("generate"))
async def generate_image_command(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        await message.reply_text("Processing...")
        prompt = message.text.split("/generate", 1)[-1].strip()
        image_file_id = message.reply_to_message.photo.file_id
        image_data = await client.download_media(message.reply_to_message, "generate_test.png")
        result = generate_image(prompt, image_data)
        if result.startswith("An error"):
            await message.reply_text(result)
        else:
            await message.reply_photo(result)
    else:
        await message.reply_text("Please reply to an image with the /generate command.")


print("start...")
app.run()
