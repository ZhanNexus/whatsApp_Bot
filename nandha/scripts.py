

import config
import requests
import time
import random

from bs4 import BeautifulSoup

def postimg(image_buffer):
    """  uploads an image buffer to postimages.org and returns direct links. """
    try:
        timestamp = int(time.time() * 1000)
        filename = f"{timestamp}.jpg"

        data = {
            'optsize': '0',
            'expire': '0',
            'numfiles': '1',
            'upload_session': str(random.random())
        }

        # 2. Prepare Files
        files = {
            'file': (filename, image_buffer, 'image/jpeg')
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        res = requests.post('https://postimages.org/json/rr', data=data, files=files, headers=headers)
        res.raise_for_status()
        
        response_data = res.json()
        target_url = response_data['url']
        
        html_res = requests.get(target_url, headers=headers)
        html_res.raise_for_status()

        soup = BeautifulSoup(html_res.text, 'html.parser')

        direct_input = soup.select_one('#direct')
        image_link = direct_input.get('value') if direct_input else None


        return {
            'link': target_url,
            'image_link': image_link, # This is the one you specifically needed
        }

    except Exception as err:
        return {'error': str(err)}


def groq(messages: list = None, api_key: str = None):  # messages: [{'role': 'user', 'content': 'Hello!'}]
    if messages is None:
        messages = []

    if messages and messages[0].get('role') != "system":
        messages.insert(0, {"role": "system", "content": config.AI_SYS_TXT})

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages
    }

    if api_key is None:
        api_key = getattr(config, "groq_api_key", None)
    if not api_key:
        return {'error': 'missing api_key'}

    headers = {"Authorization": f"Bearer {api_key}"}
    api_url = "https://api.groq.com/openai/v1/chat/completions"

    try:
        result = requests.post(api_url, json=data, headers=headers)
        if result.status_code != 200:
            return {'error': f'{result.status_code} {result.reason}: {result.text}'}
        results = result.json()
        return {'reply': results.get("choices", [{}])[0].get("message", {}).get("content", "*🥲 Sorry, no response.*")}
    except Exception as e:
        return {'error': str(e)}