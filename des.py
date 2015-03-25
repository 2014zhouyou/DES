#对target循环左移position位
def shift(position, target):
    result = []
    length_of_target = len(target)
    for index in range(0, len(length_of_target)):
        result.append(target[(position + index) % length_of_target])
    return result

#根据choose_table来选择key
def chooseKey(choose_table, origin_key):
    result = []
    for index in choose_table:
        result.append(origin_key[index])
    return result

#the main part of DES algorithm
class DES:
    def __init__(self):
        self.origin_key = []
        self.des_key = []
        self.halve_key_tableA = [57, 49, 41, 33, 25, 17, 9,
                                 1, 58, 50, 42, 34, 26, 18,
                                 10, 2, 59, 51, 43, 35, 27,
                                 19, 11, 3, 60, 50, 44, 36]#len of 28
        self.halve_key_tableB = [65, 55, 47, 39, 31, 23, 15,
                                 7, 62, 54, 46, 38, 30, 22,
                                 14, 6, 61, 53, 45, 37, 29,
                                 21, 13, 5, 28, 20, 12, 4]#len of 28
        self.key_shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]#len of 16
        self.final_key_table = [14, 17, 11, 24, 1, 5, 3, 28,
                                15, 6, 21, 10, 23, 19, 12, 4,
                                26, 8, 16, 7, 27, 20, 13, 2,
                                41, 52, 31, 37, 47, 55, 30, 40,
                                51, 45, 33, 48, 44, 49, 39, 56,
                                34, 53, 46, 42, 50, 36, 29, 32] #len of 48

    def get_des_key(self):
        return self.des_key

    #compute the key use to encrypt and decrypt
    #stored result in a two dimentional array
    def compute_key(self):
        #step one:halve the key
        key_partA = chooseKey(self.halve_key_tableA, self.origin_key)
        key_partB = chooseKey(self.halve_key_tableB, self.origin_key)

        for i in range(0, 16):
            #step two:shift
            key_partA = shift(self.key_shif_table[i], key_partA)
            key_partB = shift(self.key_shif_table[i], key_partB)
            combine_key_partAB = key_partA + key_partB

            #step three:select key
            final_key = chooseKey(self.final_key_table, combine_key_partAB)

            #step four:stored and iterate
            self.des_key.append(final_key)










