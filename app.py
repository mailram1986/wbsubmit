from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory, flash
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'verysecurekey'

# --- Configuration ---
app.config.update(
    UPLOAD_FOLDER='uploads',
    DEADLINE=datetime(2025, 7, 10, 23, 59, 59),
    
)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- User Roles ---
USERS = {
    'admin': 'bioinfo123',
    'instructor': 'teach123'
}

# --- Login Required Decorator ---
def login_required(role):
    def decorator(f):
        def wrapper(*args, **kwargs):
            user = session.get('user')
            if not user or user != role:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        # Do not modify function name to prevent Flask routing errors
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# --- Helper to list all uploaded files ---
def get_all_files():
    files = []
    for sf in os.listdir(app.config['UPLOAD_FOLDER']):
        fp = os.path.join(app.config['UPLOAD_FOLDER'], sf)
        if os.path.isdir(fp):
            for f in os.listdir(fp):
                p = os.path.join(sf, f)
                files.append({
                    'student': sf,
                    'filename': f,
                    'upload_time': datetime.fromtimestamp(os.path.getctime(os.path.join(fp, f))).strftime("%Y-%m-%d %H:%M:%S"),
                    'path': p
                })
    return files

# --- Student Upload Page ---
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if datetime.now() > app.config['DEADLINE']:
        return f"❌ Submissions are closed. Deadline was {app.config['DEADLINE']:%Y-%m-%d %H:%M:%S}"

    if request.method == 'POST':
        name = request.form.get('name', '').strip().replace(" ", "_")
        roll = request.form.get('roll', '').strip().upper()
        file = request.files.get('file')

        if not name or not roll or not file:
            flash('Missing required fields or file.')
            return redirect('/')

        filename = secure_filename(file.filename)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        student_folder = os.path.join(app.config['UPLOAD_FOLDER'], f"{roll}_{name}")
        os.makedirs(student_folder, exist_ok=True)
        final_name = f"{ts}_{filename}"
        saved_path = os.path.join(student_folder, final_name)
        file.save(saved_path)

        return "✅ Submission successful!"
    return render_template('upload.html')

# --- Login Page ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        if USERS.get(u) == p:
            session['user'] = u
            return redirect(url_for('admin_panel' if u == 'admin' else 'instructor_panel'))
        return "Invalid credentials", 403
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# --- Admin Panel ---
@app.route('/admin')
@login_required('admin')
def admin_panel():
    return render_template('admin.html', files=get_all_files(), is_admin=True)

# --- Instructor Panel ---
@app.route('/instructor')
@login_required('instructor')
def instructor_panel():
    return render_template('admin.html', files=get_all_files(), is_admin=False)

# --- File View ---
@app.route('/view/<path:filepath>')
@login_required('instructor')
def view_file(filepath):
    folder, filename = os.path.split(filepath)
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename)

# --- File Download ---
@app.route('/download/<path:filepath>')
@login_required('instructor')
def download_file(filepath):
    folder, filename = os.path.split(filepath)
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename, as_attachment=True)

# --- File Delete (Admin Only) ---
@app.route('/delete/<path:filepath>', methods=['POST'])
@login_required('admin')
def delete_file(filepath):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filepath)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('admin_panel'))

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)
