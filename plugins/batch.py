# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.
# This version contains a definitive fix for PEER_ID_INVALID issue.

import os, re, time, asyncio, json
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from config import API_ID, API_HASH, LOG_GROUP, STRING, FORCE_SUB, FREEMIUM_LIMIT, PREMIUM_LIMIT
from utils.func import get_user_data, screenshot, thumbnail, get_video_metadata, get_user_data_key, process_text_with_rules, is_premium_user, E
from shared_client import app as X
from plugins.settings import rename_file
from plugins.start import subscribe as sub
from utils.custom_filters import login_in_progress
from utils.encrypt import dcs
from typing import Dict, Any, Optional

Y = None if not STRING else __import__('shared_client').userbot
Z, P, UB, UC = {}, {}, {}, {}

# --- Utility Functions ---
def sanitize(filename):
    return re.sub(r'[<>:"/\\|?*\']', '_', filename).strip(" .")[:255]

async def upd_dlg(c):
    try:
        if c: await c.get_dialogs(limit=1)
        return True
    except Exception:
        return False

# --- Client Management ---
async def get_ubot(uid):
    if uid in UB and UB[uid]: return UB[uid]
    bt = await get_user_data_key(uid, "bot_token", None)
    if not bt: return None
    try:
        bot = Client(f"user_{uid}", bot_token=bt, api_id=API_ID, api_hash=API_HASH, no_updates=True)
        await bot.start()
        UB[uid] = bot
        return bot
    except Exception as e:
        print(f"Error starting custom bot for {uid}: {e}")
        return None

async def get_uclient(uid):
    if uid in UC and UC[uid]: return UC[uid]
    ud = await get_user_data(uid)
    if not ud: return None
    xxx = ud.get('session_string')
    if not xxx: return None
    try:
        ss = dcs(xxx)
        gg = Client(f'{uid}_client', api_id=API_ID, api_hash=API_HASH, device_model="v3saver", session_string=ss, no_updates=True)
        await gg.start()
        UC[uid] = gg
        return gg
    except Exception as e:
        print(f'User client error for {uid}: {e}')
        return None

# --- Main Processing Logic ---
async def process_msg(worker_client, message, user_id, progress_msg):
    if not message:
        return "Skipped: Message not found."
    if not message.media and not message.text:
        return "Skipped: No processable content."

    try:
        # Determine target chat
        cfg_chat = await get_user_data_key(user_id, 'chat_id', None)
        tcid, rtmid = (user_id, None)
        if cfg_chat:
            if '/' in cfg_chat:
                parts = cfg_chat.split('/', 1)
                tcid, rtmid = (int(parts[0]), int(parts[1]) if len(parts) > 1 else None)
            else:
                tcid = int(cfg_chat)
        
        # Process and send text messages
        if message.text:
            await worker_client.send_message(tcid, text=message.text.markdown, reply_to_message_id=rtmid)
            return 'Sent.'

        # Process media messages
        orig_caption = message.caption.markdown if message.caption else ''
        proc_text = await process_text_with_rules(user_id, orig_caption)
        user_cap = await get_user_data_key(user_id, 'caption', '')
        final_caption = f'{proc_text}\n\n{user_cap}'.strip()

        st = time.time()
        await progress_msg.edit('Downloading...')

        file_attr = getattr(message, message.media.value, None)
        original_filename = getattr(file_attr, 'file_name', None)
        download_filename = sanitize(original_filename or str(time.time()))
        
        downloaded_path = await worker_client.download_media(message, file_name=download_filename)
        
        if not downloaded_path or not os.path.exists(downloaded_path):
            await progress_msg.edit('Download failed.')
            return 'Download failed.'

        await progress_msg.edit('Renaming...')
        if original_filename:
            downloaded_path = await rename_file(downloaded_path, user_id, progress_msg)

        thumb_path = thumbnail(user_id)
        
        await progress_msg.edit('Uploading...')
        
        # The corrected upload logic
        if message.video:
            metadata = await get_video_metadata(downloaded_path)
            thumb_path = await screenshot(downloaded_path, metadata.get('duration', 0), user_id)
            await worker_client.send_video(tcid, video=downloaded_path, caption=final_caption, thumb=thumb_path, width=metadata.get('width', 0), height=metadata.get('height', 0), duration=metadata.get('duration', 0), reply_to_message_id=rtmid)
        elif message.document:
            await worker_client.send_document(tcid, document=downloaded_path, caption=final_caption, thumb=thumb_path, reply_to_message_id=rtmid)
        elif message.photo:
            await worker_client.send_photo(tcid, photo=downloaded_path, caption=final_caption, reply_to_message_id=rtmid)
        elif message.audio:
            await worker_client.send_audio(tcid, audio=downloaded_path, caption=final_caption, thumb=thumb_path, reply_to_message_id=rtmid)
        else: # Fallback for other media types
            await worker_client.send_document(tcid, document=downloaded_path, caption=final_caption, thumb=thumb_path, reply_to_message_id=rtmid)

        if os.path.exists(downloaded_path): os.remove(downloaded_path)
        if thumb_path and os.path.exists(thumb_path): os.remove(thumb_path)
        return 'Done.'

    except Exception as e:
        if os.path.exists(downloaded_path): os.remove(downloaded_path)
        return f'Error: {str(e)[:100]}'

