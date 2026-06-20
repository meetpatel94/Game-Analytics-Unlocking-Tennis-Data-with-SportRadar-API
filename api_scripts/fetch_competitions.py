import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env
API_KEY = os.getenv("API_KEY")

# Check API key
if not API_KEY:
    raise ValueError(
        "❌ API_KEY not found in .env file"
    )

# Build URL
url = (
    "https://api.sportradar.com/"
    "tennis/trial/v3/en/competitions.json"
    f"?api_key={API_KEY}"
)

try:
    # Send request
    response = requests.get(
        url,
        timeout=30
    )

    print(f"Status Code: {response.status_code}")

    # Success
    if response.status_code == 200:

        data = response.json()

        # Create data folder if not exists
        os.makedirs(
            "data",
            exist_ok=True
        )

        # Save JSON
        file_path = os.path.join(
            "data",
            "competitions.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"✅ Data saved successfully: {file_path}"
        )

        # Optional statistics
        competitions = data.get(
            "competitions",
            []
        )

        print(
            f"📊 Total Competitions: {len(competitions)}"
        )

    else:

        print(
            f"❌ API Error: {response.status_code}"
        )
        print(response.text)

except requests.exceptions.Timeout:

    print(
        "❌ Request timed out."
    )

except requests.exceptions.ConnectionError:

    print(
        "❌ Connection error."
    )

except requests.exceptions.RequestException as e:

    print(
        f"❌ Request failed: {e}"
    )

except Exception as e:

    print(
        f"❌ Unexpected error: {e}"
    )