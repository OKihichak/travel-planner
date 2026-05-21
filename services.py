import requests

ART_API_URL = "https://api.artic.edu/api/v1/artworks"


def validate_artwork(external_id: int):

    response = requests.get(
        f"{ART_API_URL}/{external_id}"
    )

    if response.status_code != 200:
        return None

    data = response.json()["data"]

    return {
        "id": data["id"],
        "title": data["title"]
    }