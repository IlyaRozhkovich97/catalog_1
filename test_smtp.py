import smtplib

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'solod-spb78@yandex.ru'
EMAIL_HOST_PASSWORD = 'qvwukwqtxysnimdi'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

try:
    if EMAIL_USE_SSL:
        server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
    else:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        if EMAIL_USE_TLS:
            server.starttls()

    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("Успешное подключение к SMTP серверу Яндекс")
    server.quit()
except Exception as e:
    print(f"Ошибка подключения к SMTP серверу Яндекс: {e}")
