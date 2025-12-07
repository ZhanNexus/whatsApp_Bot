
import logging
import pkgutil
import os
import importlib
import time
import config
import strings

from nandha import client, plugins, self, log
from nandha.db.chatbot import get_all_chat

from nandha.utils import _get_message_text, is_cmd, get_user, extract_text, get_chat, is_chatbot_text, send_error_reply, clean_wa_id
from nandha.scripts import groq
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event

@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv):
        print("🎉 Bot connected successfully!")

        time.sleep(3)
        client.send_message(
                self, 
                message=strings.restarted_txt
        )

temp = {}


def chatbot(client: NewClient, event: MessageEv):

        message = _get_message_text(event)
        text = extract_text(message)

        chat_id = get_chat(event)
        user_id = get_user(event)
        name = event.Info.Pushname if event.Info.Pushname else 'Unknown'

        isBotreply = bool(event.Raw.extendedTextMessage.contextInfo.participant) and clean_wa_id(event.Raw.extendedTextMessage.contextInfo.participant) in [config.owner_guid, config.owner_uid]
        isChatBotRes = is_chatbot_text(message) or isBotreply
        if chat_id in config.chatbot_chats:
                if isChatBotRes:
                        temp.setdefault(user_id, [])
                        cov_data = temp[user_id]
                        if len(cov_data) >= config.max_cov_chats:
                                temp[user_id] = [] # cleared data

                        user_prompt = f'''
        [ Info: User name: {name} User id: {user_id} ]

        Prompt: {text}
        '''
                        temp[user_id].append({'role': 'user', 'content': user_prompt})
                        cov_data = temp[user_id]
                        res = groq(cov_data)
                        if 'error' in res:
                                send_error_reply(
                        client, 
                        event, 
                        res['error']
                        )
                        else:
                                client.reply_message(
                                        res['reply'], event
                        )
                                
@client.event(MessageEv)
def main(client: NewClient, event: MessageEv):

        message = _get_message_text(event)

        if message:
                chatbot(client, event)
                log.info(f'{get_user(event)}:' + f' 📩 Received Message: {message}')

                token = message.split(maxsplit=1)[0] if message.strip() else ''
                handler = config.HANDLER.get(token, None)
                if handler:
                        handler(client, event)

def import_plugins(package):
        package_name = package.__name__
        package_file = package.__file__

        logging.debug(f'Importing plugins from package: {package_name}')
        logging.debug(f'Package file attribute: {package_file}')

        if not hasattr(package, '__file__') or package_file is None:
                raise ValueError(f'Package {package_name} does not have a file attribute; it might be a namespace package.')

        package_dir = os.path.dirname(package_file)
        logging.debug(f'Package directory: {package_dir}')

        imported_modules = []

        for _, name, is_pkg in pkgutil.iter_modules([package_dir]):
                full_name = f'{package_name}.{name}'
                logging.debug(f'Importing module: {full_name}')
                try:
                        module = importlib.import_module(full_name)
                        imported_modules.append(module.__name__)
                except Exception as e:
                        logging.warning(f'Failed importing {full_name}: {e}')

        logging.info(f"Successfully imported {len(imported_modules)} modules: [{', '.join(m.rsplit('.', 1)[-1] for m in imported_modules)}]")


if __name__ == '__main__':

        config.chatbot_chats.extend(get_all_chat())
        log.info('✅ Chatbot chats loaded!')
        import_plugins(plugins)

        client.connect()
        try:
                event.wait()
        except KeyboardInterrupt:
                print("Interrupted by user, exiting...")
        try:
                client.disconnect()
        except Exception:
                pass

        time.sleep(0.1)