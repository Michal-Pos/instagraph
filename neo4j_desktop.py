from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
import os
import instaloader
import instaloader.exceptions
import time

edges_path = r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\edges\\'

graph = Graph(password="zazuziza12")
L = instaloader.Instaloader()

login = 'pm49055047'
password = 'Zazuziza13'

# Poprawić to z object
#DZIAŁA
def creating_relations(input):
    if type(input)==list:
        for item in input:
            if os.path.exists(edges_path+item+'_edges.csv'):
                print(item)
                df = pd.read_csv(edges_path + item + '_edges.csv')
                df = pd.DataFrame(df)

                source_list = df['Source'].to_list()
                target_list = df['Target'].to_list()
                for i in range(0, len(source_list)):
                    print(source_list[i], target_list[i])
                    a = Node("Person", name=source_list[i])
                    b = Node("Person", name=target_list[i])
                    FOLLOWS = Relationship.type("FOLLOWS")
                    graph.merge(FOLLOWS(a, b), "Account", "name")
            else:
                print(item, 'does not exists in database')
    else:
        print("UNKOWN INPUT ERROR")


def specified():
    final_list=[]
    for item in os.listdir(edges_path):
        #print(item)
        df=pd.read_csv(edges_path+item)
        df = pd.DataFrame(df)

        source_list = df['Source'].to_list()
        target_list = df['Target'].to_list()

        source_list=[i for i in source_list if i != item.replace('_edges.csv','')]
        target_list=[i for i in target_list if i != item.replace('_edges.csv','')]

        final_list+=source_list
        final_list+=target_list

    final_list = list(dict.fromkeys(final_list))

    # final_df = {'profile':final_list}
    # final_df = pd.DataFrame(final_df)
    return final_list

def creating_nodes(input):
    all_list=[]
    n=0
    if type(input)==list:

        for item in input[0:1000]:
            username=item
            try:
                profile = instaloader.Profile.from_username(L.context, username)

                full_name = profile.full_name
                id = int(profile.userid)
                followees = profile.followees
                followers = profile.followers

                if profile.is_private:
                    accessibilty = 'PRIVATE'
                    verification = 'NOT VERIFIED'
                    business = 'NOT BUSINESS'
                else:
                    if profile.is_verified:
                        verification = 'VERIFIED'
                        accessibilty = 'PUBLIC'

                    else:
                        verification = 'NOT VERIFIED'
                        accessibilty = 'PUBLIC'

                    if profile.is_business_account:
                        business = profile.business_category_name
                    else:
                        business = 'NOT BUSINESS'


                print(username,
                      full_name ,
                      id,
                      followees,
                      followers,
                      accessibilty,
                      verification,
                      business)

                all_list.append([username,
                      full_name ,
                      id,
                      followees,
                      followers,
                      accessibilty,
                      verification,
                      business])

            except Exception as e:

                if e == instaloader.exceptions.ProfileNotExistsException:
                    print(username, ' profile does not exist')
                if e == instaloader.exceptions.ConnectionException:
                    print('CONNECTION HAS BEEN LOST')
                if e == instaloader.exceptions.TwoFactorAuthRequiredException:
                    print('TWO FACTOR AUTHENTHICATION REQUIERED')
                if e == instaloader.exceptions.QueryReturnedNotFoundException:
                    print(profile, 'not found')
                else:
                    print('unkown error')

            n+=1
        df = pd.DataFrame.from_records(all_list)
        print(df)
        df.to_csv(r'C:\Users\micha\PycharmProjects\instagraph 3.0\data\test_df.csv', index=None)

    else:
        print("UNKOWN INPUT ERROR")


creating_relations(['mikeshehad'])
v