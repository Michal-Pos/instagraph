from neo4j import GraphDatabase, basic_auth
from py2neo import Node, Relationship, NodeMatcher, Graph, Schema, Subgraph, Record
from py2neo.matching import *
import instaloader
import instaloader.exceptions
import igql.exceptions
from igql import InstagramGraphQL
import sys



# ustawianie połączenia z bazę Neo4j
def establish_database_connection(uri="bolt://localhost:7687", auth=("neo4j", 'zazuziza12')):
    try:
        global graphdb, graph
        graphdb = GraphDatabase.driver(uri=uri, auth=auth)
        graph = Graph(password=auth[1])

    except:
        print('Connection to database failed')
        sys.exit()
C:\Users\micha\PycharmProjects\instagraph 3.6\venv\neo4j_module.py
# Deklarowanie zmiennych potrzebnych do zarządzania bazą danych
# oraz importowaniem do nich informacji
establish_database_connection()
session = graphdb.session()
nodes = NodeMatcher(graph)
igql_api = InstagramGraphQL()

# logowanie do danego konta instagrama
# zalogowanie się jest niezbędne do importowania danych z profili,
# bez poprawnego zalogowania nastąpi zatrzymanie kodu
def login(login, password):
    try:
        global L
        L = instaloader.Instaloader()
        # L.login('kuziminskifranek','zazuziza12')
        L.login(login, password)
    except:

        print(Exception)
        print('login failed')
        sys.exit()



# sprawdzanie czy dany node istnieje w bazie Neo4j,
# zwraca opowiednio  jeśli istnieje, False jeśli nie.
def node_existence(username):
    node_information = nodes.match("Person", name=username).first()
    if node_information is None:
        return False
    else:

        name = node_information['name']
        main = node_information['main']
        return (name, main)



# Sprawdza czy można pobrać listę obserwujących i obserwowanych z profilu. Zwraca odpowiednio True i False
# Maksymalna ilość obserwujących i obserwowanych jest ustawiona domyślnie
# jako 1000 mając na uwadzę prędkość odpowiedzi z Instagrama
# oraz wiarygodność tak dużych profili w kontekście analizy społeczności.
def user_accessibility(username, followers_count=1000, followees_count=1000):
    try:
        user = igql_api.get_user(username)

        data = user.data
        is_private = data['data']['user']['is_private']
        if is_private:
            return False
        else:
            profile = instaloader.Profile.from_username(L.context, username)
            if profile.followers < followers_count and profile.followees < followees_count:
                return True
            else:
                return False
    except:
        return False



# Po nazwie użytkownika zwraca listę tupli: ((source,bool), (target, bool)).
def user_relations(username):
    # Sprawdzenie czy konto użytkownika:
    # *nie jest prywatne
    # *nie ma za dużo obserwujących lub obserwowanych innych kont
    # *istnieje
    # Jeśli wszystkie te warunki zostaną spełnione,
    # rozpocznie się import listy obserwujących i obserwowanych

    if user_accessibility(username):
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            source_list = []
            target_list = []

            for followee in profile.get_followees():
                source_list.append(followee.username)
            for follower in profile.get_followers():
                target_list.append(follower.username)

            source_list = [username] * len(target_list) + source_list
            target_list = target_list + [username] * len(source_list)

            user = igql_api.get_user(username)

            tuple = list(zip(source_list, target_list))
            output_list = []

            # przypisywanie każdej nazwie użytkownika własności True jeśli sieć relacji
            # jest budowana lub już została zbudowana wokół tego użytkownika i False jeśli nie jest.
            for x, y in tuple:
                # print(x, y)
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

                output_list.append((x_tuple, y_tuple))


            return output_list
        except:
            print('unnown error')
            return False
    else:
        print(username, 'profile is unaccesibble')
        return False



# Przyjmuje tuplę w formacie ((source,bool), (target, bool)) gdzie bool określa czy wokół
# użytkownika jest budowana lub została już budowana sieć powiązań.
def creating_relationship(tuple):
    source_tuple = tuple[0]
    target_tuple = tuple[1]

    source = source_tuple[0]
    main_s = source_tuple[1]

    target = target_tuple[0]
    main_t = target_tuple[1]

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





#importowanie relacji pierwszego stopnia użytkownika do Neo4j
def first_degree_relations(username):
    existance = node_existence(username)
    if existance == False or existance[1]==False :
        relations = user_relations(username)
        if relations !=False:
            for item in relations:
                creating_relationship(item)
    else:
        return False

# importowanie relacji drugiego stopnia do Neo4j
def second_degree_relations(username):
    if user_accessibility(username):
        user_tuple = user_relations(username)
        lista = [tuple[0][0] and tuple[1][0] for tuple in user_tuple]
        lista = list(set(lista))
        for item in lista:
            first_degree_relations(item)


# exportowanie relacji pierwszego i drugiego stopnia na temat użytkownika z Neo4j
def user_graph_data(username):

    if node_existence(username):
        result = session.run('''
           MATCH (node {{name: "{}"}})-[r1]-()-[r2]-()
           WITH apoc.coll.toSet(collect(r1) + collect(r2))
           AS rset RETURN [r IN rset | {{startname:startNode(r)["name"],endname:endNode(r)["name"]}}]
           AS res
           '''.format(username))

        names = [record['res'] for record in result]
        relationships = [(name['startname'], name['endname']) for name in names[0]]
        return relationships


# L.login('pm49055047', 'zazuziza13')

# login('pm49055047', 'zazuziza13')
# second_degree_relations('samorzadposting')
# print(node_existence('samorzadposting'))