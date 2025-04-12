from paramiko.client import SSHClient, RejectPolicy  # AutoAddPolicy eliminado

def safe_connect():
    client = SSHClient()
    client.set_missing_host_key_policy(RejectPolicy)  # Política segura
    client.connect("example.com")

    # ... interacción segura con el servidor

    client.close()

import sys
import os
import tarfile

def is_within_directory(directory, target):
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    return os.path.commonpath([abs_directory]) == os.path.commonpath([abs_directory, abs_target])

def safe_extract_tar(file_path, extract_path="/tmp/unpack/"):
    with tarfile.open(file_path) as tar:
        for member in tar.getmembers():
            member_path = os.path.join(extract_path, member.name)
            if is_within_directory(extract_path, member_path):
                tar.extract(member, extract_path)  # Segura, valida antes de extraer
            else:
                print(f"Entrada peligrosa omitida: {member.name}")

if __name__ == "__main__":
    safe_extract_tar(sys.argv[1])
