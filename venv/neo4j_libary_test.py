from neo4j import GraphDatabase, basic_auth
from py2neo import Node, Relationship, NodeMatcher, Graph, Schema
from py2neo.matching import *
import instaloader
from itertools import chain
import instaloader.exceptions
from igql import InstagramGraphQL

# establish connection
graphdb=GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", 'zazuziza12'))
graph = Graph(password="zazuziza12")
nodes = NodeMatcher(graph)
session = graphdb.session()

L = instaloader.Instaloader()
igql_api = InstagramGraphQL()

#
# """login potrzebny tulko podczas eksportowania relacji"""
def login():
    L.login('pm49055047', 'Zazuziza13')


def match_limit(int):
    session("MATCH (x) RETURN (x) LIMIT {}".format(str(int)))

def search_node(propety):
    nodes_names=[]
    results = session.run("MATCH (x) where x.lable='{}' return (x)".format(str(propety)))
    for record in results:
        nodes_names.append(record)
    return nodes_names


def records_all_nodes():
    nodes = session.run("MATCH (x) RETURN (x)")
    lista=[]
    for node in nodes:
        print(type(node))
        lista.append(node)
    print(lista)
# create_node('ned')4

def nodes_name():
    nodes_names=[]
    result = list(session.run("MATCH (n) RETURN n.name"))
    data=result.data()
    # for record in result:
    #     nodes_names.append(record)
    # return nodes_names



def username_data(username):
    user = igql_api.get_user(username)
    data = user.data
    full_name = data['data']['user']['full_name']
    id = data['data']['user']['id']

    if data['data']['user']['is_private'] == False:
        accessibility = 'PUBLIC'
    else:
        accessibility = 'PRIVATE'

    tuple = (username, full_name, id, accessibility)

    return tuple

# MATCH (x) where x.lable='{}' return (x)
# MATCH (n) RETURN n


# creating node with labels as labels and name as property
def create_node(list):
    for item in list:
        username=item

        tuple=username_data(username)

        full_name=tuple[1]
        x = full_name.repla
        id=tuple[2]
        accessibility=tuple[3]
        print(tuple)

        session.run("MERGE (N: Person{{name:'{}', full_name:'{}',"
                    "id:{}, accesibilty:'{}' }})".format(username, full_name, id, accessibility))

        # session.run("MERGE (N: Person{{name:'{}', full_name:'{}',"
        #             "id:{}, accesibilty:'{}' }})".format('frankolej', 'Michał Psoaidała', 123476, 'PRIVATE'))


        """"Czy jest mi potrzebne to poniżej?"""
        #session.run("MATCH (x:Person)return (x)")

def all_nodes():
    session.run("MATCH (x) RETURN x")


# importinf user relationships, followees and followers
def user_relations(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print(profile)

        if profile.is_private or profile.is_verified:
            print('Not Accesible')
        elif profile.is_business_account and profile.followers>1000:
            print('business account')

        else:
            source_list=[]
            target_list=[]
            for followee in profile.get_followees():
                source_list.append(followee.username)
            for follower in profile.get_followers():
                target_list.append(follower.username)
            source_list=[username] * len(target_list) + source_list
            target_list=target_list + [username] * len(source_list)

            tuple=list(zip(source_list, target_list))
            #print(tuple)

            return tuple

    except Exception as e:
        if e == instaloader.exceptions.ProfileNotExistsException:
            print(username, ' profile does not exist')
        if e == instaloader.exceptions.ConnectionException:

            print('CONNECTION HAS BEEN LOST')
        if e == instaloader.exceptions.TwoFactorAuthRequiredException:
            print('TWO FACTOR AUTHENTHICATION REQUIERED')
        if e == instaloader.exceptions.QueryReturnedNotFoundException:
            pass
        else:
            print(e)

def creating_relations_neo(source_list, target_list):
    for i in range(0, len(list1)):
        session.run("MATCH (root {name: Dhawan}) "
                    "CREATE UNIQUE (root)-[:LOVES]-(someone) RETURN someone ")



def creating_relationship(source_tuple, target_tuple):
    #print('SOURCE TUPLE', source_tuple)
    #print('TARGET TUPLE',target_tuple)
    source=source_tuple[0]
    full_name_s = source_tuple[1]
    full_name_s=full_name_s.translate({ord(i): None for i in ",'"})
    id_s = source_tuple[2]
    accessibility_s = source_tuple[3]

    target=target_tuple[0]
    full_name_t = target_tuple[1]
    full_name_t = full_name_t.translate({ord(i): None for i in ",'"})
    id_t = target_tuple[2]
    accessibility_t = target_tuple[3]

    session.run('''
    MERGE (A:Person{{name:'{}', full_name:'{}', id:{}, accesibilty:'{}'}})
    MERGE (B:Person{{name:'{}', full_name:'{}', id:{}, accesibilty:'{}'}})
    MERGE (A) -[r:FOLLOWS]->(B)
                '''.format(source, full_name_s, id_s, accessibility_s, target, full_name_t, id_t, accessibility_t))


# creating realationships from list of tuples in format (source, target)
def creating_realtionships(tuple_list):

    # creating list from tuple_list and removing duplicates
    lista=[item for t in tuple_list for item in t]
    lista=list(set(lista))
    out_list=[]
    index_list=[]
    print(lista)

    # for item in lista:
    #     node_info = node_existence(item)
    #     if node_info!=False:
    #         lista.remove(item)
    #         out_list.append(node_info)
    # print(lista)
    # print(out_list)
    #
    for item in lista:
        node_info = node_existence(item)
        # print(info)
        if node_info != False:
            out_list.append(node_info)
            index_list.append(node_info[0])
    lista=list(set(lista)-set(index_list))
    #print('LISTA', lista)
    #print('OUT_LIST', out_list)

    # Nicważnego, możesz to skasować bezproblemu
    x=1

    # creating list of deatailed info about every single node that supposed to be created
    for item in lista:
        print(x, item)
        out_list.append(username_data(item))
        x+=1
    print(out_list)

    for x,y in tuple_list:
        print(x,y)
        source_tuple=[tuple for tuple in out_list if x==tuple[0]]
        source_tuple = tuple([element for tupl in source_tuple for element in tupl])

        target_tuple=[tuple for tuple in out_list if y==tuple[0]]
        target_tuple = tuple([element for tupl in target_tuple for element in tupl])
        creating_relationship(source_tuple, target_tuple)


# # lista=[('mikeshehad','frankolej'),('mikeshehad','karta_dama'),('mikeshehad','gosia_nw'),('frankolej','_basi_p_')]

def node_existence(username):
    node_information = nodes.match("Person", name=username).first()
    # print(node_information)
    # name = node_information['name']
    # full_name = node_information['full_name']
    #
    # id = node_information['id']
    # accesibilty = node_information['accesibilty']
    # return (name, full_name, id, accesibilty)
    if node_information==None:
        return False
    else:
        name = node_information['name']
        full_name = node_information['full_name']

        id = node_information['id']
        accesibilty = node_information['accesibilty']
        return (name, full_name, id, accesibilty)


login()
creating_realtionships(user_relations('janstupkiewicz'))
# creating_realtionships([('mikeshehad', 'frankolej')])
# print(node_existence('frankolej'))
