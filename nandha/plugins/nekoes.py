import config
import strings
import requests

from nandha import client, log
from neonize.client import NewClient
from nandha.utils import messages, _get_message_text, extract_text, send_error, send_error_reply
from neonize.events import MessageEv, ConnectedEv, event

__help__ = '''
*🐈 Nekos Commands*:
`@neko` - Get random neko image.
`/waifu` - Get random waifu image.
`@husbando` - Get random husbando image.
*And many more*: 
`kitsune, lurk, shoot, sleep, shrug, stare, wave, poke, smile, peck, wink, blush, smug, tickle, yeet, think, highfive, feed, bite, bored, nom, yawn, facepalm, cuddle, kick, happy, hug, baka, pat, nod, nope, kiss, dance, punch, handshake, slap, cry, pout, handhold, thumbsup, laugh`
'''

__module__ = 'Nekos'

ENDPOINT_NAMES = [
    "neko",
    "waifu",
    "husbando",
    "kitsune",
    "lurk",
    "shoot",
    "sleep",
    "shrug",
    "stare",
    "wave",
    "poke",
    "smile",
    "peck",
    "wink",
    "blush",
    "smug",
    "tickle",
    "yeet",
    "think",
    "highfive",
    "feed",
    "bite",
    "bored",
    "nom",
    "yawn",
    "facepalm",
    "cuddle",
    "kick",
    "happy",
    "hug",
    "baka",
    "pat",
    "nod",
    "nope",
    "kiss",
    "dance",
    "punch",
    "handshake",
    "slap",
    "cry",
    "pout",
    "handhold",
    "thumbsup",
    "laugh"
]

def get_neko_image(endpoint: str) -> tuple:
    """Fetch image from nekos.best API"""
    try:
        api_url = f"https://nekos.best/api/v2/{endpoint}"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('results'):
            result = data['results'][0]
            url = result.get('url')
            anime_name = result.get('anime_name', f'{endpoint.capitalize()} UWU!')
            return url, anime_name
        return None, None
    except Exception as e:
        log.error(f"Error fetching neko image: {e}")
        return None, None

def send_media(client: NewClient, event: MessageEv, chat, media_url: str, anime_name: str):
    """Send media based on file type"""
    try:
        if media_url.endswith(('.png', '.jpg', '.jpeg')):
            client.send_image(chat, file=media_url, quoted=event)
        elif media_url.endswith(('.gif', '.mp4', '.mkv')):
            client.send_sticker(chat, file=media_url, quoted=event, animated_gif=True) #is_gif=True for video like gif
        else:
            ext = media_url.split('.')[1]
            client.send_document(chat, file=media_url, filename=f'{anime_name}.{ext}', quoted=event)
    except Exception as e:
        log.error(f"Error sending media: {e}")
        raise

# Create handlers for each endpoint dynamically
def _create_neko_handler(endpoint: str):
    @messages(f'@{endpoint}')
    def neko_handler(client: NewClient, event: MessageEv):
        try:
            chat = event.Info.MessageSource.Chat
            media_url, anime_name = get_neko_image(endpoint)
            
            if not media_url:
                send_error_reply(client, event, f"Failed to fetch {endpoint} image. Try again!")
                return
            
            send_media(client, event, chat, media_url, anime_name)
            
        except Exception as e:
            log.error(f"Error in neko handler: {e}")
            send_error_reply(client, event, str(e))
    
    return neko_handler

# Register all neko handlers
for endpoint in ENDPOINT_NAMES:
    handler = _create_neko_handler(endpoint)