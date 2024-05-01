import requests
import json
import random
import time




try:
    with open("config.json") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {
        "guild_id": "",
        "channel_id": "",
        "token": "",
        "password": "",
        "email": "",
        "total_seconds_min": "",
        "total_seconds_max": ""

    }
    with open("config.json", 'w') as config_file:
        json.dump(config, config_file, indent=4)
    input("Config.json file cannot be empty.")
    quit()



with open('config.json') as config_file:
    try:
        config = json.load(config_file)
        guild_id = int(config.get('guild_id'))
        channel_id = int(config.get('channel_id'))
        token = config.get('token')
        password = config.get('password')
        email = config.get('email')
        total_seconds_min = int(config.get('total_seconds_min'))
        total_seconds_max = int(config.get('total_seconds_max'))
    except:
        input("Correctly fill config.json.")
        quit()





data = {
    "type": 2,
    "application_id": "302050872383242240",
    "guild_id": guild_id,
    "channel_id": channel_id,
    "session_id": "bf8e7c1a2585bfe2ffa58e2eec2a350e",
    "data": {
        "version": "1051151064008769576",
        "id": "947088344167366698",
        "name": "bump",
        "type": 1,
        "options": [],
        "application_command": {
            "id": "947088344167366698",
            "application_id": "302050872383242240",
            "version": "1051151064008769576",
            "default_member_permissions": None,
            "type": 1,
            "nsfw": False,
            "name": "bump",
            "description": "Pushes your server to the top of all your server's tags and the front page",
            "description_localized": "Bumper ce serveur",
            "dm_permission": True,
            "contexts": None
        }
    }
}

headers = {
    'Authorization': token,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}





def bump(guild_id, channel_id, token, password, email):
    verif = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if verif.status_code == 200:
        pass
    else:
        tpayload = {"email": email, "password": password}
        theaders = {"Content-Type": "application/json"}
        r = requests.post("https://discord.com/api/v9/auth/login", headers=theaders, json=tpayload)
        if r.status_code == 200:
            token = r.json()["token"]
            headers["Authorization"] = token
            config["token"] = token
            with open("config.json", 'w') as config_file:
                json.dump(config, config_file, indent=4)
        else:
            print("Error, Failed to log in. Check your credentials.", r.status_code, r.text)
            return
    print(headers, json.dumps(data))
    response = requests.post("https://discord.com/api/v9/interactions", headers=headers, data=json.dumps(data))
    if response.status_code == 204:
        print("Successfully sent bump.")
    elif '"code": 10004' in response.text:
        print("Guild ID not found.")
    elif '"code": 10003' in response.text:
        print("Channel ID not found.")
    else:
        print("Failed to send bump :" + response.text + " " + str(response.status_code))






while True:
    bump(guild_id, channel_id, token, password, email)
    time.sleep(random.randint(total_seconds_min, total_seconds_max))
