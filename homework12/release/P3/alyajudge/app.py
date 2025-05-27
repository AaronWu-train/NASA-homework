from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
import re 
import time
import hashlib
from secret import secret_problem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A_super_SecUrE_$eCR37_keY'
SUBMISSIONS_DIR = 'submissions/'
ACCOUNTS_FILE = 'accounts/accounts.json'
MAX_SUBMISSIONS = 5
submission_id = 0

# --- Data Structures (Replace with Database Models Later) ---
problems = {
    1: {'title': 'Sum of Two Numbers', 'description': 'Given two integers, find their sum.',
        'time_limit': 1, 'memory_limit': 64, 'id': 1, 
        'solution': {
            'python': ['a, b', 'int', 'input()', 'print(a + b)'], 
            'c': ['int', 'scanf("%d %d",', '&a, &b', 'printf("%d", a + b)'], 
            'cpp': ['int', 'a, b', 'cin >>', 'cout << a + b']
            }
        },
    2: {'title': 'Factorial', 'description': 'Calculate the factorial of a non-negative integer.',
        'time_limit': 2, 'memory_limit': 128, 'id': 2, 
        'solution': {
            'python': ['def factorial', 'if n == 0:', 'return 1', 'else:', 'return n', 'factorial(n - 1)', 'n', 'int', 'input()', 'print(factorial(n))'], 
            'c': ['int factorial(int n)', 'if (n == 0)', 'return 1', 'else', 'return n', 'factorial(n - 1)', 'int main()', 'int n', 'scanf("%d", &n)', 'printf("%d", factorial(n))'], 
            'cpp': ['int factorial(int n)', 'if (n == 0)', 'return 1', 'else', 'return n',  'factorial(n - 1)', 'int main()', 'int n', 'cin >> n', 'cout << factorial(n)']
            }
    }
}

problems[3] = secret_problem

# --- Helper Functions ---
def special_judge(code, solution):
	# Check if code is substring of solution
    cnt, pos = 0, 0
    while cnt < len(solution) and pos + len(solution[cnt]) <= len(code):
        if code[pos: pos + len(solution[cnt])] == solution[cnt]:
            pos += len(solution[cnt])
            cnt += 1
        else:
            pos += 1
    return cnt

def get_problem(problem_id):
    return problems.get(int(problem_id))

def judge_submission(code, language, problem):
    score = special_judge(code, problem['solution'][language])
    if score == len(problem['solution'][language]):
        return "Accepted", 100
    else:
        return "Wrong Answer", (score * 100) // len(problem['solution'][language])

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_submissions(username):
    return load_data(SUBMISSIONS_DIR + username + '.json')

def save_submissions(username, submissions_list):
    save_data(submissions_list, SUBMISSIONS_DIR + username + '.json')

def load_accounts():
    return load_data(ACCOUNTS_FILE)

def save_accounts(accounts_data):
    save_data(accounts_data, ACCOUNTS_FILE)

# --- User Authentication ---
def login_user(username):
    session['username'] = username

def logout_user():
    session.pop('username', None)

def current_user():
    return session.get('username')

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html', problems=problems, current_user=current_user())

@app.route('/problem/<int:problem_id>')
def view_problem(problem_id):
    problem = get_problem(problem_id)
    if problem:
        return render_template('problem.html', problem=problem, current_user=current_user())
    else:
        flash('Problem not found.', 'error')
        return redirect(url_for('index'))

@app.route('/submit/<int:problem_id>', methods=['GET', 'POST'])
def submit_code(problem_id):
    global submission_id

    problem = get_problem(problem_id)
    if not problem:
        flash('Problem not found.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        code = request.form['code']
        language = request.form['language']
        if len(code) > 10000:
            flash(f'Submission Result for Problem {problem_id}: Time Limit Exceeded, 0', 'info')
            return redirect(url_for('view_problem', problem_id=problem_id))
        submission_result, score = judge_submission(code, language, problem)
        if current_user():
            new_submission = {
                'problem_id': problem_id,
                'code': code,
                'language': language,
                'result': submission_result,
                'score': score,
                'user': current_user(),
                'problem_title': problem['title']
            }
            submissions = load_submissions(current_user())
            accounts = load_accounts()
            if len(submissions) < MAX_SUBMISSIONS and current_user() in accounts:
                submissions[submission_id] = new_submission
                submission_id += 1
                save_submissions(current_user(), submissions)
        flash(f'Submission Result for Problem {problem_id}: {submission_result}, {score}', 'info')
        return redirect(url_for('view_problem', problem_id=problem_id))
    return render_template('submit.html', problem=problem, current_user=current_user())

@app.route('/all_submissions')
def view_all_submissions():
    accounts = load_accounts()
    submissions = {}
    for username in accounts.keys():
        user_submissions = load_submissions(username)
        for sub_id, sub in user_submissions.items():
            try:
                if sub['problem_id'] == 3:
                    continue
            except Exception as E:
                flash(f"Submission {sub_id} is missing 'problem_id'.", 'error')
                pass
            submissions[sub_id] = sub
    return render_template('all_submissions.html', submissions=submissions)

@app.route('/submissions/<path:username>')
def view_user_submissions(username):
    user_submissions = load_submissions(username)
    submissions = {}
    if username != current_user():
        for sub_id, sub in user_submissions.items():
            try:
                if sub['problem_id'] == 3:
                    continue
            except Exception as E:
                flash(f"Submission {sub_id} is missing 'problem_id'.", 'error')
                pass
            submissions[sub_id] = sub
    else:
        submissions = user_submissions
    return render_template('user_submissions.html', submissions=submissions, current_user=current_user(), username=username)

@app.route('/my_submissions')
def view_my_submissions():
    if not current_user():
        flash('You must be logged in to view your submissions.', 'warning')
        return redirect(url_for('login'))
    return redirect(url_for('view_user_submissions', username=current_user()))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        time.sleep(3)
        accounts = load_accounts()
        if username in accounts and accounts[username] == hashlib.sha256(password.encode("utf-8")).hexdigest():
            login_user(username)
            flash('Login successful.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=45588)
