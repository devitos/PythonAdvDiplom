from vk_api.longpoll import VkLongPoll
from vk_api import VkApi

app_token = ''  # СЮДА ВСТАВЛЯЕМ ТОКЕН ПРИЛОЖЕНИЯ
group_token = ''    # СЮДА ВСТАВЛЯЕМ ТОКЕН ГРУППЫ
vk = VkApi(token=group_token)
vk_app = VkApi(token=app_token)
longpoll = VkLongPoll(vk)
big_data_base = []
