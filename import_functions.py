import pandas as pd
import os
import instaloader
import instaloader.exceptions
import shutil

edges_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\edges\\'
whl_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\whl_folder\\'
private_accounts=r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\private_accounts.csv'
private_df = pd.read_csv(private_accounts)
private_df=pd.DataFrame(private_df)

# login and passwords section

login = 'pm49055047'
password = 'Zazuziza13'

# login = 'hlane976'
# password = 'Zazuziza15'
# login = 'martycox44'
# password = 'zazuziza13'
L = instaloader.Instaloader()


# Class that exports data from profiles
class Importing_data:

    # This can be used only to exporting data from public profiles
    def single_data(username):

        follower_list = []
        followee_list = []

        if os.path.exists(edges_path + username + '_edges.csv'):
            print('File ' + username + (30 - len(username)) * '.' + 'ALREADY EXISTS')
        else:
            try:
                L.login(login, password)

                profile = instaloader.Profile.from_username(L.context, username)
                if profile.is_verified:
                    print(username + (20 - len(username)) * '.' + 'VERIFIED')
                elif profile.is_business_account and profile.followers > 1000:
                    print(username + (30 - len(username)) * '.' + ' IS BUSINESS ', profile.business_category_name)

                elif profile.is_private and login != 'mikeshehad':
                    print(username + (25 - len(username)) * '.' + 'PRIVATE')
                    private_df.append({username}, ignore_index=True)


                elif profile.followers > 1000 or profile.followees > 1000:
                    print(username + ' is not worth of exporting data from it')
                else:
                    # Think about it
                    for followee in profile.get_followees():
                        followee_list.append(followee.username)
                    for follower in profile.get_followers():
                        follower_list.append(follower.username)

                    # print(followee_list)
                    # print(follower_list)

                    data_final = {'Source': [username] * len(followee_list) + follower_list,
                                  'Target': followee_list + [username] * len(follower_list)}

                    df_final = pd.DataFrame(data_final)
                    # print(df_final)
                    df_final.to_csv(edges_path + username + '_edges.csv', index=None)
                    print(username + (35 - len(username)) * '.' + 'HAS BEEN CREATED')
            except Exception as e:

                if e == instaloader.exceptions.ProfileNotExistsException:
                    print(username, ' profile does not exist')
                if e == instaloader.exceptions.ConnectionException:
                    print('CONNECTION HAS BEEN LOST')
                if e == instaloader.exceptions.TwoFactorAuthRequiredException:
                    print('TWO FACTOR AUTHENTHICATION REQUIERED')




    def list_data(list):
        list = [i for i in list if not os.path.exists(edges_path + i + '_edges.csv')]
        for item in list:
            Importing_data.single_data(item)

    def user(username):
        if os.path.exists(edges_path + username + '_edges.csv'):
            df = pd.read_csv(edges_path + username + '_edges.csv')

            source_list = df['Source'].to_list()
            target_list = df['Target'].to_list()

            source_list = [i for i in source_list if i != username]
            target_list = [i for i in target_list if i != username]

            main_list = source_list + target_list
            print(len(main_list))
            print(main_list)
            Importing_data.list_data(main_list[0:150])
        else:
            Importing_data.single_data(username)
            Importing_data.user(username)


class Updating:

    def single(username):

        if os.path.exists(edges_path + username + '_edges.csv'):

            df = pd.read_csv(edges_path + username + '_edges.csv')

            source_list = df['Source'].to_list()
            target_list = df['Target'].to_list()
            source_list = [i for i in source_list if i != username]
            target_list = [i for i in target_list if i != username]
            print(source_list)
            print(target_list)
            L.login(login, password)

            profile = instaloader.Profile.from_username(L.context, username)

            followees_count = profile.followees
            followers_count = profile.followers

            # Seeking the difference between database file and internet data
            if len(df) != (followees_count + followers_count):
                if len(source_list) != followees_count:
                    source_list.clear()
                    for followee in profile.get_followees():
                        source_list.append(followee.username)

                if len(target_list) != followers_count:
                    target_list.clear()
                    for follower in profile.get_followers():
                        target_list.append(follower.username)
                    print('followers difreence')
                print(target_list)

                data_final = {'Source': [username] * len(target_list) + source_list,
                              'Target': target_list + [username] * len(source_list)}

                df = pd.DataFrame(data_final)

                os.remove(edges_path + username + '_edges.csv')
                df.to_csv(edges_path + username + '_edges.csv', index=None)
                print(username + ' has been updated')
            else:
                print(username + (35 - len(username)) * '.' + 'IS UP TO DATE')
        else:
            print('Wrong input')

    def list(list):
        for item in list:
            Updating.list(item)

    def user(username):
        if os.path.exists(edges_path + username + '_edges.csv'):
            df = pd.read_csv(edges_path + username + '_edges.csv')

            source_list = df['Source'].to_list()
            target_list = df['Target'].to_list()

            source_list = [i for i in source_list if i != username]
            target_list = [i for i in target_list if i != username]

            main_list = source_list + target_list


def creating_folder(username):
    df = pd.read_csv(edges_path + username + '_edges.csv')
    source_list = df['Source'].to_list()
    target_list = df['Target'].to_list()
    source_list = [i for i in source_list if i != username]
    target_list = [i for i in target_list if i != username]
    main_list = source_list + target_list
    checker_list = []

    for item in main_list:
        if not os.path.exists(edges_path + item + '_edges.csv'):
            checker_list.append(item)
    print(checker_list)
    print(len(checker_list))

    if os.path.exists(whl_path + username + '_fold'):
        print(len(main_list))
        main_list = list(dict.fromkeys(main_list))
        print(len(main_list))
        for item in main_list:
            if not os.path.exists(whl_path + username + '_fold//' + item + '_edges.csv'):
                try:
                    shutil.copy(edges_path + item + '_edges.csv',
                                whl_path + username + '_fold//' + item + '_edges.csv')
                    print('Folder ' + username + ' has been updated with this files: ', item)
                except FileNotFoundError:
                    pass

    else:
        os.makedirs(whl_path + username + '_fold')
        for item in main_list:
            if os.path.exists(edges_path + item + '_edges.csv'):
                shutil.copy(edges_path + item + '_edges.csv', whl_path + username + '_fold//' + item + '_edges.csv')
                print('Folder has been created out of', item)

        shutil.copy(edges_path + username + '_edges.csv',
                    whl_path + username + '_fold//' + username + '_edges.csv')


class Creating_dataframe:
    def single(username):
        if os.path.exists(edges_path + username + '_edges.csv'):
            function_df = pd.read_csv(edges_path + username + '_edges.csv')
            return function_df
        else:
            print('Dataframe ' + username + ' can not be created, file does not exists in database')

    def list(list):
        final_df = {"Source": [], "Target": []}
        final_df = pd.DataFrame(final_df)
        for item in list:
            final_df = pd.concat([final_df, Creating_dataframe.single(item)], ignore_index=True)
        final_df.to_csv(r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\\' + 'mixed_list.csv')




Importing_data.user('spotted.staszic')