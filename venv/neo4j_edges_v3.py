from neo4j import GraphDatabase, basic_auth
from py2neo import Node, Relationship, NodeMatcher, Graph, Schema
from py2neo.matching import *
import instaloader
from itertools import chain
import instaloader.exceptions
from igql import InstagramGraphQL
import sys

# establish connection
graphdb = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", 'zazuziza12'))
graph = Graph(password="zazuziza12")
nodes = NodeMatcher(graph)
session = graphdb.session()
L = instaloader.Instaloader()
igql_api = InstagramGraphQL()

print('login')
# login potrzebny tulko podczas eksportowania relacji
def login():
    try:
        # L.login('kuziminskifranek','zazuziza12')
        # L.login('mikeshehad', 'fibbogauss')
        L.login('pm49055047', 'zazuziza13')
    except:
        print(Exception)
        print('login failed')
        sys.exit()


def node_existence(username):
    node_information = nodes.match("Person", name=username).first()
    if node_information is None:
        return False
    else:

        name = node_information['name']
        main = node_information['main']
        return (name, main)


def user_relations(username, followers_count=1000, followees_count=1000):
    try:
        user = igql_api.get_user(username)
        data = user.data
        print(data)
        is_private = data['data']['user']['is_private']
        if not is_private:

            profile = instaloader.Profile.from_username(L.context, username)
            if profile.followers < followers_count and profile.followees < followees_count:
                source_list = []
                target_list = []

                for followee in profile.get_followees():
                    source_list.append(followee.username)
                for follower in profile.get_followers():
                    target_list.append(follower.username)

                source_list = [username] * len(target_list) + source_list
                target_list = target_list + [username] * len(source_list)

                tuple = list(zip(source_list, target_list))
                output_list = []
                for x, y in tuple:
                    #print(x, y)
                    if x == username:
                        x_tuple = (x, True)

                    elif node_existence(x):
                        x_tuple = node_existence(x)

                    else:
                        x_tuple = (x, False)

                    if y == username:
                        y_tuple = (y, True)

                    elif node_existence(y):
                        y_tuple = node_existence(y)

                    else:
                        y_tuple = (y, False)

                    # print(x_tuple, y_tuple)
                    output_list.append((x_tuple, y_tuple))
                return output_list


            else:
                return 'HAS too many followers or followees'
        else:
            return  'is private'


    except Exception as e:
        if e == instaloader.exceptions.ProfileNotExistsException:
            print(username, ' profile does not exist')
            return 'not exist'
        if e == instaloader.exceptions.ConnectionException:
            print('CONNECTION HAS BEEN LOST')
        if e == instaloader.exceptions.TwoFactorAuthRequiredException:
            print('TWO FACTOR AUTHENTHICATION REQUIERED')
        if e == instaloader.exceptions.QueryReturnedNotFoundException:
            print('Query not found')
        else:
            print(e)





def creating_relationship(tuple):
    # print(tuple)
    # print('SOURCE TUPLE', source_tuple)
    # print('TARGET TUPLE', target_tuple)
    source_tuple = tuple[0]
    target_tuple = tuple[1]


    source = source_tuple[0]
    main_s = source_tuple[1]

    target = target_tuple[0]
    main_t = target_tuple[1]

    # print("MAIN S", main_s)
    # print("MAIN T", main_t)
    if main_s:
        session.run(''' 
        MATCH (A:Person{{name:'{}'}})
        SET A.main = True
        '''.format(source))

    if main_t:
        session.run('''
            MATCH (B:Person{{name:'{}'}})
            SET B.main = True
            '''.format(target, main_t))



    session.run('''
            MERGE (A:Person{{name:'{}', main:{}}})
            MERGE (B:Person{{name:'{}', main:{}}})
            MERGE (A) -[r:FOLLOWS]->(B)
                        '''.format(source, main_s, target, main_t))


# def setting_main(tuple):
#     session.run('''
#             MERGE (A:Person{{name:'{}', main:{}}})
#             MERGE (B:Person{{name:'{}', main:{}}})
#             MERGE (A) -[r:FOLLOWS]->(B)
#                         '''.format('janstupkiewcz', ''))

login()

def first_degree_relations(username):
    relations = user_relations(username)
    if relations == 'is private':
        print(username, relations)
    if relations=='HAS too many followers or followees':
        print(username, relations)
    elif relations == 'not exist':
        print(username, relations)
    else:
        print(relations)
        for item in relations:
            creating_relationship(item)


def second_degree_relations(username):
    user_tuple = user_relations(username)
    # print(user_tuple)

    lista = [tuple[0][0] and tuple[1][0] for tuple in user_tuple]
    lista = list(set(lista))
    print(lista)
    for item in lista:
        try:
            if not node_existence(item)[1]:
                try:
                    print(item)
                    fd_relations = first_degree_relations(item)
                except:

                    if fd_relations == 'is private':
                        print(item, fd_relations)
                    elif fd_relations == 'HAS too many followers or followees':
                        print(item, fd_relations)
                    elif fd_relations == 'not exist':
                        print(item, fd_relations)
                    print('Problem occured with', item)
                finally:
                    print(item, ' data extraction has been ended')

            else:
                print(item, 'already exists')
        except:
            print('problem occured with', item, 'in database')


second_degree_relations('samorzadposting')
# print(node_existence('mikeshehad'))
# second_degree_relations('mikeshehad')

# second_degree_relations('mikeshehad')
    # out_list = list(set(out_list))
    # print(out_list)
    # for item in out_list:
    #     relations_list = user_relations(item)
    #     for item in relations_list:
    #         creating_relationship(item)


# print(lista)
# print(type(lista))
# print(lista)
# out_list=[]
# for tuple in lista:
#     for tuple in tuple:
#         for item in tuple:
#             if item != (True or False):
#                 print(item)
#                 out_list.append(item)
#
#second_degree_relations('mikeshehad')
# out_list= list(set(lista))
#
# print(list)
# MERGE (A:Person{name:'mikeshehad', main: True})
# MERGE (B:Person{name:'janstupkiewicz', main:False})
# MERGE (A) -[r:FOLLOWS]->(B)
#
# MERGE (A:Person{name:'mikeshehad'})
# MERGE (A:Person{name:'mikeshehad'})
# ON MATCH SET A.main = True