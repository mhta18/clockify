@echo off
cd /d E:\clockify\clockify
call ..\env\Scripts\activate
python manage.py clear_old_notifications