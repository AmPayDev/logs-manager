import logging
import time
import requests
import schedule
from dotenv import load_dotenv
from os import getenv as env
load_dotenv()
BOT_CALLBACK_FILE_URL = env('BOT_CALLBACK_FILE_URL')


class Cleaner:
    def __init__(self, path: str) -> None:
        self.path = path
        self.filenames_list = ['all.log', 'callback.log', 'debug.log', 'django.log', 'request.log']

    def proccessing_clean(self) -> None:
        self.send_log_file_to_bot()
        for filename in self.filenames_list:
            self.clear_log_file(filename)
        logging.info('All tasks ended successful')

    def send_log_file_to_bot(self) -> bool:
        with open(f"{self.path}/all.log", 'r') as file:
            res = {'content': file.read()}
            request = requests.post(url=f"{BOT_CALLBACK_FILE_URL}/ampay", json=res)
            if request.status_code != 200:
                logging.info('Wrong request')
                return False
            return True

    def clear_log_file(self, file_name: str) -> None:
        with open(f"{self.path}/{file_name}", "w") as file:
            file.truncate(0)
        logging.info(f'File {file_name} cleaned')


def job() -> None:
    cleaner = Cleaner(path=env('LOGS_PATH'))
    cleaner.proccessing_clean()


schedule.every().day.at("00:03").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
