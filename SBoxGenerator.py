import random
#生成用户自定义的S盒算法
def getUserDefinedSBox():
    parameter_a = random.randint(1, 100)
    parameter_b = random.randint(1, 100)
    s_box = []
    for i in range(0, 8):
        s_box_part = []
        for j in range(0, 64):
            temp_num = (parameter_a * random.randint(1, 10000) + parameter_b) % 16
            s_box_part.append(temp_num)
        s_box.append(s_box_part)
    return s_box

#生成随机的S盒
def getRandomSBox():
    s_box = []
    for i in range(0, 8):
        s_box_part = []
        for j in range(0, 64):
            temp_num = random.randint(0, 15)
            s_box_part.append(temp_num)
        s_box.append(s_box_part)
    return s_box

#生成线性的s盒算法
def getLinearSBox():
    s_box = []
    for i in range(0, 8):
        num = random.randint(0, 15)
        increment = random.randint(1, 100)
        s_box.append([num] * 16 + [(num + increment) % 16] * 16 + [(num + 2 *increment) % 16] * 16 +
                     [(num + 3 * increment) % 16] * 16)
    return s_box
