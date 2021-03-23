from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from settings import *


vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)

def wait_msg(func):
    def waiting():
        for event1 in longpoll.listen():
            if event1.type == VkEventType.MESSAGE_NEW:
                if event1.to_me:
                    request1 = event1.text
                    result = func(request1)
                    break
        return result
    return waiting

@wait_msg
def start_chat(request1):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "Привет":
                    write_msg(event.user_id, f"Привет, {get_user_name(event.user_id)}. "
                                             f"\nС кем ты хочешь познакомиться?(м/ж)")


@wait_msg
def get_sex(request1):
    if request1 == 'м':
        sex = 2
        write_msg(event.user_id,
                  f"Отлично, ваш ответ {request1} вы ищите мужчину! перейдем к следующему шагу? Какой минимальный возраст?")
    elif request1 == 'ж':
        sex = 1
        write_msg(event.user_id,
                  f"Отлично, вы ищите женищну! ваш ответ {request1} перейдем к следующему шагу? Какой минимальный возраст?")
    else:
        sex = 0
        write_msg(event.user_id, f"Отлично, ваш ответ  {request1} вам не важен пол! перейдем к следующему шагу? "
                                 f"Минимальный возраст?")
    return sex


@wait_msg
def get_age_from(request1):
    if request1.isdigit():
        age_from = int(request1)
        write_msg(event.user_id, f"Отлично, вы выбрали {request1} перейдем к следующему шагу? Максимальный возраст?")
    else:
        age_from = 0
        write_msg(event.user_id, f"Отлично, вам не важен возраст перейдем к следующему шагу? Максимальный возраст?")
    return age_from


@wait_msg
def get_age_to(request1):
    if request1.isdigit():
        age_to = int(request1)
        write_msg(event.user_id, f"Отлично, вы выбрали {request1} перейдем к следующему шагу? Назовите город?")
    else:
        age_to = 100
        write_msg(event.user_id, f"Отлично, вам не важен возраст перейдем к следующему шагу? Назовите?")
    return age_to


@wait_msg
def get_city(request1):
    if request1 != None:
        write_msg(event.user_id, f"Отлично, вы выбрали город {request1} перейдем к следующему шагу? семейное положение?")
        city = request1
    else:
        write_msg(event.user_id, f"Отлично, вам не важен город перейдем к следующему шагу? семейное положение")
        city = 0
    return city


@wait_msg
def user_status(request1):
    if request1 == ('не женат' or 'не замужем'):
        us_status = 1
    elif request1 == 'встречается':
        us_status = 2
    elif request1 == ('помолвлен' or 'помолвлена'):
        us_status = 3
    elif request1 == ('женат' or 'замужем'):
        us_status = 4
    elif request1 == 'все сложно':
        us_status = 5
    elif request1 == 'в активном поиске':
        us_status = 6
    elif request1 == ('влюблен' or 'влюблена'):
        us_status = 7
    elif request1 == 'в гражданском браке':
        us_status = 8
    else:
        us_status = None
    return us_status

def search(sex, age_from, age_to, city, us_status):
    vk = vk_api.VkApi(token=app_token)
    spisok = vk.method('users.search', {'sex': sex, 'hometown': city, 'age_from': age_from, 'age_to': age_to, 'status': us_status,
                         'has_photo':1, 'count': 6})
    ids_list = list()
    for users in spisok['items']:
        if users['is_closed'] == False:
            ids = int(users['id'])
            ids_list.append(ids)
        else:
            print('Закрытый аккаунт')
    return ids_list


def get_pop_by_avatar(user_id):
    vk = vk_api.VkApi(token=app_token)
    photo_prof = vk.method('photos.get', {'user_id': user_id, 'album_id': 'profile', 'extended': 1, 'count': 1})
    count_like = photo_prof['items'][0]['likes']['count']
    count_coment = photo_prof['items'][0]['comments']['count']
    photo_prof['items'][0]['popularity'] = count_coment + count_like
    pop = photo_prof['items'][0]['popularity']
    write_msg(event.user_id, f'Популярность равна {pop}, сслыка vk.com/id{user_id}')
    return


def search_result(ids_list):
    res_list = list()
    for ids in ids_list:
        a = get_pop_by_avatar(ids)
        res_list.append(a)
        print(res_list)


def get_user_name(user_id):
    user_info = vk.method('users.get', {'user_ids': user_id})
    user_name = user_info[0]['first_name']
    return user_name


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})



