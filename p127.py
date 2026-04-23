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
#try:
#    import requests
#except ImportError:
#    print("requests library not found. run 'pip3 install requests' in your terminal.")
#    exit()

isBackedUp = False

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()

files = {
    'GTA5.exe':'GTA5.exe',
    'PlayGTAV.exe':'PlayGTAV.exe',
    'update/update.rpf':'update/update.rpf',
    'bink2w64.dll':'bink2w64.dll',
    'socialclub.dll':'socialclub.dll',
    'GFSDK_ShadowLib.win64.dll':'GFSDK_ShadowLib.win64.dll',
    'launc.dll':'launc.dll',
    'orig_socialclub.dll':'orig_socialclub.dll',
    'ROSCrypto.dll':'ROSCrypto.dll',
    'x64a.rpf':'x64a.rpf',
}

# sha256 checksums for GTA5.exe
size124 = 51248008
size127 = 55559560
size129 = 54944648

#sha256 checksum func
def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

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
if os.path.exists("p127"):
    print("p127 folder exists")
else:
    print("p127 folder not found, creating...")
    os.makedirs("p127/upgrade/update")
    os.makedirs("p127/downgrade/1.24/update")
    os.makedirs("p127/downgrade/1.27/update")
    os.makedirs("p127/downgrade/1.29/update")

### BACKUPS ###

#check if backup exists and if it doesnt, back up original non-downgraded files(kinda messy)

def backup():
    if checkVersion() == "Not Downgraded":
        for origin,dest in files.items():
            if os.path.exists(f"p127/upgrade/{dest}") and os.path.getsize(origin) == os.path.getsize(f"p127/upgrade/{dest}"):
                print(f"{origin} already backed up.")
                isBackedUp = True
            else:
                shutil.copyfile(origin, f"p127/upgrade/{dest}")
                print(f"backed up {origin}...")
                isBackedUp = True
    else:
        print("downgraded, skipping backup")
        isBackedUp = True

def upgrade(): # reverts to the original version(before downgrading)
    if checkVersion() != "Not Downgraded":
        for dest,origin in files.items():
                shutil.copyfile(f"p127/upgrade/{origin}", dest)
                print(f"reverting {origin}")
    else: 
        print("already upgraded")

def downgrade_to_124(): # downgrades to version 1.24

    if checkVersion() != "1.24":
        for dest,origin in files.items():
            shutil.copyfile(f"p127/downgrade/1.24/{origin}", dest)
            print(f"downgraded {origin}")

def downgrade_to_127(): # downgrades to version 1.27

    if checkVersion() != "1.27":
        for dest,origin in files.items():
            shutil.copyfile(f"p127/downgrade/1.27/{origin}", dest)
            print(f"downgraded {origin}")

def downgrade_to_129(): # downgrades to version 1.29

    if checkVersion() != "1.29":
        for dest,origin in files.items():
            shutil.copyfile(f"p127/downgrade/1.29/{origin}", dest)
            print(f"downgraded {origin}")

def menu():
    while True:
        if os.name == "nt":
            subprocess.run("cls", shell=True)
        else:
            subprocess.run("clear")
        backup()
        print("-----------------------------------")
        print(f"      OPEN-127 | STATUS: {checkVersion()}")
        print("-----------------------------------")
        print("1. Downgrade to 1.27")
        print("2. Downgrade to 1.24")
        print("3. Downgrade to 1.29")
        print("4. Upgrade to original")
        print("5. Exit")

        choice = input("Make your choice: ")

        if choice == '1':
            downgrade_to_127()
        elif choice == '2':
            downgrade_to_124()
        elif choice == '3':
            downgrade_to_129()
        elif choice == '4':
            upgrade()
        elif choice == '5':
            break
        else:
            print("Invalid option selected.")

#menu()

app.title("open-p127")
#app.iconbitmap("")
app.geometry("600x400")
To124Button = customtkinter.CTkButton(app, text="Downgrade to 1.24", height=35, width=150)
To127Button = customtkinter.CTkButton(app, text="Downgrade to 1.27", height=35, width=150)
To129Button = customtkinter.CTkButton(app, text="Downgrade to 1.29", height=35, width=150)
versionLabel = customtkinter.CTkLabel(app, width=50, height=20, text=f"Current Version: {checkVersion()}")
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure((0,1,2), weight = 1)

if(checkVersion() == "Not Downgraded"):
    To124Button.grid(row=2,column=0, pady=10,padx=5, sticky="ew")
    To127Button.grid(row=2,column=1, pady=10,padx=5, sticky="ew")
    To129Button.grid(row=2,column=2, pady=10,padx=5, sticky="ew")
    versionLabel.configure(fg_color="red")
    backup()
elif checkVersion() == "1.24" or checkVersion() == "1.27" or checkVersion() == "1.29":
    To124Button.grid(row=2,column=0, pady=10,padx=5, sticky="ew")
    To127Button.grid(row=2,column=1, pady=10,padx=5, sticky="ew")
    To129Button.grid(row=2,column=2, pady=10,padx=5, sticky="ew")
    versionLabel.grid(row=0,column=1, pady=10,padx=5, sticky="ew")
    versionLabel.configure(fg_color="green")
    
app.mainloop()
