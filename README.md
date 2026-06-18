# Clockify

An asynchronous, production-ready time-tracking backend application written in Python and powered by the Django framework. This tool is designed to manage high-throughput productivity tracking, offload intensive reporting data streams, and broadcast instant updates across connected clients.

---

## Features

* **Asynchronous Processing Pipeline:** Integrates **Celery** and **Redis** to offload long-running analytical operations and transactional SMTP emails from the main HTTP thread, optimizing API response times.
* **Real-Time Data Streams:** Implemented full-duplex WebSocket communication routes via **Django Channels** and **Daphne** to handle dynamic, live notification broadcasts across active workspace groups.
* **Automated Productivity Reporting:** Features an advanced metrics engine utilizing **openpyxl** that dynamically aggregates database metrics, compiles them into beautifully formatted Excel sheets, and dispatches them via automated background mail workers.
* **Secure Environment Isolation:** Built with clean environment separation protocols that shield production database credentials and SMTP keys using an untracked local profile layout.
* **RESTful API Interface:** Powered by **Django Rest Framework (DRF)**, featuring secure Token/JWT authentication schemes and full API schema documentation via **drf-spectacular**.

---

## Setting Up Environment Configurations

To ensure absolute environment separation and protect your real email credentials, Clockify relies on local configuration injection.


### 1. Configure the `.gitignore`
Before committing any code to a public repository, ensure your `.gitignore` file contains the local dev settings profile block to prevent leaking passwords:

```text
# Local secret files
clockify/clockify/settings/local.py
2. Build the local.py Template
To get your mail transmission and local server setup working, you must manually build a file named local.py inside clockify/clockify/settings/. Use this structure:

Python
from .base import *

DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "your-actual-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-16-character-google-app-password"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

Installation & Setup
### 2. Clone the Repository
```powershell
Bash
git clone [https://github.com/mhta18/clockify.git](https://github.com/mhta18/clockify.git)
cd clockify
```
### 3. Establish the Virtual Environment
```powershell
python -m venv env
Activate the virtual environment
.\env\Scripts\activate
```
### 4. Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### 5. Database Migrations
```powershell
python manage.py migrate
```
###  6. Running the Application
This architecture operates on a decoupled services model. You must open three separate terminal windows, activate the virtual environment in each, and navigate to the project directory containing manage.py:

#### Terminal 1: Core Web Application Server (Daphne/ASGI Engine)
Handles standard HTTP REST APIs and keeps full-duplex WebSocket channels open.

```powershell
cd clockify
python manage.py runserver
```
#### Terminal 2: Background Task Worker Process (Celery)
Listens to the Redis broker queue to process asynchronous tasks (like email dispatching and report calculations).

```powershell
cd clockify
celery -A clockify worker --loglevel=info --pool=solo --concurrency=1
```
#### Terminal 3: Periodic Event Scheduler (Celery Beat)
Triggers scheduled timeline checks and automates routine cron-like reporting sequences.

```powershell
cd clockify
celery -A clockify beat --loglevel=info
```
## Project Architecture Overview
```plaintext
clockify/ (Outer Root)
├── env/                         # Isolated Third-Party Python Dependencies
├── manage.py                    # Django Administrative Entrypoint
├── requirements.txt             # Project Package Manifest
└── clockify/ 
    ├── settings/
    │   ├── base.py              # Global Application Configuration Defaults
    │   └── local.py             # Protected Development Environment Secrets
    ├── asgi.py                  # Asynchronous WebSocket Routing Router
    ├── celery.py                # Asynchronous Worker Process Lifecycle Hook                 
    └── urls.py                  # Top-Level Endpoint Route Registry
```
