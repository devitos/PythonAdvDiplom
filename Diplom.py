from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = input('Token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def wait_msg(func):
# Внутри себя декоратор определяет функцию-"обёртку". Она будет обёрнута вокруг декорируемой,
# получая возможность исполнять произвольный код до и после неё.
    def waiting():
        for event1 in longpoll.listen():
            if event1.type == VkEventType.MESSAGE_NEW:
                if event1.to_me:
                    request1 = event1.text
                    func(request1)
                    write_msg(event.user_id,
                              f"Вы ответили {request1}!!!!!!!!!")
                    break
    return waiting


@wait_msg
def get_sex(request1):
    if request1 == 'м':
        sex = 2
        write_msg(event.user_id,
                  f"Отлично, ваш ответ{request1} вы ищите мужчину! перейдем к следующему шагу? Минимальный возраст?")
    elif request1 == 'ж':
        sex = 1
        write_msg(event.user_id,
                  f"Отлично, вы ищите женищну! ваш ответ{request1} перейдем к следующему шагу? Минимальный возраст?")
    else:
        sex = 0
        write_msg(event.user_id, f"Отлично, ваш ответ{request1} вам не важен пол! перейдем к следующему шагу? Минимальный возраст?")
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
        write_msg(event.user_id, f"Отлично, вы выбрали {request1} перейдем к следующему шагу? ГОРОД?")
    else:
        age_to = 100
        write_msg(event.user_id, f"Отлично, вам не важен возраст перейдем к следующему шагу? ГОРОД?")
    return age_to


@wait_msg
def get_city(request1):
    if request1 == 1:
        age_to = int(request1)
        write_msg(event.user_id, f"Отлично, вы выбрали {request1} перейдем к следующему шагу? Максимальный возраст?")
    else:
        age_to = 100
        write_msg(event.user_id, f"Отлично, вам не важен возраст перейдем к следующему шагу? Максимальный возраст?")
    return city


@wait_msg
def relation():
    return relation


def search(sex, age_from, age_to, city, relation):

    vk.method('search', {'sex': sex})
    return


def get_user_name(user_id):
    user_info = vk.method('users.get', {'user_ids': user_id})
    user_name = user_info[0]['first_name']
    return user_name


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {get_user_name(event.user_id)}. \n С кем ты хочешь познакомиться?(м/ж)")
                get_sex()
                get_age_from()
                get_age_to()

            elif request == "не знаю":
                write_msg(event.user_id, f"{get_user_name(event.user_id)} Пропускаем "
                                         f"От скольки? До скольки?")
            elif request == f"папа":
                write_msg(event.user_id, f"Принято, возраст учтён от до")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
