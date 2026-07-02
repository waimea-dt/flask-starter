#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    with connect_db() as db:
        sql = """
        SELECT * FROM TASKS
        """
        data = db.execute(sql).fetchall()
        data_sorted = sorted(data, key = lambda x: x['priority'], reverse=True)
        return render_template("pages/list.jinja",tasks=data_sorted)

@app.route("/tasks/<int:id>", methods=['GET','POST','DELETE'])
def manage_tasks(id):
    with connect_db() as db:
        if request.method == 'GET':
            sql = "SELECT * FROM TASKS WHERE id = ?"
            params = (id,)
            data = db.execute(sql,params).fetchone()
        elif request.method == 'POST':
            name = request.form['name']
            priority = request.form['priority']
            sql = "UPDATE tasks SET name = ?,priority = ? WHERE id = ?"
            #INSERT INTO tasks (name,priority) VALUES (?,?) ON CONFLICT (id) DO UPDATE SET name = excluded.name, priority = excluded.priority;
            params = (name,priority,id)
            db.execute(sql,params)
            data = {'name':name,'priority':priority, 'id':id}
        elif request.method == 'DELETE':
            sql = "DELETE FROM tasks WHERE id = ?"
            params = (id,)
            db.execute(sql,params)
            return ""
        return render_template("partials/task.jinja",task=data)

        

    

@app.get("/tasks/<int:id>/edit")
def edit_task(id):
    with connect_db() as db:
        sql = "SELECT * FROM tasks WHERE id = ?"
        params = (id,)
        data = db.execute(sql,params).fetchone()
        return render_template("partials/edit.jinja",task = data)
        


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

