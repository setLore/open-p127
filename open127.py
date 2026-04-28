import os
import hashlib
import shutil
import subprocess
import time
import threading
try:
    import customtkinter
except ImportError:
    print("customtkinter library not found. run 'pip3 install customtkinter' in your terminal")
    exit()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()

# downgrade/upgrade file list
files = [
    'GTA5.exe',
    'PlayGTAV.exe',
    'update/update.rpf',
    'bink2w64.dll',
    'socialclub.dll',
    'GFSDK_ShadowLib.win64.dll',
    'launc.dll',
    'orig_socialclub.dll',
    'ROSCrypto.dll',
    'x64a.rpf'
]

# sizes of GTA5.exe
size124 = 51248008
size127 = 55559560
size129 = 54944648

sizes = {
    "1.24": {
        "GTA5.exe": 51248008,
        "update.rpf": 397256704
    },
    "1.27": {
        "GTA5.exe": 55559560,
        "update.rpf": 352569344
    },
    "1.29": {
        "GTA5.exe": 54944648,
        "update.rpf": 397256704
    }

}

# check if downgrade files exist
def checkDowngradeFiles():
    versions = ["1.24", "1.27", "1.29"]
    for v in versions:
        for f in files:
            if os.path.exists(f"open127/downgrade/{v}/{f}"):
                pass
            else:
                print(f"file {f} not found?")

# check version func, returns version as string
def checkVersion():
    if os.path.getsize("GTA5.exe") == size124:
        return "1.24"
    elif os.path.getsize("GTA5.exe") == size127:
        return "1.27"
    elif os.path.getsize("GTA5.exe") == size129:
        return "1.29"
    else:
        return "Not Downgraded"

#folder handling
def handleDir():
    os.makedirs("open127/upgrade/update", exist_ok=True)
    os.makedirs("open127/downgrade/1.24/update", exist_ok=True)
    os.makedirs("open127/downgrade/1.27/update", exist_ok=True)
    os.makedirs("open127/downgrade/1.29/update", exist_ok=True)
    return "Folder initialization successful"

### BACKUPS ###

#check if backup exists and if it doesnt, back up fal non-downgraded files(kinda messy)

def backup():
    config_buttons("disabled")
    toggle_loading_bar(True)
    if checkVersion() == "Not Downgraded":
        for f in files:
            if os.path.exists(f"open127/upgrade/{f}") and os.path.getsize(f) == os.path.getsize(f"open127/upgrade/{f}"):
                #print(f"{f} already backed up.")
                pass
            else:
                print(f"backing up {f}...")
                shutil.copyfile(f, f"open127/upgrade/{f}")

    else:
        print("downgraded, skipping backup")
    print("safe to exit.")
    config_buttons("normal")
    toggle_loading_bar(False)

def upgrade(): # reverts to the original version(the one before downgrading)
    config_buttons("disabled")
    toggle_loading_bar(True)
    if checkVersion() != "Not Downgraded":
        for f in files:
                shutil.copyfile(f"open127/upgrade/{f}", f)
                print(f"reverting {f}")
    else: 
        return "already upgraded"
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    print("safe to exit.")
    config_buttons("normal")
    toggle_loading_bar(False)

def downgrade_to_124(): # downgrades to version 1.24
    config_buttons("disabled")
    toggle_loading_bar(True)
    if checkVersion() != "1.24":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.24/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    print("safe to exit.")
    config_buttons("normal")
    toggle_loading_bar(False)

def downgrade_to_127(): # downgrades to version 1.27
    config_buttons("disabled")
    toggle_loading_bar(True)
    if checkVersion() != "1.27":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.27/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    print("safe to exit.")
    config_buttons("normal")
    toggle_loading_bar(False)

def downgrade_to_129(): # downgrades to version 1.29
    config_buttons("disabled")
    toggle_loading_bar(True)
    if checkVersion() != "1.29":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.29/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    print("safe to exit.")
    config_buttons("normal")
    toggle_loading_bar(False)

def run_threaded(func):
    threading.Thread(target=func, daemon=True).start()

def config_buttons(state):
    To124Button.configure(state=state)
    To127Button.configure(state=state)
    To129Button.configure(state=state)
    UpgradeButton.configure(state=state)

def toggle_loading_bar(bool):
    global isBusy
    if bool == True:
        isBusy = True
        loadingBar.grid(row=2, sticky="ew", columnspan=5)
        loadingBar.start()
    else:
        isBusy = False
        loadingBar.grid_remove()

def on_close():
    if isBusy != True:
        app.destroy()

app.title("open127")
#app.iconbitmap("")
app.geometry("600x400")
To124Button = customtkinter.CTkButton(app, text="Downgrade to 1.24", height=35, width=150, command= lambda:run_threaded(downgrade_to_124))
To127Button = customtkinter.CTkButton(app, text="Downgrade to 1.27", height=35, width=150, command= lambda:run_threaded(downgrade_to_127))
To129Button = customtkinter.CTkButton(app, text="Downgrade to 1.29", height=35, width=150, command= lambda:run_threaded(downgrade_to_129))
UpgradeButton = customtkinter.CTkButton(app, text="Upgrade" , height=35, width=150, command=lambda:run_threaded(upgrade))
versionLabel = customtkinter.CTkLabel(app, text=f"Current Version: {checkVersion()}", corner_radius=5)
loadingBar = customtkinter.CTkProgressBar(app, mode="indeterminate", height=20)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure((0,1,2), weight = 1)

To124Button.grid(row=3,column=0, pady=10,padx=5, sticky="ew")
To127Button.grid(row=3,column=1, pady=10,padx=5, sticky="ew")
To129Button.grid(row=3,column=2, pady=10,padx=5, sticky="ew")
UpgradeButton.grid(row=3,column=3, pady=10,padx=5, sticky="ew")

versionLabel.grid(row=0,column=0, pady=10,padx=5, sticky="ew", columnspan=4)
versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red")

handleDir()
time.sleep(0.01)

run_threaded(backup)
time.sleep(0.01)

checkDowngradeFiles()

app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()