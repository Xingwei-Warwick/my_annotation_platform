from os.path import isfile
from os import listdir
import subprocess
from utils import get_random_string


def create_user_group(num_user: int):
    num_config_files = len(list(listdir('configs')))

    config_text = 'credentials:\n  usernames:\n'
    for i in range(num_user):
        username = get_random_string(6)
        password = get_random_string(12)
        name = username

        subprocess.run(['cp', f'data/group_{num_config_files-1}.json', f'user_progress/{username}.json'])

        this_user_info = f'    {username}:\n      logged_in: False\n      password: {password}\n      name: {name}\n'
        config_text += this_user_info
    config_text += 'cookie:\n  expiry_days: 3\n  key: some_signature_key\n  name: salient_event\n'

    if isfile('configs/config.yaml'):
        subprocess.run(['mv', 'configs/config.yaml', f'configs/config_{num_config_files-1}.yaml'])
    with open('configs/config.yaml', 'w') as f:
        f.write(config_text)


if __name__ == '__main__':
    create_user_group(2)
