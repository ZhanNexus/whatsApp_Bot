
import config
import strings

from nandha import client, log
from neonize.client import NewClient
from nandha.utils import messages, _get_message_text, extract_text, send_error, send_error_reply
from neonize.events import MessageEv, ConnectedEv, event

__help__ = '''
*📝 Base Commands*:
`hello` - replies hello.
`/add <num1> <num2>` - adds two numbers and replies the result.
`/cmds` - replies all available cmds.
'''

__module__ = 'Base'


@messages('/cmds')
def commands(client: NewClient, event: MessageEv):

        text = "📁 *Available Commands*:\n"
        if config.MODULE:
            for key, value in config.MODULE.items():
                text += value + "\n"
            client.reply_message(text, event)
                
        else:
            client.reply_message('🤔 *No Modules Loaded!*', event)


@messages('/add')
def additon(client: NewClient, event: MessageEv):
    text = _get_message_text(event)

    if not text:
        send_error_reply(client, event,  "Usage: /add <num1> <num2>")
        return

    rest = extract_text(text)
    if not rest:
        send_error_reply(client, event,  "Usage: /add <num1> <num2>")
        return

    parts = rest.split()
    if len(parts) < 2:
        send_error_reply(client, event, "Please provide two numbers. Example: /add 5 3")
        return

    a, b = parts[0], parts[1]
    try:
        value = int(a) + int(b)
        client.reply_message(f'✨ *Addtion*: `{value}`', event)

    except Exception as e:
        send_error_reply(client, event, str(e))


@messages('hello')
def hello(client: NewClient, event: MessageEv):
    client.reply_message(
        strings.hello_txt,
        quoted=event
    )

