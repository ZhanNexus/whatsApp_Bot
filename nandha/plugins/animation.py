import time
import config
import strings

from nandha import client, log
from neonize.client import NewClient
from nandha.utils import messages, _get_message_text, extract_text, send_error, send_error_reply
from neonize.events import MessageEv, ConnectedEv, event


__module__ = 'Animation'

__help__ = '''
🪄 *Animation Commands*:
`moon, loading, hearts, fire, rainbow, rocket, grow, weather, clock, party, stars, wave, dance, spin, bomb, sunrise, halloween, christmas, love, pizza, music, typing, earth, snake, battery, traffic, cat, trophy, hack, matrix, code, virus, anime, sakura, ninja, mecha`

*Example*: `@moon` `@fire` `@hack` `@anime`
'''


# Global animation delay
SLEEP = 3

@messages('@moon')
def moon(client: NewClient, event: MessageEv):
    """Moon phases animation"""
    ms = event.Info.MessageSource
    frames = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@loading')
def loading(client: NewClient, event: MessageEv):
    """Loading dots animation"""
    ms = event.Info.MessageSource
    frames = ['Loading', 'Loading.', 'Loading..', 'Loading...', '✅ Done!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@hearts')
def hearts(client: NewClient, event: MessageEv):
    """Growing hearts animation"""
    ms = event.Info.MessageSource
    frames = ['💗', '💗💗', '💗💗💗', '💓💓💓💓', '❤️❤️❤️❤️❤️', '💕💕💕💕💕💕']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@fire')
def fire(client: NewClient, event: MessageEv):
    """Fire animation"""
    ms = event.Info.MessageSource
    frames = ['🔥', '🔥🔥', '🔥🔥🔥', '🔥🔥🔥🔥', '🔥🔥🔥🔥🔥', '💨 Burned out!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@rainbow')
def rainbow(client: NewClient, event: MessageEv):
    """Rainbow colors animation"""
    ms = event.Info.MessageSource
    frames = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🌈✨']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@rocket')
def rocket(client: NewClient, event: MessageEv):
    """Rocket launch animation"""
    ms = event.Info.MessageSource
    frames = ['🚀', '🚀💨', '🚀💨💨', '  🚀💨', '    🚀', '      🚀✨']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@grow')
def grow(client: NewClient, event: MessageEv):
    """Plant growing animation"""
    ms = event.Info.MessageSource
    frames = ['🌱', '🌿', '🪴', '🌳', '🌳🌸', '🌳🌸🌺']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@weather')
def weather(client: NewClient, event: MessageEv):
    """Weather cycle animation"""
    ms = event.Info.MessageSource
    frames = ['☀️', '🌤️', '⛅', '🌥️', '☁️', '🌧️', '⛈️', '🌩️', '🌈']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@clock')
def clock(client: NewClient, event: MessageEv):
    """Clock animation"""
    ms = event.Info.MessageSource
    frames = ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@party')
def party(client: NewClient, event: MessageEv):
    """Party animation"""
    ms = event.Info.MessageSource
    frames = ['🎉', '🎊', '🎈', '🎁', '🎂', '🎉🎊🎈', '🎉🎊🎈🎁🎂']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@stars')
def stars(client: NewClient, event: MessageEv):
    """Twinkling stars animation"""
    ms = event.Info.MessageSource
    frames = ['✨', '⭐', '🌟', '💫', '⭐✨', '🌟✨⭐', '✨💫🌟⭐✨']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@wave')
def wave(client: NewClient, event: MessageEv):
    """Wave animation"""
    ms = event.Info.MessageSource
    frames = ['👋', '👋🌊', '🌊👋', '🌊🌊👋', '🌊🌊🌊', '🌊🌊🌊🌊']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@dance')
def dance(client: NewClient, event: MessageEv):
    """Dancing animation"""
    ms = event.Info.MessageSource
    frames = ['💃', '🕺', '💃', '🕺', '💃🕺', '🎉💃🕺🎉']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@spin')
def spin(client: NewClient, event: MessageEv):
    """Spinner animation"""
    ms = event.Info.MessageSource
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏', '✅ Complete!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@bomb')
def bomb(client: NewClient, event: MessageEv):
    """Bomb countdown animation"""
    ms = event.Info.MessageSource
    frames = ['💣 5', '💣 4', '💣 3', '💣 2', '💣 1', '💥💥💥']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@sunrise')
def sunrise(client: NewClient, event: MessageEv):
    """Sunrise animation"""
    ms = event.Info.MessageSource
    frames = ['🌃', '🌆', '🌅', '🌄', '☀️']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@halloween')
def halloween(client: NewClient, event: MessageEv):
    """Halloween animation"""
    ms = event.Info.MessageSource
    frames = ['🎃', '👻', '🦇', '🕷️', '🕸️', '🎃👻🦇', '🎃👻🦇🕷️']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@christmas')
def christmas(client: NewClient, event: MessageEv):
    """Christmas animation"""
    ms = event.Info.MessageSource
    frames = ['🎄', '🎅', '🎁', '⛄', '❄️', '🎄🎅🎁', '🎄🎅🎁⛄❄️']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@love')
