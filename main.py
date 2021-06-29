import os
import time
import uuid
import dotenv
import urllib
import random
import requests
import datetime

dotenv.load_dotenv()
API_URL = os.getenv("API_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
CAPTIONS = [
    "#generativeart #ai #art #artist #instagood #artwork #like #instagram #beautiful #style #nature #painting #illustration #digitalart #design #abstractart #artificialintelligence #neuralart #aiartcommunity #machinelearning #aiartists #algorithmicart #neuralstyle #neuralnetworks #artgallery #daily #contemporaryart #modernart #digitalpainting",
    "#artgallery #art #artwork #artist #contemporaryart #painting #artoftheday #artistsoninstagram #arte #instaart #drawing #fineart #artcollector #abstractart #modernart #gallery #artlovers #arts #artsy #illustration #sketch #design #artistic #abstract #creative #photography #paint #oilpainting #interiordesign #bhfyp",
]


def main():
    """Publishes random AI generated image to Instagram"""

    ratelimit_raw = requests.get(
        f"{API_URL}/{INSTAGRAM_ACCOUNT_ID}/content_publishing_limit",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )

    ratelimit = ratelimit_raw.json()

    if ratelimit_raw.status_code != 200:
        print("failed to find ratelimit")
        print(ratelimit)
        print("\n\n")
        return

    if ratelimit["data"][0]["quota_usage"] >= 25:
        print(f"skipping upload, quote usage is at - {ratelimit['data'][0]['quota_usage']}\n\n")
        return

    caption = urllib.parse.quote_plus(random.choice(CAPTIONS))
    media_raw = requests.post(
        f"{API_URL}/{INSTAGRAM_ACCOUNT_ID}/media?image_url=https://thisartworkdoesnotexist.com/?{uuid.uuid4()}&caption={caption}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )

    media = media_raw.json()

    if media_raw.status_code != 200:
        print("failed to upload media")
        print(media)
        print("\n\n")
        return

    creation_id = media["id"]

    media_publish_raw = requests.post(
        f"{API_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish?creation_id={creation_id}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )

    media_publish = media_publish_raw.json()

    if media_publish_raw.status_code != 200:
        print("failed to publish media")
        print(media_publish)
        print("\n\n")
        return

    print(f"successfully posted image\n\n")


if __name__ == "__main__":

    while True:
        now = datetime.datetime.now()
        if now.hour == 12 or now.hour == 24:
            main()
            time.sleep(21600)
        time.sleep(3600)
