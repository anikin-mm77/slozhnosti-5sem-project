#!/usr/bin/env bash
set -Eeuo pipefail

# Переходим в директорию скрипта (корень репозитория)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Проверяем наличие Python
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Ошибка: не найден Python 3. Установите Python 3 и повторите попытку." >&2
  exit 1
fi

# Проверяем необходимые файлы
if [ ! -f requirements.txt ]; then
  echo "Ошибка: файл requirements.txt не найден в $(pwd)" >&2
  exit 1
fi

if [ ! -f test.py ]; then
  echo "Ошибка: файл test.py не найден в $(pwd)" >&2
  exit 1
fi

# Создаем/используем виртуальное окружение
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
  "$PY" -m venv "$VENV_DIR"
fi

# Активируем окружение
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Обновляем pip и ставим зависимости
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Запускаем скрипт
exec python test.py
