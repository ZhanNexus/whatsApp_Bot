
import config
import strings


from nandha import client, log
from neonize.client import NewClient
from nandha.utils import messages, _get_message_text, extract_text, send_error, send_error_reply, get_user, get_uid, get_chat
from nandha.db.chatbot import add_chat, remove_chat
from neonize.events import MessageEv, ConnectedEv, event

import sys
import io
import traceback
import time
import subprocess 





@messages('/shell')
@messages('/sh')
def shell(client: NewClient, event: MessageEv):
    text = _get_message_text(event)
    code = extract_text(text)
    user_id = get_uid(event)
    start = time.time()

    if user_id not in config.devs_list:
          return send_error_reply(
client, event, "Only Dev's can access this commands!"
)

    if not code:
        send_error_reply(client, event, '🕵️ Provide code to execute... E.g: /shell ls -la')
        return

    try:
        output = subprocess.getoutput(code)
    except Exception as e:
        output = traceback.format_exc()

    taken_time = round(time.time() - start, 3)

    # Format the output
    if not output.strip():
        output = "Command executed successfully with no output! ✅"
    
    try:
        reply = f"*📥 Input:*\n```{code}```\n\n*📤 Output:*\n```{output}```\n\n*⏱️ Time Taken:* `{taken_time}`"
        client.reply_message(message=reply, quoted=event)

    except Exception as e:
        send_error_reply(client, event, str(e))




def waexec(code, client, event):
    namespace = {}
    exec(
        "def _waexec(code, client, event): "
        + "".join(f"\n {l_}" for l_ in code.split("\n")),
        namespace
    )
    return namespace["_waexec"](code, client, event)



@messages('/addai')
def AddAI(client: NewClient, event: MessageEv):
    try:
        chat_id = get_chat(event)
        if add_chat(chat_id):
            client.reply_message('*✅ AI chat [ADDED] successfully.*\n\n_AI responses are now enabled in this chat._', event)
            client.reply_message('*ℹ️ Note:* To interact with the AI, mention @nai in your messages.', event)
        else:
            send_error_reply(client, event, 'Failed to add AI chat to database.')
    except Exception as e:
        log.error(f"Error adding AI chat: {e}")
        send_error_reply(client, event, f"Failed to add AI chat: {str(e)}")

@messages('/rmai')
def RmAI(client: NewClient, event: MessageEv):
    try:
        chat_id = get_chat(event)
        if remove_chat(chat_id):
            client.reply_message('*✅ AI chat [REMOVED] successfully.*\n\n_AI responses are now disabled in this chat._', event)
        else:
            send_error_reply(client, event, 'Failed to remove AI chat from database.')
    except Exception as e:
        log.error(f"Error removing AI chat: {e}")
        send_error_reply(client, event, f"Failed to remove AI chat: {str(e)}")



@messages('@e')
@messages('/e')
def evaluate(client: NewClient, event: MessageEv):
    text = _get_message_text(event)
    code = extract_text(text)
    user_id = get_uid(event)
    start = time.time()

    if user_id not in config.devs_list:
          return send_error_reply(
client, event, "Only Dev's can access this commands!"
)


    if not code:
        send_error_reply(client, event, 'E.g /e print("hello")')
        return

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        waexec(code, client, event)
    except Exception as e:
        exc = traceback.format_exc() 

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()  

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ''

    if exc:
        evaluation = exc   
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Successfully Executed! ✅"

    output = evaluation.strip()
    taken_time = round(time.time() - start, 3)

    try:

        reply = f"*📥 Input:*\n```{code}```\n\n*📤 Output:*\n```{output}```\n\n*⏱️ Time Taken:* `{taken_time}`"
        client.reply_message(message=reply, quoted=event)

    except Exception as e:
        send_error_reply(client, event, str(e))

