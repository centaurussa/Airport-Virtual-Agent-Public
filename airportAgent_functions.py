import os
import subprocess
from sys import exit
from random import random
from platform import system
import json
from time import sleep
from datetime import datetime

import pymysql
import pyttsx3
import pyaudio
import wave
from gtts import gTTS  # Google's Text to Speech
from selenium import webdriver
from screeninfo import get_monitors
from pydub import AudioSegment

driver = None

# Set settings
with open("docs/settings.txt", "r") as f:
    settings = [i.rstrip() for i in f.readlines()]
    # Set
    go_to_monitor_index_of = int(settings[2].split(" = ")[-1])
    clear_terminal = int(settings[11].split(" = ")[-1])
    output_device_index = settings[10].split(" = ")[-1]


def aplay_devices():
	'''
	Get playable output sound devices for Linux users

	'''
	output = subprocess.check_output(["aplay", "-l"])
	output = output.decode("utf8")
	devices = []
	for line in output.split("\n"):
		if "card" in line:
			segments = line.split(":")
			devices.append("plughw:" + segments[0][-1] + "," + segments[1][-1])
	return devices


def open_link(link):
    '''Opens a Google Chrome window'''
    chrome_driver = None
    global driver, go_to_monitor_index_of

    # If there is already an opened window, navigate through it
    if driver:
        driver.get(link)
    # Else, open new one
    else:
        # Sart new window
        if system() == "Windows":
            chrome_driver = "excutable/chromedriver.exe"
        elif system() == 'Darwin':
            chrome_driver = 'excutable/chromedriver_mac'
        else:
            chrome_driver = 'excutable/chromedriver_linux'
        chrome_options = webdriver.ChromeOptions();
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', "load-extension"]);
        driver = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)

        # Take the window to the second screen -as could be defined in settings.txt-
        if go_to_monitor_index_of > -1:
            driver.set_window_position(get_monitors()[go_to_monitor_index_of].x+1, 0)
        driver.fullscreen_window()
        driver.get(link)
    return driver


def kill_chrome(driver_para):
    '''Closes past session's Google Chrome window'''
    global driver

    if driver_para: # If guest browser is opened, close it.
        driver_para.quit()
        driver = None


def scroll_window(val):
    '''Scrolls a window the cursor currently pointing at'''
    last_height = driver.execute_script("return document.documentElement.scrollTop")
    driver.execute_script(f"window.scrollTo(0, {last_height + val});")


def current_seconds():
    '''Return number of seconds passed till -for the day- before calling the
       function'''

    current = datetime.now()
    total_seconds = (current.hour * 3600) + (current.minute * 60) + current.second
    return total_seconds


def animation_state(state, communication_line):
    '''Changing the behavior of the animation while using the communication_line
    as a communication medium between the agent and the animations script.'''

    communication_line.value = state.encode()


def clearer():
    '''Clears the CLI'''

    if clear_terminal:
        os.system("cls" if os.name == "nt" else "clear")


def sql_query(query, all_rows = False):
    '''Connects to the database, executes and returns'''

    db_info = json.loads(open("docs/database.json", "r").read())

    connection = pymysql.connect(
        host = db_info["host"],
        user = db_info["user"],
        port = db_info["port"],
        password = db_info["password"],
        database = db_info["database"],
        autocommit = True
    )
    cursor = connection.cursor()
    with connection:
        status = cursor.execute(query)
        if status == 0:
            return 0
        elif all_rows:
            return cursor.fetchall()
        else:
            return cursor.fetchone()


def filter_voice_input(text):
    '''Convert a series of said numbers from the voice input to int or str'''
    text = ''.join([i for i in text if i != " "])
    # If the entire string contains integers, all find.
    if text.isdigit():
        return text
    # if non-int(s) found< replace any non-int(s) in the list by it's corresponding int value
    else:
        translate = {"one": 1, "two": 2, "to": 2, "three": 3, "four": 4, "for": 4,
                     "five": 5, "six": 6, "sex": 6, "x": 6, "seven": 7, "eight": 8,
                     "ate": 8, "nine": 9, "none": 9, "on": 1}
        for i in translate:
            text = text.replace(i, str(translate[i]))

        text = ''.join([i for i in text if i != " "])
        return text


def cache_clearer():
    '''Removes past/current session\'s activity'''

    to_remove = [".google-cookie", "debug.log"]
    for file in to_remove:
        try:
            if os.path.exists(os.path.join(os.getcwd(), file)):
                os.remove(os.path.join(os.getcwd(), file))
        except PermissionError:
            pass




