# Raman Frequency Database Web App

A lightweight Flask-based web application for storing, searching, and editing Raman spectroscopy data. Designed for collaborative scientific workflows with support for image uploads, frequency matching, and molecule metadata.

🚀 Features
- Add new molecules and frequency sets via web form
- Upload and display Raman spectra images
- Search frequency sets by target frequency ± tolerance
- Edit or delete existing entries
- SQLite backend for simplicity and portability
- Jupyter notebook version available for data exploration

🧰 Tech Stack
- Python 3.8+
- Flask
- SQLite
- HTML/CSS (Jinja templates)
- Jupyter Notebook (optional)

📦 Installation
## Clone the repo
in a terminal use: cd path/to/project
then use:
git clone https://github.com/HannahSoberman/Raman-Databse-Website.git


## (Optional) Create a virtual environment
using a terminal:

python -m venv venv

source venv/bin/activate
or venv\Scripts\activate on Windows

## Install dependencies
pip install -r requirements.txt

## Running the Flask App
python app.py


Then visit: http://127.0.0.1:5000/ in your browser.

🤝 Contributing
Pull requests welcome! If you’d like to contribute:
- Fork the repo
- Create a new branch (git checkout -b feature-name)
- Commit your changes
- Push and open a PR

📬 Contact
For questions or collaboration ideas, reach out via GitHub Issues or email [fbq7kr@virginia.edu].
