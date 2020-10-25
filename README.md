# Instagraph

Witaj w Readme Instagraph, narzędzia pozwalającego na wizualizację grafów społecznych i wykrywanie społeczności i optymalizację działań mających na celu zatrzymanie rozpowrzechniania się koronawirusa w szkołach.

 
# Aby zacząć
[Pobierz Neo4j Desktop](https://neo4j.com/download/) oraz utwórz w niej bazę danych. Zainstaluj w niej APOC, możesz to zrobić klikając ikonkę trzech kropek koło nazwy utowrzonej przez ciebie bazy. 
Pobierz potrzbne biblioteki Pythona:
 - instaloader
 - igraph
 - py2neo
 - neo4j
 Powyższe biblioteki umożliwiają modułom pobieranie danych i zarządzanie nimi w utworzonej przez ciebie bazie danych Neo4j.

Zaimportuj moduły z tego repozytorium:

    import neo4j_module
    import igraph_module 
Ustaw połącznie z utworzoną przez siebie bazą danych. Pamiętaj, musi być ona uruchomiona w Neo4j Desktop. Uri jest protokołem stosowanym przez Neo4j. Password jest ustawionym przez ciebie hasłem do bazy.

    neo4j_module.establish_database_connection(uri, password)
