# This file is a part of TG-FileStreamBot
# Coding: Jyothis Jayanth [@EverythingSuckz]

import logging
from typing import Union
from urllib.parse import quote_plus
from pyrogram import filters, errors
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, User
from pyrogram.enums.parse_mode import ParseMode
from WebStreamer.vars import Var
from WebStreamer.bot import StreamBot, logger
from WebStreamer.utils import get_hash, get_name

@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def media_receive_handler(_, m: Message) -> None:
    user: User = m.from_user
    allowed_users = Var.ALLOWED_USERS

    if allowed_users and not (str(user.id) in allowed_users or user.username in allowed_users):
        return await m.reply("<i>Access denied!</i>\n", quote=True)

    # Forward the media message to the specified channel
    log_msg: Message = await m.forward(chat_id=Var.BIN_CHANNEL)
    
    # Generate file hash and stream link
    file_hash: str = get_hash(log_msg, Var.HASH_LENGTH)
    stream_link: str = f"{Var.URL}{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}"
    short_link: str = f"{Var.URL}delta/{file_hash}{log_msg.id}"
    
    # Log the generated link
    logger.info(f"Generated link: {stream_link} for {user.first_name}")

    try:
        # Send the stream link with a shortened version and an "Open" button
        await m.reply_text(
            text=f"<code>{stream_link}</code>\n(<a href='{short_link}'>shortened</a>)",
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open", url=short_link)]]),
        )
    except errors.ButtonUrlInvalid:
        # Handle the case where the button URL is invalid
        await m.reply_text(
            text=f"<code>{stream_link}</code>\n\nshortened: {short_link}",
            quote=True,
            parse_mode=ParseMode.HTML,
        )
