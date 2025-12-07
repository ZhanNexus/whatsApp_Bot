
import re
import config
import strings
from typing import Callable
from neonize.events import MessageEv
from dataclasses import dataclass, field
from neonize.client import NewClient
from nandha import self, client


def get_uid(event: MessageEv):
    ms = event.Info.MessageSource
    if ms.IsGroup:
        user_id = int(ms.SenderAlt.User)
    else:
        user_id = int(ms.Sender.User)
        
    return user_id

def clean_wa_id(num: [int,str]):
    """Return a cleaned integer ID from a WA id-like value.

    Examples accepted: 1234567890, '1234567890@s.whatsapp.net', '1234567890-123@g.us'
    Falls back to `int` conversion of digits-only string; raises ValueError otherwise.
    """
    s = str(num or '').strip()
    # strip stuff after '@' or any non-digit characters
    if '@' in s:
        s = s.split('@', 1)[0]
    # keep only digits
    digits = re.sub(r'\D', '', s)
    if not digits:
        raise ValueError(f"Unable to parse WA id from: {num}")
    return int(digits)

def get_guid(event):
    """Return cleaned sender id (GUID) from event."""
    try:
        ms = getattr(event, 'Info', getattr(event, 'info', None))
        src = getattr(ms, 'MessageSource', None) if ms else None
        sender = getattr(src, 'Sender', None) if src else None
        lid = getattr(sender, 'User', None)
        return clean_wa_id(lid)
    except Exception:
        return None
    
def is_chatbot_text(text: str) -> bool:
    if not text:
        return False
    return bool(re.search(r'@nai', str(text), re.IGNORECASE))

def get_chat(event: MessageEv):
    """Return integer chat id for the event. Returns 0 if it cannot be determined."""
    try:
        ms = getattr(event, 'Info', getattr(event, 'info', None))
        src = getattr(ms, 'MessageSource', None) if ms else None
        chat = getattr(src, 'Chat', None) if src else None
        uid = getattr(chat, 'User', None) if chat else None
        return clean_wa_id(uid)
    except Exception:
        return 0

def get_user(event: MessageEv):
    """Return the effective user id for the event:
    - in groups: the sender (or owner id if message is from us)
    - in private chats: the chat's user id
    Returns 0 on failure.
    """
    try:
        ms = getattr(event, 'Info', getattr(event, 'info', None))
        src = getattr(ms, 'MessageSource', None) if ms else None
        if not src:
            return 0

        if getattr(ms, 'IsGroup', False):
            # prefer SenderAlt (some libs) then Sender
            if getattr(ms, 'IsFromMe', False):
                return int(getattr(config, 'owner_uid', getattr(config, 'owner_id', 0)))
            sender_alt = getattr(src, 'SenderAlt', None)
            sender = getattr(src, 'Sender', None)
            uid = getattr(sender_alt, 'User', None) or getattr(sender, 'User', None)
            return clean_wa_id(uid)
        else:
            chat = getattr(src, 'Chat', None)
            uid = getattr(chat, 'User', None)
            return clean_wa_id(uid)
    except Exception:
        return 0

def send_error(client, text):
    """Send a plain error message as the bot (`self`) recipient.

    `client` is expected to implement `send_message(recipient, message=...)`.
    """
    try:
        client.send_message(
            self,
            message=strings.error_text.format(text)
        )
    except Exception as e:
        log.error(f"send_error failed: {e}")

def send_error_reply(client, event, text):
    """Reply to the triggering `event` with an error message."""
    try:
        client.reply_message(
            message=strings.error_text.format(text),
            quoted=event
        )
    except Exception as e:
        log.error(f"send_error_reply failed: {e}")

def is_cmd(text) -> bool:
    return bool(text.startswith(config.PREFIXES, text))

def extract_text(text: str) -> str:
    """Return the message body after the first token (command).

    If there is no additional text after the command, returns an empty string.
    """
    if not text:
        return ""

    res_text = text.split(maxsplit=1)[1] if len(text.split()) > 1 else ''

    return res_text

def _get_message_text(event: MessageEv) -> str | None:
    """Robustly extract text from the incoming MessageEv.

    Handles variations in message shape used by different WhatsApp libraries / payload types:
    - plain text (`conversation`, `text`, `body`)
    - extended text (`extendedTextMessage.text`)
    - captions for media (`caption` or `imageMessage.caption` etc.)
    - quick reply / button payloads (`buttonsResponseMessage.selectedButtonId`, `selectedButtonText`)
    - list responses (`listResponse.singleSelectReply.selectedRowId`)

    Returns None if no textual content can be found.
    """
    if event is None:
        return None

    # message container may be `Message` or `message` depending on library
    msg = getattr(event, "Message", None) or getattr(event, "message", None)
    if not msg:
        return None

    # simple fields first
    for attr in ("conversation", "text", "body", "caption"):
        val = getattr(msg, attr, None)
        if val:
            return str(val)

    # nested extended text (common in several libraries)
    ext = getattr(msg, "extendedTextMessage", None)
    if ext:
        val = getattr(ext, "text", None)
        if val:
            return str(val)

    # media captions (some libs put caption inside media objects)
    for media_attr in ("imageMessage", "videoMessage", "documentMessage", "stickerMessage"):
        media = getattr(msg, media_attr, None)
        if media:
            val = getattr(media, "caption", None) or getattr(media, "text", None)
            if val:
                return str(val)

    # buttons / quick replies
    # buttonsResponseMessage may carry an ID; sometimes display text is available
    btn = getattr(msg, "buttonsResponseMessage", None)
    if btn:
        # prefer text-like fields if present
        val = getattr(btn, "selectedButtonId", None) or getattr(btn, "selectedButtonText", None) or getattr(btn, "selectedDisplayText", None)
        if val:
            return str(val)

    list_resp = getattr(msg, "listResponse", None)
    if list_resp:
        val = getattr(list_resp, "singleSelectReply", None)
        if val:
            # try known fields
            val2 = getattr(val, "selectedRowId", None) or getattr(val, "title", None) or getattr(val, "rowId", None)
            if val2:
                return str(val2)
    try:
        return str(msg)
    except Exception:
        return None

def messages(name: str) -> Callable:
    """Decorator to register message handlers."""

    def decorator(func: Callable) -> Callable:

        func_name = func.__name__.lower()
        config.ALL_FUNC.add(func_name)
        if func_name in config.DISABLED_FUNC:
            log.info(f"🔒 Function {func_name} is disabled, skipping....")
            return

        config.HANDLER[name.lower()] = func
        return func

    return decorator



@dataclass
class Message:
    client: NewClient
    event: MessageEv

    def __post_init__(self):
        ms = self.event.Info.MessageSource
        self.msg_id = self.event.Info.ID
        self.username = self.event.Info.Pushname or 'Unknown'
        self.user = ms.Sender
        self.chat = ms.Chat
        self.msg = self.event.Message
        self.is_group = ms.IsGroup
        self.is_me = ms.IsFromMe
        self.is_edited = self.event.IsEdit
        self.is_view_once = self.event.IsViewOnce
        self.text = _get_message_text(self.event) or ""
