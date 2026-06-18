# Clockify 🚀

A high-performance, real-time time tracking and project management platform built with **Django 5.1**, **Django Channels**, **Celery**, and **Redis**. This system architecture cleanly separates heavy background workloads (like complex Excel analytics generation and secure SMTP email dispatching) from the core HTTP request-response thread lifecycle.

---

##  Architecture Overview

Clockify is designed with a modern decoupled, asynchronous processing infrastructure to guarantee lightning-fast REST API responses and persistent concurrent communication handling.

* **Primary Application Server:** Handles standard structural REST API traffic and database transaction state tracking.
* **ASGI Server (Daphne):** Manages asynchronous networking capabilities and persistent, full-duplex WebSocket connections.
* **Message Broker & Channel Layer (Redis):** Serves as a multi-database performance core:
  * `db 0`: Orchestrates Django Channels' data routing layer for stateful WebSocket connections.
  * `db 1`: Acts as the upstream message broker tracking background task priorities.
  * `db 2`: Retains task outcome serialization receipts (Results Backend).
* **Asynchronous Task Workers (Celery):** Runs isolated processing operations across multiple tasks, executing file attachments and SMTP operations in safe threads.

---

## Key Features

* **Real-time Notifications:** Uses structural stateful ASGI connections (`AsyncWebsocketConsumer`) to cleanly dispatch dynamic real-time broadcast packages immediately upon action events.
* **Decoupled Job Lifecycle:** Heavy computing steps are captured cleanly via Celery signature wrappers (`.delay()`), preventing request blocking.
* **Automated Analytical Reports:** Processes relational information fields across `Users`, `Contracts`, and `TimeLog` entries using `openpyxl`. Generates fully custom spreadsheet workbooks utilizing programmatic styling, zebra-striping, dynamic formatting, and automated column width evaluation.
* **Production SMTP Engine:** Integrated cleanly with Google SMTP server endpoints using application-specific verification strings to process secure transactional notifications (OTPs) and multi-part spreadsheet file attachments.

---

##  System Requirements & Dependencies

* **Operating System:** Windows 11 (Development)
* **Runtime:** Python 3.12+
* **Cache Architecture:** Redis Server (Default Port `6379`)

---

##  Setting Up Environment Configurations

To ensure absolute environment separation and protect your real email credentials, Clockify relies on local configuration injection. 

### 1. Configure the `.gitignore`
Before committing any code to a public repository, ensure your `.gitignore` file contains the local dev settings profile block to prevent leaking passwords:

```text
# Local secret files
clockify/settings/local.py


###  Local Environment Configuration

This project uses environment separation to protect sensitive credentials (like SMTP email passwords and secret keys). The main configuration track ignores the local setup file via `.gitignore`. 

To get your mail transmission and local server setup working, you **must** manually build a file named `local.py` inside your settings directory:

 **Path:** `clockify/clockify/settings/local.py`

#### Example `local.py` Template:
```python
from .base import *

# Activate development debugging
DEBUG = True

# Outbound SMTP Mail Service Configurations
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#  REPLACE THESE WITH YOUR OWN REAL GMAIL CREDENTIALS
EMAIL_HOST_USER = "your-actual-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-16-character-google-app-password" or "your-password"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

Terminal 1: Core Django Application (Daphne/ASGI Engine)

PowerShell

.\env\Scripts\activate
cd clockify
python manage.py migrate
python manage.py runserver

Terminal 2: Background Task Worker Process

PowerShell

.\env\Scripts\activate
cd clockify
$env:DJANGO_SETTINGS_MODULE="clockify.settings.local"
celery -A clockify worker --loglevel=info --pool=solo --concurrency=1


Terminal 3: Periodic Task Scheduler Engine (Celery Beat)

PowerShell

.\env\Scripts\activate
cd clockify
$env:DJANGO_SETTINGS_MODULE="clockify.settings.local"
celery -A clockify beat --loglevel=info

