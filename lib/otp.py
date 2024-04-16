from threading import Thread


def send_message_handler(phone_number, password):
    print(f"{phone_number} : {password}")


def send_otp(phone_number, password):
    thread = Thread(target=send_message_handler, args=(phone_number, password), daemon=True)
    thread.start()
    thread.join()
