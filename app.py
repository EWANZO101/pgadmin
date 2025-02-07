from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import subprocess
import sys
import os

app = Flask(__name__)
app.secret_key = 'awffafaihfiahfihaifhaihfaihfihahifiafhi'  # Used for session flash messages

# Function to reset the password in PostgreSQL database
def reset_password(db_name, db_user, db_password, db_host, db_port, username, new_password):
    try:
        # Connect to the PostgreSQL database with user-provided details
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port
        )
        cursor = conn.cursor()

        # SQL query to update the password
        cursor.execute('UPDATE public."User" SET "password" = %s WHERE "username" = %s', (new_password, username))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Function to disable a feature in PostgreSQL (like FORCE_DISCORD_AUTH)
def disable_feature(db_name, db_user, db_password, db_host, db_port):
    try:
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port
        )
        cursor = conn.cursor()

        # SQL to disable the feature
        cursor.execute('UPDATE public."CadFeature" SET "isEnabled" = false WHERE feature = %s', ('FORCE_DISCORD_AUTH',))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Function to execute a shell command (for sudo)
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr.decode()}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Capture form data
        db_name = request.form['db_name']
        db_user = request.form['db_user']
        db_password = request.form['db_password']
        db_host = request.form['db_host']
        db_port = request.form['db_port']
        username = request.form['username']
        new_password = request.form['new_password']
        action = request.form['action']

        # Handle password reset based on selected action
        if action == 'reset_password':
            if reset_password(db_name, db_user, db_password, db_host, db_port, username, new_password):
                flash(f"Your password has been changed successfully for {username}!", 'success')
            else:
                flash("There was an error resetting your password.", 'error')

        elif action == 'disable_feature':
            if disable_feature(db_name, db_user, db_password, db_host, db_port):
                flash("The feature has been disabled successfully.", 'success')
            else:
                flash("There was an error disabling the feature.", 'error')

        return redirect(url_for('index'))

    return render_template('')

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6007)  # Set port to 6005