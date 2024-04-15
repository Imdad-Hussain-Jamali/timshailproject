from flask import Flask, render_template,session,request, redirect, url_for,flash
import sqlite3
# App Congifuration
app = Flask(__name__)

app.secret_key = 'Imdadjan.jan.71'
# Create Database

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        firstname TEXT NOT NULL,
                        lastname TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        repeatpassword TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Call the function to create the database
create_database()
#get DB Cinnection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn
# Regestrationform
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['exampleFirstName']
        lastname = request.form['exampleLastName']
        email = request.form['exampleInputEmail']
        password = request.form['exampleInputPassword']
        repeatpassword=request.form['exampleRepeatPassword']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username or email already exists in the database
        cursor.execute("SELECT * FROM users WHERE  email = ?", ( email,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return "Email already exists!"
        
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (firstname,lastname,email,password,repeatpassword) VALUES (?, ?, ?, ?, ?)", (firstname, lastname, email, password, repeatpassword))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('userhtmls/register.html')


dummy_users = {'Imdad': 'password1', 'Atif': 'password2'}
# -------------Login-----------------Functionality------------With Session
# @app.route('/login', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('exampleInputEmail')
        password = request.form.get('exampleInputPassword')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query the database to find the user
        cursor.execute("SELECT * FROM users WHERE email = ?", (username,))
        user = cursor.fetchone()
        
        if user and user['password'] == password:
            # If user is found and password matches, set session
            session['email'] = user['email']
            conn.close()
            return redirect(url_for('userdashboard'))
        else:
            conn.close()
            return "Invalid username or password"
    return render_template('/userhtmls/login.html')



#----------------------------------------------------------------------
#index ROute for Homepage
@app.route('/')
def index():
    return render_template('index.html')

#-------------------------------------------------------------------
#router for COurces
@app.route('/courses')
def courses():
    return render_template('courses.html')
#---------------------------------------------------------------------
#route FOr Events
@app.route('/events')
def events():
    return render_template('events.html')
#--------------------------------------------------------------------
@app.route('/contact')
def contact():
    return render_template('contact.html')

#--------------------------------------------------------------------------
@app.route('/Pricing')
def Pricing():
    return render_template('pricing.html')

#--------------------------------------------------------------------------
@app.route('/topbar')
def topbar():
    
    return render_template('topbar.html' )

#--------------------------------------------------------------------------
@app.route('/userdashboard')
def userdashboard():
    if 'email' in session:
        username = session['email']
        # Assuming you have some data to display in the dashboard
        # You can pass any required data to the template here
        return render_template('/userhtmls/dashboard.html', username=username)
    else:
        return redirect(url_for('login'))
    return render_template('userhtmls/Dashboard.html' )

#--------------------------------------------------------------------------

@app.route('/cus')
def cus():
    
    return render_template('CustomTestOption.html' )

#----------------------------------------------------------------------------
@app.route('/ser')
def ser():
    
    return render_template('serviceindex.html' )
#------------------------------------------------------------------------
@app.route('/selecttaste')
def selecttaste():
    return render_template ('SelectTest.html')

#--------------------------------------------------------------------------
# @app.route('/oktest')
# def oktest():
#     return render_template ('oktest.html')


#------------------------------------------------------------------------------
@app.route('/index')
def const():
    
    return render_template('index.html' )

#------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    # Check if user is logged in
    if 'email' in session:
        # Remove the email from the session
        session.pop('email', None)
        flash('You have been logged out.', 'info')
    else:
        flash('You are not logged in.', 'warning')
    
    # Redirect to the login page
    return redirect(url_for('index'))


#-------------------------------------------
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['London', 'Paris', 'Berlin', 'Rome'],
        'correct_answer': 'Paris',
        'category': 'Geography'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Mars', 'Venus', 'Jupiter', 'Saturn'],
        'correct_answer': 'Mars',
        'category': 'Science'
    },
    {
        'question': 'What is the capital of Spain?',
        'options': ['London', 'Madrid', 'Berlin', 'Rome'],
        'correct_answer': 'Madrid',
        'category': 'Geography'
    },
    {
        'question': 'Who wrote "Romeo and Juliet"?',
        'options': ['Charles Dickens', 'William Shakespeare', 'Jane Austen', 'Mark Twain'],
        'correct_answer': 'William Shakespeare',
        'category': 'Literature'
    },
    {
        'question': 'What is the chemical symbol for Gold?',
        'options': ['Go', 'Ag', 'Au', 'G'],
        'correct_answer': 'Au',
        'category': 'Science'
    }
] 

@app.route('/oktest')
@app.route('/oktest')
def oktest():
    page = int(request.args.get('page', 0))
    per_page = 2  # Number of questions per page
    start = page * per_page
    end = start + per_page

    total_questions = len(questions)
    
    return render_template('oktest.html', questions=questions[start:end], start=start, end=end, per_page=per_page), 200, {'context': {'page': page , 'total_questions':total_questions} }
#results.html here
@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    page = int(request.args.get('page', 0))
    per_page = 2  # Number of questions per page
    start = page * per_page
    end = start + per_page

    for question in questions[start:end]:
        user_answer = request.form.get(question['question'])
        if user_answer == question['correct_answer']:
            score += 1

    return render_template('result.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)
