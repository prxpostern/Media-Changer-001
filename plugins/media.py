import logging
from pyrogram import Client, filters
from pyromod import listen
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InputMediaPhoto,InputMediaDocument,InputMediaVideo,InputMediaAnimation,InputMediaAudio
from asyncio import TimeoutError
PACK = filters.animation | filters.document| filters.video|filters.audio |filters.photo

logger = logging.getLogger(__name__)

@Client.on_message(PACK  & filters.private)
async def media(client, message):
    if message.photo:
        file_id = message.photo.file_id
        mid = InputMediaPhoto(file_id, caption=message.caption and message.caption.html)

    elif message.document:
        file_id = message.document.file_id
        mid = InputMediaDocument(file_id, caption=message.caption and message.caption.html)

    elif message.video:
        file_id = message.video.file_id
        mid = InputMediaVideo(file_id, caption=message.caption and message.caption.html)

    elif message.animation:
        file_id = message.animation.file_id
        mid = InputMediaAnimation(file_id, caption=message.caption and message.caption.html)

    elif message.audio:
        file_id  = message.audio.file_id
        mid = InputMediaAudio(file_id, caption=message.caption and message.caption.html)
    else:
        print('no way')

    try:
        print("print: 1")
        logger.info(f"1")
        a = await client.ask(message.chat.id,'Now send me the link of the message of the channnel that you need to edit',
                    filters=filters.text, timeout=30)
        logger.info(f"2")
        print("print: 2")
    except TimeoutError:
        await message.reply_text(
            "```Session Timed Out.Resend the file to Start again```",
            parse_mode="md",
            quote=True
        )
        return
    link = a.text
    try:
        logger.info(f"3")
        print("print: 3")
        b = await client.ask(message.chat.id,'Now send me Duration:',
                    filters=filters.text, timeout=30)
        logger.info(f"4")
        print("print: 4")
    except TimeoutError:
        await message.reply_text(
            "```Session Timed Out.Resend the file to Start again```",
            parse_mode="md",
            quote=True
        )
        return
    
    #link = a.text
    if  message.video:
        duration = int(b.text)
        file_id = message.video.file_id
        mid = InputMediaVideo(file_id, caption=message.caption and message.caption.html, duration=duration)
        logger.info(f"5---{mid}")
        print(f"print: 5---{mid}")
            
         
    a = "-100"
    try:
        id = link.split('/')[4]
        msg_id = link.split('/')[5]
        cd = a + str(id)
        chid = int(cd)
        logger.info(f"1---{chid}")    
    except:
        chid = link.split('/')[3]
        msg_id = link.split('/')[4]
        logger.info(f"2---{chid}")
        
    try:
        is_admin=await client.get_chat_member(chat_id=chid, user_id=message.from_user.id)
    except UserNotParticipant:
        await message.reply("It seems you are not a member of this channel and hence you can't do this action.")
        return
    if not is_admin.can_edit_messages:
        await message.reply("You are not permited to do this, since you do not have the right to edit posts in this channel.")
        return
            
    try:
        await client.edit_message_media(
          chat_id = chid,
          message_id = int(msg_id),
          media = mid
        )
        await client.send_video(
            chat_id = message.chat.id,
            video = file_id,
            duration = duration,
            caption=message.caption
        )    
            
    except Exception as e:
        await message.reply_text(e)
        return
    await message.reply_text('**successfully Edited the media**')
