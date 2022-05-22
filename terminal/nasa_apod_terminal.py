from time import sleep
import nasa_apod
import os
import ctypes

user_api_url = None
user_apod = None

def show_help():
    print('→NASA APOD TERMINAL HELP←\n    →help: Show this.\n    →get: Gets the media from current NASA APOD API Get request\n    →save <path>: saves NASA APOD Image and explanation in <path>\n    →set-url <url>: Sets the NASA APOD API Get request Url.\n    →exit: Exits the program.\n    →set-desktop: Sets the current NASA APOD as desktop image, only temporary, goes to black after system restart.')

def set_desktop():
    already_exists = os.path.exists('APOD.jpg')
    if not already_exists:
        user_apod.save_media(os.getcwd(), False)

    ctypes.windll.user32.SystemParametersInfoW(20, 0, f'{os.getcwd()}\APOD.jpg' , 0)

    if not already_exists:
        sleep(0.050)
        os.remove('APOD.jpg')

def main():
    global user_api_url
    global user_apod

    user_input = input('NASA APOD → ')
    if user_input == 'help':
        show_help()
    else:
        commands = user_input.split(' ')
        if commands[0] == 'set-url':
            user_api_url = commands[1]
            user_apod = nasa_apod.get_nasa_apod(user_api_url)
        else:
            if user_apod is None:
                print('→Must set url first! "set-url <url>"←')
                return

        if commands[0] == 'get':
            user_apod.get_media()

        if commands[0] == 'save':
            if user_apod.media is None:
                print('→Must get media first! "get"←')
                return
            if len(commands) == 2:
                user_apod.save_media(commands[1])
            else:
                user_apod.save_media(os.getcwd())

        if commands[0] == 'set-desktop':
            if user_apod is None:
                print('→Must get media first! "get"←')
                return
            if user_apod.media is None:
                print('→Must get media first! "get"←')
                return
            set_desktop()

        if commands[0] == 'exit':
            print('NASA APOD | Exiting...')
            exit()

while True:
    print('→NASA APOD TERMINAL←')
    user_input = input('NASA APOD | Set NASA API URL first → set-url https://api.nasa.gov/planetary/apod?api_key=BDgmN5ZwPvfydl3vOJms7netc2VbaaptisdvdKlM')
    if user_input == 'help':
        print('→→→Set NASA API URL First←←←')
        show_help()
    else:
        user_api_url = user_input
        user_apod = nasa_apod.get_nasa_apod(user_api_url)
        break

while True:
    main()