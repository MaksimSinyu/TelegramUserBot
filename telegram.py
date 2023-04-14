# Import required libraries
from telethon import TelegramClient, events
import datetime
import asyncio
import openai
import app

# Set OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Set Telegram API credentials
api_id = 'YOUR_API_ID(E: 123456789)'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'

# Set start time
start_time = datetime.datetime.now()

# Create TelegramClient object
client = TelegramClient('session_name', api_id, api_hash)


# Define event handler for new messages
@client.on(events.NewMessage())
async def hello(event):
    try:
        # If the message starts with 'ut', reply with uptime
        if event.text.split()[0] == "ut":
            # Calculate uptime
            uptime = datetime.datetime.now() - start_time
            # Reply with uptime
            msgUptime = await event.reply(f"Ut: {uptime}")
            await asyncio.sleep(2)
            # Delete the original message and the reply after 2 seconds
            await client.delete_messages(event.chat_id, [event.id])
            await client.delete_messages(event.chat_id, [msgUptime.id])

        # If the message starts with 'Гриша' (Grisha in Russian) and the second word is not 'skip', 
        # then send the message to OpenAI for response generation
        elif event.text.split()[0] == "Grisha" and event.text.split()[1] != "skip":
            # Remove 'Гриша' from the message text
            t = event.text.replace('Grisha', '')

            print(t)

            # Send the message to OpenAI for response generation
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "assistant", "content": t},
                ]
            )

            # Get the generated response from OpenAI and reply to the message in Telegram
            print(response.choices[0].message['content'])
            await event.reply(
                f"Original text :\n{response.choices[0].message['content']}")

        # If the message starts with 'гриша' (Grisha in Russian), then 
        # send the message to OpenAI for image generation
        elif event.text.split()[0] == "img":
            # Remove 'гриша' from the message text
            i = event.text.replace('img', '')

            print(i)

            # Send the message to OpenAI for image generation
            response = openai.Image.create(
                prompt=i,
                n=1,
                size="1024x1024"
            )

            # Get the generated image URL from OpenAI, download it and send it to the chat in Telegram
            image_url = response['data'][0]['url']
            image = await app.download_image(image_url)
            await client.send_file(
                event.chat_id,
                file=image,
                caption="Here is what I found for you!",
                reply_to=event
            )

    # If there is an error, print it
    except Exception as e:
        print(f"Error: {e}")
