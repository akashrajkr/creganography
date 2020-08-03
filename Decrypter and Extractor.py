#!/usr/bin/env python
# coding: utf-8

from PIL import Image
from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import cv2
import numpy as np
from tqdm import tqdm

# constants
stegoImageFile = 'output/stego.png'
output = 'output/extracted_image.jpg'


print('Reading stego-image...')
stegoImg = cv2.imread(stegoImageFile)

if stegoImg is None:
    print('File not found.')
    exit(-1)

sList = stegoImg.flatten()
# Extraction process
# step 1 - extract hidden size
tempSize = ''
for i in range(64):
    tempSize += str(sList[i]&1)
n,m,totLen= int(tempSize[0:16],2),int(tempSize[16:32],2),int(tempSize[32:64],2)


if n > 1500 or m > 1500:
    print('Hidden image size seems too long', [n,m], 'check if the stego image is the proper one.')
    exit(-1)

print("Reading encrypted data...")

i = 64
resImg = []
bit = ''
pbar = tqdm(total=totLen*8)
while i < (totLen*8)+64:
    bit += str(sList[i]&1)
    if(len(bit) == 8):
        val = int(bit,2)
        resImg.append(val) 
        bit = ''
    pbar.update(1)
    i+=1
pbar.close()

print('Decrypting data...')
while True:
    try:
        password = input("Enter password: ")
        sha = bytes(hashlib.sha256(bytes(password.encode())).digest())
        iv = b'This is an IV456'
        cipher = AES.new(sha, AES.MODE_CBC, iv)
        dct = unpad(cipher.decrypt(bytes(resImg)), AES.block_size)
        break
    except ValueError:
        print('Entered password is wrong! unable to decrypt.')

resImgList = list(b64decode(dct))
outputImg = np.array(resImgList).reshape((n,m,3))
print('Writing output to jpg file...')
try:
    cv2.imwrite(output, outputImg)
    print('Successfully written to file '+output)
except Exception as inst: 
    print('Exception caught!')
    print(inst.with_traceback)
    print(inst.args)
