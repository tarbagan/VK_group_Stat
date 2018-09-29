from urllib.request import urlopen
import json
import math
import time
import datetime

token = "YOU TOKEN"
group_id = "ID GROUP VK"

def count_user():
    filter = "members_count,is_closed,can_create_topic,can_post,contacts"
    url = "https://api.vk.com/method/groups.getById.json?group_ids=" + group_id + "&fields="+filter+"&access_token=" + token + "&v=5.52"
    response = urlopen(url)
    data = response.read()
    jsn = json.loads(data)

    print ("Подключаем группу - " + jsn["response"][0]["name"])
    print( "Подписчиков групы:  - " + str(jsn["response"][0]["members_count"]))

    if jsn["response"][0]["is_closed"] == 0: print ("Тип: открытая группа")
    if jsn["response"][0]["is_closed"] == 1: print ("Тип: закрытая группа")
    if jsn["response"][0]["is_closed"] == 2: print ("Тип: частная группа")

    #if jsn["response"][0]["can_create_topic"] == 1: print ("Вы можете оставлять посты в группе")
    #if jsn["response"][0]["can_create_topic"] == 0: print ("Вы не можете оставлять посты в группе")

    #if jsn["response"][0]["can_post"] == 1: print ("Вы можете оставлять посты на стене")
    #if jsn["response"][0]["can_post"] == 0: print ("Вы не можете оставлять посты на стене")

    print( "-------------------------------------------------------------" )
    count_group = jsn["response"][0]["members_count"]
    return count_group

def pagination():
    """Доступные значения через запятую: sex, bdate, city, country, photo_50, photo_100,
    photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig,
    online, online_mobile, lists, domain, has_mobile, contacts, connections,
    site, education, universities, schools, can_post, can_see_all_posts,
    can_see_audio, can_write_private_message, status, last_seen,
    common_count, relation, relatives"""

    filter = "sex,bdate,city,online,blacklisted,can_post,is_favorite,is_friend,can_see_all_posts,can_write_private_message,counters,last_seen"

    tmpus = count_user()
    url_page = set()
    for x in range(0, tmpus, 999):
        url_page.add("https://api.vk.com/method/groups.getMembers?group_id=" + group_id + "&params=id_asc&fields="+filter+"&count=1000&offset="+str(x)+"&access_token=" + token + "&v=5.52")
    return url_page

def get_user():
    user_notgood = set()
    user_good = set()
    user_notsex = set()
    user_woman = set()
    user_man = set()
    user_blacklisted_true = set()
    user_blacklisted_false = set()
    user_writeadmin = set()
    is_favorite = set()
    is_friend = set()
    can_see_all_posts = set()
    can_write_private_message = set()
    #last_seen = set()

    for url in pagination():
        response = urlopen(url,timeout=20)
        #time.sleep(0.2)
        data = response.read()
        jsn = json.loads(data)
        for us in jsn["response"]["items"]:
            #print (us)
            if 'deactivated' in us:
                user_notgood.add(us["id"])
                if 'blacklisted' in us:
                    if us["blacklisted"] == 1: user_blacklisted_false.add(us["id"])

            else:
                user_good.add(us["id"])
                if us["sex"] == 0: user_notsex.add(us["id"])
                if us["sex"] == 1: user_woman.add( us["id"])
                if us["sex"] == 2: user_man.add( us["id"])

                if 'blacklisted' in us:
                    if us["blacklisted"] == 1: user_blacklisted_true.add(us["id"] )

                if 'can_post' in us:
                    if us["can_post"] == 1: user_writeadmin.add(us["id"] )

                if 'can_see_all_posts' in us:
                    if us["can_see_all_posts"] == 1: can_see_all_posts.add(us["id"] )

                if 'is_favorite' in us:
                    if us["is_favorite"] == 1: is_favorite.add( us["id"] )

                if 'is_friend' in us:
                    if us["is_friend"] == 1: is_friend.add( us["id"] )

                if 'can_write_private_message' in us:
                    if us["can_write_private_message"] == 1: can_write_private_message.add(us["id"])

                #if 'last_seen' in us:
                #    date_last = (datetime.datetime.fromtimestamp(int((us["last_seen"]["time"]))).strftime( '%Y-%m-%d' )) #'%Y-%m-%d %H:%M:%S'
                #    now = datetime.datetime.now().strftime( '%Y-%m-%d' )
                #    if date_last == now: last_seen.add(us["id"])

    print ("Заблокированных или неактивных пользователей: " + str(len(user_notgood)))
    print("Активные пользователи: " + str( len( user_good ) ) )
    print("    Из них мужчин: " + str( len( user_man ) ) )
    print("    Из них женщин: " + str( len( user_woman ) ))
    print("Заблокированно администрацией группы (активные акаунты): " + str( len(user_blacklisted_true) ) )
    print("Заблокированно администрацией группы (неактивные акаунты): " + str( len( user_blacklisted_false ) ) )
    print ("-------------------------------------------------------------")
    print( "Пользователи с разрешенным просмотром: " + str( len( can_see_all_posts ) ) )
    print( "Ядро группы с разрешением на публикацию: " + str( len( user_writeadmin ) ) )
    print( "Взаимосвязаны с администратором: " + str( len( is_favorite ) ) )
    print( "Административный круг: " + str( len( is_friend ) ) )
    print( "Доступ на приватные сообщения: " + str( len( can_write_private_message ) ) )
    print( "-------------------------------------------------------------" )
    #print( "Сегодня в ВК заходило: " + str( len(last_seen ) ) )

get_user()
