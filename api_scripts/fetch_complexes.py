import requests
import json

API_KEY = "hlYJEW0gRYmeToyLcciJOIowLK3LQHtudQ4nkZEo"

url = (
    "https://api.sportradar.com/"
    "tennis/trial/v3/en/complexes.json"
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
        "complexes.json",
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
        "✅ complexes.json saved"
    )

else:

    print(response.text)