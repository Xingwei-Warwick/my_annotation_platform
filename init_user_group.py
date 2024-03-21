from os.path import isfile
from os import listdir
import subprocess
from utils import get_random_string
from argparse import ArgumentParser
import json


def create_user_group(num_user: int, target_path: str):
    # base on which file we initial the progress data
    num_config_files = len(list(listdir('configs')))

    with open('data/name_2_source.json', 'r') as f:
        name_2_source = json.loads(f.read())

    config_text = 'credentials:\n  usernames:\n'
    copy_and_paste = ""
    for i in range(num_user):
        username = get_random_string(6)
        print(username)
        password = get_random_string(12)
        name = username
        copy_and_paste += f"{username}, {password}\n"

        name_2_source[username] = target_path

        subprocess.run(['cp', target_path, f'user_progress/{username}.json'])

        this_user_info = f'    {username}:\n      logged_in: False\n      password: {password}\n      name: {name}\n'
        config_text += this_user_info
    config_text += 'cookie:\n  expiry_days: 3\n  key: some_signature_key\n  name: salient_event\n'

    if isfile('configs/config.yaml'):
        subprocess.run(['mv', 'configs/config.yaml', f'configs/config_{num_config_files-1}.yaml'])
    with open('configs/config.yaml', 'w') as f:
        f.write(config_text)
    
    with open('data/name_2_source.json', 'w') as f:
        f.write(json.dumps(name_2_source, indent=4))
    
    with open('data/account_copy_and_paste.txt', 'w') as f:
        f.write(copy_and_paste)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--num_user", type=int, required=True, help="Number of users")
    parser.add_argument("--target_path", type=str, required=True, help="Target progress data path")
    args = parser.parse_args()

    create_user_group(args.num_user, args.target_path)
