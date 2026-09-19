import socket
import threading


HOST = "127.0.0.1"
PORT = 6000
NAME = "Client4"


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Регистрация
client_socket.sendto(f"REGISTER|{NAME}".encode(), (HOST, PORT))
data, address = client_socket.recvfrom(1024)
print("[CLIENT]", data.decode())


def receive_messages():
    """Отдельный поток: постоянно читает входящие сообщения."""
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            print(f"\n[ПОЛУЧЕНО] {data.decode()}")
            print("Получатель: ", end="", flush=True)
        except OSError:
            break


# Запускаем поток приёма
recv_thread = threading.Thread(target=receive_messages, daemon=True)
recv_thread.start()

print(f"[{NAME}] Формат ввода: получатель → приоритет → текст")

while True:
    target = input("Получатель: ")
    priority = input("Приоритет (NORMAL/HIGH): ").upper()
    message = input("Сообщение: ")

    data = f"{target}|{priority}|{message}"
    client_socket.sendto(data.encode(), (HOST, PORT))

    if message.lower() == "exit":
        break

client_socket.close()
print(f"[{NAME}] Клиент завершил работу.")