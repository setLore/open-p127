import os
import hashlib
import shutil
#try:
#    import requests
#except ImportError:
#    print("requests library not found. run 'pip install requests' in your terminal.")
#    exit()

reqFiles = {}
currentVer = "Not Downgraded/Unknown"
backed_up_update_size = int

# sha256 checksums for GTA5.exe
sha124 = "d04e37f70bbfa7b4b202fcd9c8ae2a68b71e45f8ba95ce0c6f3cbd85169241c2"
sha127 = "7b3c0053db37eca7c6cdd0ecd268882cdd5f693f416e5a8e97fd31de66324d04"
sha129 = "35269ac593041043230e21db9e5b643e6182acbe65c0b42853ea61bf42ed199a"
# update.rpf file sizes for the different patches
size124 = 328273920
size127 = 352569344
size129 = 397256704

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
        currentVer == "Not Downgraded/Unknown"
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
    os.makedirs("p127/downgrade/general")

### BACKUPS ###

#check if backup exists and if it doesnt, back up original non-downgraded files(kinda messy)

def backup():
    if currentVer == "Not Downgraded/Unknown":
        original_update_size = os.path.getsize("update/update.rpf")
        if os.path.exists("p127/upgrade/update/update.rpf"):
            backed_up_update_size = os.path.getsize("p127/upgrade/update/update.rpf")
        else:
            shutil.copyfile("update/update.rpf","p127/upgrade/update/update.rpf")
            print("backed up original")
            backed_up_update_size = os.path.getsize("p127/upgrade/update/update.rpf")

        if original_update_size == size124 or original_update_size == size127 or original_update_size == size129:
            pass
        elif original_update_size == backed_up_update_size:
            print("backed up update.rpf matches current update.rpf")
        elif original_update_size != backed_up_update_size:
            shutil.copyfile("update/update.rpf","p127/upgrade/update/update.rpf")
            print("backed up original")

        print("backing up socialclub.dll")
        shutil.copyfile("socialclub.dll","p127/upgrade/socialclub.dll")

        print("backing up GTA5.exe")
        shutil.copyfile("GTA5.exe", "p127/upgrade/GTA5.exe")

        print("backing up bink2w64.dll")
        shutil.copyfile("bink2w64.dll", "p127/upgrade/bink2w64.dll")

        print("backing up PlayGTAV.exe")
        shutil.copyfile("PlayGTAV.exe", "p127/upgrade/PlayGTAV.exe")
    else:
        print("already downgraded, skipping backup")
        pass

def upgrade(): # reverts to the original version(before downgrading)
    shutil.copyfile("p127/upgrade/update/update.rpf", "update.rpf")
    shutil.copyfile("p127/upgrade/PlayGTAV.exe", "PlayGTAV.exe")
    shutil.copyfile("p127/upgrade/bink2w64.dll", "bink2w64.dll")
    shutil.copyfile("p127/upgrade/socialclub.dll", "socialclub.dll")
    shutil.copyfile("p127/upgrade/PlayGTAV.exe", "GTA5.exe")

def downgrade_to_124(): # downgrades to version 1.24
    shutil.copyfile("p127/downgrade/general/PlayGTAV.exe","PlayGTAV.exe")
    shutil.copyfile("p127/downgrade/general/bink2w64.dll", "bink2w64.dll")
    shutil.copyfile("p127/downgrade/1.24/update/update.rpf", "update/update.rpf")
    shutil.copyfile("p127/downgrade/1.24/socialclub.dll", "socialclub.dll")
    shutil.copyfile("p127/downgrade/1.24/GTA5.exe", "GTA5.exe")

def downgrade_to_127(): # downgrades to version 1.27
    shutil.copyfile("p127/downgrade/general/PlayGTAV.exe","PlayGTAV.exe")
    shutil.copyfile("p127/downgrade/general/bink2w64.dll", "bink2w64.dll")
    shutil.copyfile("p127/downgrade/1.27/update/update.rpf", "update/update.rpf")
    shutil.copyfile("p127/downgrade/1.27/socialclub.dll", "socialclub.dll")
    shutil.copyfile("p127/downgrade/1.27/GTA5.exe", "GTA5.exe")

def downgrade_to_129(): # downgrades to version 1.29
    shutil.copyfile("p127/downgrade/general/PlayGTAV.exe","PlayGTAV.exe")
    shutil.copyfile("p127/downgrade/general/bink2w64.dll", "bink2w64.dll")
    shutil.copyfile("p127/downgrade/1.29/update/update.rpf", "update/update.rpf")
    shutil.copyfile("p127/downgrade/1.29/socialclub.dll", "socialclub.dll")
    shutil.copyfile("p127/downgrade/1.29/GTA5.exe", "GTA5.exe")




print(f"\nCurrent Version:{checkVersion()}")
