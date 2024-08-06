# Telegram Bot for Product Management

Этот бот на Python предназначен для управления товарами в Telegram. Он позволяет администраторам добавлять и удалять товары, а также загружать фотографии и видео для каждого товара.

## Установка

1. Скачайте репоиторий
2. Установите библиотеку telebot `pip install telebot`
3. Измените `[token]` в 14 строке на токен вашего бота
4. Запустите бота

## Взаимодействуйте с ботом через Telegram. Администраторы могут добавлять товары, отправляя фотографии и видео, а также удалять их по запросу.

### Команды
- **Получение прав Адиминистратора**: Отправьте команду /admin и введите пароль "111". Вдальнейшем вы сможете изменить пароль к админ панели.

## Структура проекта

- main.py: Основной файл с логикой бота.
- photos/: Директория для хранения загруженных фотографий и видео товаров.
- dict.pkl: Файл инвормацией о товарах.
