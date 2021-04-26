from random import randrange
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from settings import app_token, vk_app, vk, longpoll
from search_base import get_id, add_user


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
    write_msg(event.user_id, f"Привет, {get_user_name(event.user_id)}. \n С кем ты хочешь познакомиться?(м/ж)")


@wait_msg
def get_sex(request1, event):
    sex = {
        'ж': 1,
        'м': 2
    }
    if request1 in sex.keys():
        write_msg(event.user_id,
                  f"Отлично, ваш ответ {request1} вы ищите мужчину! перейдем к следующему шагу! "
                  f"Какой минимальный возраст?")
    else:
        sex[request1] = 0
        write_msg(event.user_id, f"Отлично, ваш ответ  {request1} вам не важен пол! перейдем к следующему шагу! "
                                 f"Минимальный возраст?")
    return sex.get(request1)


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
        age_to = 99
        write_msg(event.user_id, f"Отлично, вам не важен возраст перейдем к следующему шагу? Назовите город!!!")
    return age_to


@wait_msg
def get_city(request1, event):
    if request1.isdigit():
        write_msg(event.user_id, f"Отлично, вам не важен город перейдем к следующему шагу? семейное положение")
        city = 0
    else:
        write_msg(event.user_id,
                  f"Отлично, вы выбрали город {request1} перейдем к следующему шагу? семейное положение?")
        city = request1

    return city


@wait_msg
def user_status(request1, event):
    us_status = {
        'не женат': 1,
        'не замужем': 1,
        "встречается": 2,
        'помолвлен': 3,
        'помолвлена': 3,
        'женат': 4,
        'замужем': 4,
        'все сложно': 5,
        'в активном поиске': 6,
        'влюблен': 7,
        'влюблена': 7,
        'в гражданском браке': 8
    }
    if request1 in us_status.keys():
        write_msg(event.user_id,
                  f"Вы выбрали {request1}. "
                  f"НАЧИНАЕМ ПОИСК!")
    else:
        us_status[request1] = None
    write_msg(event.user_id,
              f"Вам неважно!"
              f"НАЧИНАЕМ ПОИСК!")
    return us_status.get(request1)


def search(sex, age_from, age_to, city, us_status):
    vk_app = VkApi(token=app_token)
    temp_list = vk_app.method('users.search', {'sex': sex, 'hometown': city, 'age_from': age_from, 'age_to': age_to,
                                               'status': us_status, 'has_photo': 1, 'count': 100})
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
        count_comment = photos['comments']['count']
        photos['pop'] = count_comment + count_like
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
    dbp = get_id()
    print(dbp)
    for user in s_list:
        if user['id'] not in dbp:
            print(user)
            end_res.append(user)
            add_user(user)
        if len(end_res) > 9:
            break
    return end_res


def show_db():
    base = get_id()
    return base
