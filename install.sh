#!/usr/bin/env bash
set -euo pipefail

## Подготовка|Настройки к запуску install.sh
# ==================== Настройки ====================
APP_DIR="${APP_DIR:-$HOME/cloud-storage}"
REPO_URL="https://github.com/MityaiS/cloud.git"
SSH_PORT="${SSH_PORT:-2222}"

# ==================== Функции цвета ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()   { echo -e "${GREEN}[+]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
error() { echo -e "${RED}[x]${NC} $*" >&2; exit 1; }

# ==================== Функция очистки при ошибке ====================
cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        warn "Установка прервана (код $exit_code)."
        if [[ -d "$APP_DIR" ]]; then
            warn "Удаляю $APP_DIR..."
            rm -rf "$APP_DIR"
        fi
        # Остановка и удаление контейнеров проекта, если они были созданы
        if [[ -f "$APP_DIR/docker-compose.yml" ]]; then
            cd "$APP_DIR" && sudo docker compose down -v 2>/dev/null || true
        fi
    fi
}
trap cleanup EXIT

# ==================== Проверки ====================
[[ $EUID -ne 0 ]] || error "Не запускай от root. Используй обычного пользователя с sudo."
command -v apt >/dev/null || error "Скрипт для Ubuntu/Debian (apt)."


#### Начало работы install.sh
# ==================== 1. Обновление системы ====================
log "Обновление системных пакетов"
sudo apt update && sudo apt upgrade -y

# ==================== 2. Базовые пакеты ====================
log "Установка базовых утилит"
sudo apt install -y curl git ufw

# ==================== 3. Docker ====================
if ! command -v docker >/dev/null; then
    log "Установка Docker"
    curl -fsSL https://get.docker.com | sudo sh
    sudo usermod -aG docker "$USER"
    warn "Пользователь $USER добавлен в группу docker. Нужен повторный вход."
else
    warn "Docker уже установлен — пропускаю"
fi

# ==================== 4. Docker Compose ====================
if ! docker compose version >/dev/null 2>&1; then
    log "Установка Docker Compose"
    sudo apt install -y docker-compose-plugin
fi

# ==================== 5. UFW ====================
log "Настройка брандмауэра"
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow "$SSH_PORT"/tcp comment 'SSH'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'
sudo ufw --force enable
sudo ufw status verbose

# ==================== 6. Клонирование ====================
if [[ -d "$APP_DIR" ]]; then
    warn "Папка $APP_DIR уже существует — пропускаю клон"
else
    log "Клонирование проекта в $APP_DIR"
    git clone "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"

# ==================== 7. .env ====================
if [[-f ".env"]]; then 
    warn "Найден готовый .env в текущей папке - использую его."
    cp .env "$APP_DIR/.env"
elif [[-f "$APP_DIR/.env"]]; then 
    warn ".env уже существует в $APP_DIR - не трогаю."
else 
    log "Создание .env из шаблона и генерация паролей..."
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"

    #Генерация
    SECRET_KEY=$(openssl rand -hex 32)
    DB_PASS=$(openssl rand -hex 16)

    #Подстановка
    sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" "$APP_DIR/.env"
    sed -i "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$DB_PASS|" "$APP_DIR/.env"

    warn "Сгенерированы случайные пароли."
fi 

# ==================== 8. Запуск ====================
log "Сборка и запуск контейнеров"

success=false
for i in {1..3}; do
    log "Попытка запуска $i из 3..."
    if sudo docker compose up -d --build; then
        success=true
        break
    fi
    warn "Попытка $i не удалась. Жду 10 секунд..."
    sleep 10
done

if [[ "$success" != "true" ]]; then
    error "Не удалось запустить контейнеры после 3 попыток."
fi

# Проверка, что все контейнеры Up (не Restarting / не Exited)
log "Проверка статуса контейнеров..."
sleep 10
if ! sudo docker compose ps | grep -q "Up"; then
    error "Контейнеры не запустились корректно."
fi

if sudo docker compose ps | grep -qE "Restarting|Exited"; then
    error "Один или несколько контейнеров в состоянии ошибки."
fi

log "Ожидание готовности (15 секунд)"
sleep 15
sudo docker compose ps
sudo docker compose logs --tail 50 backend

# ==================== 9. Итоговый вывод ====================
IP=$(hostname -I | awk '{print $1}')
echo
log "Готово."
echo
echo "  Swagger:  http://$IP:8000/docs"
echo "  MinIO:    http://$IP:9001"
echo
warn "Если Docker установлен впервые — перелогинься, чтобы применилась группа docker."