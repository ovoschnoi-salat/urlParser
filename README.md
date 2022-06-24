## Url Parser

### Описание

Парсит ссылки со страниц поисковик и проверяет на наличие метрик на сайтах

### Настройка

Перед запуском отредактируйте файл ```conf.py```  
* `folder_for_results` - путь до папки для сохранения результатов
* `use_random_proxy` - переменная, отвечающая за использование прокси при запросах
* `path_to_proxy_list` - путь до файла, который содержит адреса прокси серверов

### Запуск

Установка зависимостей: 
```commandline
python -m pip install requirements.txt
```

Запуск программы:

```
~ python3 main.py --help
usage: main.py [-h] [-S {google,yandex}] [-M {yandex,google,liveinternet,no}] [-N NUM] [-H] input_file

url parser

positional arguments:
  input_file            File with requests to be parsed

optional arguments:
  -h, --help            show this help message and exit
  -S {google,yandex}, --search-engine {google,yandex}
                        Search engine to be used (default: google)
  -M {yandex,google,liveinternet,no}, --metrics {yandex,google,liveinternet,no}
                        metrics (default: no)
  -N NUM, --num NUM     Number of results to be parsed for each request (default: 8)
  -H, --hints           Save hint for each request (default: False)
```
