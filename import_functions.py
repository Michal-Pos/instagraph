import pandas as pd
import os
import instaloader
import instaloader.exceptions

L = instaloader.Instaloader()
edges_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\edges\\'
whl_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\whl_folder\\'

# login and passwords section

login = 'pm49055047'
password = 'zazuziza12'


# login = 'hlane976'
# password = 'Zazuziza15'
# login = 'martycox44'
# password = 'zazuziza13'


# Class that exports data from profiles
class Exporting_data:
    L.login(login, password)

    # This can be used only to exporting data from poblic profiles
    def single_data(username):
        follower_list = []
        followee_list = []
        if os.path.exists(edges_path + username + '_edges.csv'):
            print('File ' + username + (20 - len(username)) * '.' + 'ALREADY EXISTS')
        else:
            try:
                profile = instaloader.Profile.from_username(L.context, username)
                if profile.is_verified:
                    print(username + (20 - len(username)) * '.' + 'VERIFIED')
                elif profile.is_business_account:
                    print(username + (20 - len(username)) * '.' + ' IS BUSINESS ', profile.business_category_name)

                elif profile.is_private and login != 'mikeshehad':
                    print(username + (25 - len(username)) * '.' + 'PRIVATE')

                elif profile.followers > 1000 or profile.followees > 1000:
                    print(username + ' is not worth of exporting data from it')
                else:
                    # Think about it
                    for followee in profile.get_followees():
                        followee_list.append(followee.username)
                    for follower in profile.get_followers():
                        follower_list.append(follower.username)

                    print(followee_list)
                    print(follower_list)

                    data_final = {'Source': [username] * len(followee_list) + follower_list,
                                  'Target': followee_list + [username] * len(follower_list)}

                    df_final = pd.DataFrame(data_final)
                    print(df_final)
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
        for item in list:
            Exporting_data.single_data(item)

    def user(username):
        if os.path.exists(edges_path + username + '_edges.csv'):
            df = pd.read_csv(edges_path + username + '_edges.csv')

            source_list = df['Source'].to_list()
            target_list = df['Target'].to_list()

            source_list = [i for i in source_list if i != username]
            target_list = [i for i in target_list if i != username]

            main_list = source_list + target_list
            print(main_list)
            Exporting_data.list_data(main_list[150:300])
        else:
            Exporting_data.single_data(username)
            Exporting_data.user(username)



class Updating:

    def single(username):
        profile = instaloader.Profile.from_username(L.context, username)
        if os.path.exists(edges_path + username + '_edges.csv'):

            df = pd.read_csv(edges_path + username + '_edges.csv')

            source_list = df['Source'].to_list()
            target_list = df['Target'].to_list()
            source_list = [i for i in source_list if i != username]
            target_list = [i for i in target_list if i != username]
            if len(df) != (profile.followers + profile.followees):
                if len(source_list)!=profile.followees:
                    print('Profile ' + username + 'is being updated')

                    #print(df)
                    print(len(df))
                    print(profile.followers + profile.followees)


                # os.remove(edges_path + username + '_edges.csv')
                # df.to_csv(edges_path + username + '_edges.csv', index=None)
                # print(username + 'has been updated')
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
            print(main_list)

Exporting_data.user('spotted_jezioranski')