# --- Command Handlers ---
@X.on_message(filters.command(['batch']))
async def batch_handler(c, m: Message):
    user_id = m.from_user.id
    if await sub(c, m) == 1: return
    
    # Check for active process
    if user_id in Z:
        await m.reply_text("You already have an active process. Please wait for it to complete or use /stop (not implemented yet).")
        return

    Z[user_id] = {'step': 'link'}
    await m.reply_text('Send the starting message link...')

@X.on_message(filters.text & filters.private & ~filters.command(['start']))
async def text_handler(c, m: Message):
    user_id = m.from_user.id
    if user_id not in Z: return
    
    user_step = Z[user_id].get('step')

    if user_step == 'link':
        link = m.text
        channel_id, start_msg_id, link_type = E(link)
        if not channel_id or not start_msg_id:
            await m.reply_text('Invalid link format. Please send a valid Telegram message link.')
            del Z[user_id]
            return
        Z[user_id].update({'step': 'count', 'channel': channel_id, 'start_id': start_msg_id, 'type': link_type})
        await m.reply_text('How many messages do you want to process?')

    elif user_step == 'count':
        try:
            count = int(m.text)
        except ValueError:
            await m.reply_text("Please enter a valid number.")
            return

        # Limit check
        limit = PREMIUM_LIMIT if await is_premium_user(user_id) else FREEMIUM_LIMIT
        if count > limit:
            await m.reply_text(f"Your maximum limit is {limit}. Please enter a smaller number.")
            return

        channel = Z[user_id]['channel']
        start_id = Z[user_id]['start_id']
        link_type = Z[user_id]['type']
        del Z[user_id] # Clear user state

        # Determine which client to use based on link type
        worker = None
        if link_type == 'private':
            worker = await get_uclient(user_id)
            if not worker:
                await m.reply_text("This is a private link. Please /login with your personal account first.")
                return
        else: # public
            worker = await get_ubot(user_id)
            if not worker:
                await m.reply_text("This is a public link. Please /setbot with a bot token first.")
                return

        progress_msg = await m.reply_text(f"Processing batch of {count} messages...")
        success_count = 0
        
        try:
            for i in range(count):
                msg_id = start_id + i
                try:
                    message_to_process = await worker.get_messages(channel, msg_id)
                    result = await process_msg(worker, message_to_process, user_id, progress_msg)
                    if result == 'Done.':
                        success_count += 1
                except PeerIdInvalid:
                    await m.reply_text(f"{i+1}/{count}: Error: PEER_ID_INVALID. The bot/account is not a member of this channel. Please join the channel and try again.")
                    await asyncio.sleep(2)
                except Exception as e:
                    await m.reply_text(f"{i+1}/{count}: Skipped. Error: {str(e)[:100]}")
                    await asyncio.sleep(2)
                await asyncio.sleep(5) # Delay between messages to avoid flood waits

            await progress_msg.edit(f'Batch Completed ✅ Success: {success_count}/{count}')
        except Exception as e:
            await progress_msg.edit(f"An unexpected error occurred during the batch process: {e}")
        finally:
            # Clean up state if it wasn't cleared before
            if user_id in Z:
                del Z[user_id]