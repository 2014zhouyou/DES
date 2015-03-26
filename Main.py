import PictureHelper
import des
import random

#use the ecb model to encrypt a picture and stored into stored_name
def des_ecb_image(type, des, image_name):
    #read and format data
    data = PictureHelper.read_picture(image_name)
    data = PictureHelper.format_data(data)

    #begin process
    result = []
    for i in range(0, len(data) - 1):
        result.append(des.action(type, data[i]))
    result.append(data[-1])

    #stored result
    PictureHelper.reshape(result, type + image_name)

#the following two function for test
def generateKey():
    result = []
    for i in range(0, 64):
        result.append(random.randint(0, 1))
    return result

def test():
    input_key = generateKey()
    my_des = des.DES(input_key)
    my_des.compute_key()
    des_ecb_image('encrypt', my_des, "1.bmp")
    des_ecb_image('decrypt', my_des, 'encrypt1.bmp')


test()


