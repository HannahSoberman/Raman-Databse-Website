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
git clone https://github.com/your-username/raman-db-project.git
cd raman-db-project

## (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate
or venv\Scripts\activate on Windows

## Install dependencies
pip install -r requirements.txt



## Running the Flask App
python app.py


Then visit: http://127.0.0.1:5000/ in your browser.

📓 Using the Jupyter Notebook
If you prefer working interactively:
jupyter notebook


Open notebook.ipynb to explore, add, or search data directly.

📁 Project Structure
raman-db-project/
├── app.py                  # Flask app
├── notebook.ipynb          # Jupyter version
├── molecules.db            # SQLite database
├── templates/              # HTML templates
├── static/uploads/         # Uploaded images
├── requirements.txt        # Python dependencies
└── README.md               # You're reading it!



🤝 Contributing
Pull requests welcome! If you’d like to contribute:
- Fork the repo
- Create a new branch (git checkout -b feature-name)
- Commit your changes
- Push and open a PR

📬 Contact
For questions or collaboration ideas, reach out via GitHub Issues or email [your-email@example.com].

Let me know if you'd like me to customize this with your actual GitHub username, email, or add a Zenodo badge for citation. We can also add screenshots or a demo GIF if you want to make it pop!
