import logging
import random
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

from django import db

from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from .models import Club, Kudos

BYTES_IN_KB = 1024


class KudosBot:
    def __init__(self):
        log_formatter = logging.Formatter(
            fmt='%(asctime)s :: %(levelname)s :: %(message)s',
            datefmt='%Y/%m/%d %H:%M:%S')
        self.handler = RotatingFileHandler(
            config("LOGFILE"), mode='a',
            maxBytes=BYTES_IN_KB * config("LOFGILE_SIZE_IN_KB", cast=int),
            backupCount=1, encoding=None, delay=0)
        self.handler.setFormatter(log_formatter)
        self.handler.setLevel(logging.INFO)

        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.INFO)

        self.logger.addHandler(self.handler)

        options = Options()
        if not config("VISIBLE_BROWSER", default=False, cast=bool):
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

        ser = Service(config("DRIVER_PATH"))

        self.driver = webdriver.Chrome(
            service=ser, options=options)
        self.login()

        try:
            self.enable_bot()
        except Exception as e:
            print(f"error :: {e} | Emergency disabling bot...")
        finally:
            self.disable_bot()

    def login(self):
        self.driver.get("https://www.strava.com/login")
        self.sleep(config("STRAVA_LOGGING_TIME", cast=int))

        mail = self.driver.find_element(by="id", value="email")
        mail.send_keys(config("STRAVA_EMAIL"))

        password = self.driver.find_element(by="id", value="password")
        password.send_keys(config("STRAVA_PASSWORD"))
        password.send_keys(Keys.RETURN)
        self.sleep(config("STRAVA_LOGGING_TIME", cast=int))

    def go_to_club_recent_activities(self, club_name):
        if club_name.lower() == "following":
            self.driver.get(
                f"https://www.strava.com/dashboard?feed_type=following")
        else:
            self.driver.get(
                f"https://www.strava.com/clubs/{club_name}/recent_activity")
        self.sleep(config("STRAVA_REFRESH_TIME", cast=int))

    def enable_bot(self, clubs_number=5):
        db.connections.close_all()
        self.log_current_time()

        selected_clubs = random.choices(Club.get_all_clubs(), k=clubs_number)
        print(f"info :: selected_clubs:\n{selected_clubs}")

        for club in selected_clubs:
            club_kudos = 0
            kudos_limit = random.randint(10, 16)
            self.go_to_club_recent_activities(club_name=club.name)

            unfilled_kudos = self.driver.find_elements(
                by="xpath", value="//*[@data-testid='unfilled_kudos']")

            if not unfilled_kudos:
                print(f"error :: No unfilled kudos: {unfilled_kudos}")
                break

            new_kudos_quantity = 0

            for kudos_button in unfilled_kudos:
                try:
                    kudos_button.click()
                    k = Kudos(club_id=club.id)
                    k.save()
                except Exception as e:
                    print(f"error while clicking kudos:: {e}")
                    break
                new_kudos_quantity += 1
                club_kudos += 1

                if new_kudos_quantity >= kudos_limit:
                    break
                self.sleep(random.randint(30, 65))

            print(f"info :: Club: {club} | Kudos: {club_kudos}")
            self.logger.info(f"{club.name} | Kudos: {club_kudos}")

    def sleep(self, sleep_time, verbose=False):
        if verbose:
            print(f"info :: Sleeping for: {sleep_time} seconds...")
        time.sleep(sleep_time)

    def disable_bot(self):
        print(f"info :: Disabling bot...")
        self.close_logger()
        self.driver.close()
        self.driver.quit()

    def log_current_time(self):
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M")
        print(f"\ninfo :: Time: {dt_string}")

    def close_logger(self):
        self.handler.close()
        self.logger.removeHandler(self.handler)


def create_bot():
    while True:
        try:
            KudosBot()
        except Exception as e:
            error_msg = f"error while creating bot:: {e}"
            print(error_msg)

        cooldown = config("BOT_COOLDOWN", cast=int)
        print(f"info :: Sleeping for {cooldown} seconds...")
        time.sleep(cooldown)
