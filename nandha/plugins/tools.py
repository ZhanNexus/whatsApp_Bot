import config
import strings
import requests
import json
import html

from nandha import client, log
from neonize.client import NewClient
from nandha.utils import messages, _get_message_text, extract_text, send_error_reply
from neonize.events import MessageEv, ConnectedEv, event

__module__ = 'Tools'

__help__ = '''
🛠️ *Tools Commands*:
`/myip, /ipinfo, /weather, /shorten, /qrcode, /translate, /currency, /dns, /whois, /activity, /time, /reddit, /github, /crypto, /define, /urbandict`

🧠 *Fun & Knowledge*:
`/joke, /quote, /fact, /trivia, /math, /uselessweb, /advice, /affirmation`

🎯 *Utilities*:
`/uuid, /hash, /password, /base64`
'''

@messages('/myip')
def myip(client: NewClient, event: MessageEv):
    """Get your public IP address (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        data = response.json()
        client.send_message(ms.Chat, f"🌐 *Your Public IP*\n\n`{data.get('ip', 'Unknown')}`")
    except Exception as e:
        send_error_reply(client, event, f"Failed to retrieve IP address: {str(e)}")


@messages('/ipinfo')
def ipinfo(client: NewClient, event: MessageEv):
    """Get detailed IP info"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    ip = extract_text(text).strip()

    if not ip:
        client.send_message(ms.Chat, "⚠️ *Missing IP Address*\n\nUsage: `/ipinfo <ip>`\nExample: `/ipinfo 8.8.8.8`")
        return

    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        data = response.json()
        if 'error' in data:
            send_error_reply(client, event, "Invalid IP address provided")
            return

        msg = f"""
🔍 *IP Information for {ip}*

📍 Country: {data.get('country_name', 'N/A')}
🏙️ City: {data.get('city', 'N/A')}
🌐 ISP: {data.get('org', 'N/A')}
🗺️ Region: {data.get('region', 'N/A')}
📮 Postal: {data.get('postal', 'N/A')}
🧭 Coordinates: {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}
"""
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error retrieving IP information: {str(e)}")


@messages('/weather')
def weather_info(client: NewClient, event: MessageEv):
    """Get weather"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    city = extract_text(text).strip()

    if not city:
        client.send_message(ms.Chat, "⚠️ *Missing City*\n\nUsage: `/weather <city>`\nExample: `/weather London`")
        return

    try:
        response = requests.get(f'https://wttr.in/{city}?format=j1', timeout=5)
        data = response.json()
        current = data['current_condition'][0]

        msg = f"""
🌤️ *Weather in {city}*

🌡️ Temperature: {current['temp_C']}°C (Feels like {current['FeelsLikeC']}°C)
💧 Humidity: {current['humidity']}%
🎯 Condition: {current['weatherDesc'][0]['value']}
💨 Wind: {current['windspeedKmph']} km/h
👁️ Visibility: {current['visibility']} km
"""
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Could not retrieve weather for '{city}'")


@messages('/shorten')
def shorten(client: NewClient, event: MessageEv):
    """Shorten URL"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    url = extract_text(text).strip()

    if not url:
        client.send_message(ms.Chat, "⚠️ *Missing URL*\n\nUsage: `/shorten <link>`\nExample: `/shorten https://google.com`")
        return

    try:
        response = requests.get(f'https://tinyurl.com/api-create.php?url={url}', timeout=5)
        client.send_message(ms.Chat, f"🔗 *Shortened URL*\n\n`{response.text.strip()}`")
    except Exception as e:
        send_error_reply(client, event, f"Failed to shorten URL: {str(e)}")


