import os
from pathlib import Path
from shutil import rmtree, copy, copytree
import plistlib
import requests
from urllib.parse import urlparse
import zipfile
import sys
import subprocess
import tempfile

# Functions
def copy_postinst(file_path, app_name):
    """Copy postinst file.

    Args:
        file_path (String): Path of the copy destination.
        app_name (String): Name of the app being processed.
    """
    
    # Read the file
    with open("postinst", 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("{APP_NAME}", app_name)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)
        
def copy_postrm(file_path, app_name):
    """Copy postrm file.

    Args:
        file_path (String): Path of the copy destination.
        app_name (String): Name of the app being processed.
    """
    
    # Read the file
    with open('postrm', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("{APP_NAME}", app_name)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)
        
def copy_control(file_path, app_name, app_bundle, app_version, app_min_ios, app_author):
    """Copy control file.

    Args:
        file_path (String): Path of the copy destination.
        app_name (String): Name of the app being processed.
        app_bundle (String): Bundle ID of the app being processed.
        app_version (String): Version of the app being processed.
        app_min_ios (String): Minimum iOS version required by the app being processed.
        app_author (String): Author of the app being processed.
    """
    
    # Read the file
    with open('control', 'r') as file:
        filedata = file.read()

    # Replace the target strings
    filedata = filedata.replace("{APP_NAME}", app_name)
    filedata = filedata.replace("{APP_BUNDLE}", app_bundle)
    filedata = filedata.replace("{APP_VERSION}", app_version)
    filedata = filedata.replace("{APP_MIN_IOS}", app_min_ios)
    filedata = filedata.replace("{APP_AUTHOR}", app_author)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(filedata)


