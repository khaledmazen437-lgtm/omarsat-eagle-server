#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. تسطيب المكتبات
pip install -r requirements.txt

# 2. تجميع الملفات الثابتة
python manage.py collectstatic --no-input

# 3. تحديث الداتابيز
python manage.py migrate