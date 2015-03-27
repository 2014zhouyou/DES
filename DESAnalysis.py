import DESProcessor
import os
import pickle
import random
from ImageEncryptor import getKey

#find the different number between two text and return the different number
def countDifference(source1, source2):
    count = 0
    for i in range(0, len(source1)):
        if source1[i] != source2[i]:
            count += 1
    return count

#分析des的雪崩性质
def analyzeSnowSlide(des):
    print("Analyze the snow slide start:")
    source1 = [0] * 64
    source2 = [1] + [0] * 63
    data_for_round_source1 = des.actionForStatistic('encrypt', source1)
    data_for_round_source2 = des.actionForStatistic('encrypt', source2)

    for i in range(0, 16):
        print("The differenc in the round " + str(i) + ":" +
              str(countDifference(data_for_round_source1[i],data_for_round_source2[i])))
    print("Analyze the snow slide end")

#分析des的完整性
def analyzeIntegrity(des):
    print("Analyze the integrity start")
    data_sets = constructDataSets(2**8)
    frequency_of_data_sets = []
    for i in range(0, len(data_sets)):
        frequency_of_data_sets.append(countFrequency(data_sets[i]))
    print(frequency_of_data_sets)
    print("Analyze the integrity end")

#construct data_sets
def constructDataSets(data_set_length):
    data_set = []
    first_bit = random.randint(0, 1)
    for i in range(0, data_set_length):
        temp = []
        for i in range(0, 63):
            temp.append(random.randint(0, 1))
        temp.insert(0, first_bit)
        data_set.append(temp)
    return data_set

#count the frequency of 0 and 1, return the form(0's frequency, 1's frequency)
def countFrequency(data):
    count = 0
    length = len(data)
    for i in range(0, length):
        if data[i] == 0:
            count += 1
    frequency_of_0 = float(count) / length
    return (frequency_of_0, 1 - frequency_of_0 )


#function for test
def combine():
    print("Analyze process start...")
    key = getKey()
    my_des = DESProcessor.DES(key)
    my_des.compute_key()
    analyzeSnowSlide(my_des)
    analyzeIntegrity(my_des)
    print("Analyze process end.")

if __name__ == '__main__':
    combine()