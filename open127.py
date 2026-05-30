# TO-DO
# multi-threaded downloading of files needed to downgrade and tracking of its progress via a loading bar

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
try:
    import requests
except ImportError:
    print("requests library not found. run 'pip3 install requests' in your terminal")
    exit()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()

downloadLink = r"https://pub-a57af296c0df4b2aa06445a4064b40de.r2.dev/downgrade/"

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

sizes = {
    "1.24": {
        "GTA5.exe": 51248008,
        "update/update.rpf": 328273920
    },
    "1.27": {
        "GTA5.exe": 55559560,
        "update/update.rpf": 352569344
    },
    "1.29": {
        "GTA5.exe": 54944648,
        "update/update.rpf": 397256704
    }
}


# check if downgrade files exist
def checkDowngradeFiles():
    versions = ["1.24", "1.27", "1.29"]
    for v in versions:
        if all(os.path.exists(f"open127/downgrade/{v}/{f}") for f in files):
            if v == "1.24":
                To124Button.configure(state = "normal")
            elif v == "1.27":
                To127Button.configure(state = "normal")
            elif v == "1.29":
                To129Button.configure(state = "normal")
        else:
            if v == "1.24":
                To124Button.configure(state = "disabled")
            elif v == "1.27":
                To127Button.configure(state = "disabled")
            elif v == "1.29":
                To129Button.configure(state = "disabled")

# check version func, returns version as string
def checkVersion():
    for version, file_sizes in sizes.items():
        if all(os.path.getsize(f) == size for f, size in file_sizes.items()):
            return version
    return "Not Downgraded"

#folder handling
def handleDir():
    os.makedirs("open127/upgrade/update", exist_ok=True)
    os.makedirs("open127/downgrade/1.24/update", exist_ok=True)
    os.makedirs("open127/downgrade/1.27/update", exist_ok=True)
    os.makedirs("open127/downgrade/1.29/update", exist_ok=True)
    return "Folder initialization successful"

def handleScemuCfg(preorderbonus='False', ign='Player', wintitle='Grand Theft Auto V', returningplayerbonus='False', stutterfix='True', audiofix='True', crashfix='True', admin='False'):
    savepath = ""

    if os.path.exists("scemu.cfg"):
        with open("scemu.cfg", "r") as f:
            for line in f:
                if line.startswith("SavePath:"):
                    savepath = line.strip()
    with open("scemu.cfg", "w") as f:
        f.write(f'PreOrderBonus: "{preorderbonus}"\n')
        f.write(f'InGameName: "{ign}"\n')
        f.write(f'{savepath}\n')
        f.write(f'WindowTitleTomfoolery: "{wintitle}"\n')
        f.write(f'ReturningPlayerBonus: "{returningplayerbonus}"\n')
        f.write(f'StutterFix: "{stutterfix}"\n')
        f.write(f'AudioFix: "{audiofix}"\n')
        f.write(f'CrashFix: "{crashfix}"\n')
        f.write(f'RunGameAsAdmin: "{admin}"\n')

def readScemuCfg():
    config = {}
    with open("scemu.cfg", "r") as f:
        for line in f:
            if ":" in line and not line.startswith("#"):
                key,value = line.strip().split(": ", 1)
                config[key] = value.strip('"')
    return config

### BACKUPS ###

#check if backup exists and if it doesnt, back up fal non-downgraded files(kinda messy)

def backup():
    setUIBusy(True)
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
    setUIBusy(False)
    checkDowngradeFiles()

def upgrade(): # reverts to the original version(the one before downgrading)
    setUIBusy(True)
    if checkVersion() != "Not Downgraded":
        for f in files:
                shutil.copyfile(f"open127/upgrade/{f}", f)
                print(f"reverting {f}")
    else: 
        print("already upgraded")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    setUIBusy(False)
    checkDowngradeFiles()

def downgrade_to_124(): # downgrades to version 1.24
    setUIBusy(True)
    if checkVersion() != "1.24":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.24/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    setUIBusy(False)
    checkDowngradeFiles()

def downgrade_to_127(): # downgrades to version 1.27
    setUIBusy(True)
    if checkVersion() != "1.27":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.27/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    setUIBusy(False)
    checkDowngradeFiles()

