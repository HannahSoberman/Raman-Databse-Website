from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__, template_folder='templates')
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DB_FILE = "molecules.db"

def init_db():                                      # creates databases to add raman data to
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Molecules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS FrequencySets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                molecule_id INTEGER NOT NULL,
                frequencies TEXT NOT NULL,
                intensities TEXT,
                phase TEXT,
                source TEXT,
                description TEXT,
                image_path TEXT,
                FOREIGN KEY (molecule_id) REFERENCES Molecules(id)
            )
        ''')


@app.route('/molecule/<int:id>')                                    # defines the molecule detail page's functionality
def molecule_detail(id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM Molecules WHERE id = ?", (id,))
        row = c.fetchone()
        if not row:
            return f"<h2>Molecule with ID {id} not found.</h2>"
        name = row[0]

        c.execute(
            "SELECT id, frequencies, intensities, phase, source, description, image_path FROM FrequencySets WHERE molecule_id = ?",
            (id,))
        frequency_sets = c.fetchall()

    return render_template('molecule_detail.html', name=name, frequency_sets=frequency_sets)


@app.route('/delete/<int:id>', methods=['POST'])            #function to delete a molecule from the database
def delete_molecule(id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Molecules WHERE id = ?", (id,))
    return redirect('/')


@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):                               # provides functionality for editing pre-existing entries
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        if request.method == 'POST':
            # Collect updated form data
            frequencies = request.form.get('frequencies')
            intensities = request.form.get('intensities')
            phase = request.form.get('phase')
            source = request.form.get('source')
            description = request.form.get('description')

            # Optional: handle new image upload
            image_file = request.files.get('image')
            image_filename = None
            if image_file and image_file.filename:
                image_filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_path)

            # Update the database
            update_query = '''UPDATE FrequencySets SET frequencies = ?, intensities = ?, phase = ?, source = ?, description = ?'''
            params = [frequencies, intensities, phase, source, description]

            if image_filename:
                update_query += ', image_path = ?'
                params.append(image_filename)
            update_query += ' WHERE id = ?'
            params.append(entry_id)

            c.execute(update_query, params)
            return redirect('/')  # or redirect to the molecule page

        # If GET: fetch current data for the form
        c.execute(
            "SELECT frequencies, intensities, phase, source, description, image_path FROM FrequencySets WHERE id = ?",
            (entry_id,))
        entry = c.fetchone()

    return render_template('edit_entry.html', entry=entry, entry_id=entry_id)

@app.route('/', methods=['GET', 'POST'])
def home():
    all_molecules = []
    message = ""
    results = []
    if request.method == 'POST':
        if 'search' in request.form:
            target_freq = request.form['search'].strip()
            tolerance_str = request.form.get('tolerance', '').strip()
            try:
                target_freq = float(target_freq)
                tolerance = float(tolerance_str) if tolerance_str else 5.0

                with sqlite3.connect(DB_FILE) as conn:
                    c = conn.cursor()
                    c.execute('''
                        SELECT m.name, fs.frequencies
                        FROM Molecules m
                        JOIN FrequencySets fs ON m.id = fs.molecule_id
                    ''')
                    for name, freq_str in c.fetchall():
                        freqs = [f.strip() for f in freq_str.split(',') if f.strip()]
                        matched = []
                        for f in freqs:
                            try:
                                f_val = float(f)
                                if abs(f_val - target_freq) <= tolerance:
                                    matched.append(f)
                            except ValueError:
                                continue
                        if matched:
                            results.append((name, matched))  # Only store name + matched freqs
            except ValueError:
                message = f"⚠️ Invalid frequency input: '{target_freq}, tolerance='{tolerance_str}''"
        elif 'name' in request.form and 'frequencies' in request.form:
            new_name = request.form['name']
            new_freqs = request.form['frequencies']
            new_phase = request.form.get('phase') or None
            new_intensities = request.form.get('intensities') or None
            new_source = request.form.get('source') or None
            new_description = request.form.get('description') or None
            image_file = request.files.get('image') or None
            image_filename = None
            if image_file and image_file.filename:
                image_filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_path)
            with sqlite3.connect(DB_FILE) as conn:
                c = conn.cursor()
                c.execute("SELECT id FROM Molecules WHERE name = ?", (new_name,))
                row = c.fetchone()
                if row:
                    molecule_id = row[0]
                else:
                    c.execute("INSERT INTO Molecules (name) VALUES (?)", (new_name,))
                    molecule_id = c.lastrowid
                c.execute('''INSERT INTO FrequencySets 
                                     (molecule_id, frequencies, intensities, phase, source, description, image_path)
                                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (molecule_id, new_freqs, new_intensities, new_phase, new_source, new_description,
                           image_filename))
            message = f"✅ Added a new frequency set to {new_name}"
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, name FROM Molecules")
        all_molecules = c.fetchall()

    return render_template('index.html', results=results, message=message, molecules=all_molecules)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)