def love(client: NewClient, event: MessageEv):
    """Love animation"""
    ms = event.Info.MessageSource
    frames = ['❤️', '💕', '💖', '💗', '💓', '💞', '💝', '❤️‍🔥']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@pizza')
def pizza(client: NewClient, event: MessageEv):
    """Pizza eating animation"""
    ms = event.Info.MessageSource
    frames = ['🍕🍕🍕🍕', '🍕🍕🍕', '🍕🍕', '🍕', '😋']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@music')
def music(client: NewClient, event: MessageEv):
    """Music animation"""
    ms = event.Info.MessageSource
    frames = ['🎵', '🎶', '🎵🎶', '🎸', '🎹', '🎤', '🎧', '🎵🎶🎸🎹']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@typing')
def typing(client: NewClient, event: MessageEv):
    """Typing animation"""
    ms = event.Info.MessageSource
    frames = ['T', 'Ty', 'Typ', 'Typi', 'Typin', 'Typing', 'Typing.', 'Typing..', 'Typing...']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@earth')
def earth(client: NewClient, event: MessageEv):
    """Earth rotation animation"""
    ms = event.Info.MessageSource
    frames = ['🌍', '🌎', '🌏', '🌍', '🌎', '🌏']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@snake')
def snake(client: NewClient, event: MessageEv):
    """Snake animation"""
    ms = event.Info.MessageSource
    frames = ['🐍', '🐍_', '🐍__', '🐍___', '🐍____', '🐍_____']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@battery')
def battery(client: NewClient, event: MessageEv):
    """Battery charging animation"""
    ms = event.Info.MessageSource
    frames = ['🪫', '🔋▯▯▯', '🔋▮▯▯', '🔋▮▮▯', '🔋▮▮▮', '🔋 100%']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@traffic')
def traffic(client: NewClient, event: MessageEv):
    """Traffic light animation"""
    ms = event.Info.MessageSource
    frames = ['🔴', '🔴 STOP', '🟡', '🟡 READY', '🟢', '🟢 GO!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@cat')
def cat(client: NewClient, event: MessageEv):
    """Cat animation"""
    ms = event.Info.MessageSource
    frames = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@trophy')
def trophy(client: NewClient, event: MessageEv):
    """Trophy achievement animation"""
    ms = event.Info.MessageSource
    frames = ['🏃', '🏃‍♂️💨', '🏁', '🥉', '🥈', '🥇', '🏆', '🎉🏆🎉']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@hack')
def hack(client: NewClient, event: MessageEv):
    """Hacking animation"""
    ms = event.Info.MessageSource
    frames = ['💻', '💻🔓', '💻🔓📊', '💻🔓📊⚡', '🔐→🔓', '✅ Access Granted!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@matrix')
def matrix(client: NewClient, event: MessageEv):
    """Matrix digital rain animation"""
    ms = event.Info.MessageSource
    frames = ['0️⃣', '0️⃣1️⃣', '0️⃣1️⃣0️⃣', '1️⃣0️⃣1️⃣0️⃣', '0️⃣1️⃣1️⃣0️⃣1️⃣', '🟢 Matrix Mode']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@code')
def code(client: NewClient, event: MessageEv):
    """Coding animation"""
    ms = event.Info.MessageSource
    frames = ['👨‍💻', '👨‍💻💻', '👨‍💻💻📝', '👨‍💻💻📊', '👨‍💻💻⚙️', '✅ Code Complete!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@virus')
def virus(client: NewClient, event: MessageEv):
    """Virus spread animation"""
    ms = event.Info.MessageSource
    frames = ['🦠', '🦠🦠', '🦠🦠🦠', '⚠️ Alert!', '🛡️ Protected!', '✅ Virus Eliminated!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@anime')
def anime(client: NewClient, event: MessageEv):
    """Anime character animation"""
    ms = event.Info.MessageSource
    frames = ['👤', '😊', '😍', '🤩', '✨😍✨', '🌟 Sugoi!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@sakura')
def sakura(client: NewClient, event: MessageEv):
    """Sakura cherry blossoms animation"""
    ms = event.Info.MessageSource
    frames = ['🌸', '🌸🌸', '🌸🌸🌸', '🌸🌸🌸🌸', '🌸🌸🌸🌸🌸', '🌷🌸🌷✨']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@ninja')
def ninja(client: NewClient, event: MessageEv):
    """Ninja action animation"""
    ms = event.Info.MessageSource
    frames = ['🥷', '🥷💨', '🥷⚔️', '🥷⚔️💨', '⚡🥷⚡', '🥷 Ninja Strike!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})


@messages('@mecha')
def mecha(client: NewClient, event: MessageEv):
    """Mecha robot animation"""
    ms = event.Info.MessageSource
    frames = ['🤖', '🤖⚙️', '🤖⚙️🔧', '🤖💪', '🤖💪⚡', '🤖 Mecha Activated!']
    msg = client.reply_message(frames[0], event)
    for frame in frames[1:]:
        time.sleep(SLEEP)
        client.edit_message(ms.Chat, msg.ID, {"conversation": frame})