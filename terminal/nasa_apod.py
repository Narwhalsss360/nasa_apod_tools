from PIL import Image
import json
from black import main
import requests
from io import BytesIO
import os

class nasa_apod_helper:
    def __init__(self, title, explanation, media_url, date, media_type, copyright):
        self.title = title
        self.explanation = explanation
        self.media_url = media_url
        self.date = date
        self.media_type = media_type
        self.copyright = copyright
        self.media = None

    def get_media(self):
        media_request = requests.get(self.media_url)
        self.media = BytesIO(media_request.content)

    def save_media(self, path, save_explanation=True):
        if save_explanation:
            self.explanation = self.explanation.replace('.', '.\n')
            with open(os.path.join(os.path.dirname(__file__), f'{path}\\APOD Info.txt'), 'w') as info_file:
                info_file.write(f'---{self.title}---\nDate:\n    {self.date}\nCopyright:\n    {self.copyright}    \nExplanation:\n    {self.explanation}')

        if self.media_url.endswith('.gif'):
            print(f'nasa_apod_helper | Image type "gif" not supprted for saving, sorry open here { self.media_url }.')
            return

        if self.media_type == 'image':
            with Image.open(self.media) as image:
                image.save(os.path.join(os.path.dirname(__file__), f'{path}\\APOD.jpg'))
        else:
            print('nasa_apod_helper | Non-image media not supported yet :(.')

def get_nasa_apod(api_url):
    main_request = requests.get(api_url)
    main_json = main_request.json()

    title = json.dumps(main_json["title"]).replace('"', '')
    explanation = json.dumps(main_json["explanation"]).replace('"', '')
    hdurl = json.dumps(main_json["hdurl"]).replace('"', '')
    date = json.dumps(main_json["date"]).replace('"', '')
    media_type = json.dumps(main_json["media_type"]).replace('"', '')
    if not (main_json.get('copyright') is None):
        _copyright = json.dumps(main_json["copyright"]).replace('"', '')
    else:
        _copyright = "None"
    return nasa_apod_helper(title, explanation, hdurl, date, media_type, _copyright)