import pandas as pd

edges_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\edges\\'
whl_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\whl_folder\\'


# creating test data set

def test_dataset_in(list):
    in_list = []
    for item in list:
        df = pd.read_csv(edges_path + item + '_edges.csv')

        in_list += df['Target'].to_list()
    return in_list


def test_dataset_out(list):
    out_list = []
    for item in list:
        df = pd.read_csv(edges_path + item + '_edges.csv')
        out_list += df['Source'].to_list()
    return out_list


def test_dataset_in_out(list):
    in_list = []
    out_list = []
    for item in list:
        df = pd.read_csv(edges_path + item + '_edges.csv')

        out_list += df['Source'].to_list()
        in_list += df['Target'].to_list()


# test_dataset(['mikeshehad', 'nawrocenie', '_kubawilk_', '_wervel_', 'zyciezaleczka', 'iguanadeszczyk'])


# calculating In and Out Degrees of nodes with respect to two arguments
class Degrees:
    def counting_out(list, x, y):
        list.sort()
        print('OUT LIST')

        for i in range(0, len(list)):
            if i + 2 > len(list):
                break
            elif list[i + 1] != list[i] and list.count(list[i]) in range(x, y):
                print(list[i], list.count(list[i]))

    def counting_in(list, x, y):
        list.sort()
        print('IN LIST')
        for i in range(0, len(list)):
            if i + 2 > len(list):
                break
            elif list[i + 1] != list[i] and list.count(list[i]) in range(x, y):
                print(list[i], list.count(list[i]))


Degrees.counting_out(
    test_dataset_in(['mikeshehad', 'nawrocenie', '_kubawilk_', '_wervel_', 'zyciezaleczka', 'iguanadeszczyk']), 4, 5)
Degrees.counting_in(
    test_dataset_in(['mikeshehad', 'nawrocenie', '_kubawilk_', '_wervel_', 'zyciezaleczka', 'iguanadeszczyk']), 4, 5)
