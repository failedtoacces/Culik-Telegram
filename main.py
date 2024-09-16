from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError
import configparser
import os
import sys
import csv
import traceback
import time
import asyncio
import random

# Color codes for terminal output
re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

SLEEP_TIME_1 = 10  # Sleep time between requests
SLEEP_TIME_2 = 100  # Sleep time for flood errors

# Initialize the config parser
cpass = configparser.RawConfigParser()

def setup_config():
    print(gr + "[+] Installing requirements ...")
    os.system('pip3 install telethon')
    if not os.path.isfile('config.data'):
        with open('config.data', 'w') as f:
            pass
    cpass.add_section('cred')
    xid = input(gr + "[+] Enter API ID: " + re)
    cpass.set('cred', 'id', xid)
    xhash = input(gr + "[+] Enter API Hash: " + re)
    cpass.set('cred', 'hash', xhash)
    xphone = input(gr + "[+] Enter Phone Number: " + re)
    cpass.set('cred', 'phone', xphone)
    with open('config.data', 'w') as f:
        cpass.write(f)
    print(gr + "[+] Setup complete!")
    menu()

def setup_api():
    global client
    cpass.read('config.data')
    try:
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        phone = cpass['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))
        print(gr + "[+] API setup complete!")
    except KeyError:
        print(re + "[!] Run setup first !!\n")
        menu()
    menu()

def scrape_group_members():
    if 'client' not in globals():
        setup_api()
    os.system('cls' if os.name == 'nt' else 'clear')
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except:
            continue

    print(gr + '[+] Choose a group to scrape members :' + re)
    i = 0
    for g in groups:
        print(gr + '[' + cy + str(i) + '] - ' + g.title)
        i += 1

    print('')
    g_index = int(input(gr + "[+] Enter a Number: " + re))
    target_group = groups[g_index]

    print(gr + '[+] Fetching Members...')
    time.sleep(1)
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)

    print(gr + '[+] Saving In file...')
    time.sleep(1)

    with open("members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])

        for user in all_participants:
            if user.bot:
                continue
            username = user.username if user.username else ""
            first_name = user.first_name if user.first_name else ""
            last_name = user.last_name if user.last_name else ""
            name = (first_name + ' ' + last_name).strip()

            try:
                writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
            except Exception as e:
                print(re + f"[!] Error writing to file: {e}")

            time.sleep(1)  # Adjust the sleep duration as needed

    print(gr + '[+] Members scraped successfully.')
    menu()

async def add_members_to_group():
    if 'client' not in globals():
        setup_api()
    # Load users from CSV file
    users = []
    with open("members.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)  # Skip header
        for row in rows:
            user = {
                'username': row[0],
                'id': int(row[1]),
                'access_hash': int(row[2]),
                'name': row[3]
            }
            users.append(user)

    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = await client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except Exception as e:
            continue

    print(gr + 'Choose a group to add members:' + cy)
    for i, group in enumerate(groups):
        print(str(i) + '- ' + group.title)

    g_index = int(input(gr + "Enter a Number: " + re))
    target_group = groups[g_index]
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

    mode = int(input(gr + "Enter 1 to add by username or 2 to add by ID: " + cy))

    number_to_add = int(input(gr + "Enter the number of members to add: " + cy))
    
    print(gr + 'Adding members...')
    n = 0
    for user in users[:number_to_add]:
        n += 1
        if n % 80 == 0:
            await asyncio.sleep(10)  # Enforce a wait after every 80 attempts
        
        try:
            print("Checking if {} is a bot.".format(user['id']))
            user_entity = await client.get_entity(user['username'] if mode == 1 else InputPeerUser(user['id'], user['access_hash']))

            if user_entity.bot:
                print("Skipping bot: {}".format(user['username']))
                continue

            print("Adding {}".format(user['id']))

            user_to_add = (await client.get_input_entity(user['username']) if mode == 1 else InputPeerUser(user['id'], user['access_hash']))
            await client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print("User added. Waiting for a short while...")
            await asyncio.sleep(random.uniform(1, 3))  # Random sleep between 1-3 seconds

        except FloodWaitError as e:
            print(f"{re}Flood wait for {e.seconds} seconds. Waiting...")
            await asyncio.sleep(e.seconds)  # Wait for the specified amount of time
            continue  # Continue to the next user after waiting
            
        except PeerFloodError:
            print("Flood error from Telegram. Stopping. Please try again later.")
            await asyncio.sleep(SLEEP_TIME_2)
            break
            
        except UserPrivacyRestrictedError:
            print("User's privacy settings prevent adding them. Skipping...")
            await asyncio.sleep(random.uniform(1, 2))  # Short wait before next action
            
        except Exception as e:
            traceback.print_exc()
            print("Unexpected Error, skipping...")
            continue

    print(gr + 'Members added successfully!')
    menu()

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(gr + """

 _____ _   _ _     _____ _   __
/  __ \ | | | |   |_   _| | / /
| /  \/ | | | |     | | | |/ / 
| |   | | | | |     | | |    \ 
| \__/\ |_| | |_____| |_| |\  \
 \____/\___/\_____/\___/\_| \_/
                               

""" + re + "by Amar\n")
    
    print(gr + "[+] Menu:")
    print(gr + "1. Setup")
    print(gr + "2. Setup API")
    print(gr + "3. Scrape group members")
    print(gr + "4. Add member to groups")
    
    choice = input(gr + "Enter your choice: " + re)
    
    if choice == '1':
        setup_config()
    elif choice == '2':
        setup_api()
    elif choice == '3':
        scrape_group_members()
    elif choice == '4':
        asyncio.run(add_members_to_group())
    else:
        print(re + "[!] Invalid choice, please try again.")
        menu()

if __name__ == "__main__":
    menu()
