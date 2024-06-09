#!/usr/bin/env python3
import configparser
import json
import os
from datetime import datetime, date, timezone
from configparser import ConfigParser

import requests
from requests import Response

# path to the token file
config_folder: str = 'Config'
token_file: str = config_folder + '/HoneygainToken.json'
config_path: str = config_folder + '/HoneygainConfig.toml'

header: dict[str, str] = {'Authorization': ''}

print('Started HoneygainAutoClaim!')

def create_config() -> None:
    """
    Creates a config with default values.
    """
    print('Generating new Config!')
    cfg: ConfigParser = ConfigParser()

    cfg.add_section('User')
    email: str = os.environ['HG_EMAIL'].replace('%', '%%')
    cfg.set('User', 'email', f"{email}")
    password: str = os.environ['HG_PASSWORD'].replace('%', '%%')
    cfg.set('User', 'password', f"{password}")

    cfg.add_section('Settings')
    cfg.set('Settings', 'Lucky Pot', 'True')
    cfg.set('Settings', 'Achievements', 'True')

    cfg.add_section('Url')
    cfg.set('Url', 'login', 'https://dashboard.honeygain.com/api/v1/users/tokens')
    cfg.set('Url', 'pot', 'https://dashboard.honeygain.com/api/v1/contest_winnings')
    cfg.set('Url', 'balance', 'https://dashboard.honeygain.com/api/v1/users/balances')
    cfg.set('Url', 'achievements', 'https://dashboard.honeygain.com/api/v1/achievements/')
    cfg.set('Url', 'achievement_claim', 'https://dashboard.honeygain.com/api/v1/achievements/claim')

    with open(config_path, 'w') as configfile:
        configfile.truncate(0)
        configfile.seek(0)
        cfg.write(configfile)


def get_urls(cfg: ConfigParser) -> dict[str, str]:
    """
    :param cfg: config object that contains the config
    :return: a dictionary with all urls of the config
    """
    urls_conf: dict[str, str] = {}
    try:
        urls_conf: dict[str, str] = {'login': cfg.get('Url', 'login'),
                                     'pot': cfg.get('Url', 'pot'),
                                     'balance': cfg.get('Url', 'balance'),
                                     'achievements': cfg.get('Url', 'achievements'),
                                     'achievement_claim': cfg.get('Url', 'achievement_claim')}
    except configparser.NoOptionError or configparser.NoSectionError:
        create_config()
    return urls_conf


def get_login(cfg: ConfigParser) -> dict[str, str]:
    """
        :param cfg: config object that contains the config
        :return: a dictionary with all user information of the config
        """
    user: dict[str, str] = {}
    try:
        user: dict[str, str] = {'email': cfg.get('User', 'email'),
                                'password': cfg.get('User', 'password')}
    except configparser.NoOptionError or configparser.NoSectionError:
        create_config()
    return user


def get_settings(cfg: ConfigParser) -> dict[str, bool]:
    """
        :param cfg: config object that contains the config
        :return: a dictionary with all settings of the config
        """
    settings_dict: dict[str, bool] = {}
    try:
        settings_dict: dict[str, bool] = {'lucky_pot': cfg.getboolean('Settings', 'Lucky Pot'),
                                          'achievements_bool': cfg.getboolean('Settings', 'Achievements')}
    except configparser.NoOptionError or configparser.NoSectionError:
        create_config()
    return settings_dict


if not os.path.exists(config_folder):
    print('Creating config folder!')
    os.mkdir(config_folder)

if not os.path.isfile(config_path) or os.stat(config_path).st_size == 0:
    create_config()

config: ConfigParser = ConfigParser()
config.read(config_path)

if not config.has_section('User') or not config.has_section('Settings') or not config.has_section('Url'):
    create_config()

try:
    # settings
    settings: dict[str, bool] = get_settings(config)
    # urls
    urls: dict[str, str] = get_urls(config)
    # user credentials
    payload: dict[str, str] = get_login(config)
except configparser.NoOptionError or configparser.NoSectionError:
    """
    creating a new config if the there were some changes in the config file
    """
    create_config()
    # settings
    settings: dict[str, bool] = get_settings(config)
    # urls
    urls: dict[str, str] = get_urls(config)
    # user credentials
    payload: dict[str, str] = get_login(config)


def login(s: requests.session) -> json.loads:
    """
    Gets the new token with login data.
    :param s: currently used session
    :return: json containing the new token
    """
    print('Logging in to Honeygain!')
    token: Response = s.post(urls['login'], json=payload)
    try:
        return json.loads(token.text)
    except json.decoder.JSONDecodeError:
        print("You have exceeded your login tries.\n\nPlease wait a few hours or return tomorrow.")
        exit(-1)


