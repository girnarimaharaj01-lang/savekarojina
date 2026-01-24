# Copyright (c) 2025 Gagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

# MODIFIED: Random image selection has been added.

from shared_client import client as bot_client, app
from telethon import events
from datetime import timedelta
from config import OWNER_ID, JOIN_LINK as JL, ADMIN_CONTACT as AC
from utils.func import add_premium_user, is_private_chat
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton as IK, InlineKeyboardMarkup as IKM
import base64 as spy
import random  # <-- Yahan random module import kiya gaya hai
from utils.func import a1, a2, a3, a4, a5, a7, a8, a9, a10, a11
from plugins.start import subscribe


@bot_client.on(events.NewMessage(pattern='/add'))
async def add_premium_handler(event):
    if not await is_private_chat(event):
        await event.respond(
            'This command can only be used in private chats for security reasons.'
            )
        return
    """Handle /add command to add premium users (owner only)"""
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        await event.respond('This command is restricted to the bot owner.')
        return
    text = event.message.text.strip()
    parts = text.split(' ')
    if len(parts) != 4:
        await event.respond(
            """Invalid format. Use: /add user_id duration_value duration_unit
Example: /add 123456 1 week"""
            )
        return
    try:
        target_user_id = int(parts[1])
        duration_value = int(parts[2])
        duration_unit = parts[3].lower()
        valid_units = ['min', 'hours', 'days', 'weeks', 'month', 'year',
            'decades']
        if duration_unit not in valid_units:
            await event.respond(
                f"Invalid duration unit. Choose from: {', '.join(valid_units)}"
                )
            return
        success, result = await add_premium_user(target_user_id,
            duration_value, duration_unit)
        if success:
            expiry_utc = result
            expiry_ist = expiry_utc + timedelta(hours=5, minutes=30)
            formatted_expiry = expiry_ist.strftime('%d-%b-%Y %I:%M:%S %p')
            await event.respond(
                f"""✅ User {target_user_id} added as premium member
Subscription valid until: {formatted_expiry} (IST)"""
                )
            await bot_client.send_message(target_user_id,
                f"""✅ Your have been added as premium member
**Validity upto**: {formatted_expiry} (IST)"""
                )
        else:
            await event.respond(f'❌ Failed to add premium user: {result}')
    except ValueError:
        await event.respond(
            'Invalid user ID or duration value. Both must be integers.')
    except Exception as e:
        await event.respond(f'Error: {str(e)}')
        
        
# Obfuscated /start command handler (Now Modified)
@app.on_message(filters.command(spy.b64decode(a5.encode()).decode()))
async def start_handler(client, message):
    subscription_status = await subscribe(client, message)
    if subscription_status == 1:
        return

    # Decode the necessary text content from utils/func.py
    caption_text = spy.b64decode(a7).decode()
    button1_text = spy.b64decode(a8).decode()
    button2_text = spy.b64decode(a9).decode()

    # List of your image URLs
    image_links = [
        "https://babubhaikundan.pages.dev/Assets/logo/bbk.png",
        "https://babubhaikundan.pages.dev/Assets/logo/hacker.png",
        "https://babubhaikundan.pages.dev/Assets/logo/1.jpg"
    ]

    # Select one image randomly from the list
    random_image_url = random.choice(image_links)

    # Create the keyboard with buttons
    keyboard_markup = IKM([
        [IK(button1_text, url=JL)],
        [IK(button2_text, url=AC)]
    ])

    # Send the randomly selected photo with caption and buttons
    await message.reply_photo(
        photo=random_image_url,
        caption=caption_text,
        reply_markup=keyboard_markup
    )

