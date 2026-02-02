import requests
import json
import random
import tkinter as tk
from tkinter import messagebox
import os
import shutil
from PIL import Image, ImageTk
import PIL
from tkinter import ttk


#while True:
#    try:
#        selected_image = input()
#        if not selected_image:
#            selected_image = "img1.png"
#        original_image = Image.open(f"theme//{selected_image}")
#        break
#    except:
#          pass



selected_image = "img1.png"
original_image = Image.open(f"theme//{selected_image}")



mycolor = "#000000"  # Main color
mycolor2 = "#292929"  # Champs text color 
mycolor3 = "#FFFFFF"  #Text color

total_seconds = 7200
total_seconds2 = 9000





val = False
val2 = False
val3 = False


default_texts = {
    "guild_id": "Enter Guild ID (Exemple: 1234567891011121314)",
    "channel_id": "Enter Channel ID (Exemple: 1234567891011121314)",
    "email": "Enter Email (Exemple: MyEmail@gmail.com)",
    "password": "Enter Password (Exemple: MySecretPassword)",
    "token": "Enter Token (Exemple: MTAwNTUwMTEyMDk8MDU3NTEwNQ.GTCvcG.sEcRe0tO7ke40NIoySQgaNgPzhtba_xslhaF-na)",
    "val": False
}

data = {
    "type": 2,
    "application_id": "302050872383242240",
    "guild_id": "",
    "channel_id": "",
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
    'Authorization': "",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}


def save_settings():
    guild_id = guild_id_entry.get()
    channel_id = channel_id_entry.get()
    password = password_entry.get()
    token = token_entry.get()
    email = email_entry.get()


    settings = {
        "guild_id": guild_id,
        "channel_id": channel_id,
        "email": email,
        "password": password,
        "token": token,
        "val": False
    }


    if settings == default_texts:
        messagebox.showerror("Error", "Please fill in all required fields.")
    else:
        with open("settings.txt", "w") as file:
            json.dump(settings, file)
            print("Settings saved.")


def delete_settings():
    if os.path.exists("settings.txt"):
        rep = messagebox.askyesno("Confirmation", "All current parameters will be deleted. Continue and delete?")
        if rep:
            os.remove("settings.txt")
            print("Settings deleted.")


def load_settings():
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as file:
            settings = json.load(file)
            guild_id_entry.delete(0, tk.END)
            guild_id_entry.insert(0, settings["guild_id"])
            channel_id_entry.delete(0, tk.END)
            channel_id_entry.insert(0, settings["channel_id"])
            email_entry.delete(0, tk.END)
            email_entry.insert(0, settings["email"])
            password_entry.delete(0, tk.END)
            password_entry.insert(0, settings["password"])
            token_entry.delete(0, tk.END)
            token_entry.insert(0, settings["token"])



def start_bump():
    global bump_active
    guild_id = guild_id_entry.get()
    data["guild_id"] = guild_id
    channel_id = channel_id_entry.get()
    data["channel_id"] = channel_id
    password = password_entry.get()
    email = email_entry.get()
    token = token_entry.get()


    if not token:
        token = None
    #headers["Authorization"] = token

    if not guild_id or not channel_id or ((not password or not email) and not token):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return


    bump_active = True
    bump(guild_id, channel_id, token, password, email)

def stop_bump():
    global bump_active
    bump_active = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    bump_status_label.config(text="Status: Stopped Bump")

def bump(guild_id, channel_id, token, password, email):
    if bump_active:
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
            else:
                messagebox.showerror("Error", "Failed to log in. Check your credentials.")
                return

        response = requests.post("https://discord.com/api/v9/interactions", headers=headers, data=json.dumps(data))
        if response.status_code == 204:
            print("Successfully sent bump.")
            bump_status_label.config(text="Status: Bumping...")
            start_button.config(state=tk.DISABLED)
            stop_button.config(state=tk.NORMAL)
        elif '"code": 50035' in response.text:
            print("Please fill in the fields 'Guild ID' and 'Channel ID' correctly.")
            messagebox.showerror("Error", "Please fill in the fields 'Guild ID' and 'Channel ID' correctly.")
        elif '"code": 10004' in response.text:
            print("Guild ID not found.")
            messagebox.showerror("Error", "Guild ID not found.")
        elif '"code": 10003' in response.text:
            print("Channel ID not found.")
            messagebox.showerror("Error", "Channel ID not found.")
        else:
            print("Failed to send bump :" + response.text + " " + str(response.status_code))
            messagebox.showerror("Error", "Failed to send bump.")

        root.after(random.randint(total_seconds, total_seconds2) * 1000, bump, guild_id, channel_id, token, password, email)
    else:
        bump_status_label.config(text="Status: Stopped Bump")



