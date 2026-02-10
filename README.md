для генерациия секретного ключа для jwt создаем папку certs в корне сервиса a

генерация приватного ключа 

'''shell
openssl genrsa -out private.pem 2048
'''

генерация публичного ключа 

'''shell
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
'''