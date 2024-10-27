### Mini-Twitter API

## Descrição
O projeto é uma API RESTful construída com Django e Django REST Framework, usando PostgreSQL como banco de dados. Ele permite que usuários se registrem, façam login e gerenciem postagens (criação, leitura, atualização e exclusão). A autenticação é feita via JWT e a API utiliza Redis para cache, com paginação de 10 postagens por vez para melhorar a eficiência. Além disso, implementa um recurso assíncrono com Celery para notificar os usuários sobre novos seguidores, e inclui limitação de requisições e validação de dados para aumentar a segurança e a robustez do sistema.

## Pré-requisitos
- Python 3.x
- Docker
- PostgreSQL

## Instalação e execução
```bash
    git clone <https://github.com/italoflx/mini-twitter.git>
    cd <mini-twitter-main>
    celery -A users.tasks worker --loglevel=info
    python manage.py runserver
```

## Execução dos testes
```bash
    python manage.py test posts
    python manage.py test users
```

## Links 
[Download da documentação (Postman)](https://drive.google.com/file/d/1ZCG5o0VUDGAqk0NM8BnLtP0PU-rQAsoX/view?usp=sharing)
