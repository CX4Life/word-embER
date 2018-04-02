import requests
import json
import sys

AUTH_URL = "https://auth.emergencyreporting.com/Token.php"
API_URL = 'https://api.emergencyreporting.com'
ACCTS = [96]
DEBUG = True


def get_credentials(account):
    ret = None
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


def assert_each_narrative_has_text(returned_narratives):
    for n in returned_narratives:
        assert n


def get_narratives_for_account_number(acct_num):
    credentials, postman_token = get_credentials(acct_num)
    auth_tokens = get_auth_and_refresh_token(credentials, postman_token)

    def get_narratives(auth_tokens, post_token):
        endpoint = '/V2/exposures/narratives?limit=100000'
        headers = define_headers(auth_tokens, post_token)
        all_narratives = get_request_wrapper(endpoint, headers)

        narrative_texts = [x['narrative'] for x in all_narratives['narratives'] if x['narrative']]
        return narrative_texts

    texts = get_narratives(auth_tokens, postman_token)

    if DEBUG:
        with open('{}_checkpoint.json'.format(acct_num), 'w') as checkpoint_file:
            json.dump(texts, checkpoint_file)

    return texts


def word_count(narratives):
    count = 0
    for n in narratives:
        count += len(n.split(' '))
    return count


def print_progress_bar(iteration, total):
    bar_len = 40
    loaded_len = int(40 * (iteration / (total - 1)))
    loaded = '█' * loaded_len
    unloaded = '░' * (bar_len - loaded_len)
    sys.stdout.write('\r' + loaded + unloaded + '\r')
    sys.stdout.flush()
    if iteration == total - 1:
        print()


def main():
    for i, account_number in enumerate(ACCTS):
        get_narratives_for_account_number(account_number)


if __name__ == '__main__':
    main()
