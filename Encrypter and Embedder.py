#!/usr/bin/env python
# coding: utf-8

from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import cv2
import numpy as np
from tqdm import tqdm
from getpass import getpass
import os

# constants
hiddenImageFile = input('Enter file path of the file to be hidden: ')
coverImageFile = input('Enter the path to cover image: ')
output = 'output/stego.png'

print('Reading files...')

# Hidden image
img = cv2.imread(hiddenImageFile)
if img is None:
    print('File to be hidden not found in the path given directory.')
    exit(-1)
# Cover image
cimg = cv2.imread(coverImageFile)
if cimg is None:
    print('Cover image file is not found in the given directory.')
    exit(-1)

cn, cm, cch = cimg.shape
flattenedCList = np.ndarray.flatten(cimg)

n,m,ch = img.shape
binaryImageSize = '{0:016b}'.format(n)+'{0:016b}'.format(m)

print('Encrypting file data...')
flattenedList = np.ndarray.flatten(img)
data = b64encode(bytes(flattenedList))

password = getpass()
sha = bytes(hashlib.sha256(bytes(password.encode())).digest())
iv = b'This is an IV456'
try:
    cipher = AES.new(sha,AES.MODE_CBC,iv)
    ct = cipher.encrypt(pad(data, AES.block_size))
except ValueError:
    print('Value error exception! Unable to encrypt.')
encryptedList = list(ct)

# cipher2 = AES.new(sha, AES.MODE_CBC, iv)
# dct = unpad(cipher2.decrypt(ct), AES.block_size)
# dList = list(b64decode(dct))

print('Writing encrypted data into cover...')
# storing sizes
i = 0
binaryImageSize += '{0:032b}'.format(len(encryptedList))
for bit in binaryImageSize:
    if (int(bit) == 1):
        flattenedCList[i] |= 1
    else:
        flattenedCList[i] &= ~(1 << 0) 
    i += 1

i = 64 # restoring (redundant though)
j = 0
pbar = tqdm(total=len(encryptedList))
while i < len(flattenedCList):
    if j >= len(encryptedList):
        break
    byteStr = '{0:08b}'.format(encryptedList[j])
    for bit in byteStr:
        if int(bit) == 1:
            flattenedCList[i] = flattenedCList[i] | 1
        else:
            flattenedCList[i] &= ~(1 << 0)
        i += 1
    pbar.update(1)
    j += 1
pbar.close()

print('Writing into output file...')
# reshaping and saving
CList = flattenedCList.reshape(cimg.shape)
try:    
    if not os.path.exists('output'):
        try:
            os.mkdir('output')
        except OSError as error:
            print(error)
            exit(-1)
    cv2.imwrite(output,CList)
    print('Successfully saved the stego image in \'output\' directory.')
except:
    print('Writing operation failed!')
    exit(-1)