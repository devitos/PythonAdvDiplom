from random import randrange
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from settings import group_token, app_token, big_data_base, vk_app, vk, longpoll
from pprint import pprint


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


def wait_msg(func):
    def waiting():
        for event1 in longpoll.listen():
            if event1.type == VkEventType.MESSAGE_NEW:
                if event1.to_me:
                    request1 = event1.text
                    result = func(request1, event=event1)
                    break
        return result
    return waiting


def get_user_name(user_id):
    user_info = vk.method('users.get', {'user_ids': user_id})
    user_name = user_info[0]['first_name']
    return user_name


@wait_msg
def start(request1, event):
    if request1 == "СТАРТ":
        write_msg(event.user_id, f"Привет, {get_user_name(event.user_id)}. \n С кем ты хочешь познакомиться?(м/ж)")
    else:
        write_msg(event.user_id, "Я вас не понимаю")


@wait_msg
def get_sex(request1, event):
    if request1 == 'м':
        sex = 2
        write_msg(event.user_id,
                  f"Отлично, ваш ответ {request1} вы ищите мужчину! перейдем к следующему шагу? "
                  f"Какой минимальный возраст?")
    elif request1 == 'ж':
        sex = 1
        write_msg(event.user_id,
                  f"Отлично, вы ищите женищну! ваш ответ {request1} перейдем к следующему шагу? "
                  f"Какой минимальный возраст?")
    else:
        sex = 0
        write_msg(event.user_id, f"Отлично, ваш ответ  {request1} вам не важен пол! перейдем к следующему шагу? "
                                 f"Минимальный возраст?")
    return sex


@wait_msg
def get_age_from(request1, event):
    if request1.isdigit():
        age_from = int(request1)
        write_msg(event.user_id, f"Отлично, вы выбрали {request1} перейдем к следующему шагу? Максимальный возраст?")
    else:
        age_from = 0
        write_msg(event.user_id, f"Отлично, вам не важен возраст перейдем к следующему шагу? Максимальный возраст?")
    return age_from


@wait_msg
def get_age_to(request1, event):
    if request1.isdigit():
        age_to = int(request1)
        write_msg(event.user_id, f"Отлично, вы выбрали {request1} перейдем к следующему шагу? Назовите город?")
    else:
        age_to = 100
        write_msg(event.user_id, f"Отлично, вам не важен возраст перейдем к следующему шагу? Назовите?")
    return age_to


@wait_msg
def get_city(request1, event):
    if request1 is False:
        write_msg(event.user_id, f"Отлично, вам не важен город перейдем к следующему шагу? семейное положение")
        city = 0
    else:
        write_msg(event.user_id,
                  f"Отлично, вы выбрали город {request1} перейдем к следующему шагу? семейное положение?")
        city = request1

    return city


@wait_msg
def user_status(request1, event):
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
    write_msg(event.user_id,
              f"НАЧИНАЕМ ПОИСК!")
    return us_status


def search(sex, age_from, age_to, city, us_status):
    vk_app = VkApi(token=app_token)
    temp_list = vk_app.method('users.search', {'sex': sex, 'hometown': city, 'age_from': age_from, 'age_to': age_to,
                                               'status': us_status, 'has_photo': 1, 'count': 999})
    ids_list_s = list()
    for users in temp_list['items']:
        if users['is_closed'] is False:
            ids = int(users['id'])
            ids_list_s.append({'id': ids})
        else:
            print('Закрытый аккаунт')
    return ids_list_s


def sort_by_pop(any_list):

    def sorting(input_data):
        return input_data['pop']

    any_list.sort(key=sorting, reverse=True)
    return any_list


def get_user_info(user):

    user_id = user['id']
    photo_prof = vk_app.method('photos.get', {'user_id': user_id, 'album_id': 'profile', 'extended': 1})
    for photos in photo_prof['items']:
        count_like = photos['likes']['count']
        count_coment = photos['comments']['count']
        photos['pop'] = count_coment + count_like
    sort_by_pop(photo_prof['items'])
    user['pop'] = 0
    user['photo'] = []
    for photo in photo_prof['items']:
        if len(user['photo']) < 3:
            a = {'type': 'a'}
            for params in (photo['sizes']):
                if params['type'] > a['type']:
                    a = params
            user['photo'].append({'url': a['url'], 'pop': photo['pop']})
        else:
            break
    for ph in user['photo']:
        user['pop'] += ph['pop']
    return user


def list_work(s_list):
    sort_by_pop(s_list)
    end_res = []
    for user in s_list:
        if user not in big_data_base:
            end_res.append(user)
            big_data_base.append(user)
        if len(end_res) > 9:
            break
    return end_res
