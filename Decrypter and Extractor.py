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
n, m, ch = stegoImg.shape

sList = stegoImg.flatten()
# Extraction process
# step 1 - extract hidden size
tempSize = ''
for i in range(64):
    tempSize += str(sList[i]&1)
n,m,totLen= int(tempSize[0:16],2),int(tempSize[16:32],2),int(tempSize[32:64],2)


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
password = 'hackerman'
sha = bytes(hashlib.sha256(bytes(password.encode())).digest())
iv = b'This is an IV456'
cipher2 = AES.new(sha, AES.MODE_CBC, iv)
dct = unpad(cipher2.decrypt(bytes(resImg)), AES.block_size)
resImgList = list(b64decode(dct))


print('Writing output to jpg file...')
cv2.imwrite(output, np.array(resImgList).reshape((n,m,3)))