# Use Google's Text to Speech, save it as wav and play it
def say1(lines, communication_line):
    '''Text parsed to Google\'s Text-to-Speech API
        to return a playable voice'''

    # If "talking" triggered, wite in communication_line the signal of moving the animations
    if "sharedctypes" in str(type(communication_line)):
        animation_state('1', communication_line)

    # If Windows
    if os.name == "nt":
        tts = gTTS(text=lines, lang='en', slow=False)
        tts.save('output_' + str(id(communication_line)) + ".mp3")
        if output_device_index == "auto":
            ms_play_mp3('output_' + str(id(communication_line)) + ".mp3")
        else:
            ms_play_mp3('output_' + str(id(communication_line)) + ".mp3", int(output_device_index))

        cache_clearer()

    # If talking is finished, wite in communication_line the signal of stopping the animations
        if "sharedctypes" in str(type(communication_line)):
            animation_state('0', communication_line)
    # If Linux
    else:
        if "sharedctypes" in str(type(communication_line)):
            animation_state('1', communication_line)
        tts = gTTS(text=lines, lang='en', slow=False)
        file_name = 'output_' + str(id(communication_line)) + ".mp3"
        tts.save(file_name)
        wave_file = AudioSegment.from_mp3(file_name)
        wave_file.export(file_name.split(".")[0] + ".wav", format="wav")

        if output_device_index.lower() != "auto":
            device = aplay_devices()[int(output_device_index)]
            subprocess.run(['aplay', file_name.split(".")[0] + ".wav", '-D', device, "-q"])
        # If device not specified (auto)
        else:
            subprocess.run(['aplay', file_name.split(".")[0] + ".wav", "-q"])

        cache_clearer()
        os.remove(file_name.split(".")[0] + ".wav")
        os.remove(file_name.split(".")[0] + ".mp3")
        if "sharedctypes" in str(type(communication_line)):
            animation_state('0', communication_line)


def ms_play_mp3(file_name, device_index = None):
    '''Play an MP3 on a desired output speaker on Microsoft's operating systems'''

    # Convert MP3 to Wav
    wave_file = AudioSegment.from_mp3(file_name)
    wave_file.export(file_name.split(".")[0] + ".wav", format="wav")
    chunk = 1024

    # Make it ready
    wf = wave.open(file_name.split(".")[0] + ".wav", 'rb')
    p = pyaudio.PyAudio()
    if device_index is not None:
        usable_indexcies = []
        for index in range(p.get_device_count()):
            if p.get_device_info_by_index(index)['maxOutputChannels'] > 0 and "Microsoft Sound Mapper" not in p.get_device_info_by_index(index)['name']:
                usable_indexcies.append(p.get_device_info_by_index(index)['index'])

    try:
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True,
                        output_device_index= (usable_indexcies[device_index] if device_index is not None else None))
    except Exception as e:
        print(e)
    else:
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.close()
        p.terminate()
        wf.close()
        os.remove(file_name.split(".")[0] + ".wav")
        os.remove(file_name.split(".")[0] + ".mp3")


# Use pyttsx3's offline Text to Speech
def say2(lines, communication_line):
    '''Text parsed to pyttsx3's offline Text-to-Speech'''

    # If "talking" triggered, wite in communication_line the signal of moving the animations
    if "sharedctypes" in str(type(communication_line)):
        animation_state('1', communication_line)

    # Linux systems
    if system() == "Linux":
        # If device specified
        lines = "\"<pitch level='140'>" + lines + "</pitch>\""
        lines = lines.replace(".", '<break time="500ms"/>.')
        subprocess.run(['pico2wave', '-w', 'output_' + str(id(communication_line)) + ".wav", '-l', "en-US", lines])
        if output_device_index.lower() != "auto":
            device = aplay_devices()[int(output_device_index)]
            subprocess.run(['aplay', 'output_' + str(id(communication_line)) + ".wav", '-D', device, "-q"])
        # If device not specified (auto)
        else:
            subprocess.run(['aplay', 'output_' + str(id(communication_line)) + ".wav", "-q"])
    # Windows systems
    elif system() == "Windows":
        from winreg import ConnectRegistry, OpenKey, HKEY_LOCAL_MACHINE

        engine = pyttsx3.init()
        engine.setProperty('volume', 1)

        # Set output device source
        if output_device_index.lower() == "auto":
            pass
        else:
            engine.setProperty('output_source', int(output_device_index))

        key_to_read = r"SOFTWARE\Microsoft\Speech\Voices\Tokens\T"

        # Try using Window's regisrered voiceses
        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            k = OpenKey(reg, key_to_read+"TS_MS_EN-US_ZIRA_11.0")
        # If failed, let the library handle it
        except Exception as e:
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 120)
        # If worked, then all set!
        else:
            voice = f"HKEY_LOCAL_MACHINE\\{key_to_read}TS_MS_EN-US_ZIRA_11.0"
            engine.setProperty('voice', voice)
            engine.setProperty('rate', 120)

        engine.say(lines)
        engine.runAndWait()

    if "sharedctypes" in str(type(communication_line)):
        animation_state('0', communication_line)
