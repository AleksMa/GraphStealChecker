# Graph Steal Checker

Проверка исходных текстов программ на плагиат с использованием графового представления (program dependence graph).

Поддержанные языки программирования:
* Python

## Использование

```bash
go build main.go && ./main -p1=./data/test.py -p2=./data/test.py -s=0.9 -t=100
```