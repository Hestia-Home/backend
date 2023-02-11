# Hestia Home
***

1. Тесты
   1. Подтянуть pytest
   2. Начать писать тесты в test_auth

2. Пересмотреть код, добавить документацию
3. Добавить логирование
3. Посмотреть про websocets 
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user_test@example.com",
  "password": "usertest",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "username": "user_test"
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=user_test%40example.com&password=usertest&scope=&client_id=&client_secret='