# Creganography
Using a multilevel approach, the main objective of this project is to provide high level security to sensitive digital data against steganalysis techniques, while keeping the operational time low. This objective can be achieved by encrypting and authenticating the image that has user’s sensitive data and then embedding the resultant document on to a carrier.

This program basically hides an image inside another image (carrier) using bit manipulation and AES and SHA encryption and hashing techniques.

`This code has been implemented using python and some modules like opencv and tqdm might needs to be explicitly installed before executing this code.`

Sample input and output images to run the program are provided in the repository.

### Requirements
* Image to be hidden. Eg. baby.jpg/harold.jpg
* Image that acts as a carrier. Eg. cover.jpg/cover2.jpg
* You need to provide a password (which won't be shown while typing for security purposes) for this program to encrypt and embed the image into the carrier and that same password will be later used for decryption and extraction.
* Some modules that doesn't come pre-installed with python 3 such as opencv, tqdm, numpy, PIL must be installed.

### Sample run
#### Embedding the image into cover (carrier) image
```
> python 'Encryptor and Embedder.py'
Enter file path of the file to be hidden: baby.jpg
Enter the path to cover image: cover.jpg
Reading files...
Encrypting file data...
Password:
Writing encrypted data into cover...
100%|███████████████████████████████████████████████████████████████████████| 403232/403232 [00:08<00:00, 46803.86it/s]
Writing into output file...
Successfully saved the stego image in 'output' directory.
```
#### Extracting the hidden image from the cover (carrier)/stego image
```
> python 'Decryptor and Extractor.py'
Reading stego-image...
Reading encrypted data...
100%|████████████████████████████████████████████████████████████████████| 3225856/3225856 [00:11<00:00, 277160.34it/s]
Decrypting data...
Password:
Writing output to jpg file...
Successfully written to file output/extracted_image.jpg
```
