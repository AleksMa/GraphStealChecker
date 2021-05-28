# Graph Steal Checker

Проверка исходных текстов программ на плагиат с использованием графового представления (program dependence graph).

Поддержанные языки программирования:
* Python

## Установка

Требуются установленные go1.11+ и python3.6+.

```bash
git clone https://github.com/AleksMa/GraphStealChecker.git
pip install -r requirements.txt
```

## Использование

```bash
go build -o ./bin/main main.go && ./bin/main -p=8080
```