<h1>KanMind Backend</h1>

<p>
KanMind is a Kanban-style task management application inspired by tools like Trello.
This repository contains the Django-based backend that provides a REST API
for user authentication, boards, and task management.
</p>

<h2>Features</h2>
<ul>
  <li>User registration and login</li>
  <li>Create and manage boards</li>
  <li>Create, update and delete tasks</li>
  <li>Assign tasks to boards</li>
  <li>RESTful API structure</li>
</ul>

<h2>Tech Stack</h2>
<ul>
  <li>Python 3.14+</li>
  <li>Django</li>
  <li>Django REST Framework</li>
  <li>SQLite (development)</li>
</ul>

<h2>Setup (Local Development)</h2>

<h3>1. Clone Repository</h3>
<pre><code>git clone https://github.com/Greedrache/KanMind-Backend .</code></pre>

<h3>2. Create Virtual Environment</h3>
<pre><code>python -m venv venv</code></pre>

<h3>3. Activate Virtual Environment</h3>
<p><strong>PowerShell:</strong></p>
<pre><code>venv\Scripts\Activate.ps1</code></pre>

<p><strong>cmd:</strong></p>
<pre><code>venv\Scripts\activate</code></pre>

<h3>4. Install Dependencies</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>5. Apply Migrations</h3>
<pre><code>python manage.py migrate</code></pre>

<h3>6. Load Dummy Data (Optional)</h3>
<p>If you don't want to populate the database yourself, you can load test data:</p>
<pre><code>python manage.py loaddata dummy_data.json</code></pre>

<h3>7. Reset Test User Passwords (Optional)</h3>
<p>If you are using dummy data, reset the passwords for all test users (e.g. to '123123123'):p>
<pre><code>python manage.py shell -c "from django.contrib.auth.models import User; [u.set_password('123123123') or u.save() for u in User.objects.all()]"</code></pre>

<h3>8. Run Development Server</h3>
<pre><code>python manage.py runserver</code></pre>

<p>
Server runs at: <br>
http://127.0.0.1:8000/
</p>

<h2>Optional</h2>

<p><strong>Create Superuser:</strong></p>
<pre><code>python manage.py createsuperuser</code></pre>

<p><strong>Deactivate Virtual Environment:</strong></p>
<pre><code>deactivate</code></pre>

<h2>Troubleshooting</h2>
<ul>
  <li>If activation fails due to ExecutionPolicy: <br>
  <code>Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass</code></li>
  <li>If migrations are missing: run <code>python manage.py migrate</code></li>
</ul>