@messages('/qrcode')
def qrcode(client: NewClient, event: MessageEv):
    """Generate QR"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    data = extract_text(text).strip()

    if not data:
        client.send_message(ms.Chat, "⚠️ *Missing Data*\n\nUsage: `/qrcode <text>`\nExample: `/qrcode Hello World`")
        return

    try:
        qr_url = f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={data}'
        client.send_message(ms.Chat, f"📱 *QR Code Generated*\n\n{qr_url}")
    except Exception as e:
        send_error_reply(client, event, str(e))


@messages('/translate')
def translate(client: NewClient, event: MessageEv):
    """Translate text"""
    ms = event.Info.MessageSource
    raw_msg = _get_message_text(event)
    text = extract_text(raw_msg).strip()
    args = text.split('|')

    if not text or len(args) < 2:
        client.send_message(ms.Chat, "⚠️ *Usage Error*\n\nFormat: `/translate <text>|<lang>`\nExample: `/translate Hello|es`")
        return

    try:
        text_to_translate = args[0].strip()
        target_lang = args[1].strip()
        response = requests.get(f'https://api.mymemory.translated.net/get?q={text_to_translate}&langpair=en|{target_lang}', timeout=5)
        data = response.json()
        translated = data['responseData']['translatedText']
        client.send_message(ms.Chat, f"🌐 *Translated ({target_lang})*\n\n`{translated}`")
    except Exception as e:
        send_error_reply(client, event, f"Translation failed: {str(e)}")


@messages('/currency')
def currency(client: NewClient, event: MessageEv):
    """Convert currency"""
    ms = event.Info.MessageSource
    raw_msg = _get_message_text(event)
    text = extract_text(raw_msg).strip()
    args = text.split('|')

    if not text or len(args) < 3:
        client.send_message(ms.Chat, "⚠️ *Usage Error*\n\nFormat: `/currency <amount>|<from>|<to>`\nExample: `/currency 100|USD|EUR`")
        return

    try:
        amount = float(args[0].strip())
        from_curr = args[1].strip().upper()
        to_curr = args[2].strip().upper()

        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_curr}', timeout=5)
        data = response.json()
        rate = data['rates'].get(to_curr)

        if rate:
            msg = f"💱 *Currency Conversion*\n\n`{amount} {from_curr}` = `{amount * rate:.2f} {to_curr}`\n\nRate: 1 {from_curr} = {rate:.4f} {to_curr}"
            client.send_message(ms.Chat, msg)
        else:
            send_error_reply(client, event, f"Unknown currency code: {to_curr}")
    except ValueError:
        send_error_reply(client, event, "Invalid amount provided")
    except Exception as e:
        send_error_reply(client, event, f"Conversion error: {str(e)}")


@messages('/dns')
def dns(client: NewClient, event: MessageEv):
    """DNS Lookup"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    domain = extract_text(text).strip()

    if not domain:
        client.send_message(ms.Chat, "⚠️ *Missing Domain*\n\nUsage: `/dns <domain>`\nExample: `/dns google.com`")
        return

    try:
        response = requests.get(f'https://dns.google/resolve?name={domain}', timeout=5)
        data = response.json()
        answers = data.get('Answer', [])
        if answers:
            msg = f"🔍 *DNS Records for {domain}*\n\n" + "\n".join([f"• `{a['data']}`" for a in answers[:5]])
            client.send_message(ms.Chat, msg)
        else:
            send_error_reply(client, event, "No DNS records found for this domain")
    except Exception as e:
        send_error_reply(client, event, str(e))


@messages('/whois')
def whois(client: NewClient, event: MessageEv):
    """Whois Lookup"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    domain = extract_text(text).strip()

    if not domain:
        client.send_message(ms.Chat, "⚠️ *Missing Domain*\n\nUsage: `/whois <domain>`\nExample: `/whois google.com`")
        return

    try:
        api_key = 'at_lJfQwfXl8lKJqRVnSLSLmfXa5xUqG'
        response = requests.get(f'https://api.whoisxmlapi.com/v1?apiKey={api_key}&domain={domain}', timeout=5)
        data = response.json()
        r = data.get('WhoisRecord', {})

        if not r:
            send_error_reply(client, event, "No WHOIS data found for this domain")
            return

        msg = f"""