bump_active = False
app_data = os.getenv("APPDATA")  # Chemin vers le dossier AppData de l'utilisateur
source_path = os.path.abspath(__file__)  # Chemin absolu du script en cours
target_path = os.path.join(app_data, "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
                       os.path.basename(source_path))









root = tk.Tk()
root.title("Discord Bump Bot")
root.geometry("515x278")
root.resizable(False, False)



background_photo = ImageTk.PhotoImage(original_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)




def clear_entry_text(event):
    widget = event.widget
    if widget.get() == default_texts[widget._name]:
        widget.delete(0, tk.END)
        widget.config(fg="white")  

def reset_entry_text(event):
    widget = event.widget
    if not widget.get():
        widget.insert(0, default_texts[widget._name])
        widget.config(fg="grey")  




def open_settings():
    global val3
    global save_settings_var
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x150")
    settings_window.resizable(False, False)
    settings_window.configure(bg=mycolor)


    def apply_settings():
        global target_path
        if add_to_startup_var.get():
            # Ajouter l'application au démarrage (pour Windows)
            if not os.path.exists(target_path):
                shutil.copyfile(source_path, target_path)
                print("Application successfully added to startup.")

        else:
            # Supprimer l'application du démarrage (pour Windows)
            app_data = os.getenv("APPDATA")
            target_path = os.path.join(app_data, "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
                                   os.path.basename(__file__))
            if os.path.exists(target_path):
                os.remove(target_path)
                print("Application removed from startup.")


        if save_settings_var.get():
            save_settings()
        else:
            delete_settings()


        if auto_start_var.get():
            if os.path.exists("settings.txt"):
                with open("settings.txt", "r") as file:
                    settings = json.load(file)
                settings["val"] = True
                with open("settings.txt", "w") as file:
                    json.dump(settings, file)





        settings_window.destroy()



    if os.path.exists(target_path):
        val = True
    else:
        val = False

    if os.path.exists("settings.txt"):
        val2 = True
        with open("settings.txt", "r") as file:
            settings = json.load(file)
            val3 = settings["val"]
    else:
        val2 = False



    add_to_startup_var = tk.BooleanVar(value=val)
    save_settings_var = tk.BooleanVar(value=val2)
    auto_start_var = tk.BooleanVar(value=val3)

    add_to_startup_checkbox = tk.Checkbutton(settings_window, text="Add to Startup", variable=add_to_startup_var, fg=mycolor3, bg=mycolor, selectcolor=mycolor)
    add_to_startup_checkbox.pack()

    save_settings_checkbox = tk.Checkbutton(settings_window, text="Save settings", variable=save_settings_var, fg=mycolor3, bg=mycolor, selectcolor=mycolor)
    save_settings_checkbox.pack()

    auto_start_checkbox = tk.Checkbutton(settings_window, text="Auto start", variable=auto_start_var, fg=mycolor3, bg=mycolor)
    auto_start_checkbox.pack()

    apply_button = tk.Button(settings_window, text="Apply", command=apply_settings, fg=mycolor3, bg=mycolor2)
    apply_button.pack()

    if save_settings_var.get():
        auto_start_checkbox.config(state="normal")
    else:
        auto_start_checkbox.config(state="disabled")



    if save_settings_var.get():
        auto_start_checkbox.config(state="normal")
    else:
        auto_start_checkbox.config(state="disabled")



