# telegram-bot
Сбор добровольных пожертвований на исследовательские и экспериментально научные цели.

donate_bot/
├── bot.py              # основной файл запуска
├── config.py           # конфигурация
├── handlers/
│   ├── __init__.py
│   ├── commands.py     # /start, /help, /about, /donate
│   └── payments.py     # обработка платежей
├── keyboards/
│   ├── __init__.py
│   └── inline.py       # inline-клавиатуры
├── texts/
│   ├── __init__.py
│   └── content.py      # ВСЕ ВАШИ ТЕКСТЫ ЗДЕСЬ
├── utils/
│   ├── __init__.py
│   └── stats.py        # статистика сборов
└── requirements.txt
