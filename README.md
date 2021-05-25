# Graph Steal Checker

Проверка исходных текстов программ на плагиат с использованием графового представления (program dependence graph).

Поддержанные языки программирования:
* Python

## Использование

```bash
 go build -o ./bin/main main.go && ./bin/main -p1=./data/prog1.py -p2=./prog2.py -s=0.7 -t=5 -l=0.99
```