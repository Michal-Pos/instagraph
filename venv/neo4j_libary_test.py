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


def login_with_instaloader(login, passowrd):
    try:
        L.login(login, password)
    except:
        print('login error','Zazuziza13')

login_with_instaloader('pm49055047', )

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
        print(username_data(username))
        print(type(username_data(username)))




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
            print('1')
            source_list=[]
            target_list=[]
            for followee in profile.get_followees():
                source_list.append(followee.username)
            for follower in profile.get_followers():
                target_list.append(follower.username)
            source_list=[username] * len(target_list) + source_list
            target_list=target_list + [username] * len(source_list)

            return source_list, target_list

    except Exception as e:
        if e == instaloader.exceptions.ProfileNotExistsException:
            pass
            # print(username, ' profile does not exist')
        if e == instaloader.exceptions.ConnectionException:

            print('CONNECTION HAS BEEN LOST')
        if e == instaloader.exceptions.TwoFactorAuthRequiredException:
            pass
            # print('TWO FACTOR AUTHENTHICATION REQUIERED')
        if e == instaloader.exceptions.QueryReturnedNotFoundException:
            pass

def creating_relations_neo(source_list, target_list):
    for i in range(0, len(list1)):
        session.run("MATCH (root {name: Dhawan}) "
                    "CREATE UNIQUE (root)-[:LOVES]-(someone) RETURN someone ")
def creating_list_nodes(source_list,target_list):
    final_list = source_list + target_list
    for item in final_list:
        create_node(item)

