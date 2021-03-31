from vk_api.longpoll import VkLongPoll
from vk_api import VkApi

app_token = ''   # insert token from application for searching
group_token = ''   # insert token from group for chatting
vk = VkApi(token=group_token)
vk_app = VkApi(token=app_token)
longpoll = VkLongPoll(vk)
big_data_base = []
