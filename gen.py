import sys
import config

from neonize.client import NewClient
from neonize.events import ConnectedEv, PairStatusEv


session_name = input('Enter session name:') or  config.session_name

client = NewClient(session_name)
client.connect()
    
@client.event(PairStatusEv)
def on_paired(_: NewClient, message: PairStatusEv):
      print(f"✓ Logged in as: {message.ID.User}")
      sys.exit(0)
