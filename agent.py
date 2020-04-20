def goAirportAgent(parent=None, communication_line=None):
    import os
    import sys
    import signal
    import ctypes
    import multiprocessing
    from time import sleep
    from threading import Thread
    from time import sleep
    from random import random

    import speech_recognition as sr

    import responder
    import airportAgent_functions as aaf

    r = sr.Recognizer()

    # Set
    _i = 0
    driver = None
    _worked = None
    currentUserTicket = None
    _asking_for_flight = False
    _asking_for_lost = False
    _asking_for_hotel = False
    _asking_for_taxi = False
    _hold_number = False
    _hold_destination = False
    _monitor_stop = 0
    if communication_line is None:
        communication_line = random()

    with open("docs/settings.txt", "r") as f:
        settings = [i.rstrip() for i in f.readlines()]
        reset_after_being_idle_for = int(settings[7].split(" = ")[-1])
        input_device_index = settings[9].split(" = ")[-1]
        output_device_index = settings[10].split(" = ")[-1]
        offline_text_to_speech = int(settings[0].split(" = ")[-1].rstrip())

    aaf.clearer()
    print("Please wait...")

    def reset():
        '''Resets current session's variables and activities'''
        global currentUserTicket, _asking_for_flight, _asking_for_lost, _asking_for_hotel, _asking_for_taxi, _hold_number, _hold_destination
        aaf.cache_clearer()
        currentUserTicket = 33
        _asking_for_flight = 33
        _asking_for_lost = 33
        _asking_for_hotel = 33
        _asking_for_taxi = 33
        _hold_number = 33
        _hold_destination = 33
        # If it's a ctypes object, treat it differently
        if "sharedctypes" in str(type(communication_line)):
            communication_line.value = "/go_red".encode()
        aaf.kill_chrome(driver)


    def resetter():
        while not _monitor_stop:
            sleep(3)
            # Reset variables if no user talked to the agent for X seconds
            if (responder.last_activity + reset_after_being_idle_for) > aaf.current_seconds():
                pass
            else:
                reset()

    # Realtime monitoring whether if the agent is idle.
    Thread(target=resetter).start()

    while 1:
        try:
            # Set listening port
            # if 'auto' .. try all indexes till you find one working.
            # if already set to an index, then use that.
            with sr.Microphone(device_index=(_i if input_device_index.lower() == "auto" else int(input_device_index))) as source:
                print("Input Device Index:", (str(_i) + " (auto)" if input_device_index.lower() == "auto" else int(input_device_index)))
                print("Output Device Index:", output_device_index)

                _worked = _i  # If no error raised at device_index=_i,
                              # then the said _i is a source of voice input

                aaf.clearer()  # Clear the screen
                print("Listening...")

                # if agent launched without animations
                if not communication_line:
                    aaf.cache_clearer()

                while 1:  # Keep listening
                    # Filter noise
                    r.adjust_for_ambient_noise(source)

                    # Listen to the port (the source)
                    audio = r.listen(source)
                    try:
                        # Send then hold what Googgle's Speech-to-Text returns
                        text = r.recognize_google(audio)

                        # Respond or do an action
                        refresh_vars = responder.responder(text,
                            communication_line,
                            (aaf.say2 if offline_text_to_speech else aaf.say1),
                            aaf.clearer,
                            currentUserTicket,
                            _asking_for_flight,
                            _asking_for_lost,
                            _asking_for_hotel,
                            _asking_for_taxi,
                            _hold_number,
                            _hold_destination
                            )
                        # Refresh variables
                        currentUserTicket = refresh_vars[0]
                        _asking_for_flight = refresh_vars[1]
                        _asking_for_lost = refresh_vars[2]
                        _asking_for_hotel = refresh_vars[3]
                        _asking_for_taxi = refresh_vars[4]
                        _hold_number = refresh_vars[5]
                        _hold_destination = refresh_vars[6]
                        driver = refresh_vars[7]

                        # Reset if Idle for more than X seconds
                    # Exit from the listening loop if the session ended
                    except SystemExit:
                        # Let resetter know that execution stopped
                        _monitor_stop = 1
                        # clear current session's activity
                        aaf.cache_clearer()
                        # exit chrome if currently working
                        if driver:
                            aaf.kill_chrome(driver)
                        # Remove voice outputs
                        output_file = 'output_' + str(id(communication_line))
                        if os.path.exists(os.path.join(os.getcwd(), output_file + ".wav")):
                            os.remove(os.path.join(os.getcwd(), output_file + ".wav"))
                        if os.path.exists(os.path.join(os.getcwd(), output_file + ".mp3")):
                            os.remove(os.path.join(os.getcwd(), output_file + ".mp3"))

                        # kill parent (Animations; If initialized from there)
                        if parent:
                            os.kill(parent, signal.SIGTERM)
                        # kill self
                        os.kill(os.getpid(), signal.SIGTERM)
                    # Handle the error if voice was not recognized
                    except sr.UnknownValueError:
                        print("Sorry I didn't hear that. Can you repeat that?")
                    except Exception as e:
                        print(e)
                        sleep(5)

        # Inform the user if the device at index of '_i' was not found
        except AssertionError:
            print(f"Device at device_index={_i} was not found, trying another"
                   " one.")
            sleep(3)

        # Check if the input source is being used by another device
        except OSError as e:
            if e.errno == -9998:
                aaf.clearer()
                print(f"device_index at {_i} is being used by another program"
                       " or not available. Trying another one")
                sleep(2)
            else:
                print(e)
                sleep(2)

        # If no input device found at index of '_i', then try another one
        if _worked is None and input_device_index.lower() == "auto":
            _i += 1
        # If it wasn't auto, and reached this place, then the above while
        # already finished exectuing, therefore, break.
        else:
            break

if __name__ == "__main__":
    goAirportAgent()
