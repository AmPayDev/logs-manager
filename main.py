import logging
import time
import requests
import schedule

BOT_CALLBACK_FILE_URL = 'https://eba8-46-0-170-182.ngrok-free.app/bot/7887265810:AAHUTu_H3Glj7s3oO7VeSKyKIt-QYZWaCUw/log/file/all'


class Cleaner:
    def __init__(self, path: str) -> None:
        self.path = path

    def clear_file(self) -> None:
        with open(self.path, 'w') as file:
            file.truncate(0)
            logging.info('File cleaned')

    def send_log_file_to_bot(self) -> bool:
        with open(self.path, 'r') as file:
            res = {'content': file.read()}
            request = requests.post(url=BOT_CALLBACK_FILE_URL, json=res)
            if request.status_code != 200:
                logging.info('Wrong request')
                return False
            return True


    def proccessing_clean(self) -> None:
        self.send_log_file_to_bot()
        self.clear_file()
        logging.info('All tasks ended successful')


def job() -> None:
    cleaner = Cleaner(path="/Users/dmitriy/Desktop/work/backend/new_backend/logs/all.log")
    cleaner.proccessing_clean()


schedule.every(20).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)