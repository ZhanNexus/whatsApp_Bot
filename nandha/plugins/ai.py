
import config
import strings

from nandha import client, log
from neonize.client import NewClient
from nandha.scripts import groq
from nandha.utils import messages, _get_message_text, extract_text, send_error, send_error_reply
from neonize.events import MessageEv, ConnectedEv, event


__module__ = 'AI'

__help__ = '''
🤖 *AI Commands*:
- `/ask or @ask <question>`: Ask any question to the AI bot.
'''

@messages('@ask')
@messages('/ask')
def ask(client: NewClient, event: MessageEv):
    text = _get_message_text(event)
    rest = extract_text(text)

    if not rest:
        send_error_reply(client, event, '🤖 Ask something e.g: /ask how are you doing?')

    try:
        msgs = [{'role': 'user', 'content': rest}]
        response: dict = groq(messages=msgs)
        if 'error' in response:
            send_error_reply(client, event, response['error'])
            return  
        answer = response['reply']
        client.reply_message(answer, event)

    except Exception as e:
        send_error_reply(client, event, str(e))    


