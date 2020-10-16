from neo4j import GraphDatabase, basic_auth
from py2neo import Node, Relationship, NodeMatcher, Graph, Schema
import instaloader
import instaloader.exceptions

# establish connection
graphdb=GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", 'zazuziza12'))
# graph = Graph(password="zazuziza12")

session = graphdb.session()
#session.run("CREATE CONSTRAINT ON (n:Person) ASSERT n.id IS UNIQUE")

L = instaloader.Instaloader()


"""login potrzebny tulko podczas eksportowania relacji"""
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
    for node in nodes:
        print(node)
# create_node('ned')4

def nodes_name():
    nodes_names=[]
    result = list(session.run("MATCH (n) RETURN n.name"))
    for record in result:
        nodes_names.append(record)
    return nodes_names

def username_data(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)

        full_name = profile.full_name
        id = int(profile.userid)
        if profile.is_private:
            accessibility = 'PRIVATE'
        else:
            accessibility = 'PUBLIC'


        return username, full_name, id, accessibility

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
            print(e)


# creating node with labels as labels and name as property
def create_node(list):
    for item in list:
        username=item

        tuple=username_data(username)

        full_name=tuple[1]
        id=tuple[2]
        accessibility=tuple[3]
        print(tuple)




        session.run("MERGE (N: Person{{name:'{}', full_name:'{}',"
                    "id:{}, accesibilty:'{}' }})".format(username, full_name, id, accessibility))

        # session.run("MERGE (N: Person{{name:'{}', full_name:'{}',"
        #             "id:{}, accesibilty:'{}' }})".format('frankolej', 'Michał Psoaidała', 123476, 'PRIVATE'))


        """"Czy jest mi potrzebne to poniżej?"""
        #session.run("MATCH (x:Person)return (x)")



        #
        # session.run("CREATE (N: Person{{username:'{}',full_name:'{}',"
        #             "id:'{}',accesibilty:'{}})".format(username_data(username)))
        #
        # session.run("MATCH (x:{})return (x)".format(label))


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
            print(source_list)
            print(target_list)

            tuple=list(zip(source_list, target_list))

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



#
# creating_list_nodes(user_relations('mikeshehad'))
# creating_reltionships(user_relations('mikeshehad'))
# list1=tuple[0]+tuple[1]
# print(list1)
# list1=list(dict.fromkeys(list1))
# for item in list1:
#     username_data(item)
# create_node(['karinagomolka', 'romantywka'])
#creating_list_nodes('frankolej')
# MICHAŁ, JEŚLI PADNIESZ TO PAMIETAJ
# TO PONIŻEJ JEST W OPÓR WAŻNE


# #create_node('Person', 'franek' )
# tuple1=username_data('mikeshehad')
# tuple2=username_data('brodaty_filip')
# print(tuple1, tuple2)


# session.run("MATCH (N: Person{{name:'{}', full_name:'{}', id:{}, accesibilty:'{}' }})".format(target, full_name, id, accessibility))


def creating_reltionships(source, target):
    tuple_s = username_data(source)
    full_name_s = tuple_s[1]
    id_s = tuple_s[2]
    accessibility_s = tuple_s[3]

    tuple_t = username_data(target)
    full_name_t = tuple_t[1]
    id_t = tuple_t[2]
    accessibility_t = tuple_t[3]

    session.run('''
    MERGE (A:Person{{name:'{}', full_name:'{}', id:{}, accesibilty:'{}'}})
    MERGE (B:Person{{name:'{}', full_name:'{}', id:{}, accesibilty:'{}'}})
    MERGE (A) -[r:FOLLOWS]->(B)
                '''.format(source, full_name_s, id_s, accessibility_s, target, full_name_t, id_t, accessibility_t))

print(user_relations('mikeshehad'))

for item in user_relations("mikeshehad"):
    print(itema)
    source=item[0]
    target=item[1]
    creating_reltionships(source, target)