# Fitness CRM

A full-stack web application for fitness trainers to manage their clients. Built with FastAPI, PostgreSQL, and deployed live on Render.

## Live Demo

https://fitness-crm-sknl.onrender.com

## Features

- **Add clients** with name, phone, number of sessions, payment date, start date, and training days (e.g., Mon, Wed, Fri).
- **Automatic date calculation:** The app finds the first training day based on the schedule and calculates the subscription end date (last training day).
- **Search by name:** Quickly find any client.
- **Edit client:** Change any data, including dates, manually if needed.
- **Extend subscription:** One click to automatically calculate new dates for the next month.
- **Overdue warning:** The app highlights expired subscriptions in red.
- **Mobile-friendly:** Responsive design for use on phones.

## Technologies

- **Python 3.12**
- **FastAPI** — web framework
- **PostgreSQL** — cloud database (Neon)
- **psycopg2** — PostgreSQL adapter for Python
- **HTML/CSS** — responsive frontend
- **Render** — deployment platform

## How to run

1. Install dependencies:
   pip install -r requirements.txt

2. Create a `.env` file with your database connection string:
   DATABASE_URL=postgresql://user:password@host:5432/dbname

3. Run the server:
   uvicorn main:app --reload

4. Open in browser:
   http://127.0.0.1:8000

## Author

Viktoria Zykova — Junior Python / AI Developer
GitHub: https://github.com/ViktoriaFit
