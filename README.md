Пример шифрования файлов.

Помощь
>uv run python main.py --help
>uv run python main.py encryption --help
>uv run python main.py dencryption --help

Зашифровать
>uv run python main.py encryption -f /home/user/Видео/IMG_9100.MP4 -nn /tmp/file.enc

Расшифровать
>uv run python main.py dencryption -f /tmp/file.enc -nn ~/fake.MP4
