import hashlib

wordlistfile = "xato-net-10-million-passwords-1000000.txt"
hash = "40c3d69c8a012e181bd63d215d61a1df44e8fe7c182da6d24f26b0fae5348010"

def find_password(wordlistfile, hash):
    with open(wordlistfile, 'r') as f:
        wordlist = f.read().splitlines()
    
    for password in wordlist:
        if hash == hashlib.sha256(password.encode("utf-8")).hexdigest():
            return password
    
    return None

if __name__ == "__main__":
    password = find_password(wordlistfile, hash)
    if password:
        print(f"Password found: {password}")
    else:
        print("Password not found.")
    
