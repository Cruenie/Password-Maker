from hashlib import sha256
from re import sub

from dotenv import load_dotenv # type: ignore
from os import getenv

# Search Terms (ST: ) ADD, IMPROVE

MINSIGNLEN = 10
MINKEYLEN = 3

# To skip https:// and get google.com from the URL
URLSKIPLIST = ['https:', 'http:', '']

try:
    load_dotenv()
    SIGNS = getenv('SIGNS')
    KEY = getenv('KEY')
except:
    print('.env could not be loaded. Please create a .env file in the main directory and restart the program.')
    input('Press ENTER to exit...')
    exit()
if len(SIGNS) < MINSIGNLEN:
    print(f'The SIGNS field must include {MINSIGNLEN} signs. You can use the same character, but it is not recommended.')
    input('Press ENTER to exit...')
    exit()
elif len(SIGNS) > MINSIGNLEN:
    print(f'Your SIGNS has {len(SIGNS)} characters. The last {len(SIGNS) - MINSIGNLEN} characters will not be used!')
    if input('Do you want to continue? y/n').lower() not in ['y', 'yes']:
        exit()
if len(KEY) <= 3:
    print(f'The KEY must be longer than {MINKEYLEN} characters. The longer the key, the securer the password!')
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
    # To avoid exception on bare input of 'google.com'
    # instead of 'google.com/page' or smt 
    try:
        siteParsed = url.split('/')
    except:
        siteParsed = url
        
    # find the www.webpage.co, .net .com .uk or whatever
    # I could've used siteParsed[2] probably but idk XD
    webpage = None
    for part in siteParsed:
        if('.' in part):
            webpage = part
            break

    # Hash the webpage 'www.webpage.co' with SHA256
    # and return the hash
    if webpage:
        return hashString(webpage)
    else:
        # There is a URL but no . for some reason ex: https://google
        if type(siteParsed) == list:
            for i in siteParsed:
                if i not in URLSKIPLIST:
                    return hashString(i)
        # It's just google
        if type(siteParsed) == str:
            return hashString(siteParsed)
        
        raise Exception('Man :(')

# Parse the 64 char hash into 16 strs of 4 chars
# This will be used to make passwords more complicated

# I should add options to shuffle using private key - ST: ADD
def parseHash(hash_hex):
    parsedHashList = []
    currentStr = ''
    # 4-%4?
    for i in hash_hex:
        if len(currentStr) < 4: # Magic number, ik...
            currentStr += i
        if len(currentStr) == 4:
            parsedHashList.append(currentStr)
            currentStr = ''

    return parsedHashList

# Input the URL form the user, to generate the Password
url = input('URL: ')

theHash = hashWebsite(url)

# This turns h3u7kan234kj5 to 372345
theHashNumeric = sub(r'\D', '', theHash)

# More like splitHashs
parsedHash = parseHash(theHash)

# Leave only numeric characters of KEY hash
numericKeyHash = sub(r'\D', '', hashString(KEY))

# Just to use more memory and make the program inefficient
numericKeyHashReversed = numericKeyHash[::-1]

# Get the first 2 different digits of
# numericKeyHash, and use them as
# indexes to pick the Passwords chars
# from the parsedHash list

# example: 
# parsedHash = ['a8w7', 'h42c', 'jh1k', '3hlv', '3l1b', '1vnb', 'xgt2', 's7v6', 'a8w7', 'rct1', 'cqt4', 's5b3', 'xtr6', '1hr3', '24j6', 'qh3d']
# 2 digits from numeric private key hash = [7, 4]
# passString = 'xgt23hlv'

# Yes, this renders the last indexes of parsedHash useless.
# Maybe I can add smt to include them. - ST: ADD
passString = ''
lastIndex = None
for i in numericKeyHash:
    if i is lastIndex:
        continue
    if len(passString) == 8:
        break
    passString += parsedHash[int(i)]
    lastIndex = i

# Create the Password using passString we created earlier and
# infuse the SIGNS in .env by using the hash of the URLs numeric values
finalPass = ''
for i in range(8):
    finalPass += f'{passString[i]}{SIGNS[int(theHashNumeric[i])]}'

# Create another hash to override a few characters of the Password
rkeyInfusedUrl = (numericKeyHashReversed + url)
rkeyInfusedUrlHash = hashString(rkeyInfusedUrl)

# Replace hardcoded indexes like a monkey - ST: IMPORVE
replacementStr = list(finalPass)
replacementStr[6], replacementStr[14] = rkeyInfusedUrlHash[12], rkeyInfusedUrlHash[28] 
finalPass = ''.join(replacementStr)

print(finalPass)
print('')
