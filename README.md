
# CloudStorage
> Облачное хранилище для частного использования. Полный контроль над данными.  

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C7202C?logo=minio&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

## Возможности
- JWT-аутентификация (регистрация и вход)
- Загрузка и удаление файлов
- Квоты на пользователя (по умолчанию 15 ГБ)
- Роли: пользователь и администратор
- Админ-панель (управление квотами и пользователями)
- S3-совместимое хранилище (MinIO)

## Стек 
- **Backend:** Python 3.13, FastAPI, SQLAlchemy 2.0 (async)
- **База данных:** PostgreSQL 15
- **Хранилище:** MinIO (S3)
- **Аутентификация:** JWT, bcrypt
- **Инфраструктура:** Docker, Docker Compose

## Структура проекта  

```
app/ 
├── database/      # подключение к БД
├── repositories/  # запросы sql для работы с БД
├── routers/       # эндпоинты
├── schemas/       # схемы валидации данных
└── services/      # бизнес-логика, MinIO, JWT
```

#### Значения по умолчанию (.env.example)
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changeme
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=cloud_pj

MINIO_BUCKET=cloud-storage
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

SECRET_KEY=change-me-to-random-hex
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Настройка и работа
#### Установка (install.sh)
> **[WARNING]**  
> **Перед запуском в production** обязательно создайте собственный .env со своими значениями рядом с install.sh, он автоматически копирует его в проект. 
```
cp -r /mnt/c/директория_куда_скачали/install.sh ~/
cd ~
./install.sh
```
<!-- ##### **install.sh**: -->
> [+] *Обновляет систему*   
> [+] *Устанавливает базовые утилиты: curl, git, ufw*  
> [+] *Устанавливает (при отсутствии): docker, docker-compose*  
> [+] *Открывает порты: 2222(ssh), 80(http), 443(https)*  
> [+] *Клонирует репозиторий*  
> [+] *Запускает контейнеры: db, minio, backend*

#### Проверка работы
```
cd ~/cloud-storage
docker compose ps
docker compose logs --tail 50 
```

#### Адреса панелей
```
<IP-сервера>:8000 (uvicorn) 
<IP-сервера>:8000/docs (Swagger UI)
<IP-сервера>:9001 (Console Object Storage MinIO)
```

#### Работа с db из терминала
```
docker compose exec db psql -U postgres -d cloud_pj 
```

## API 
#### standard
```
- POST
  ├── /auth/register -> Регистрация
  ├── /auth/login -> Вход
  └── /files/upload -> Загрузка файла
- GET 
  ├── /users/me -> Текущий пользователь
  ├── /users/me/quota -> Информация о квоте 
  └── /files/ -> Список файлов
- DELETE
  └── /files/{id} -> Удаление файла
```

#### admin
```
- GET 
  └── /admin/users -> Все пользователи
- PUT 
  └── /admin/users/{id}/quota -> Изменить квоту
- DELETE 
  └── /admin/users/{id} -> Удалить пользователя
```

## Roadmap
✅ JWT-аутентификация  
✅ Загрузка в MinIO  
✅ Квоты  
❌ Тесты  
❌ Alembic-миграции  