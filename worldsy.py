### Imports ###
import base64
import time
import tkinter
from tkinter.constants import DISABLED, NORMAL
import pypresence
import webbrowser
from itertools import cycle
import requests
import json
import os

B64_ICO = 'AAABAAEAICD/AAAAAACoCAAAFgAAACgAAAAgAAAAQAAAAAEACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM2b/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEBAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEBAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQEBAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEAAAABAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEBAQAAAAAAAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQEBAAAAAAAAAAEBAAAAAAAAAAAAAAAAAAAAAAAAAQEBAQAAAAAAAAAAAAABAQAAAAAAAAAAAAAAAAAAAAEBAQEBAAAAAAAAAAAAAAAAAQEBAAAAAAAAAAAAAAEBAQEBAQAAAAAAAAAAAAAAAAAAAAABAQEBAQEBAQEBAQEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQEBAQEBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM////+B////wH////Af///8B////wP////A////8H////gf///8D////wP///+B////wP///+B////wP///+B////wP///+B////wP///+B////gf///8A////AD///wIP//8DA///A8D//gfwH/gH/AAAD/8AAB//4AA///wA/' # b

### Setup pypresence ###
RPC: pypresence.Presence = pypresence.Presence("808882523647508481")

### Classes ###
class Worldsy(tkinter.Tk):
  VERSION: str = "1.0.0"

  def __init__(self, master=None) -> None:
    tkinter.Tk.__init__(self, master)

    # https://stackoverflow.com/questions/9929479/embed-icon-in-python-script
    # Create temporary file for the icon.
    icon_data = base64.b64decode(B64_ICO)
    temp_file = "worldsy_temp.ico"
    icon_file = open(temp_file, "wb")
    icon_file.write(icon_data)
    icon_file.close()

    self.title("worldsy")
    self.iconbitmap(temp_file)
    os.remove(temp_file)
    self.geometry("400x250")
    self.resizable(0, 0)
    #self.wm_state("iconic")

    self.lb = tkinter.Label(self, text="").pack()
    self.txt = tkinter.StringVar()
    self.debug_console = tkinter.Text(self, state=DISABLED, width=45, height=5)
    self.debug_console.pack()

    self.check_for_update()

  def debug_log(self, message: str) -> None:
    self.debug_console['state'] = NORMAL

    # Yes, the space is intentional.
    timestamp = time.strftime("%H:%M:%S ", time.gmtime())
    self.debug_console.insert("end", timestamp + message + "\n")

    self.debug_console.see("end")
    self.debug_console['state'] = DISABLED

  def check_for_update(self) -> None:
    api = requests.get(url="https://api.github.com/repos/fuwn/worldsy/releases")
    data = json.loads(api.content)
    latest_release: str = data[0]["tag_name"]

    if int(latest_release.replace('.', '')) > int(Worldsy.VERSION.replace('.', '')):
      self.debug_log("New version available! Current: " + self.VERSION +
        ", new: " + latest_release + ". To update, click on the GitHub link below" +
        " and download the newest release.")


class Utilities(object):
  def open_url(self, url: str) -> None:
    webbrowser.open_new(url)

class RPCHandler(object):
  enabled: bool = False

  def toggle(self) -> None:
    self.enabled = not self.enabled
    status_button["text"] = "Stop RPC" if self.enabled == True else "Start RPC"

    if self.enabled:
      worldsy.debug_log("Enabled RPC.")
      RPC.connect()
      worldsy.debug_log("Connected to websocket.")
      RPC.update(
        details="Exploring GroundZero",
        large_image="worldsy512x512",
        large_text="Worlds",
        small_image="fuwn",
        small_text="Created by fun#1337",
        start=time.time())
      worldsy.debug_log("Updated RPC.")
    elif not self.enabled:
      worldsy.debug_log("Disabled RPC.")
      RPC.close()
      worldsy.debug_log("Closed websocket.")

### Initialize Classes ###
utilities: Utilities = Utilities()
worldsy: Worldsy = Worldsy()
rpcHandler: RPCHandler = RPCHandler()

### GUI ###
status_button: tkinter.Button = tkinter.Button(
  worldsy, text="Start RPC", command=rpcHandler.toggle)
github_link: tkinter.Button = tkinter.Label(
  worldsy, text="GitHub", fg="blue", cursor="hand2")
author_label: tkinter.Button = tkinter.Label(
  worldsy, text="Created by fun#1337")
version_label: tkinter.Button = tkinter.Label(
  worldsy, text="Version: " + worldsy.VERSION)
debug_console: tkinter.Text = tkinter.Text()

### Pack Un-initialized GUI Components ###
tkinter.Label(worldsy, text="").pack() # Rudimentary line-break...
status_button.pack()
tkinter.Label(worldsy, text="").pack()
github_link.pack()
github_link.bind("<Button-1>",
  lambda e: utilities.open_url("https://github.com/fuwn/worldsy"))
author_label.pack()
version_label.pack()

### Main-loop ###
worldsy.mainloop()