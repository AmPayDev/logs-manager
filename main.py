import logging
import time
import requests
import schedule
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()
BOT_CALLBACK_FILE_URL = env('BOT_CALLBACK_FILE_URL')
# Базовая настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Cleaner:
    def __init__(self, path: str) -> None:
        self.path = path
        self.filenames_list = ['all.log', 'callback.log', 'debug.log', 'django.log', 'request.log']

    def proccessing_clean(self) -> None:
        if not self.send_log_file_to_bot():
            logging.error(
                '>>>>>>>>>>>>>>> Ошибка очистики логов, не удалось обработать лог ботом <<<<<<<<<<<<<<<\n\n\n')
            return None
        else:
            for filename in self.filenames_list:
                self.clear_log_file(filename)
            logging.info('Файл all.log был отправлен в бота')
            logging.info('>>>>>>>>>>>>>>> Все .log файлы были очищены на хосте <<<<<<<<<<<<<<<\n\n\n')

    def send_log_file_to_bot(self) -> bool:
        with open(f"{self.path}/all.log", 'r') as file:
            files = {
                'file': ('all.log', open(f"{self.path}/all.log", 'rb'), 'text/plain')
            }
            request = requests.post(url=f"{BOT_CALLBACK_FILE_URL}/AmPay", files=files, timeout=180)
            if request.status_code != 200:
                logging.error(' !! Except bad response from Logs Bot !!')
                return False
            return True

    def clear_log_file(self, file_name: str) -> None:
        with open(f"{self.path}/{file_name}", "w") as file:
            file.truncate(0)
            file.close()
        logging.info(f'Файл {file_name} очищен')


def job() -> None:
    cleaner = Cleaner(path='/web/logs/')
    logging.info('>>>>>>>>>>>>>>> Старт очистки логов <<<<<<<<<<<<<<<')
    cleaner.proccessing_clean()


schedule.every().day.at("00:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
