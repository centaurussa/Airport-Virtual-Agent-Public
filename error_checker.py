from os import environ, system, name, devnull
import subprocess

import json
import smtplib

import pymysql

# Read from settings.txt
with open("docs/settings.txt", "r") as f:
    settings = [i.rstrip() for i in f.readlines()]
    database_enabled =  int(settings[12].split(" = ")[-1])
    smtp_server_enabled = int(settings[13].split(" = ")[-1])


def check_database_server():
    if database_enabled:
        # Fetch Database's Tables From The Configuration File
        db_info = json.loads(open("docs/database.json", "r").read())
        try:
            connection = pymysql.connect(
                host = db_info["host"],
                user = db_info["user"],
                port = db_info["port"],
                password = db_info["password"],
                database = db_info["database"],
                autocommit = True
            )
        except Exception as e:
            if __name__ == "__main__":
                print("\u001b[31mError\u001b[0m: Problem found connecting to MySQL database")
                print(e)
            return False
        else:
            if __name__ == "__main__":
                print("Connected to the database server\u001b[32m successfully\u001b[0m.\nChecking for table names...")

            # Now, check for database's configuration
            with connection:
                db = connection.cursor()
                # Get all table names in the database
                db.execute(f'select table_name from information_schema.tables where table_schema = \'{db_info["database"]}\';')
                tables_in_db = [i[0] for i in db.fetchall()]
            # Group all provided table names in the database.json
            tables_in_database_json = [db_info['flight_information_table'],
                                       db_info['lost_and_found_table'],
                                       db_info['hotels_table'],
                                       db_info['rooms_table']]
            # Case in-sensitive
            tables_in_db = [i.lower() for i in tables_in_db]
            tables_in_database_json = [i.lower() for i in tables_in_database_json]

            # Check if the provided tables same in name and animaton_size
            if len(tables_in_db) == len(tables_in_database_json):
                for table in tables_in_database_json:
                    if table not in tables_in_db:
                        if __name__ == "__main__":
                            print(f"\u001b[31mError\u001b[0m: You provided a table named \"{table}\" in which it does not exist in the database." )
                        return  False
            else:
                if __name__ == "__main__":
                    print("\u001b[31mError\u001b[0m: Length of the provided database table names as a constrains in the database.json does not mach the ones in the database.")
                return False
        # If no error raised, then all good.
        if __name__ == "__main__":
            print("Tables matched\u001b[32m successfully\u001b[0m.")
        return True
    else:
        if __name__ == "__main__":
            print("Since you turned off 'database_enabled' from the docs/seetings.txt, checking for database is not required.")
        return None


def check_smtp_server():
    if smtp_server_enabled:
        # Set SMTP Server
        smtp_info = json.loads(open("docs/smtp_server.json", "r").read())
        try:
            mail = smtplib.SMTP(smtp_info["smtp_server"], smtp_info["port"])
            mail.ehlo()
            mail.starttls()
        except Exception as e:
            if __name__ == "__main__":
                print("\u001b[31mError\u001b[0m: Can't reach SMTP server.")
            return False
        else:
            if __name__ == "__main__":
                print("SMTP server reached\u001b[32m successfully\u001b[0m.\nTrying to login...")

            try:
                mail.login(smtp_info["FROM"], smtp_info["password"])
            except Exception as e:
                if __name__ == "__main__":
                    print("\u001b[31mError\u001b[0m: Please check your E-mail or Password.")
                    print(e)
                return False
            else:
                if __name__ == "__main__":
                    print("Logging-in:\u001b[32m Success\u001b[0m")
                return True

    else:
        if __name__ == "__main__":
            print("Since you tuned off 'smtp_server_enabled' from the docs/seetings.txt, checking for SMTP server is not required.")
        return None



def check_for_dependencies():
        libs = ['pyaudio',
                'pymysql',
                'pyttsx3', # Centaurussa's repo
                'selenium',
    			"screeninfo",
                'PIL',
                'requests',
                'gtts',
                'speech_recognition',
                'googlesearch',
                'bs4',
                'tkinter',
                'pydub'
                ]

        _satisfied = 1
        notInstalled1 = []
        notInstalled2 = []
        notInstalled3 = []
        for lib in libs:
            try:
                exec(f"import {lib}")
            except Exception as e:
                notInstalled1 += [lib]
                _satisfied = 0

        # If it's Linux
        if name != "nt":
            # And if libttspico-utils wasn't installed, don't launch
            retval = subprocess.call(["dpkg","-s","libttspico-utils"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            if retval != 0:
                _satisfied = 0
                notInstalled2.append("libttspico-utils")
        # If it's Windows
        if name == "nt":
            try:
                # And if libttspico-utils wasn't installed, don't launch
                retval = subprocess.call(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            except FileNotFoundError:
                _satisfied = 0
                notInstalled3.append("ffmpeg")
            else:
                if retval != 0:
                    _satisfied = 0
                    notInstalled3.append("ffmpeg")

        # If all set, launch the agent
        if _satisfied == 1:
            if __name__ == "__main__":
                print("Required Libraries/Packages:\u001b[32m Success\u001b[0m")
            return True
        # If not, inform the user with the missing dependencies
        elif _satisfied == 0 and (len(notInstalled1) > 0 or len(notInstalled2) > 0 or len(notInstalled3) > 0):
            if __name__ == "__main__":
                if notInstalled1:
                    print("\u001b[31mError\u001b[0m: The following library/ies or Package/s can't be found or imported:-\n-------Python--------")
                    for lib in notInstalled1:
                        print("- ", lib)
                    print("---------------------\n")
                if notInstalled2:
                    print("-------Linux--------")
                    for package in notInstalled2:
                        print("- ", package)
                    print("--------------------\n")
                if notInstalled3:
                    print("-------Windows--------")
                    for package in notInstalled3:
                        print("- ", package)
                    print("----------------------\n")
                print("\n\nPlease resolve it/them and try again.\n")
        return False

def main():
    print("Check:\n\t 0 - Database\n\t 1 - SMTP Server\n\t 2 - Required Libraries\n\t 3 - All")
    while 1:
        check_for = input("Please provide an integer: ")
        if check_for.isdigit():
            if check_for in ["0", "1", "2", "3"]:
                break
            else:
                print("\u001b[31mError\u001b[0m: Please provide a valid integer.\n")
        else:
            print("\u001b[31mError\u001b[0m: Please provide an integer.\n")

    system('cls' if name == "nt" else "clear")

    if check_for == "0":
        check_database_server()
    elif check_for == "1":
        check_smtp_server()
    elif check_for == "2":
        check_for_dependencies()
    elif check_for == "3":
        ready = 1
        print("Checking Database server...")
        if check_database_server() == False:
            ready = 0
        print("______________________________________________________")
        print("Checking SMTP server...")
        if check_smtp_server() == False:
            ready = 0
        print("______________________________________________________")
        print("Checking required packages and libraries...")
        if check_for_dependencies() == False:
            ready = 0
        if ready is not 0 and __name__ == "__main__":
            print("\n\u001b[32mSuccess\u001b[0m. You're ready to launch the virtual agent.")

        if ready is 0 and __name__ == "__main__":
            print("\n\u001b[31mError\u001b[0m: You can't launch the virtual agent until you resolve the above errors.")
            print("NOTE: If you don't need the database and smtp server to bother you and error-bypass them you can set database_enabled and/or smtp_server_enabled to 0 in /docs/settings.txt.\nCheck README.md for more information.")

if __name__ == "__main__":
    main()
    input("\nError checker finished executing.")
