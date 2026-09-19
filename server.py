import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Сервер запущен.")
print(f"Ожидание подключения по адресу {HOST}:{PORT}...")

client_socket, client_address = server_socket.accept()

print("Клиент подключён.")
print("Адрес клиента:", client_address)

# Счётчик полученных сообщений
message_count = 0

while True:
    data = client_socket.recv(1024)

    if not data:
        print("Клиент отключился.")
        break

    message = data.decode()

    # Проверка команды выхода выполняется до увеличения счётчика,
    # чтобы exit не считался обычным сообщением
    if message.lower() == "exit":
        print("Клиент завершил работу.")
        client_socket.send("Соединение завершено.".encode())
        break

    # Увеличиваем счётчик для обычных сообщений
    message_count += 1

    print(f"Получено сообщение №{message_count}")
    print("Сообщение от клиента:", message)

    response = f"Получено сообщение №{message_count}: {message}"
    client_socket.send(response.encode())

client_socket.close()
server_socket.close()
print("Сервер завершил работу.")