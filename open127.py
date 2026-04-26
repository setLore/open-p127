import os
import hashlib
import shutil
import subprocess
import time
try:
    import customtkinter
except ImportError:
    print("customtkinter library not found. run 'pip3 install customtkinter' in your terminal")
    exit()
isBackedUp = False

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

# check if downgrade files exist
def checkDowngradeFiles():
    versions = ["1.24", "1.27", "1.29"]
    for v in versions:
        for f in files:
            if os.path.exists("open127/"):
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
    if checkVersion() == "Not Downgraded":
        for f in files:
            if os.path.exists(f"open127/upgrade/{f}") and os.path.getsize(f) == os.path.getsize(f"open127/upgrade/{f}"):
                print(f"{f} already backed up.")
            else:
                shutil.copyfile(f, f"open127/upgrade/{f}")
                print(f"backed up {f}...")
        isBackedUp = True
    else:
        return "downgraded, skipping backup"

def upgrade(): # reverts to the fal version(before downgrading)
    if checkVersion() != "Not Downgraded":
        for f in files:
                shutil.copyfile(f"open127/upgrade/{f}", f)
                print(f"reverting {f}")
    else: 
        return "already upgraded"
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")

def downgrade_to_124(): # downgrades to version 1.24
    if checkVersion() != "1.24":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.24/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")

def downgrade_to_127(): # downgrades to version 1.27

    if checkVersion() != "1.27":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.27/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")

def downgrade_to_129(): # downgrades to version 1.29

    if checkVersion() != "1.29":
        for f in files:
            shutil.copyfile(f"open127/downgrade/1.29/{f}", f)
            print(f"downgraded {f}")
    versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red", text=f"Current Version: {checkVersion()}")
    

app.title("open127")
#app.iconbitmap("")
app.geometry("600x400")
To124Button = customtkinter.CTkButton(app, text="Downgrade to 1.24", height=35, width=150, command=downgrade_to_124)
To127Button = customtkinter.CTkButton(app, text="Downgrade to 1.27", height=35, width=150, command=downgrade_to_127)
To129Button = customtkinter.CTkButton(app, text="Downgrade to 1.29", height=35, width=150, command=downgrade_to_129)
UpgradeButton = customtkinter.CTkButton(app, text="Upgrade" , height=35, width=150, command=upgrade)
versionLabel = customtkinter.CTkLabel(app, text=f"Current Version: {checkVersion()}", corner_radius=5)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure((0,1,2), weight = 1)

To124Button.grid(row=2,column=0, pady=10,padx=5, sticky="ew")
To127Button.grid(row=2,column=1, pady=10,padx=5, sticky="ew")
To129Button.grid(row=2,column=2, pady=10,padx=5, sticky="ew")
versionLabel.grid(row=0,column=0, pady=10,padx=5, sticky="ew", columnspan=4)
UpgradeButton.grid(row=2,column=3, pady=10,padx=5, sticky="ew")
versionLabel.configure(fg_color="green" if checkVersion() != "Not Downgraded" else "red")


#print(handleDir())
#backup()
#app.mainloop()
checkDowngradeFiles()
