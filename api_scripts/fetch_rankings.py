import requests
import json

API_KEY = "hlYJEW0gRYmeToyLcciJOIowLK3LQHtudQ4nkZEo"

url = (
    "https://api.sportradar.com/"
    "tennis/trial/v3/en/"
    "double_competitors_rankings.json"
    f"?api_key=hlYJEW0gRYmeToyLcciJOIowLK3LQHtudQ4nkZEo"
)

response = requests.get(
    url,
    timeout=30
)

print("Status:", response.status_code)

if response.status_code == 200:

    data = response.json()

    with open(
        "double_competitors_rankings.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        "✅ double_competitors_rankings.json saved"
    )

else:

    print(response.text)