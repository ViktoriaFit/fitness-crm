from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

def init_db():
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            phone TEXT, 
            payment_date TEXT
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
        <title>Фитнес CRM</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
            h2 {{ color: #34495e; margin-top: 40px; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
            .form-group {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }}
            input[type="text"], input[type="date"] {{ padding: 12px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 16px; flex: 1; min-width: 150px; }}
            button {{ padding: 12px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: 0.3s; }}
            button:hover {{ background-color: #2980b9; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ background: #ecf0f1; margin-bottom: 10px; padding: 15px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }}
            .client-info {{ display: flex; flex-direction: column; gap: 5px; }}
            .client-name {{ font-weight: bold; font-size: 18px; color: #2c3e50; }}
            .client-details {{ font-size: 14px; color: #7f8c8d; }}
            .delete-btn {{ color: #e74c3c; text-decoration: none; font-weight: bold; padding: 5px 10px; border: 1px solid #e74c3c; border-radius: 3px; transition: 0.3s; }}
            .delete-btn:hover {{ background: #e74c3c; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>База клиентов фитнес-клуба</h1>
            
            <form action="/add_client" method="post" class="form-group">
                <input type="text" name="client_name" placeholder="Имя клиента" required>
                <input type="text" name="client_phone" placeholder="Телефон" required>
                <input type="date" name="payment_date" required>
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
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, payment_date FROM clients")
    rows = cursor.fetchall()
    conn.close()

    clients_html = ""
    for row in rows:
        client_id = row[0]
        name = row[1]
        phone = row[2]
        date = row[3]
        
        clients_html += f"""
        <li>
            <div class="client-info">
                <span class="client-name">{name}</span>
                <span class="client-details">📞 {phone} | 📅 Оплата до: {date}</span>
            </div>
            <a href="/delete/{client_id}" class="delete-btn">Удалить</a>
        </li>
        """

    return HTMLResponse(content=get_html(clients_html))

@app.post("/add_client")
def add_client(
    client_name: str = Form(...), 
    client_phone: str = Form(...), 
    payment_date: str = Form(...)
):
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clients (name, phone, payment_date) VALUES (?, ?, ?)", 
        (client_name, client_phone, payment_date)
    )
    conn.commit()
    conn.close()

    return HTMLResponse(content="<h2 style='text-align:center; font-family:sans-serif; color:green;'>Клиент добавлен!</h2><p style='text-align:center;'><a href='/'>Вернуться назад</a></p>")

@app.get("/delete/{client_id}")
def delete_client(client_id: int):
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

    return HTMLResponse(content="<h2 style='text-align:center; font-family:sans-serif; color:red;'>Клиент удален!</h2><p style='text-align:center;'><a href='/'>Вернуться назад</a></p>")