def gen_token(s: requests.session, invalid: bool = False) -> str | None:
    """
    Gets the token from the HoneygainToken.json if existent and valid, if not generates a new one.
    :param s: currently used session
    :param invalid: true if the token read before was invalid
    :return: string containing the token
    """
    # creating token.json if not existent
    if not os.path.isfile(token_file) or os.stat(token_file).st_size == 0 or invalid:
        print('Generating new Token!')
        # generating new token if the file is empty or is invalid
        with open(token_file, 'w') as f:
            # remove what ever was in the file and jump to the beginning
            f.truncate(0)
            f.seek(0)
            # get json and write it to the file
            token: dict = login(s)
            # check if token is valid and doesn't have false credentials in it.
            if "title" in token:
                print("Wrong Login Credentials. Please enter the right ones.")
                return None
            json.dump(token, f)

    # reading the token from the file
    with open(token_file, 'r+') as f:
        token: dict = json.load(f)

    # get the token
    return token["data"]["access_token"]


def achievements_claim(s: requests.session) -> bool:
    """
    function to claim achievements
    """
    global header
    if settings['achievements_bool']:
        # get all achievements
        achievements: Response = s.get(urls['achievements'], headers=header)
        achievements: dict = achievements.json()
        # Loop over all achievements and claim them, if completed.
        try:
            for achievement in achievements['data']:
                try:
                    if not achievement['is_claimed'] and achievement['progresses'][0]['current_progress'] == \
                            achievement['progresses'][0]['total_progress']:
                        s.post(urls['achievement_claim'], json={"user_achievement_id": achievement['id']},
                               headers=header)
                        print(f'Claimed {achievement["title"]}.')
                except IndexError:
                    if not achievement['is_claimed']:
                        s.post(urls['achievement_claim'], json={"user_achievement_id": achievement['id']},
                               headers=header)
                        print(f'Claimed {achievement["title"]}.')
        except KeyError:
            if 'message' in achievements:
                token: str = gen_token(s, True)
                if token is None:
                    print("Closing HoneygainAutoClaim! Due to false login Credentials.")
                    exit(-1)
                # header for all further requests
                header = {'Authorization': f'Bearer {token}'}
            return False
        return True

def write_last_completed_date(file_path) -> None:
    """
    Writes current UTC date to the specified file
    :param file_path: path of the file to be written
    """
    with open(file_path, 'w') as file:
        today_date = datetime.now(timezone.utc).date().strftime("%Y-%m-%d")
        file.write(today_date)

def read_last_completed_date(file_path) -> str | None:
    """
    Reads the specified file
    :param file_path: path of the file to be read
    :return: string containing the file's contents
    """
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as file:
        return file.read().strip()

def main() -> None:
    """
    Automatically claims the Lucky pot and prints out current stats.
    """
    # exit if lucky pot has already been claimed today
    file_path = '/tmp/last_completed'
    last_completed_date = read_last_completed_date(file_path)

    today_utc_date = datetime.now(timezone.utc).date().strftime("%Y-%m-%d")
    if last_completed_date == today_utc_date:
        print("HoneygainAutoClaim: Lucky pot has already been claimed today. Exiting.")
        return

    global header
    # starting a new session
    with requests.session() as s:
        token: str = gen_token(s)
        if token is None:
            print("Closing HoneygainAutoClaim! Due to false login Credentials.")
            exit(-1)
        # header for all further requests
        header = {'Authorization': f'Bearer {token}'}
        if not achievements_claim(s):
            print('Failed to claim achievements.')
        # check if the token is valid by trying to get the current balance with it
        dashboard: Response = s.get(urls['balance'], headers=header)
        dashboard: dict = dashboard.json()
        if 'code' in dashboard and dashboard['code'] == 401:
            print('Invalid token generating new one.')
            token: str = gen_token(s, True)
            header['Authorization'] = f'Bearer {token}'
        # gets the pot winning credits
        pot_winning: Response = s.get(urls['pot'], headers=header)
        pot_winning: dict = pot_winning.json()

        if settings['lucky_pot'] and pot_winning['data']['winning_credits'] is None:
            # The post below sends the request, so that the pot claim gets made
            pot_claim: Response = s.post(urls['pot'], headers=header)
            pot_claim: dict = pot_claim.json()
            print(f'Claimed {pot_claim["data"]["credits"]} Credits.')

        # gets the pot winning credits
        pot_winning: Response = s.get(urls['pot'], headers=header)
        pot_winning: dict = pot_winning.json()
        print(f'Won today {pot_winning["data"]["winning_credits"]} Credits.')
        
        if pot_winning['data']['winning_credits'] is not None:
            # Write the claim date to file, unless date changed during execution
            current_utc_date = datetime.now(timezone.utc).date().strftime("%Y-%m-%d")
            if current_utc_date == today_utc_date:
                write_last_completed_date(file_path)

        # gets the current balance
        balance: Response = s.get(urls['balance'], headers=header)
        balance: dict = balance.json()
        print(f'You currently have {balance["data"]["payout"]["credits"]} Credits.')
        print('Closing HoneygainAutoClaim!')

if __name__ == '__main__':
    main()