def downgrade_to_129(): # downgrades to version 1.29
    setUIBusy(True)
    if checkVersion() != "1.29":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.29/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    setUIBusy(False)
    checkDowngradeFiles()

def run_threaded(func):
    threading.Thread(target=func, daemon=True).start()

def on_close():
    if isBusy != True:
        app.destroy()

def setUIBusy(bool):
    global isBusy
    if bool == True:
        isBusy = True
        To124Button.configure(state="disabled")
        To127Button.configure(state="disabled")
        To129Button.configure(state="disabled")
        UpgradeButton.configure(state="disabled")

        loadingBar.grid(row=3, sticky="ew", columnspan=5)
        loadingBar.start()
    else:
        isBusy = False
        To124Button.configure(state="normal")
        To127Button.configure(state="normal")
        To129Button.configure(state="normal")
        UpgradeButton.configure(state="normal")

        loadingBar.grid_remove()

def saveSettings():
    handleScemuCfg(
        preorderbonus=preorder_var.get(),
        ign=config["InGameName"],
        wintitle=config["WindowTitleTomfoolery"],
        stutterfix=config["StutterFix"],
        returningplayerbonus=returning_var.get(),
        audiofix=config["AudioFix"],
        crashfix=config["CrashFix"],
        admin=config["RunGameAsAdmin"]
    )

def downloadFile(ver,name):
    if not os.path.exists(f"open127/downgrade/{ver}/{name}"):
        file = open(f"open127/downgrade/{ver}/{name}", "wb")
        response = requests.get(f"{downloadLink}{ver}/{name}", stream=True)
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
        file.close()
    else:
        pass

app.title("open127")
#app.iconbitmap("")
app.geometry("600x400")

To124Button = customtkinter.CTkButton(app, text="Downgrade to 1.24", height=35, width=150, command= lambda:run_threaded(downgrade_to_124))
To127Button = customtkinter.CTkButton(app, text="Downgrade to 1.27", height=35, width=150, command= lambda:run_threaded(downgrade_to_127))
To129Button = customtkinter.CTkButton(app, text="Downgrade to 1.29", height=35, width=150, command= lambda:run_threaded(downgrade_to_129))
UpgradeButton = customtkinter.CTkButton(app, text="Upgrade" , height=35, width=150, command=lambda:run_threaded(upgrade))

config = readScemuCfg()
preorder_var = customtkinter.StringVar(value=config["PreOrderBonus"])
returning_var = customtkinter.StringVar(value=config["ReturningPlayerBonus"])

preOrderCheckbox = customtkinter.CTkCheckBox(app, text="Pre-Order Bonus", variable=preorder_var, onvalue="True", offvalue="False",command=saveSettings, width=175)
returningPlayerCheckbox = customtkinter.CTkCheckBox(app, text="Returning Player Bonus", variable=returning_var, onvalue="True", offvalue="False", command=saveSettings, width=175)

versionLabel = customtkinter.CTkLabel(app, text=f"Current Version: {checkVersion()}", corner_radius=5)

loadingBar = customtkinter.CTkProgressBar(app, mode="indeterminate", height=20)

app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=0)
app.grid_rowconfigure(3, weight=0)
app.grid_rowconfigure(4, weight=1)
#app.grid_rowconfigure()
app.grid_columnconfigure((0,1,2), weight = 1)

To124Button.grid(row=5,column=0, pady=10,padx=5, sticky="ew")
To127Button.grid(row=5,column=1, pady=10,padx=5, sticky="ew")
To129Button.grid(row=5,column=2, pady=10,padx=5, sticky="ew")
UpgradeButton.grid(row=5,column=3, pady=10,padx=5, sticky="ew")

preOrderCheckbox.grid(row=2, column=3, padx=5, pady=2, sticky="e")
returningPlayerCheckbox.grid(row=3, column=3, padx=5, pady=2, sticky="e")

versionLabel.grid(row=0,column=0, pady=10,padx=5, sticky="ew", columnspan=4)
versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red")

handleDir()
time.sleep(0.01)

run_threaded(backup)
time.sleep(0.01)

checkDowngradeFiles()

app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()