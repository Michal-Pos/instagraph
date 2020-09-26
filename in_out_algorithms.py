import pandas as pd
import os
from collections import Counter

edges_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\edges\\'
whl_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\whl_folder\\'


# creating test data set

def test_dataset_in(list):
    in_list = []
    for item in list:
        if os.path.exists(edges_path + item + '_edges.csv'):

            df = pd.read_csv(edges_path + item + '_edges.csv')
            in_list += df['Target'].to_list()
        else:
            print(item, 'does not exists in database')
    return in_list


def test_dataset_out(list):
    out_list = []
    for item in list:
        if os.path.exists(edges_path + item + '_edges.csv'):

            df = pd.read_csv(edges_path + item + '_edges.csv')
            out_list += df['Source'].to_list()
        else:
            print(item, 'does not exists in database')

    return out_list


def test_dataset_in_out(list):
    in_list = []
    out_list = []
    for item in list:
        df = pd.read_csv(edges_path + item + '_edges.csv')

        out_list += df['Source'].to_list()
        in_list += df['Target'].to_list()

    return out_list + in_list


# test_dataset(['mikeshehad', 'nawrocenie', '_kubawilk_', '_wervel_', 'zyciezaleczka', 'iguanadeszczyk'])


# calculating In and Out Degrees of nodes with respect to two arguments
class Degrees:
    # def counting_out(list, x, y):
    #     if y=='max':
    #         print('nice')
    #         y=len(list)
    #     list.sort()
    #     print(list)
    #     print('OUT LIST')
    #
    #     for i in range(0, len(list)):
    #         if i + 2 > len(list):
    #             break
    #         elif list[i + 1] != list[i] and list.count(list[i]) in range(x, y):
    #             print(list[i], list.count(list[i]))
    #
    # def counting_in(list, x, y):
    #     if y=='max':
    #         print('nice')
    #         y=len(list)
    #
    #     list.sort()
    #     print(list)
    #     print('IN LIST')
    #     for i in range(0, len(list)):
    #         if i + 2 > len(list):
    #             break
    #         elif list[i + 1] != list[i] and list.count(list[i]) in range(x, y):
    #             print(list[i], list.count(list[i]))
    def counting_in(list):
        in_list=[]
        for item in list:
            if os.path.exists(edges_path + item + '_edges.csv'):

                df = pd.read_csv(edges_path + item + '_edges.csv')
                in_list += df['Target'].to_list()
                print(len(in_list))

                print(in_list)
            else:
                print(item, 'does not exists in database')
        print(in_list)
        print(Counter(in_list))




# Degrees.counting_out(
#     test_dataset_out(['mikeshehad', 'nawrocenie', '_kubawilk_', '_wervel_', 'zyciezaleczka', 'iguanadeszczyk','wild.mai']), 4, 'max')
# # Degrees.counting_in(
#     test_dataset_in(['mikeshehad', 'nawrocenie', '_kubawilk_', '_wervel_', 'zyciezaleczka', 'iguanadeszczyk']), 4, 5)

Degrees.counting_in(['mikeshehad', 'nawrocenie'])