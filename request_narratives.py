import requests
import json
import sys
import os

__author__ = 'Tim Woods'
__copyright__ = 'Copyright (c) 2018 Tim Woods'
__license__ = 'MIT'

AUTH_URL = 'https://auth.emergencyreporting.com/Token.php'
API_URL = 'https://api.emergencyreporting.com'
ACCTS = [12, 17, 20, 26, 43, 44, 51, 62, 66, 67, 82, 88, 90, 96, 326,
         387, 628, 814, 1246, 1382, 1430, 1464, 1737, 1824, 2066, 2169,
         2338, 2535, 2635, 2736, 2737, 5002,
         1588, 288, 5798, 5751, 2682, 4508, 5919, 309, 363, 6654, 5346,
         107, 864, 70, 1190, 5164, 2152, 143, 964, 248, 399, 5492, 5082,
         5106, 2301, 6957, 447, 2643, 1811, 5010, 5592, 956, 1549, 2348]


def get_credentials(account):
    with open('creds.json', 'r') as cred_file:
        ret = json.load(cred_file)

    ret['username'] = ret['username'].format(account)
    postman_token = ret['postman_token']
    del (ret['postman_token'])

    return ret, postman_token


def get_auth_and_refresh_token(credentials, post_token):
    payload = json.dumps(credentials)
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': post_token
    }

    response = requests.request("POST", AUTH_URL, data=payload, headers=headers)
    return json.loads(response.text)


def define_headers(auth_tokens, post_token):
    return {
        'Content-Type': "application/json",
        'Authorization': auth_tokens['access_token'],
        'Postman-Token': post_token
    }


def get_request_wrapper(endpoint, headers):
    response = requests.request("GET", API_URL + endpoint, headers=headers)
    return json.loads(response.text)


def get_equipment():
    creds, pt = get_credentials(1500)
    at = get_auth_and_refresh_token(creds, pt)
    print(at)

    endpoint = '/V1/equipment?limit=2000'
    headers = define_headers(at, pt)
    return get_request_wrapper(endpoint, headers)['equipment']


def assert_each_narrative_has_text(returned_narratives):
    for n in returned_narratives:
        assert n


def get_narratives_for_account_number(acct_num):
    credentials, postman_token = get_credentials(acct_num)
    auth_tokens = get_auth_and_refresh_token(credentials, postman_token)

    def get_narratives(auth_tokens, post_token):
        endpoint = '/V2/exposures/narratives?limit=99999&&filter=isCADNarrative eq 0'
        headers = define_headers(auth_tokens, post_token)
        all_narratives = get_request_wrapper(endpoint, headers)

        narrative_texts = [x['narrative'] for x in all_narratives['narratives'] if x['narrative']]
        return narrative_texts
    
    def write_narratives_to_json(narrative_texts, acct_num):
         with open('{}_checkpoint.json'.format(acct_num), 'w') as checkpoint_file:
                  json.dump(narrative_texts, checkpoint_file)
    
    texts = get_narratives(auth_tokens, postman_token)
    write_narratives_to_json(texts, acct_num)


def word_count(narratives):
    count = 0
    for n in narratives:
        count += len(n.split(' '))
    return count


def print_progress_bar(iteration, total):
    bar_len = 40
    loaded_len = int(40 * (iteration / (total - 1)))
    loaded = '█' * loaded_len
    unloaded = '-' * (bar_len - loaded_len)
    sys.stdout.write('\r' + loaded + unloaded + '\r')
    sys.stdout.flush()
    if iteration == total - 1:
        print()


def main():
    for i, account_number in enumerate(ACCTS):
        print_progress_bar(i, len(ACCTS))
        if not os.path.isfile(str(account_number) + '_checkpoint.json'):
            try:
                get_narratives_for_account_number(account_number)
            except Exception:
                print('Error - {}'.format(account_number))


if __name__ == '__main__':
    main()
