import DESProcessor
import os
import pickle
import random
from ImageEncryptor import getKey
import SBoxGenerator

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
        result_data_sets_i = des.action('encrypt', data_sets[i])
        frequency_of_data_sets.append(countFrequency(result_data_sets_i))
    print(frequency_of_data_sets)
    print("Analyze the integrity end")

#get the difference table and return in list of list
def getDifferenceTable(one_s_box):
    input_case = getInputDifferenceCase()
    result = []
    for case in input_case:
        specific_input = getCorrespondingInput(case)
        result.append(countSpecificInput(specific_input, one_s_box))
    return result

#get all the input binary string and each case represent by a list, and return a list of list
#representing all the case
def getInputDifferenceCase():
    all_case = []
    for i in range(0, 64):
        one_case = []
        difference = '{0:06b}'.format(i)
        for ch in difference:
            one_case.append(int(ch))
        all_case.append(one_case)
    return all_case

#get the corresponding tuple of the specific input case
def getCorrespondingInput(a_input_difference_case):
    input_case = getInputDifferenceCase()
    result = []
    for case in input_case:
        corresponding_case = DESProcessor.exclusiveByBit(a_input_difference_case, case)
        result.append((case, corresponding_case))
    return result

#count the output difference of the tuple list
def countSpecificInput(specific_input, one_s_box):
    result = [0] * 16
    for input_x, input_y in specific_input:
        #mapping through the s box
        output_x = one_s_box[int(str(input_x[0]) + str(input_x[-1]), 2) * 16 + int(str(input_x[1]) + str(input_x[2])
                   + str(input_x[3]) + str(input_x[4]), 2)]
        output_y = one_s_box[int(str(input_y[0]) + str(input_y[-1]), 2) * 16 + int(str(input_y[1]) + str(input_y[2])
                   + str(input_y[3]) + str(input_y[4]), 2)]

        #turn output into binary string
        output_x_list = []
        output_y_list = []
        temp = '{0:04b}'.format(output_x)
        for ch in temp:
            output_x_list.append(int(ch))
        temp = '{0:04b}'.format(output_y)
        for ch in temp:
            output_y_list.append(int(ch))

        #count
        output_difference = DESProcessor.exclusiveByBit(output_x_list, output_y_list)
        temp = str(output_difference[0]) + str(output_difference[1]) + str(output_difference[2])  + \
               str(output_difference[3])
        result[int(temp, 2)] += 1
    return result


#get the max case in the difference table
def findMax(difference_table):
    rows = len(difference_table)
    cols = len(difference_table[0])
    max_pos = (0, 0)
    result = [max_pos]
    difference_table[0][0] = 0
    for i in range(0, rows):
        for j in range(0, cols):
            if difference_table[max_pos[0]][max_pos[1]] > difference_table[i][j] :
                continue
            elif difference_table[max_pos[0]][max_pos[1]] == difference_table[i][j]:
                if not(max_pos[0] == i and max_pos[1] == j):
                    result.append((i, j))
            else:
                max_pos = (i, j)
                temp_length = len(result)
                for i in range(0, temp_length):
                    result.pop()
                result.append(max_pos)
    return result

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

#analyze
def analyze(s_box):
    key = getKey()
    my_des = DESProcessor.DES(key, s_box)
    my_des.compute_key()
    analyzeSnowSlide(my_des)
    analyzeIntegrity(my_des)
    table = getDifferenceTable(my_des.get_s_box()[0])
    print(table)
    print(findMax(table))

#function for test
def combine():
    print("Analyze process start...")

    #using default s_box
    print("Enalyze using default S box")
    analyze('default')

    #using linear s_box
    print("Enalyze using linear s box")
    linear_s_box = SBoxGenerator.getLinearSBox()
    analyze(linear_s_box)

    #using random s_box
    print("Enalyze using random s box")
    random_s_box = SBoxGenerator.getRandomSBox()
    analyze(random_s_box)

    #using user defined s_box
    print("Enalyze using user defined s box")
    user_defined_s_box = SBoxGenerator.getUserDefinedSBox()
    analyze(user_defined_s_box)

    print("Process End!")

if __name__ == '__main__':
    combine()