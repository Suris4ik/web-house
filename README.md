# 🏠 Web House — Категоризированная блог-платформа

## 📌 Описание
Веб-приложение на Flask, включающее интерфейс пользователя и REST API (v1 и v2).
Позволяет:
- Регистрироваться и входить в аккаунт
- Создавать/удалять посты
- Создавать категории
- Работать с REST API (GET, POST, PUT, DELETE)

## 🚀 Как запустить

```bash
pip install -r requirements.txt
и запустите app.py
```

Открой в браузере [http://localhost:8080](http://localhost:8080)

## 🧪 API

REST API:
- GET /api/v2/posts — список постов
- POST /api/v2/posts — создать пост
- GET /api/v2/categories — категории
- Авторизация через flask-login

## ⚙️ Технологии

- Flask
- Flask-RESTful
- Flask-Login
- SQLAlchemy
- WTForms
- Bootstrap
- Jinja2

## 📁 Структура проекта

```
├── app/               # Точка входа и маршруты
├── api/               # REST API v1 и v2
├── templates/         # Шаблоны Jinja2
├── static/            # CSS, изображения
├── forms/             # Формы WTForms
├── data/              # SQLAlchemy модели и сессии
├── db/                # SQLite база
└── test/              # Юнит-тесты
```

## 🔒 Авторизация

- Регистрация / логин
- Ограничение доступа к функционалу для гостей

