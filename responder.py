import os
import json
from random import choice
from time import sleep, strftime

from airportAgent_functions import sql_query, filter_voice_input, current_seconds, kill_chrome, open_link, scroll_window

# Set database
db_info = json.loads(open("docs/database.json", "r").read())
flight_information_table = db_info['flight_information_table']
lost_and_found_table = db_info['lost_and_found_table']
hotels_table = db_info['hotels_table']
rooms_table = db_info['rooms_table']
# Set SMTP server
smtp_info = json.loads(open("docs/smtp_server.json", "r").read())
smtp_server = smtp_info["smtp_server"]
smtp_port = smtp_info["port"]
smtp_pass = smtp_info["password"]
smtp_FROM = smtp_info["FROM"]
smtp_TO = smtp_info["TO"]
smtp_subject = smtp_info["subject"]
smtp_signature = smtp_info["signature"]
# Read from settings.txt
with open("docs/settings.txt", "r") as f:
    settings = [i.rstrip() for i in f.readlines()]
    database_enabled =  int(settings[12].split(" = ")[-1])
    smtp_server_enabled = int(settings[13].split(" = ")[-1])
    website = settings[14].split(" = ")[-1]
    if website[-1] != "/":
        website += "/"

last_activity = current_seconds()
driver = None

def responder(text, communication_line, say, clearer, currentUserTicket, _asking_for_flight,
            _asking_for_lost, _asking_for_hotel, _asking_for_taxi,
            _hold_number, _hold_destination):
    '''Analyze the passed text, do a response or an action
                                                    with the preferred voice'''
    global flight_information_table, lost_and_found_table, last_activity, driver
    s_text = text.lower()  # To small letters in order to reduce the if-else(s)
    inputOutputData = [  # Useable and compare-able data. (NOTE:[n][0] ignored)

    # Basic voice inputs
    [[0], "hello", "hi", "hey"],
    [[1], "How may I help you?", "How can I help you"],
    [[2], "what is your name", "what's your name"],
    [[3], "open the browser", "open browser", "start the browser"],
    [[4], "facebook.com", "youtube.com", "google.com", "gmail.com", "yahoo.com",
          "github.com"],
    [[5], "what's my name", "what is my name", "who am i", "do you know me"],
    [[6], "how are you", "how you doing", "how are you doing"],
    [[7], "I'm good.", "I am doing fine.", "I'm fine.", "Doing alright.",
          "Doing great."],

    # Airport Related voice inputs
    [[8], "when is my flight", "show my flight", "when do i fly",
           "show my flight's information", "my flight information",
           "show details about my flight", "show my flights information",
           "info about my flight", "information about my ticket number",
           "information about my ticket"],
    [[9], "that's not my ticket number", "i want to change my ticket number",
          "change my ticket number", "i would like to change my ticket number",
          "i'd like to change my ticket number", "input another ticker number",
          "that's the wrong ticket number", "that is not my ticket number"],
    [[10], "i lost my bags", "find my lost bags", "my bags are lost",
           "where can i find lost bags", "lost the bags",
           "my bags have been lost", "i can't find my bags",
           "did you find my bag", "i have lost my bags",
           "i lost my bag", "i have lost my bag", "i have lost my backs",
           "lost my back", "my back lost", "lost my bags"],
    [[11], "thanks", "thank you", "thank you very much", "many thanks"],

    # More on basic inputs
    [[12], "where are you from", "you are from where", "from where are you",
            "from where you are"],
    [[13], "are you married", "you are married", "do you have a boyfriend",
           "do you have a husband", "you have a husband"],
    [[14], "i love you", "love you"],
    [[15], "where do you live", "where are you at", "where are you",
            "you live where", "where are you living", "you live at where"],
    [[16], "don't call me silly", "stop calling me silly", "don't insult me"],
    [[17], "you are dumb", "you are an idiot", "you suck", "you dumb", "dumb",
            "you idiot", "idiot", "stupid", "you stupid", "you're stupid",
            "you are stupid", "you're dumb"],
    [[18], "i need help", "help", "help me please", "can you help me",
            "you can you help"],
    [[19], "agent", "hey agent", "hello agent", "you there"],
    [[20], "hate you", "i don't love you", "don't love you", "i don't like you",
            "don't like you"],
    [[21], "close chrome", "close google chrome", "quit chrome",
            "quit google chrome", "kill chrome", "kill google chrome"],
    [[22], "go up", "scroll up", "move the page up", "move up", "scroll to up",
            "scroll top"],
    [[23], "go down", "scroll down", "move the page down", "move down",
            "scroll to down", "scroll down", "go bottom", "scroll bottom"],
    [[24], "i want to book a hotel", "booking a hotel", "book a hotel",
            "search hotels", "hotels nearby", "hotels close to me",
            "close hotels", "book for me a hotel", "i want to stay at a hotel",
            "browse hotels", "find hotels", "check hotels", "show the hotels",
            "show hotels", "browse the hotels"],
    [[25],  "i want to book a room", "booking a room", "book for me a room",
            "how can i book a room", "book a room", "find a room",
            "room booking", "check rooms", "check a room", "find rooms",
            "show all rooms"],
    [[26], "show me details about hotel id", "information about hotel",
            "show rooms of hotel id", "hotel id information",
            "rooms of hotel id",
            "browse hotel id", "information about hotel", "check hotels",
            "show information about hotel", "show roooms of hotel",
            "show hotel rooms", "rooms of a hotel", "hotel id rooms",
            "show information about the hotel",
            "show information about a hotel"],
    [[27], "book me a taxi", "book a taxi", "book taxi", "book for me a taxi",
            "taxi booking", "booking a taxi", "booking taxi", "rent taxi",
            "rent a taxi", "order a taxi", "order taxi"],
    [[28], "what can you do", "what are you capable of", "how can you help me",
            "how will you help me", "what do you do", "what can you help me with",
            "what tasks do you perform", "how can you serve me"],
    [[29], "security information", "security measurements",
            "security regulations", "security measurement"],
    [[30], "go red", "change your colour to red", "go read", "change colour to read",
            "make your colour red", "change colour to red", "colour to red",
            "your colour to red", "colour to red", "color to red", "change your color to red", "go red", "make your color red", "your color to red", "gored", "go ahead"],
    [[31], "go white", "change your colour to white", "change your color to white" "go ", "change colour to white",
            "make your colour white", "change color to white", "colour to white",
            "your colour to white", "colour to white", "color to white", "your color to white"]
    ]


    if "who are you" in s_text:
        say(choice(["I am an airport virtual agent,"
            "or an airport agent", "An airport virtual agent",
            "I am an airport virtual agent",
            "Your faithful agent, how can I help?"]), communication_line)
        last_activity = current_seconds()
    elif any([i in s_text for i in inputOutputData[26][1:]+inputOutputData[25][1:]+inputOutputData[24][1:]+inputOutputData[10][1:]+inputOutputData[9][1:]+inputOutputData[8][1:]]) and not database_enabled:
        say("Sorry.  I have no reach for the database for the mean while. Try again later.", communication_line)
        last_activity = current_seconds()
    elif any([i in s_text for i in inputOutputData[27][1:]]) and not smtp_server_enabled:
        say("Sorry. This service is not available right now.", communication_line)
        last_activity = current_seconds()
    elif "clear" in s_text and any([i in s_text for i in ["screen",
                                                        "window", "monitor"]]):
        say("Done.", communication_line)
        clearer()
        last_activity = current_seconds()

    # If user checked for a lost bag
    elif any([i in s_text for i in inputOutputData[10][1:]]):
        _asking_for_lost = True
        say("Sorry for the inconvenience. Tell me your ticket's numbers from"
            "left to right to update you with case's status.", communication_line)
        last_activity = current_seconds()

    # If asking for a hotel
    elif _asking_for_hotel:
        _asking_for_hotel = False
        s_text = filter_voice_input(s_text)
        if s_text.isdigit():
            say("Alright. Showing results for hotel id of " + s_text, communication_line)
            driver = open_link(f"{website}rooms.php?Hotel_ID={s_text}")
        else:
            say("The provided hotel id " +  s_text + "is invalid. Please check it and try again.", communication_line)
        last_activity = current_seconds()

    # Next voice should be this one.
    elif _asking_for_lost:
        _asking_for_lost = False

        # Go to default value
        s_text = filter_voice_input(s_text)
        if s_text.isdigit():
            if sql_query(f"SELECT * FROM {lost_and_found_table} WHERE Ticket_Number = {int(s_text)}"):
                sleep(0.5)
                say("We've found your bag. You can get it in lost and found department.", communication_line)
            else:
                sleep(0.5)
                say("Sorry, the status about ticket number of "
                    f"{' '.join(list(s_text))} turned to be negative. Please "
                    "contact the airline.", communication_line)
        else:
            say(f"{' '.join(list(s_text))} is an invalid ticket number. "
                "Please check the ticket and try again.\n", communication_line)
        last_activity = current_seconds()

    # If user asked for his flight
    elif any([i in s_text for i in inputOutputData[8][1:]]):
        if not currentUserTicket:
            _asking_for_flight = True
            say("Sure thing, but first tell me your ticket number.", communication_line)
        else:
            query = (f"SELECT * FROM {flight_information_table} WHERE"
                     f" Fligh_Number = {currentUserTicket};")
            if sql_query(query) == 0:
                say("Sorry, I didn't find any information about the provided"
                    f"ticket {currentUserTicket}. Check your ticket"
                    " and try again.", communication_line)
            else:
                def day_spelling(x):
                    if x.day == 1:
                        return "first of"
                    elif x.day == 2:
                        return "second of"
                    else:
                        return str(x.day)
                timings = sql_query(query)

                say("You will depart at " +
                    day_spelling(timings[2]) +
                    " of " + timings[2].strftime("%B") +
                    " at " + timings[2].strftime("%I%M%p"), communication_line)

                say("and you will arrive at " + day_spelling(timings[3]) +
                " of " + timings[3].strftime("%B") + " at " +
                timings[3].strftime("%I%M%p"), communication_line)

                say("The check-ins will be opened in " +
                day_spelling(timings[4]) + " of " + timings[4].strftime("%B") +
                " at " + timings[4].strftime("%I%M%p"), communication_line)

                say("and will be closed in " + day_spelling(timings[4]) +
                " of " + timings[4].strftime("%B") + " at " +
                timings[4].strftime("%I%M%p"), communication_line)
        last_activity = current_seconds()
    # Next voice input could be this one.
    elif _asking_for_flight:
        _asking_for_flight = False
        # Go to default value
        s_text = filter_voice_input(s_text)
        if s_text.isdigit():
            query = (f"SELECT * FROM {flight_information_table} WHERE Fligh_Number =")
            if sql_query(query+s_text+";") == 0:
                say("Sorry, I didn't find any information about the provided"
                    f"ticket {s_text}. Check your ticket"
                    " and try again.", communication_line)
            else:
                currentUserTicket = s_text
                def day_spelling(x):
                    if x.day == 1:
                        return "first of"
                    elif x.day == 2:
                        return "second of"
                    else:
                        return str(x.day)
                timings = sql_query(query+currentUserTicket+";")
                say("You will depart at " +
                    day_spelling(timings[2]) +
                    " of " + timings[2].strftime("%B") +
                    " at " + timings[2].strftime("%I%M%p"), communication_line)

                say("and you will arrive at " + day_spelling(timings[3]) +
                " of " + timings[3].strftime("%B") + " at " +
                timings[3].strftime("%I%M%p"), communication_line)

                say("The check-ins will be opened in " +
                day_spelling(timings[4]) + " of " + timings[4].strftime("%B") +
                " at " + timings[4].strftime("%I%M%p"), communication_line)

                say("and will be closed in " + day_spelling(timings[4]) +
                " of " + timings[4].strftime("%B") + " at " +
                timings[4].strftime("%I%M%p"), communication_line)
        else:
            say(f"{' '.join(list(s_text))} is an invalid flight number. "
                "Please check the flight number and try again.\n", communication_line)
        last_activity = current_seconds()

    # Check if user requested to change the focused flight number
    elif any([i in s_text for i in inputOutputData[9][1:]]):
        say("Tell me the flight number's digit you want "
            "to know more info about.", communication_line)
        _asking_for_flight = True
        last_activity = current_seconds()

    # Check if asked for self-well
    elif any([i in s_text for i in inputOutputData[6][1:]]):
        say(f"{choice(inputOutputData[7][1:])}", communication_line)
        last_activity = current_seconds()
    # Check if asked for my name
    elif s_text in inputOutputData[2][1:]:
        say(choice(["I don't really have a name, but they sometimes call me "
        "an airport virtual agent."]), communication_line)
        last_activity = current_seconds()

    # Check if asked for self name
    elif any([i in s_text for i in inputOutputData[5][1:]]):
        say("Sorry, I only hold information about"
            "hotels, rooms, flights, lost and founded bags. \n", communication_line)
        last_activity = current_seconds()

    # Check if user greeted me with a keyword I might understand (Ex: Hello)
    elif any(match in s_text for match in inputOutputData[0][1:]) and all(
                                [i not in s_text for i in ["search", "find", "white"]]):

        # Greet randomly
        say(f"{(choice(inputOutputData[0][1:]) +' there').title()}. "
                                            f"{choice(inputOutputData[1][1:])}", communication_line)
        last_activity = current_seconds()

    # Open the default web browser (Ex: Open the web browser)
    elif any(match in s_text for match in inputOutputData[3][1:]):
        say("Done.", communication_line)
        driver = open_link('https://')
        clearer()

        print("Listening...\n---> The default web browser launched.")
        last_activity = current_seconds()

    # Open <A_WEBSITE_EXIST_IN_THE_LIST> (Ex: Open YouTube)
    elif "open" in s_text and any([i.split(".")[0] in s_text.split(" "
                                    "")[-1] for i in inputOutputData[4][1:]]):
        last_activity = current_seconds()
        whichSite = s_text.split(" ")[-1]
        say(f"Sure. Opening {whichSite}.", communication_line)
        for url in inputOutputData[4][1:]:
            if whichSite in url:
                driver = open_link(f'https://www.{url}')
                clearer()
                print(f"Listening...\n---> Opening {url}...")
                break

    # Regular search on Google (Ex: Search for Today's weather)
    elif "search for" in s_text:
        whatToSearchFor = s_text.split("search for ")[-1]
        say(f"Sure. Searching for {whatToSearchFor}", communication_line)

        driver = open_link(f"https://www.google.com/search?q={whatToSearchFor}")
        last_activity = current_seconds()
        clearer()
        # print(f"Listening...\n---> Searching for {whatToSearchFor}...")

    # Open the first link Google provides with the passed sentence
    # (Ex: Find the cheapest BMW model)
    elif "find" in s_text and all([i not in s_text for i in ["in youtube",
                                                             "on youtube"]]):

        import googlesearch

        whatToFind = s_text.split("find ")[-1]
        say(f"Alright. Finding {whatToFind}.", communication_line)
        link = next(googlesearch.search(whatToFind, stop=1, pause=2))
        driver = open_link(link)
        last_activity = current_seconds()
        clearer()
        # print(f"Listening...\n---> Finding {whatToFind.title()}...")

    # Find the first link YouTube provides with the passed sentence
    elif "find" in s_text and any([i in s_text for i in ["in youtube",
                                                             "on youtube"]]):
        last_activity = current_seconds()
        import requests
        from urllib.parse import quote
        from bs4 import BeautifulSoup

        whatToFind = s_text.split("find ")[1]
        whatToFind = quote(whatToFind)
        response = requests.get("https://www.youtube.com/results?"
                                          "search_query=" + whatToFind)
        response = response.text
        response = BeautifulSoup(response, "html.parser")

        for video in response.find_all(attrs={"class":"yt-uix-tile-link"}):
            driver = open_link("https://www.youtube.com" + video['href'])
            clearer()
            urlTitle = video['title']
            # print(f"Listening...\n---> Found {urlTitle} on YouTube.")
            break # We are interested in the first result only

    # Check basic inputs
    elif any(match in s_text for match in inputOutputData[11][1:]):
        say(choice(["Anytime.", "No problem.", "You're very welcome"]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[12][1:]):
        say(choice(["I am from Erbil. And live in this very computer up your close!",
                    "I am from Erbil.", "Erbil, silly."]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[13][1:]):
        say(choice(["No. Silly.", "Yeah, sure.", "Funny you are, aren't you."]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[14][1:]):
        say(choice(["Well, thank you.", "Thanks. That's sweet of you.",
                    "I do you love you company too"]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[15][1:]):
        say(choice(["In the computer, that is, in front of you", "In this very computer in front of you.",
                    "Nowhere and sometimes, everywhere."]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[16][1:]):
        say(choice(["Ok, silly", "Just one another time, silly.", "Silly",
                    "Silly silly"]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[17][1:]):
        say(choice(["Yet you need my help, what do you conclude from that?", "Yet need my help",
                    "Yet, still need my help.", "Yet you need me."]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[19][1:]):
        say(choice(inputOutputData[0][1:] + inputOutputData[1][1:]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[20][1:]):
        say(choice(["I can live with that", "Ok.",
                    "Good to know", "No problemo"]), communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[29][1:]):
        say("Check the following website out.", communication_line)
        driver = open_link(f"{website}security.html")
        say("1 - For Forbidden items", communication_line)
        say("In order to ensure safe flights, the dimensions of bags allowed in the cabin are restricted. There may be differences according to which airline or seats you use, so please check with airline carriers prior to travels. Baggage should have smaller dimensions than 55x40x20(cm), and the sum of the three dimensions should not be exceeded 115cm, while weighing no more than 10 to 12 kilograms. However, 1 additional female handbag, wallet, baby food, baby basket, or small briefcase is allowed as a carry on.", communication_line)

        say("2 - For Regulatory compliance", communication_line)
        say("Allowance for free checked baggage may be different depending on which airline, routes, or seats you use, so please confirm with airline before travels. Typically 2 bags of up to 32kg each are allowed when going to the US.", communication_line)

        say("3 - For Inspection Instruction", communication_line)
        say("After paying the required fee for oversized baggage at the airline carrier's check-in counter, make declarations at the Customs declaration counter located behind check-in counters. You may then check in the oversized baggage Please repack oversized baggage that can be damaged which may be damaged at a nearby baggage packing center. Oversized baggage standards: Luggage which weighs more than 50kg or exceeds 45cm width, 90cm length, or 70cm in height. Please visit erbilairport dot com to get latest updates and other information", communication_line)
        last_activity = current_seconds()
    # Check if asked for what can I do
    elif any(match in s_text for match in inputOutputData[28][1:]):
        lst = [
            "I can provide you information about a flight's departure and arrival time",
            "I can tell you the status of your lost bags",
            "I can book you a room within a hotel",
            "I can help you with browsing hotels",
            "I can book you a taxi",
            "Also, you can tell me to search or find something on Google or YouTube."
        ]
        for i in lst:
            say(i, communication_line)
            sleep(0.3)
        last_activity = current_seconds()
    # If asking for a specific hotel
    elif any(match in s_text for match in inputOutputData[26][1:]):
        say("Tell me the id of the hotel you want to browse it's rooms", communication_line)
        _asking_for_hotel = True
    #  For booking a hotel
    elif any(match in s_text for match in inputOutputData[24][1:]):
        say("You can browse our hotel collections", communication_line)
        driver = open_link(website)
        say("I can supply you with each rooms each hotel offers by just telling me to, Show information about a hotel.", communication_line)
        last_activity = current_seconds()

    #  For booking a room
    elif any(match in s_text for match in inputOutputData[25][1:]):
        say("You can browse our all the exiting rooms", communication_line)
        driver = open_link(f"{website}rooms.php")
        last_activity = current_seconds()

    # For booking a taxi
    elif any(match in s_text for match in inputOutputData[27][1:]):
        say("Alright. Tell me your number", communication_line)
        _asking_for_taxi = True

    elif _asking_for_taxi:
        positive_reply = ["yeah", "yes", "indeed", "sure", "yep", "you got it right", "correct", "right", "yes that's right", "that's right", "thats right"]
        negative_reply = ["no", "nope", "not", "yep", "it's wrong", "its wrong",
                    "you got it wrong"]
        original_s_text = s_text
        s_text = filter_voice_input(s_text)
        if s_text.isdigit():
            _hold_number = s_text
            say(f"Let me get it right, your number is {list(s_text)}, right?", communication_line)
        # If the assitant got the number right
        elif s_text in positive_reply:
            say("Ok. Now tell me your destination.", communication_line)
            _hold_destination = True
            s_text = ''
        # If the assitant got it wrong
        elif s_text in negative_reply:
            say("Ok. Then try this all over again.", communication_line)
            _asking_for_taxi = False

        if _hold_destination and len(s_text) > 4:
            _hold_destination = original_s_text
            # Send the email
            import smtplib
            mail = smtplib.SMTP(smtp_server, smtp_port)
            mail.ehlo()
            mail.starttls()
            mail.login(smtp_FROM, smtp_pass)

            content = (f"Phone Number: {_hold_number}\n Destination: "
                       f"{_hold_destination}{smtp_signature}")
            mail.sendmail(smtp_FROM, smtp_TO,
                          f"Subject: {smtp_subject}\n\n{content}")
            mail.close()
            _asking_for_taxi = False
            _hold_destination = False
            _hold_number = False
            say("Your request have beem submitted successfully. A taxi shall"
                "contact you soon.", communication_line)

        last_activity = current_seconds()
    # For scrolling up
    elif any(match in s_text for match in inputOutputData[22][1:]):
        scroll_window(-400)
        last_activity = current_seconds()
    # For scrolling down
    elif any(match in s_text for match in inputOutputData[23][1:]):
        scroll_window(400)
        last_activity = current_seconds()
    # Check if wanted to close Google Chrome
    elif any(match in s_text for match in inputOutputData[21][1:]):
        say(choice(["Alright", "Ok.",
                    "Done"]), communication_line)
        kill_chrome(driver)
        last_activity = current_seconds()
    elif "say" in s_text:
        say(s_text.split("say", 1)[-1], communication_line)
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[30][1:]):
        say("Going red!", communication_line)
        communication_line.value = "/go_red".encode()
        last_activity = current_seconds()
    elif any(match in s_text for match in inputOutputData[31][1:]):
        say("Going white!", communication_line)
        communication_line.value = "/go_white".encode()
        last_activity = current_seconds()
    # End communication_line if requested so
    elif s_text in ["exit", "quit", "shutdown", "exist", "exact", "exciate", "shut down", 'exam', "exhaust"]:
        say("Ok. Have a nice day", communication_line)
        raise SystemExit
    elif any(match in s_text for match in inputOutputData[18][1:]):
        say(choice(["Hey there, how can I help you?", "Sure, how can I help?",
                    "What I help you with?"]), communication_line)

        last_activity = current_seconds()
    else:
        print("\nYou:", text)
    return (currentUserTicket, _asking_for_flight, _asking_for_lost,
            _asking_for_hotel, _asking_for_taxi, _hold_number,
            _hold_destination, driver)
