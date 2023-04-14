from telegram import client

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()