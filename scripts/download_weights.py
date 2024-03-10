import requests
import traceback
import os


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIGHTS_PATH = os.path.join(ROOT_PATH, "weights")
os.makedirs(WEIGHTS_PATH, exist_ok=True)


def download_weights(url: str, filename: str):
    try:
        filename = os.path.join(WEIGHTS_PATH, filename)
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded weights successfully {filename}")

        else:
            print("Downloading weights failed..!")

    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    WEIGHTS_URL = [
        ('https://huggingface.co/spaces/jbrinkma/segment-anything/resolve/main/sam_vit_b_01ec64.pth?download=true',
         'sam_vit_b_01ec64.pth')
    ]
    print("Downloading the weights...")
    for url, filename in WEIGHTS_URL:
        download_weights(url, filename)
    