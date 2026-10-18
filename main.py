from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import psycopg2
import os

app = FastAPI()

PG_CONN = os.environ.get("DATABASE_URL")

def init_db():
    conn = psycopg2.connect(PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY, 
            last_name TEXT, 
            phone TEXT, 
            payment_date TEXT,
            expiry_date TEXT,
            visits INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_html(clients_html):
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Фитнес CRM</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
            h2 {{ color: #34495e; margin-top: 40px; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
            .form-group {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }}
            input[type="text"], input[type="date"], input[type="number"] {{ padding: 12px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 16px; flex: 1; min-width: 120px; }}
            button {{ padding: 12px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: 0.3s; width: 100%; }}
            button:hover {{ background-color: #2980b9; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ background: #ecf0f1; margin-bottom: 10px; padding: 15px; border-radius: 5px; display: flex; flex-direction: column; gap: 10px; }}
            .client-info {{ display: flex; flex-direction: column; gap: 5px; }}
            .client-name {{ font-weight: bold; font-size: 18px; color: #2c3e50; }}
            .client-details {{ font-size: 14px; color: #7f8c8d; }}
            .delete-btn {{ color: #e74c3c; text-decoration: none; font-weight: bold; padding: 8px; border: 1px solid #e74c3c; border-radius: 3px; text-align: center; transition: 0.3s; }}
            .delete-btn:hover {{ background: #e74c3c; color: white; }}
            @media (min-width: 600px) {{
                .form-group {{ flex-wrap: nowrap; }}
                button {{ width: auto; }}
                li {{ flex-direction: row; justify-content: space-between; align-items: center; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>База клиентов</h1>
            
            <form action="/add_client" method="post" class="form-group">
                <input type="text" name="last_name" placeholder="Фамилия и Имя" required>
                <input type="text" name="phone" placeholder="Телефон" required>
                <input type="date" name="payment_date" required title="Дата оплаты">
                <input type="date" name="expiry_date" required title="Действует до">
                <input type="number" name="visits" placeholder="Посещений (8/12)" required>
                <button type="submit">Добавить</button>
            </form>

            <h2>Список клиентов:</h2>
            <ul>{clients_html}</ul>
        </div>
    </body>
    </html>
    """

@app.get("/")
def read_index():
    conn = psycopg2.connect(PG_CONN)
    cursor = conn.cursor()
    cursor.execute("SELECT id, last_name, phone, payment_date, expiry_date, visits FROM clients")
    rows = cursor.fetchall()
    conn.close()

    clients_html = ""
    for row in rows:
        client_id = row[0]
        last_name = row[1]
        phone = row[2]
        pay_date = row[3]
        exp_date = row[4]
        visits = row[5]
        
        clients_html += f"""
        <li>
            <div class="client-info">
                <span class="client-name">{last_name}</span>
                <span class="client-details">📞 {phone} | 📅 Оплата: {pay_date} | ⌛ До: {exp_date} | 🏋️ Посещений: {visits}</span>
            </div>
            <a href="/delete/{client_id}" class="delete-btn">Удалить</a>
        </li>
        """

    return HTMLResponse(content=get_html(clients_html))

@app.post("/add_client")
def add_client(
    last_name: str = Form(...), 
    phone: str = Form(...), 
    payment_date: str = Form(...),
    expiry_date: str = Form(...),
    visits: int = Form(...)
):
    conn = psycopg2.connect(PG_CONN)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clients (last_name, phone, payment_date, expiry_date, visits) VALUES (%s, %s, %s, %s, %s)", 
        (last_name, phone, payment_date, expiry_date, visits)
    )
    conn.commit()
    conn.close()

    return HTMLResponse(content="<h2 style='text-align:center; font-family:sans-serif; color:green;'>Клиент добавлен!</h2><p style='text-align:center;'><a href='/'>Вернуться назад</a></p>")

@app.get("/delete/{client_id}")
def delete_client(client_id: int):
    conn = psycopg2.connect(PG_CONN)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
    conn.commit()
    conn.close()

    return HTMLResponse(content="<h2 style='text-align:center; font-family:sans-serif; color:red;'>Клиент удален!</h2><p style='text-align:center;'><a href='/'>Вернуться назад</a></p>")
