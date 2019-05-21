import requests
from tqdm import tqdm


def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        # 32 MB of dataset
        CHUNK_SIZE = 32768
        total_downloaded = 0
        with open(destination, "wb") as f:
            for chunk in tqdm(response.iter_content(CHUNK_SIZE)):
                total_downloaded += 1
                if total_downloaded % 1024 == 0:
                    # print 'Total = {} KB and {} MB'.format(total_downloaded * 32, total_downloaded * 32 / 1024)
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    print 'Start Downloading'
    save_response_content(response, destination)


if __name__ == "__main__":
    import sys
    if len(sys.argv) is not 3:
        print "Usage: python google_drive.py drive_file_id destination_file_path"
    else:
        # TAKE ID FROM SHAREABLE LINK
        file_id = sys.argv[1]
        # DESTINATION FILE ON YOUR DISK
        destination = sys.argv[2]
        download_file_from_google_drive(file_id, destination)