def main():
    print("IPA Permasigner")
    print("Program created by Nebula | Original scripts created by zhuowei | CoreTrust bypass by Linus Henze")
    print("")
    
    # Check if script is running on macOS
    if not sys.platform == "darwin":
        print("[-] Script must be ran on macOS.")
        exit(1)
        
    # Check if dpkg is installed
    if ("dpkg not found" in subprocess.run("which dpkg".split(), capture_output=True, text=True).stdout) or (subprocess.run("which dpkg".split(), capture_output=True, text=True).stdout == ""):
        print("[-] dpkg is not installed. Install it though brew to continue.")
        exit(1)
    
    # Prompt the user if they'd like to use an external IPA or a local IPA
    option = input("[?] Would you like to use an IPA stored on the web, or on your system? [external, local] ")
    option = option.lower()
    
    with tempfile.TemporaryDirectory() as tmpfolder:
        print("[*] Created temporary directory.")
        
        # If the user's choice is external, download an IPA
        # Otherwise, copy the IPA to the temporary directory
        if option == "external":
            url = input("[?] Paste in the *direct* path to an IPA online: ")
            
            if not os.path.splitext(urlparse(url).path)[1] == ".ipa":
                print("[-] URL provided is not an IPA, make sure to provide a direct link.")
                exit(1)
            
            res = requests.get(url, stream=True)
            
            try:
                if res.status_code == 200:
                    print(f"[*] Downloading file...")
                    
                    with open(f"{tmpfolder}/app.ipa", "wb") as f:
                        f.write(res.content)
                else:
                    print(f"[-] URL provided is not reachable. Status code: {res.status_code}")
                    exit(1)
            except requests.exceptions.RequestException as err:
                print(f"[-] URL provided is not reachable. Error: {err}")
                exit(1)  
        elif option == "local":
            path = input("[?] Paste in the path to an IPA in your file system: ")
            
            if os.path.exists(path):
                copy(path, f"{tmpfolder}/app.ipa")
            else:
                print("[-] That file does not exist! Make sure you're using a direct path to the IPA file.")
                exit(1)
        else:
            print("[-] That is not a valid option!")
            exit(1)
        
        # Unzip the IPA file
        print("[*] Unzipping IPA...")
        with zipfile.ZipFile(f"{tmpfolder}/app.ipa", 'r') as f:
            os.makedirs(f"{tmpfolder}/app", exist_ok=False)
            f.extractall(f"{tmpfolder}/app")
            
        # Read data from the plist
        print("[*] Reading plist...")
        global folder, app_name, app_bundle, app_version, app_min_ios, app_author, app_executable
        
        if os.path.exists(f"{tmpfolder}/app/Payload"):
            for fname in os.listdir(path=f"{tmpfolder}/app/Payload"):
                if fname.endswith(".app"):
                    folder = fname
        else:
            print("[-] IPA is not valid!")
            exit(1)
            
        if os.path.isfile(f"{tmpfolder}/app/Payload/{folder}/Info.plist"):
            with open(f"{tmpfolder}/app/Payload/{folder}/Info.plist", 'rb') as f:
                info = plistlib.load(f)
                app_name = info["CFBundleName"]
                app_bundle = info["CFBundleIdentifier"]
                app_version = info["CFBundleShortVersionString"]
                app_min_ios = info["MinimumOSVersion"]
                app_author = app_bundle.split(".")[1]
                if info["CFBundleExecutable"]:
                    app_executable = info["CFBundleExecutable"]
                else:
                    app_executable = None
        
        # Get the deb file ready
        print("[*] Preparing deb file...")
        os.makedirs(f"{tmpfolder}/deb/Applications", exist_ok=False)
        os.makedirs(f"{tmpfolder}/deb/DEBIAN", exist_ok=False)
        copy_postrm(f"{tmpfolder}/deb/DEBIAN/postrm", app_name)
        copy_postinst(f"{tmpfolder}/deb/DEBIAN/postinst", app_name)
        copy_control(f"{tmpfolder}/deb/DEBIAN/control", app_name, app_bundle, app_version, app_min_ios, app_author)
        copytree(f"{tmpfolder}/app/Payload/{folder}", f"{tmpfolder}/deb/Applications/{folder}", dirs_exist_ok=False)
        subprocess.run(f"chmod 0755 {tmpfolder}/deb/DEBIAN/postrm".split(), stdout=subprocess.DEVNULL)
        subprocess.run(f"chmod 0755 {tmpfolder}/deb/DEBIAN/postinst".split(), stdout=subprocess.DEVNULL)
        if app_executable is not None:
            subprocess.run(f"chmod 0755 {tmpfolder}/deb/Applications/{folder}/{app_executable}".split(), stdout=subprocess.DEVNULL)
        
        # Sign the app
        print("[*] Signing app...")
        # subprocess.run("chmod +x ldid".split(), stdout=subprocess.DEVNULL)
        # subprocess.run(f"./ldid -Sapp.entitlements -Upassword -Kresign_taurine/fakeiphonecert/dev_certificate.p12 {tmpfolder}/deb/Applications/{folder}".split(), stdout=subprocess.DEVNULL)
        subprocess.run(f"security import ./dev_certificate.p12 -P password -A".split(), stdout=subprocess.DEVNULL)
        # subprocess.run(["codesign", "-s", 'Worth Doing Badly iPhone OS Application Signing', "-f", "--entitlements=app.entitlements", f"{tmpfolder}/deb/Applications/{folder}"], stdout=subprocess.DEVNULL)
        os.system(f"codesign -s 'Worth Doing Badly iPhone OS Application Signing' --force --deep --entitlements=app.entitlements {tmpfolder}/deb/Applications/{folder}")
            
        # Package the deb file
        print("[*] Packaging the deb file...")
        os.makedirs("output", exist_ok=True)
        if os.path.exists(f"output/{app_name}.deb"):
            os.remove(f"output/{app_name}.deb")
        subprocess.run(f"dpkg-deb --root-owner-group -b {tmpfolder}/deb output/{app_name}.deb".split(), stdout=subprocess.DEVNULL)
        
    # Done!!!
    print("")
    print("[*] We are finished!")
    print("[*] Copy the newly created deb from the output folder to your jailbroken iDevice and install it!")
    print("[*] The app will continue to work when rebooted to stock.")
        
if __name__ == '__main__':
    main()
