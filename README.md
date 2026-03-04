1. Clone the repository
git clone https://github.com/Greedrache/KanMind-Backend .

2. Create a virtual environment
python -m venv env

3. Activate the virtual environment

Windows:

env\Scripts\activate


4. Install dependencies
pip install -r requirements.txt

5. Apply migrations
python manage.py migrate

6. Run the development server
python manage.py runserver


The backend will be available at:

http://127.0.0.1:8000/
