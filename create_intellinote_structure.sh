#!/bin/bash
# create_intellinote_structure.sh

mkdir -p intellinote-app/app/routes
mkdir -p intellinote-app/templates/notes
mkdir -p intellinote-app/static/css
mkdir -p intellinote-app/static/js
mkdir -p intellinote-app/static/images

touch intellinote-app/.env
touch intellinote-app/requirements.txt

# Create base files for app
touch intellinote-app/app/__init__.py
touch intellinote-app/app/main.py
touch intellinote-app/app/database.py
touch intellinote-app/app/models.py
touch intellinote-app/app/schemas.py
touch intellinote-app/app/auth.py
touch intellinote-app/app/ai_services.py

# Create routes files
touch intellinote-app/app/routes/__init__.py
touch intellinote-app/app/routes/users.py
touch intellinote-app/app/routes/notes.py

# Create template files
touch intellinote-app/templates/base.html
touch intellinote-app/templates/index.html
touch intellinote-app/templates/login.html
touch intellinote-app/templates/register.html
touch intellinote-app/templates/notes/list.html
touch intellinote-app/templates/notes/detail.html
touch intellinote-app/templates/notes/create.html
touch intellinote-app/templates/notes/edit.html

# Create a static CSS and JS file
touch intellinote-app/static/css/styles.css
touch intellinote-app/static/js/main.js

echo "IntelliNote structure created successfully!"