#def open_theme():
    #settings_window = tk.Toplevel(root)
    #settings_window.title("Theme")
    #settings_window.geometry("300x150")
    #settings_window.resizable(False, False)    
    #settings_window.configure(bg=mycolor)

    #selected_theme = tk.StringVar(settings_window)
    
    #theme_options = ["Theme 1", "Theme 2", "Theme 3"]
    
    #theme_menu = tk.OptionMenu(settings_window, selected_theme, *theme_options)
    #theme_menu.pack()







tk.Label(root, text="", bg=mycolor, font=("arial", 5)).pack()

guild_id_label = tk.Label(root, text="Guild ID:", fg=mycolor3, bg=mycolor, anchor="center", justify="center")
guild_id_label.pack()
guild_id_entry = tk.Entry(root, name="guild_id", width=50, bg=mycolor2, fg="#808080", justify="center")
guild_id_entry.pack()
guild_id_entry.insert(0, default_texts["guild_id"])

channel_id_label = tk.Label(root, text="Channel ID:", fg=mycolor3, bg=mycolor, anchor="center", justify="center")
channel_id_label.pack()
channel_id_entry = tk.Entry(root, name="channel_id", width=50, bg=mycolor2, fg="#808080", justify="center")
channel_id_entry.pack()
channel_id_entry.insert(0, default_texts["channel_id"])

email_label = tk.Label(root, text="Email:", fg=mycolor3, bg=mycolor, anchor="center", justify="center")
email_label.pack()
email_entry = tk.Entry(root, name="email", width=50, bg=mycolor2, fg="#808080", justify="center")
email_entry.pack()
email_entry.insert(0, default_texts["email"])

password_label = tk.Label(root, text="Password:", fg=mycolor3, bg=mycolor, anchor="center", justify="center")
password_label.pack()
password_entry = tk.Entry(root, show="", name="password", width=50, bg=mycolor2, fg="#808080", justify="center")
password_entry.pack()
password_entry.insert(0, default_texts["password"])

token_label = tk.Label(root, text="Token:", fg=mycolor3, bg=mycolor)
token_label.pack()
token_entry = tk.Entry(root, name="token", width=50, bg=mycolor2, fg="#808080")
token_entry.pack()
token_entry.insert(0, default_texts["token"])

tk.Label(root, text="", bg=mycolor, font=("arial", 2)).pack()

load_settings()



# Start and Stop buttons
button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(button_frame, text="Start Bump", command=start_bump, bg=mycolor2, fg=mycolor3, anchor="center", justify="center")
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(button_frame, text="Stop Bump", command=stop_bump, state=tk.DISABLED, bg=mycolor2, fg=mycolor3, anchor="center", justify="center")
stop_button.pack(side=tk.LEFT)

settings_button = tk.Button(button_frame, text="Settings", command=open_settings, bg=mycolor2, fg=mycolor3, anchor="center", justify="center")
settings_button.pack(side=tk.LEFT)


#theme_button = tk.Button(button_frame, text="Theme", command=open_theme, bg=mycolor2, fg=mycolor3, anchor="center", justify="center")
#theme_button.pack(side=tk.LEFT)


bump_status_label = tk.Label(root, text="Status: Waiting...", bg=mycolor, fg=mycolor3, anchor="center", justify="center")
bump_status_label.pack()
bump_status_label.pack(pady=6)



# Clear entry text on click
guild_id_entry.bind("<FocusIn>", clear_entry_text)
channel_id_entry.bind("<FocusIn>", clear_entry_text)
email_entry.bind("<FocusIn>", clear_entry_text)
password_entry.bind("<FocusIn>", clear_entry_text)
token_entry.bind("<FocusIn>", clear_entry_text)

guild_id_entry.bind("<FocusOut>", reset_entry_text)
channel_id_entry.bind("<FocusOut>", reset_entry_text)
email_entry.bind("<FocusOut>", reset_entry_text)
password_entry.bind("<FocusOut>", reset_entry_text)
token_entry.bind("<FocusOut>", reset_entry_text)

if os.path.exists("settings.txt"):
    with open("settings.txt", "r") as file:
        settings = json.load(file)
        if settings["val"] == True:
            start_bump()




root.mainloop()
