from http.client import HTTPSConnection
from json import dumps
from time import sleep
import json, os, pystray, threading, traceback
from pystray import MenuItem as item
import tkinter as tk
from tkinter import messagebox
from PIL import Image

##-- Config Load --##
try:
    with open('config.json') as config_file:
        config_data = json.load(config_file)
except JSONDecodeError:
    messagebox.showinfo("Auto Adbot", "There was an error loading the config.json file. Please ensure it is valid JSON.")
    os._exit(5)
except Exception as e:
    messagebox.showinfo("Auto Adbot", f"There was an error loading the config.json file:\n\n{str(e)}")
    os._exit(5)

tokens = config_data['tokens']
channels = config_data['channels']
message = config_data['message']
timer = config_data['timer']
notsent = config_data['Notify_if_Message_Not_Sent']
##-- END --##

exit_flag = False

def get_connection():
    return HTTPSConnection("discordapp.com", 443)

def send_message(conn, channel_id, message_data, token):
    header_data = {
        "content-type": "application/json",
        "user-agent": "discordapp.com",
        "authorization": token,
        "host": "discordapp.com",
        "referer": "https://discord.gg/"
    }
    try:
        json_data = dumps(message_data)
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", json_data.encode(), header_data)
        conn.getresponse()
    except:
        if notsent:
            messagebox.showinfo("Auto Adbot", "Bot might have broke there was a error sending message.")
            os._exit(5)
        else:
            pass

def on_exit_clicked(icon, item):
    icon.stop()
    global exit_flag
    exit_flag = True
    os._exit(0)

def main():
    message_data = {
        "content": message,
        "tts": False,
    }
    conn = get_connection()
    for channel_id in channels:
        for token in tokens:
            if exit_flag:
                return
            send_message(conn, channel_id, message_data, token)

def tray_thread():
    tray_icon.run()

def tkinter_thread():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Auto Adbot", "The program is running in the background.\nto close it right click it in the taskbar (its the blue icon)")
    root.mainloop()

if __name__ == '__main__':
    img = Image.new('RGBA', (16, 16), (0, 0, 255, 255))
    tray_icon = pystray.Icon("Auto Ad Bot", menu=pystray.Menu(item('Exit', on_exit_clicked)), icon=img)
    tray_thread = threading.Thread(target=tray_thread)
    tray_thread.start()
    tkinter_thread = threading.Thread(target=tkinter_thread)
    tkinter_thread.start()
    while True:
        try:
            if exit_flag:
                os._exit(0)
            main()
            sleep(timer)
        except Exception as e:
            messagebox.showinfo("Auto Adbot", f"There was an error:\n\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}")
            os._exit(5)
