Парсер собирает все списки подавших заявление в СПбПУ на очное форму бюджета.
Происходит сортировка списков по БВИ/баллам
Так же можно посмотреть ФИО подавшего заявление (на сайте СПбПУ этого сделать нельзя)
Все собранные данные сохраняются в папке parsed_data/. Имя файла - код направления

Чтобы запустить парсер, следуйте инструкции:
1. Сохраните проект локально
2. Перейдите в папку проекта
3. Выполните команды в терминале:
  pip install poetry
  $HOME/.local/bin/poetry install  - для UNIX
  %APPDATA%\Python\Scripts\poetry install  - для Windows
4. Запустите файл main.py из виртуального окружения poetry shell

  если код падает с ошибкой, обновите cookies и headers в config.py