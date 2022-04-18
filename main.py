import os
import hashlib
import csv

def writesha256(filepath, csvpath, header):
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        chunk = f.read(4096)
        while chunk:
            hash_sha256.update(chunk)
            chunk = f.read(4096)
    sha256 = hash_sha256.hexdigest()

    with open(csvpath, 'a',  newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(header)
        writer.writerow([filepath, sha256])

def main():
    path = 'd:\\tool\\'
    csvpath = os.path.join(path,'result.csv')
    csvheader = ['name', 'sha256']
    for filename in os.listdir(path):
        filepath = os.path.join(path,filename)
        if not os.path.exists(filepath):
            continue
        if not os.path.isfile(filepath):
            continue

        if filepath == csvpath:
            continue

        writesha256(filepath, csvpath, csvheader)
if __name__ == '__main__':
    main()
