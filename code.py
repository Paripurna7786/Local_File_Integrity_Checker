import hashlib

def get_hash(filename):
    with open(filename, "rb") as f:
        data = f.read()
        return hashlib.sha256(data).hexdigest()

file = input("Enter file name: ")

hash1 = get_hash(file)
print("Original Hash:", hash1)

input("Modify the file and press Enter...")

hash2 = get_hash(file)
print("New Hash:", hash2)

if hash1 == hash2:
    print("File is NOT changed")
else:
    print("File has been MODIFIED")