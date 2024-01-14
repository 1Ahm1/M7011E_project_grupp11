@echo off
set MYSQL_USER=root
set MYSQL_PASSWORD=root
set MYSQL_HOST=localhost
set DATABASE_NAME=bookstore

mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% -h%MYSQL_HOST% < Fastapi-project1/db/main.sql
mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% -h%MYSQL_HOST% %DATABASE_NAME% < Fastapi-project1/db/initial_data.sql


cd Fastapi-project1
start /b cmd /c python main.py

cd ..

cd library-front
start /b cmd /c ng serve --open

