import os
import hashlib
import requests
from utils.downloader import Ldid

class Hash:
    def get_hash(filePath, url):
        m = hashlib.md5()
        if url == None:
            with open(filePath, 'rb') as fh:
                m = hashlib.md5()
                while True:
                    data = fh.read(8192)
                    if not data:
                        break
                    m.update(data)
                return m.hexdigest()
        else:
            r = requests.get(url)
            for data in r.iter_content(8192):
                m.update(data)
            return m.hexdigest()
    
class LdidHash:
    def check_linux_64():
        remote_hash = Hash.get_hash(None, Ldid.linux_64_url)
        local_hash = Hash.get_hash("ldid", None)
        
        if remote_hash == local_hash:
            return True
        else:
            return False
        
    def check_linux_arm64():
        remote_hash = Hash.get_hash(None, Ldid.linux_arm64_url)
        local_hash = Hash.get_hash("ldid", None)
        
        if remote_hash == local_hash:
            return True
        else:
            return False
        
    def check_macos_64():
        remote_hash = Hash.get_hash(None, Ldid.macos_64_url)
        local_hash = Hash.get_hash("ldid", None)
        
        if remote_hash == local_hash:
            return True
        else:
            return False
        
    def check_macos_arm64():
        remote_hash = Hash.get_hash(None, Ldid.macos_arm64_url)
        local_hash = Hash.get_hash("ldid", None)
        
        if remote_hash == local_hash:
            return True
        else:
            return False