# # creating_list_nodes(user_relations('mikeshehad'))tu
# tuple=(['frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'pamcinema', 'pampam.mp4', 'i.succ.my.nutv2', 'i.succ.my.nut', 'tarkovmemes', 'prywatnabaha', 'taxedmemesforconservativeteens', 'radaetyki', 'buzzsmokes', 'xdankest_boi', 'aleksander_rojewski', 'krulaczek', 'holdup.comments', 'top_comments_god', 'memepold', 'zwidepomleko', 'thedeeepestpartoftheinternet', 'escapefromtarkovofficial', 'dailystolenmemenews_pt.2', 'petroltown', 'pogforever', 'transporter_pl', 'the.collection', 'movendus.mag', 'maly._.prl', 'wielobarwny', 'bborowsky_', 'kaczorpaw', 'street_spotting', 'dankmonkeymemes', 'harc.memy', 'szyszunie_squad', 'stalinsgulagcamp', '_jckz_', 'mucked', 'jeffgoldblum', 'nick_history_secrets', 'dittonitto', 'the.amazing.meme.machine2', 'flakpanzer_iv_wirbelwind', 'poldi73_', 'mememonk_', 'spicydeepfriedmemesv3', 'the.amazing.meme.machine', 'bepiz.man', 'dankersaurusrex', 'mateu.kk', 'qualityqontent', 'pzkpfw_6b', '_werav_', 'the_collection1', 'spotted_jezioranski', 'kazik_balety', 'tankmuseum', 'mariusz1996', 'safely_endangered', 'ketnipz', 'webcomic_name', 'taikawaititi', 'lo43warszawa', 'helikontex', 'verteusz', 'lavenderlivre', 'vancityreynolds', 'weronika_roxana', 'roger_dubuis_boutique_aspen', 'roger_dubuis', 'lamborghiniclubamerica', 'serataitaliana', 'themarkhull', 'shmarc150', 'blenderseyewear', 'dundon_motorsports', 'theshmeemobiles', 'fastlanedrive', 'californiamotorsports', 'danwierck', 'misfits', 'quackity', 'callmecarsonyt', 'idubbbz', 'louder.memes', 'tinder_kazik', 'jameskii', 'spottedkazik', 'axistrackservices', 'fotojohny', 'aduulaa21', '63_wdh_echo', 'recrut74', 'ausarmour', 'dzemorek', 'youtooz', 'szczep69wdhiz', 'natalia_styczyszyn', 'd3ari_a', 'ula.ludwin', 'm_zsuetam', 'zhp_pl', 'mak_kes_', 'borowicz.artur', 'topazskinltd', 'wrxhe', 'gosia_nw', 'the_vintager_herald', 'mikejohnstanislaw', 'theselcouthgabi', 'mgcharoudin', 'robert_mitchell', 'peciakjulian', 'shopmrbeast', 'mrbeast', 'therealtavarish', 'jamesmaybloke', 'szymonbanas', 'goodguyfitz', 'jeremyclarkson1', 'dagsson', 'swaggersouls', 'itsthegrandtour', 'bendito_sea_el_boi', 'miszel1556', 'jontronshow', 'darkdolan', 'grandayyyyyy', 'palmetypie', 'isaiasian99elden', 'gercollector', 'maltanskadominika', 'zuzaolczyk', 'goldkate_', 'a.h_pekala', 'youngtimerwarsaw', 'ihopeyouaredope', 'yunggravy', 'billyisterrible', 'minghi90', 'airsoft_store_export', 'swagger_nailer', 'bulldog_entertainment', 'swycar', 'novritsch', 'shmee150', '_nie_normalna', 'carsandcoffeeitaly', 'jan_bulira', 'dday_hel', 'marcinandrzejzbigniew', 'and___sm', 'makslakocy', 'tobiascton_21s6g', 'codaevolution', 'lv99_priest', 'oliwkawys', 'pmshooter', 'squawk1ident', 'makspott_', 'krzysiu_2002_', 'martaprzybytniak', 'kaczqa_', 'odyssons', 'niewiadomska_paulina', 'zuziaaaaaaaaaaa', 'oliskqa_a', 'viva_la_meme_man.ig', 'kuczekkonrad', 'uroczebubu', 'kaczprzak', 'justelathings', 'mikeshehad', 'marcinekfoto', 'aleksandrajarkiewicz', '__pawulon__', 'kubatymieniecki', 'gregb.23', 'adif_7960', 'gustaw_czernik', 'tobythedoogg', 'frostedclouds', 'amelieamoureux', 'anomalyxd', 'salomondrin', 'avi1kanobi', 'kubsonkubica', 'alekpilecki', 'gala.michal_', 'amazingaslan', 'yeman35', 'jacobx_____', '_karpiu___', 'backwards.dog', 'wera_wiki_wixi13', 'mcm4ks', 'bianca_the_destroyer', 'invierno098', 'xsproject', 'drdemolitionmatt', 'corridordigital', 'k_swiecki', 'swiatlacy_', 'kosmuuusz', 'dark_xue_hu', 'patryk_the_intellectual_elite', 'gargamel5000', 'patrycja_karasinska', 'kadzetano', 'jameneliada', 'julafilipiuk', 'grzegorzcizlaoncars', 'mikolaj.muldner', 'tenbungo21', 'godlike.megamaster', 'olofkajbjer', 'panzerfarm', 'ananas.warsaw', 'senorita.puperrita', 'zubrzysta', '_filipiuk_', 'erandolleshi', 'wende_emilia', 'kitasando', 'wiktoriatelak', 'h0ndakid', 'natalka_miszczyk', 'xxlusiax', 'pikle2x2', 'the_life_of_boris', 'citizen.lame', 'akswezsinatsm', '_karpiu__', 'oldzisroldzi', 'kamil7736', 'pruuuchin1911', 'kurczak_johnny', 'fabrice_matz', 'j_radlicki', 'iamkubaaaaaa', 'hejkapatka', 'ulka_kulkaa', '_basia_szy_', 'franekdzierzyk', 'wwii_traveler', 'qurwix01', 'serwinterofficial', 'the_ww2_archives', 'fjamie013', 'v.stadnicka', 'veganart.blogspot.hr', 'axis_and_allies45', 'reform_life', 'old.world.now', 'cropp_clothing', 'warsawdrive', 'balunio', 'dylanwishop', 'axialracing', 'rockstargames', 'vxazxv', 'basiadochuja', '_swiatekjestem_', 'the_history_of_ww2', 'divisiontipsandtricks', '4admin__r0xx', 'thedivisiongame_us', 'ubisoftpl', 'ubisoft', 'msigaming_poland', 'mery.maria.w', 'programzdupy', 'the_ww2_album', '_mike1206_', 'gerlowska__', 'czorciki', 'pewdiepie', 'kubson1992', 'kwejk', 'the_war_collection', 'ww2tanksdaily', 'worldwar2.memes', 'llerouxx', 'sucharcodzienny', 'jarockie', 'selectfmg', 'battlefield_unlimited', 'chausmaan', 'niemakontaxx', 'rc_central', 'paszkiewiicz', 'discoverearth', 'azarmory', 'mati_gajda', 'catsofinstagram', 'olgazygmunt', 'szyjeizyje', 'gunsdaily', 'amazingcars247', 'kvrolynv'], ['wsm_ja_ale_priv', 'aleksander_rojewski', 'krulaczek', 'peace87324', 'marreeckii', 'krypto_kocur', '_jckz_', 'poldi73_', 'mateu.kk', 'pzkpfw_6b', 'justyna_plaskota', 'car.shotsbh', '_fvilip', 'domi.milka', 'skoppay', 'finezjaa.sso', 'tak_ambitnie_agata', 'gosia_nw_pv', 'pdtopografiaeprojetos', 'verteusz', 'lavenderlivre', 'oliwirko17', 'piojdj', 'xx_nico_nis', 'ola_.w._', 'wikgont', 'odyssons', 'widar.ski', 'aduulaa21', 'dzemorek', 'roksana.janus', 'szczep69wdhiz', 'dark_xue_hu', 'wiktoriablaszczyk_', 'ajzxk', 'natalia_styczyszyn', 'd3ari_a', 'm_zsuetam', 'ula.ludwin', 'tomek.mackenthun', 'mak_kes_', 'bi3dr0nka', 'zoskaantoska', 'wrxhe', 'zarabiscie', 'juleczka_14_', 'the_vintager_herald', 'dominikazwiech', 'jagodablachnia', 'custombarbers', 'mikejohnstanislaw', 'krowysapiekne', 'theselcouthgabi', 'tomeknozderka', 'mcm4ks', 'bendito_sea_el_boi', 'invierno098', 'miszel1556', 'tomedchannel3', 'tomedchannel2', 'palmetypie', 'earthbydrones', 'pilot_of_knowledge', 'isaiasian99elden', 'kokartka_art', 'maltanskadominika', 'samsudin_leaderpaytren', 'zuzaolczyk', 'asiok.mopsik', 'alka_ole', 'borowicz.artur', 'pitlane_garda_lake', 'grindec1993', 'totalgeo.topografia', 'cpetecnologia', 'tanarosemusic', '_nie_normalna', 'marcinandrzejzbigniew', 'al.angelalewis', 'lv99_priest', 'squawk1ident', 'oliwkawys', 'mkapicaa', 'koziolekkkkkkkk', 'and___sm', 'kaczqa_', 'oliskqa_a', 'uroczebubu', 'kaczprzak', 'gosia_nw', 'mikeshehad', 'marcinekfoto', 'aleksandrajarkiewicz', 'cafeiluzja', 'white_horse0894', 'gustaw_czernik', 'j_radlicki', 'kubatymieniecki', 'kubsonkubica', 'jurasportcars', 'a.h_pekala', 'alekpilecki', 'amazingaslan', 'adabelier', 'opexp', 'swiatlacy_', '__pawulon__', '_karpiu___', 'k_swiecki', 'wera_wiki_wixi13', 'patryk_the_intellectual_elite', 'patrycja_karasinska', 'kadzetano', 'kosmuuusz', 'crazyempress3090', 'florence_duft', 'mikolaj.muldner', 'backwards.dog', 'wojtekkuryllo', 'kurpiikumpel', 'jameneliada', 'bartek_lamecki', 'wende_emilia', 'pikle2x2', 'citizen.lame', 'pruuuchin1911', 'amienhdavidson', 'ulka_kulkaa', 'csgo.sellings.and.duplicates', 'f0ll.owers_now_uwxtoi', 'veganart.blogspot.hr', 'beamng.shots', 'proffile_emissary_4022', '_marta_kl', 'mishyachka', '_maleprzyjemnosci_', '_awesome_gift_xboxone_', 'basiadochuja', '_swiatekjestem_', 'j.4510', 'kamil7736', '_karpiu__', 'mery.maria.w', '_mike1206_', 'gerlowska__', 'czorciki', 'xxlusiax', 'niemakontaxx', 'kuba_kowal_', 'szyjeizyje', 'wera_nowa', 'olgazygmunt', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej', 'frankolej'])
#
# list1=tuple[0]+tuple[1]
# print(list1)
# list1=list(dict.fromkeys(list1))
# for item in list1:
#     username_data(item)
create_node([''])
#creating_list_nodes('frankolej')
# MICHAŁ, JEŚLI PADNIESZ TO PAMIETAJ
# TO PONIŻEJ JEST W OPÓR WAŻNE
#create_node('Person', 'franek' )