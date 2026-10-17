
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
                <span class="client-details">Phone: {phone} | Paid until: {date}</span>
            </div>
            <a href="/delete/{client_id}" class="delete-btn">Delete</a>
        </li>
        """

    with open("index.html", "r") as file:
        html_content = file.read()

    html_content = html_content.replace("<!-- CLIENT_LIST -->", f"<ul>{clients_html}</ul>")
    
    return HTMLResponse(content=html_content)

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

    return HTMLResponse(content="<h2 style='text-align:center; font-family:sans-serif; color:green;'>Client added!</h2><p style='text-align:center;'><a href='/'>Back</a></p>")

@app.get("/delete/{client_id}")
def delete_client(client_id: int):
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

    return HTMLResponse(content="<h2 style='text-align:center; font-family:sans-serif; color:red;'>Client deleted!</h2><p style='text-align:center;'><a href='/'>Back</a></p>")