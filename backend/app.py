from flask import Flask, render_template, request
import easyocr
import os
import difflib
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'])

def extract_text(image_path):
    result = reader.readtext(image_path, detail=0)
    return result

def match_medicines(prescription_list, order_list):
    matches = []
    unmatched = []
    for med in order_list:
        found = False
        for pres_med in prescription_list:
            if difflib.SequenceMatcher(None, med.lower(), pres_med.lower()).ratio() > 0.7:
                matches.append((med))
                found = True
                break
        if not found:
            unmatched.append(med)
    return matches, unmatched

def get_medicines_from_db():
    conn = sqlite3.connect('medicines.db')  # Connect to the database
    c = conn.cursor()
    c.execute('SELECT name FROM medicines')  # Fetch the names of medicines
    medicines = [row[0] for row in c.fetchall()]  # Get list of medicine names
    conn.close()
    return medicines

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Save uploaded prescription
        file = request.files['prescription']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Get predefined customer order from the database
        order_list = get_medicines_from_db()  # Fetch list from the database

        # OCR on prescription
        prescription_items = extract_text(filepath)

        # Match medicines
        matched, unmatched = match_medicines(prescription_items, order_list)

        result = {
            "matched": matched,
            "unmatched": unmatched,
            "extracted": prescription_items
        }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