📋 *WHOIS Information: {domain}*

🏢 Organization: {r.get('registrant', {}).get('organization', 'N/A')}
📅 Created: {r.get('createdDate', 'N/A')}
⏰ Expires: {r.get('expiresDate', 'N/A')}
🔄 Updated: {r.get('updatedDate', 'N/A')}
"""
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, str(e))


@messages('/joke')
def get_joke(client: NewClient, event: MessageEv):
    """Get a random joke (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart', timeout=5)
        data = response.json()

        if data.get('error'):
            send_error_reply(client, event, "Failed to fetch joke")
            return

        setup = data.get('setup')
        delivery = data.get('delivery')

        msg = f"😂 *Joke Time*\n\n{setup}\n\n... {delivery}"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching joke: {str(e)}")


@messages('/quote')
def get_quote(client: NewClient, event: MessageEv):
    """Get a random inspirational quote (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://zenquotes.io/api/random', timeout=5)
        data = response.json()[0]
        
        quote = html.unescape(data['q']) 
        author = html.unescape(data['a'])

        msg = f"💬 *Quote of the Moment*\n\n_{quote}_\n\n— *{author}*"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching quote: {str(e)}")


@messages('/fact')
def get_fact(client: NewClient, event: MessageEv):
    """Get a random fun fact (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en', timeout=5)
        data = response.json()
        
        fact = data.get('text')
        
        msg = f"💡 *Fun Fact*\n\n{fact}"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching fact: {str(e)}")


@messages('/activity')
def bored_activity(client: NewClient, event: MessageEv):
    """Suggest an activity if you're bored (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://www.boredapi.com/api/activity/', timeout=5)
        data = response.json()
        
        activity = data.get('activity')
        activity_type = data.get('type', 'unknown').capitalize()
        participants = data.get('participants', 'N/A')
        
        msg = f"🎯 *Bored? Try This*\n\n**Activity:** {activity}\n**Type:** {activity_type}\n**Participants:** {participants}"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching activity: {str(e)}")


@messages('/trivia')
def get_trivia(client: NewClient, event: MessageEv):
    """Get a random trivia question (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://opentdb.com/api.php?amount=1&type=multiple', timeout=5)
        data = response.json()
        
        if data['response_code'] != 0:
            send_error_reply(client, event, "Failed to fetch trivia question")
            return
        
        question_data = data['results'][0]
        question = html.unescape(question_data['question'])
        correct = html.unescape(question_data['correct_answer'])
        category = html.unescape(question_data['category'])
        difficulty = question_data['difficulty'].capitalize()
        
        msg = f"🧠 *Trivia Time*\n\n**Category:** {category}\n**Difficulty:** {difficulty}\n\n**Question:** {question}\n\n_Answer will be revealed in the next message..._"
        client.send_message(ms.Chat, msg)
        
        import time
        time.sleep(2)
        client.send_message(ms.Chat, f"✅ *Answer:* {correct}")
        
    except Exception as e:
        send_error_reply(client, event, f"Error fetching trivia: {str(e)}")


@messages('/math')
def calculate_math(client: NewClient, event: MessageEv):
    """Evaluate a mathematical expression"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    expression = extract_text(text).strip()

    if not expression:
        client.send_message(ms.Chat, "⚠️ *Missing Expression*\n\nUsage: `/math <expression>`\nExample: `/math 2+2*3`")
        return

    try:
        response = requests.get(f'https://api.mathjs.org/v4/?expr={expression}', timeout=5)
        result = response.text.strip()
        
        msg = f"🔢 *Math Result*\n\n`{expression}` = `{result}`"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, "Invalid mathematical expression")


@messages('/time')
def world_time(client: NewClient, event: MessageEv):
    """Get current time in a timezone"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    timezone = extract_text(text).strip()

    if not timezone:
        client.send_message(ms.Chat, "⚠️ *Missing Timezone*\n\nUsage: `/time <timezone>`\nExample: `/time America/New_York`")
        return

    try:
        response = requests.get(f'http://worldtimeapi.org/api/timezone/{timezone}', timeout=5)
        data = response.json()
        
        if 'error' in data:
            send_error_reply(client, event, "Invalid timezone provided")
            return
        
        datetime_str = data['datetime']
        timezone_name = data['timezone']
        
        msg = f"🕐 *Current Time*\n\n**Timezone:** {timezone_name}\n**Time:** {datetime_str[:19]}"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching time: {str(e)}")


@messages('/reddit')
def reddit_post(client: NewClient, event: MessageEv):
    """Get a random post from a subreddit"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    subreddit = extract_text(text).strip() or 'showerthoughts'

    try:
        response = requests.get(f'https://www.reddit.com/r/{subreddit}/random.json', 
                              headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        data = response.json()
        
        post = data[0]['data']['children'][0]['data']
        title = post['title']
        author = post['author']
        score = post['score']
        
        msg = f"🔴 *Reddit Post from r/{subreddit}*\n\n**{title}**\n\n👤 u/{author} | ⬆️ {score}"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Could not fetch post from r/{subreddit}")


@messages('/github')
def github_user(client: NewClient, event: MessageEv):
    """Get GitHub user information"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    username = extract_text(text).strip()

    if not username:
        client.send_message(ms.Chat, "⚠️ *Missing Username*\n\nUsage: `/github <username>`\nExample: `/github torvalds`")
        return

    try:
        response = requests.get(f'https://api.github.com/users/{username}', timeout=5)
        data = response.json()
        
        if 'message' in data:
            send_error_reply(client, event, "GitHub user not found")
            return
        
        msg = f"""
🐙 *GitHub Profile*

👤 **{data['name'] or data['login']}**
📝 Bio: {data['bio'] or 'N/A'}
📍 Location: {data['location'] or 'N/A'}
📦 Public Repos: {data['public_repos']}
👥 Followers: {data['followers']}
🔗 {data['html_url']}
"""
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching GitHub data: {str(e)}")


@messages('/crypto')
def crypto_price(client: NewClient, event: MessageEv):
    """Get cryptocurrency price"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    crypto = extract_text(text).strip().lower() or 'bitcoin'

    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd&include_24hr_change=true', timeout=5)
        data = response.json()
        
        if crypto not in data:
            send_error_reply(client, event, f"Cryptocurrency '{crypto}' not found")
            return
        
        price = data[crypto]['usd']
        change = data[crypto].get('usd_24h_change', 0)
        
        emoji = "📈" if change >= 0 else "📉"
        msg = f"{emoji} *{crypto.capitalize()}*\n\n💰 Price: ${price:,.2f}\n📊 24h Change: {change:.2f}%"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching crypto price: {str(e)}")


@messages('/define')
def define_word(client: NewClient, event: MessageEv):
    """Get dictionary definition"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    word = extract_text(text).strip()

    if not word:
        client.send_message(ms.Chat, "⚠️ *Missing Word*\n\nUsage: `/define <word>`\nExample: `/define serendipity`")
        return

    try:
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}', timeout=5)
        data = response.json()
        
        if isinstance(data, dict) and 'title' in data:
            send_error_reply(client, event, f"Word '{word}' not found in dictionary")
            return
        
        word_data = data[0]
        meanings = word_data['meanings'][0]
        definition = meanings['definitions'][0]['definition']
        part_of_speech = meanings['partOfSpeech']
        
        msg = f"📖 *Definition: {word}*\n\n**Part of Speech:** {part_of_speech}\n\n**Definition:** {definition}"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching definition: {str(e)}")


@messages('/urbandict')
@messages('/ud')
def urban_dictionary(client: NewClient, event: MessageEv):
    """Get Urban Dictionary definition"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    term = extract_text(text).strip()

    if not term:
        client.send_message(ms.Chat, "⚠️ *Missing Term*\n\nUsage: `/urbandict <term>`\nExample: `/urbandict yeet`")
        return

    try:
        response = requests.get(f'https://api.urbandictionary.com/v0/define?term={term}', timeout=5)
        data = response.json()
        
        if not data['list']:
            send_error_reply(client, event, f"No definition found for '{term}'")
            return
        
        definition = data['list'][0]
        meaning = definition['definition'].replace('[', '').replace(']', '')
        example = definition.get('example', 'N/A').replace('[', '').replace(']', '')
        
        msg = f"🗣️ *Urban Dictionary: {term}*\n\n**Definition:** {meaning[:300]}...\n\n**Example:** {example[:200]}"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching Urban Dictionary definition: {str(e)}")


@messages('/uselessweb')
def useless_website(client: NewClient, event: MessageEv):
    """Get a random useless website (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://api.uselessfacts.jsph.pl/api/v2/links/random', timeout=5)
        data = response.json()
        
        url = data.get('url', 'https://theuselessweb.com')
        
        msg = f"🌐 *Random Useless Website*\n\n{url}\n\n_Click at your own risk!_"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching useless website: {str(e)}")


@messages('/advice')
def get_advice(client: NewClient, event: MessageEv):
    """Get random advice (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://api.adviceslip.com/advice', timeout=5)
        data = response.json()
        
        advice = data['slip']['advice']
        
        msg = f"💭 *Random Advice*\n\n{advice}"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching advice: {str(e)}")


@messages('/affirmation')
def get_affirmation(client: NewClient, event: MessageEv):
    """Get a positive affirmation (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://www.affirmations.dev/', timeout=5)
        data = response.json()
        
        affirmation = data['affirmation']
        
        msg = f"✨ *Daily Affirmation*\n\n_{affirmation}_"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error fetching affirmation: {str(e)}")


@messages('/uuid')
def generate_uuid(client: NewClient, event: MessageEv):
    """Generate a random UUID (No args needed)"""
    ms = event.Info.MessageSource
    try:
        response = requests.get('https://www.uuidgenerator.net/api/version4', timeout=5)
        uuid = response.text.strip()
        
        msg = f"🆔 *Generated UUID*\n\n`{uuid}`"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error generating UUID: {str(e)}")


@messages('/hash')
def hash_text(client: NewClient, event: MessageEv):
    """Generate hash of text"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    data = extract_text(text).strip()

    if not data:
        client.send_message(ms.Chat, "⚠️ *Missing Text*\n\nUsage: `/hash <text>`\nExample: `/hash hello world`")
        return

    try:
        import hashlib
        md5 = hashlib.md5(data.encode()).hexdigest()
        sha256 = hashlib.sha256(data.encode()).hexdigest()
        
        msg = f"🔐 *Hash Values*\n\n**MD5:** `{md5}`\n\n**SHA256:** `{sha256[:32]}...`"
        client.send_message(ms.Chat, msg)
    except Exception as e:
        send_error_reply(client, event, f"Error generating hash: {str(e)}")


@messages('/password')
def generate_password(client: NewClient, event: MessageEv):
    """Generate a random password"""
    ms = event.Info.MessageSource
    text = _get_message_text(event)
    length_str = extract_text(text).strip() or '16'

    try:
        length = int(length_str)
        if length < 8 or length > 128:
            send_error_reply(client, event, "Password length must be between 8 and 128")
            return
        
        import random
        import string
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        
        msg = f"🔑 *Generated Password*\n\n`{password}`\n\n_Length: {length} characters_"
        client.send_message(ms.Chat, msg)
    except ValueError:
        send_error_reply(client, event, "Invalid length specified")
    except Exception as e:
        send_error_reply(client, event, f"Error generating password: {str(e)}")

