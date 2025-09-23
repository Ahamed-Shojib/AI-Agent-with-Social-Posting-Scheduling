# AI-Agent-with-Social-Posting-Scheduling 

## Task-1 & 3 : Social Media Posting Agent + Analytics Dashboard
Django + DRF reference solution for the challenge: a lightweight AI-enabled scheduler that accepts text + image, target platforms (mock), scheduled time, stores everything in SQLite, uses APScheduler with a persistent jobstore to auto-publish, and exposes listing/status APIs
This project is a Django application for scheduling social media posts with an AI-powered analytics dashboard.

-----

### 1. Features

* **Scheduled Posting:** Schedule posts for Facebook, Twitter, and LinkedIn.
* **Celery Task Queue:** Handles background post publishing.
* **AI-Powered Insights:** Generates simple insights based on post performance.
* **Analytics Dashboard:** A frontend to visualize post status and AI insights.
* **RESTful API:** Manages posts and provides data for the dashboard.

-----

### 2. Technologies Used

* **Backend:** Python 3.10+, Django 5.2, Django REST Framework, Celery, Redis
* **Frontend:** Bootstrap 5, Chart.js, HTML, CSS, JavaScript
* **Database:** SQLite3

-----

### 3. Getting Started (Linux)

#### Prerequisites

* Python 3.10+
* pip (Python package installer)
* Redis server

You can install Redis on most Linux distributions using your package manager:

```bash
sudo apt-get update
sudo apt-get install redis-server
or
sudo apt-get install redis
```

#### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ahamed-Shojib/AI-Agent-with-Social-Posting-Scheduling.git
   cd AI-Agent-with-Social-Posting-Scheduling
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the database and run migrations:**
   ```bash
   python manage.py migrate
   ```

#### Running the Project

You'll need **three separate terminal windows** to run all components simultaneously.

1. **Terminal 1: Start the Django development server:**
   ```bash
   python manage.py runserver
   ```
2. **Terminal 2: Start the Celery worker:**
   ```bash
   celery -A social_scheduler worker --loglevel=info
   ```
3. **Terminal 3: Start the Celery beat scheduler:**
   ```bash
   celery -A social_scheduler beat --loglevel=info
   ```

The application will be accessible at `http://127.0.0.1:8000/`. The dashboard will be at `http://127.0.0.1:8000/dashboard/`.

-----

### 5. Project Modules

* **`social_scheduler/`**: The main Django project directory.
* **`posting_agent/`**: The core Django app with models, views, and business logic.
* **`tasks.py`**: Contains **Celery tasks** for background post publishing.
* **`ai_utils.py`**: Utility for **AI-related functions**.
* **`dashboard.html`**: The frontend file for the **analytics dashboard**.

-----

### 6. API Endpoints

* **`POST /api/posts/`**: Create a new scheduled post.
* **`GET /api/posts/`**: List all scheduled posts.
* **`GET /api/dashboard/stats/`**: Get post statistics. Accepts an optional `platform` query parameter (e.g., `?platform=Facebook`).
* **`GET /api/dashboard/insight/`**: Get AI-generated insights. Accepts an optional `platform` query parameter (e.g., `?platform=Twitter`).

-----

