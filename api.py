import logging
import sys
import os
import time
import json

from vk_api import VkApi, VkApiError


logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler('work.log', 'w'),
                                                   logging.StreamHandler(sys.stdout)])

VK_TOKEN = os.getenv('VK_TOKEN')
VK_USER_ID_START = int(input('Enter vk ID you are going to parse: '))


class VkApiParser:

    def __init__(self, token: str, time_to_sleep=0.5):
        self._token = token
        self._get_vk_api()

        self._time_to_sleep = time_to_sleep

    def _get_vk_api(self):
        session = VkApi(token=VK_TOKEN)
        self.api = session.get_api()

    def start_parsing(self, from_user_id: int):
        logging.debug('going to start parse from user %d', from_user_id)
        start = self.api.friends.get(user_id=from_user_id, fields='nickname')
        logging.info('got %d user friends', start['count'])

        start_user_data = self.api.users.get(user_ids=from_user_id)[0]

        total_dict = {VK_USER_ID_START: {'name': start_user_data['first_name'] + ' ' + start_user_data['last_name'],
                      'friends': [{'id': i['id'], 'name': i['first_name'] + ' ' + i['last_name']} for i in start['items']]}}

        user_friends_dict = {from_user['id']:
            {
            'name': from_user['first_name'] + ' ' + from_user['last_name'],
            'friends': [{'id': i['id'], 'name': i['first_name'] + ' ' + i['last_name']} for i in answer]
            }
            for answer, from_user in zip(map(self.parse_friends, start['items']), start['items'])}

        total_dict.update(user_friends_dict)

        return total_dict

    def parse_friends(self, user_id: dict) -> list:
        try:
            answer = self.api.friends.get(user_id=user_id['id'], fields='nickname')
            time.sleep(self._time_to_sleep)
        except VkApiError as e:
            logging.error('couldnt parse user %d reason: %s', user_id['id'], str(e))
            return []
        else:
            logging.info('successfully parsed friends of user %d', user_id['id'])
            return answer['items']


def main():
    parser = VkApiParser(VK_TOKEN)
    result = parser.start_parsing(VK_USER_ID_START)
    save_result(result)


def save_result(data):
    with open('temp_result.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
