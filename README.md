 # Formula-1-Season-Tracker
 
📦 Installation Guide

1️⃣ Clone the Repository

git clone <repository-url>\

2️⃣ Create Virtual Environment

Windows\
python -m venv venv\
venv\Scripts\activate

macOS / Linux\
python3 -m venv venv\
source venv/bin/activate

3️⃣ Install Dependencies

cp .env.template .env
pip install -r requirements.txt

4️⃣ Apply Migrations

python manage.py migrate

5️⃣ (Optional) Load Sample Data

python manage.py load_sample_data

6️⃣ Create Superuser (Admin Access)

python manage.py createsuperuser

Follow the prompts to set username, email, and password.

7️⃣ Run the Development Server

python manage.py runserver

Open in your browser:

http://127.0.0.1:8000/

Admin panel:

http://127.0.0.1:8000/admin/