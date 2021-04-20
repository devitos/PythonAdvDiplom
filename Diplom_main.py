from dipfunctions import get_sex, get_age_from, get_age_to, get_city, user_status, search, get_user_info, write_msg, \
    start, list_work, show_db
from vk_api.longpoll import VkLongPoll, VkEventType
from settings import vk
from tqdm import tqdm
from search_base import start_db, create_db, clear_db
from time import sleep


if __name__ == '__main__':
    connection = start_db()
    create_db()

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
                        sleep(1)
                        get_user_info(user)
                    result = list_work(ids_user)
                    write_msg(event.user_id, f"Вот список подходящих тебе пользователей:")
                    for us in result:
                        write_msg(event.user_id, f"vk.com/id{us['id']} с популярность {us['pop']}")
                    print('ПОИСК ЗАВЕРШЕН')
                if request == 'очистить базу данных':
                    clear_db()
                if request == 'ПОКАЖИ':
                    base = show_db()
                    write_msg(event.user_id, f"ВОТ БАЗА ID {base}")
