from dipfunctions import *

if __name__ == '__main__':


    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "привет":
                    write_msg(event.user_id,
                              f"Привет, {get_user_name(event.user_id)}. \n С кем ты хочешь познакомиться?(м/ж)")
                    sex = get_sex()
                    age_from = get_age_from()
                    age_to = get_age_to()
                    city = get_city()
                    us_status = user_status()
                    print(sex, age_from, age_to, city, us_status)
                    ids_user = search(sex, age_from, age_to, city, us_status)
                    write_msg(event.user_id, f"Вот список подходящих тебе пользователей:")
                    for ids in ids_user:
                        a = get_pop_by_avatar(ids)