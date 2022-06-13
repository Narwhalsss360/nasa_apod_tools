import ctypes
import os
from time import sleep
from requests import Response
from npy import terminal
import nasa_apod

URL_FILE_NAME = 'url.txt'

apod_terminal = terminal.TerminalApp('NASA APOD', ' → ')
apod = None
api_url = ''

def exit_app(statements):
    print('Exiting...')
    exit()

def get(statements, extra_message = ''):
    global apod
    global api_url
    if api_url == '':
        apod_terminal.ask('Set URL: ')

    apod = nasa_apod.get_nasa_apod(api_url)
    if apod is Response:
        print(f'HTTP Error Response: {apod.status_code} {apod.reason} {apod.url}')
    else:
        apod.get_media()
        print(f'Got APOD: {apod.title} {apod.date}{extra_message}')

def load_url():
    global api_url
    if not os.path.exists(URL_FILE_NAME):
        return
    print('Getting APOD...')
    with open(URL_FILE_NAME, 'r') as url_file:
        api_url = url_file.readline()
    get(None, ' use "help" for more.')

def set_url(statements):
    global api_url
    api_url = statements.args[0]
    with open(URL_FILE_NAME, 'w') as url_file:
        url_file.write(api_url)
    
    if '--skip' in statements.flags:
        return
    get(None)

def save(statements):
    global apod
    if apod is None:
        print('Error: Current APOD does not exist yet.')
        return
    if len(statements.args) != 0:
        apod.save_media(statements.args[0], False if '--noinfo' in statements.flags else True)
    else:
        apod.save_media(os.getcwd())

def set_desktop(statements):
    global apod
    if apod is None:
        print('Error: Current APOD does not exist yet.')
        return
    already_exists = os.path.exists('APOD.jpg')
    if not already_exists:
        apod.save_media(os.getcwd(), False)

    ctypes.windll.user32.SystemParametersInfoW(20, 0, f'{os.getcwd()}\APOD.jpg' , 0)

    if not already_exists:
        sleep(0.050)
        os.remove('APOD.jpg')

load_url()

set_url_command = terminal.TerminalCommand('set-url', set_url, ': Sets the API URL as yours.')
get_command = terminal.TerminalCommand('get', get, ': Gets NASA APOD API Response and image.')
save_command = terminal.TerminalCommand('save', save, ': <path?> Saves the APOD in the specified path, if none, saves in file dir.')
set_desktop_command = terminal.TerminalCommand('set-bg', set_desktop, ': Sets the APOD as the desktop background.')
clear_command = terminal.TerminalCommand('clear', terminal.clear, ': Clears the terminal output window.')
exit_command = terminal.TerminalCommand('exit', exit_app, ': Exits the application.')
quit_command = terminal.TerminalCommand('quit', exit_app, ': Exits the application.')
q_command = terminal.TerminalCommand('q', exit_app, ': Exits the application.')

apod_terminal.commands.append(set_url_command)
apod_terminal.commands.append(get_command)
apod_terminal.commands.append(save_command)
apod_terminal.commands.append(set_desktop_command)
apod_terminal.commands.append(clear_command)
apod_terminal.commands.append(exit_command)
apod_terminal.commands.append(quit_command)
apod_terminal.commands.append(q_command)

while True:
    apod_terminal.get()