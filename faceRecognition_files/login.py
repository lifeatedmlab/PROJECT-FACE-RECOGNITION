from database import mycursor

def login_user(request, render_template, flash, redirect, url_for):
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        mycursor.execute("SELECT * FROM Admin WHERE username = %s AND password = %s", (username, password))
        account = mycursor.fetchone()

        if account:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)
