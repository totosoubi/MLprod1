import argparse

import requests


def main():
    parser = argparse.ArgumentParser(description="Tester les prédictions GET et POST.")
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    url = f"{args.url.rstrip('/')}/predict"
    features = {"size": 120, "nb_rooms": 3, "garden": 1}

    get_response = requests.get(url, params=features, timeout=10)
    get_response.raise_for_status()
    post_response = requests.post(url, json=features, timeout=10)
    post_response.raise_for_status()
    if get_response.json() != post_response.json():
        raise RuntimeError("Les prédictions GET et POST diffèrent.")
    print(post_response.json())


if __name__ == "__main__":
    main()
