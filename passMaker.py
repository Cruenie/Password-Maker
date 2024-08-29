from hashlib import sha256
from re import sub

from dotenv import load_dotenv
from os import getenv

try:
    load_dotenv()
    SIGNS = getenv('SIGNS')
    KEY = getenv('KEY')
except:
    print('.env could not be loaded. Please create a .env file in the main directory and restart the program.')
    input('Press ENTER to exit...')
    exit()
if len(SIGNS) < 10:
    print('The SIGNS field must include 10 signs. You can use the same character, but it is not recommended.')
    input('Press ENTER to exit...')
    exit()
if len(KEY) == 0:
    print('Please enter a key. The longer the key, the securer the password!')
    input('Press ENTER to exit...')
    exit()

# Uses SHA256 to hash a string
def hashString(text):
    hash_obj = sha256()
    hash_obj.update(text.encode())
    hash_hex = hash_obj.hexdigest()
    return hash_hex

# Turns https://www.google.com/index.html
# into www.google.com
def hashWebsite(url):
    siteParsed = url.split('/')
    webpage = None

    # find the www.webpage.co, .net .com .uk or whatever
    # I could've used siteParsed[2] probably but idk XD
    for part in siteParsed:
        if('.' in part):
            webpage = part
            break

    # Hash the webpage 'www.webpage.co' with SHA256
    # and return the hash
    if webpage:
        hash_hex = hashString(webpage)
        print(f'Returned the hash for: {webpage}')
        return hash_hex
    else:
        return False

# Parse the 64 char hash into 16 strs of 4 chars
# This will be used to make complicated passwords
def parseHash(hash_hex):
    parsedHashList = []
    currentStr = ''
    for i in hash_hex:
        if len(currentStr) < 4: # Magic number, ik...
            currentStr += i
        if len(currentStr) == 4:
            parsedHashList.append(currentStr)
            currentStr = ''

    return parsedHashList


url = input('URL: ')
theHash = hashWebsite(url)
print(theHash)
parsedHash = parseHash(theHash)
print(parsedHash)
print(len(parsedHash))
print(f'The hash for the key {KEY} is {hashString(KEY)}')

# Leave only numeric characters
numericKeyHash = sub(r'\D', '', hashString(KEY))
numericKeyHashReversed = numericKeyHash[::-1]
print(numericKeyHash)
print(numericKeyHashReversed)

passString = ''
lastIndex = None
for i in numericKeyHash:
    if i is lastIndex:
        continue
    if len(passString) == 8:
        break
    passString += parsedHash[int(i)]
    lastIndex = i

print(passString)

finalPass = ''
for i in range(8):
    finalPass += f'{passString[i]}{SIGNS[int(numericKeyHashReversed[i])]}'

print(finalPass)
print('')