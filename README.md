# wbsubmit
Workbook Submission Portal
📁 Bioinformatics Lab Submission Portal
A lightweight, local-first Flask web application for collecting student workbook submissions in bioinformatics and biotechnology labs. Built for seamless management by instructors and administrators.

🚀 Features
📤 Student file uploads with name and roll number

🛑 Automatic deadline enforcement

🔐 Role-based login for Admin and Instructor

🗂 Admin panel with:

View submissions

Download or preview files

Delete files (admin only)

🧑‍🏫 Instructor panel with view/download access

🧭 Clean, responsive web interface (HTML/CSS)

🌐 Local server deployment (no external dependencies like Drive/Mail)

🖥️ Tech Stack
Python 3

Flask

Jinja2 templating

HTML/CSS

Optional: .env for future environment configs

📦 Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/bioinfo-lab-submission.git
cd bioinfo-lab-submission
2. Install Dependencies
Make sure you're using Python 3.7+ and install required packages:

bash
Copy
Edit
pip install flask werkzeug
3. Run the Application
bash
Copy
Edit
python app.py
Visit http://localhost:5000 in your browser.

🔐 Default Login Credentials
Role	Username	Password
Admin	admin	bioinfo123
Instructor	instructor	teach123

🗃 Directory Structure
cpp
Copy
Edit
bioinfo-lab-submission/
├── app.py
├── uploads/
│   └── [roll_name]/[timestamp_filename]
├── templates/
│   ├── upload.html
│   ├── login.html
│   └── admin.html
└── static/ (optional)
📌 Notes
Deadline is hardcoded in app.py:

python
Copy
Edit
DEADLINE = datetime(2025, 7, 10, 23, 59, 59)
You can disable/extend this easily by modifying the logic in the upload_file() route.
