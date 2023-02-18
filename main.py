import requests
import urllib.parse
import os
import argparse

from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='?')
    return parser


def shorten_link(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    shortened_res = requests.post("https://api-ssl.bitly.com/v4/shorten",
                                json={"long_url": url},
                                headers=headers)
    shortened_res.raise_for_status()
    short_url = shortened_res.json()[link]
    return short_url


def is_bitlink(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    url_components = urllib.parse.urlparse(url)
    bitlink_res = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/"
                               f"{url_components.netloc}"
                               f"{url_components.path}",
                               headers=headers
                               )
    return bitlink_res.ok


def count_clicks(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    url_comp = urllib.parse.urlparse(url)
    clicks_res = requests.get(f"https://api-ssl.bitly.com//v4/bitlinks/"
                              f"{url_comp.netloc}"
                              f"{url_comp.path}"
                              f"/clicks/summary",
                              headers=headers)
    clicks_res.raise_for_status()
    clicks_count = clicks_res.json()["total_clicks"]
    return clicks_count


def main():
    load_dotenv()
    token = os.environ['BITLY_TOKEN']

    parser = create_parser()
    command_arguments = parser.parse_args()

    input_url = command_arguments.url

    try:
        if not is_bitlink(input_url, token):
            short_url = shorten_link(input_url, token)
            print(f"Короткая ссылка: {short_url}")
        else:
            clicks_sum = count_clicks(input_url, token)
            print(f"По вашей ссылки перешли {clicks_sum} раз(а)")
    except requests.exceptions.HTTPError:
        print(f'Неверная ссылка: {input_url}')


if __name__ == "__main__":
    main()
