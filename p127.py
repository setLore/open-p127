import os
import hashlib
import shutil
import subprocess
#try:
#    import requests
#except ImportError:
#    print("requests library not found. run 'pip install requests' in your terminal.")
#    exit()

backed_up_update_size = int
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
sha124 = "d04e37f70bbfa7b4b202fcd9c8ae2a68b71e45f8ba95ce0c6f3cbd85169241c2"
sha127 = "7b3c0053db37eca7c6cdd0ecd268882cdd5f693f416e5a8e97fd31de66324d04"
sha129 = "35269ac593041043230e21db9e5b643e6182acbe65c0b42853ea61bf42ed199a"

#sha256 checksum func
def sha256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

# check version func, returns version as string
def checkVersion():
    if sha256_checksum('GTA5.exe') == sha124:
        return "1.24"
    elif sha256_checksum('GTA5.exe') == sha127:
        return "1.27"
    elif sha256_checksum('GTA5.exe') == sha129:
        return "1.29"
    else:
        return "Not Downgraded"
checkVersion()

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
            else:
                shutil.copyfile(origin, f"p127/upgrade/{dest}")
                print(f"backed up {origin}...")
    else:
        print("already downgraded, skipping backup")
        pass

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

menu()


