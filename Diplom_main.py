from dipfunctions import get_sex, get_age_from, get_age_to, get_city, user_status, search, get_user_info, write_msg, \
    start, list_work
from vk_api.longpoll import VkLongPoll, VkEventType
from settings import vk
from tqdm import tqdm


if __name__ == '__main__':
    longpoll = VkLongPoll(vk)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "СТАРТ":
                    start()
                    sex = get_sex()
                    age_from = get_age_from()
                    age_to = get_age_to()
                    city = get_city()
                    us_status = user_status()
                    print(sex, age_from, age_to, city, us_status)
                    ids_user = search(sex, age_from, age_to, city, us_status)
                    for user in tqdm(ids_user):
                        get_user_info(user)
                    result = list_work(ids_user)
                    write_msg(event.user_id, f"Вот список подходящих тебе пользователей:")
                    for us in result:
                        write_msg(event.user_id, f"vk.com/id{us['id']} с популярность {us['pop']}")
                    print('ПОИСК ЗАВЕРШЕН')
