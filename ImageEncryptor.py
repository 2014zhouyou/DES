import PictureHelper
import DESProcessor
import random
import pickle
import os

#use the ecb model to encrypt a picture
def des_ecb_image(type, des, image_name):
    #read and format data
    data = PictureHelper.read_picture(image_name)
    data = PictureHelper.format_data(data)

    #begin process
    result = []
    for i in range(0, len(data) - 1):
        result.append(des.action(type, data[i]))
    result.append(data[-1])

    #reshape an image
    PictureHelper.reshape(result, 'ecb' + type + image_name)

#use the cbc mode to encrypt a picture
def des_cbc_image(type, des, image_name):
    #read and format data
    data = PictureHelper.read_picture(image_name)
    data = PictureHelper.format_data(data)

    #begin process
    vector = [0] * 64
    result = []
    if type == 'encrypt':
        for i in range(0, len(data) - 1):
            data[i] = DESProcessor.exclusiveByBit(data[i], vector)
            vector = des.action(type, data[i])
            result.append(vector)
        result.append(data[-1])
    elif type == 'decrypt':
        for i in range(0, len(data) - 1):
            temp = data[i]
            data[i] = des.action(type, data[i])
            data[i] = DESProcessor.exclusiveByBit(data[i], vector)
            result.append(data[i])
            vector = temp
        result.append(data[-1])
    else:
        print("The cbc action type is invalid")

    #reshape an image
    PictureHelper.reshape(result, 'cbc' + type + image_name)

#the following two function for test
def getKey():
    if not os.path.exists("key.txt"):
        key = []
        for i in range(0, 64):
            key.append(random.randint(0, 1))
        f = open("key.txt", "w")
        pickle.dump(key, f)
        f.close()
    else:
        f = open("key.txt", "rb")
        key = pickle.load(f)
        f.close()
    return key

def combine():
    print("Image encryptor start:")
    key = getKey()
    my_des = DESProcessor.DES(key)
    my_des.compute_key()
    while True:
        command = input("Please input you command(0 for ecb mode, 1 for cbc mode, else exit):")
        command = int(command)
        if command == 0:
            print("execute ecb mode encrypt...")
            des_ecb_image('encrypt', my_des, "3.bmp")
            des_ecb_image('decrypt', my_des, 'ecbencrypt3.bmp')
        elif command == 1:
            print("execute cbc mode encrypt...")
            des_cbc_image('encrypt', my_des, "3.bmp")
            des_cbc_image('decrypt', my_des, 'cbcencrypt3.bmp')
        else:
            print("Exit encryptor !")
            break

if __name__ == '__main__':
    combine()