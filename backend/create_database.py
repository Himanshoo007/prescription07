import sqlite3

def create_database():
    conn = sqlite3.connect('medicines.db')  # This will create a file 'medicines.db' in the current directory
    c = conn.cursor()

    # Create the 'medicines' table if it doesn't already exist
    c.execute('''CREATE TABLE IF NOT EXISTS medicines (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT)''')

    # Insert predefined medicines into the table if it's empty
    medicines = [
        ('Paracetamol', 'Painkiller'),
        ('Aspirin', 'Painkiller'),
        ('Amoxicillin', 'Antibiotic'),
        ('Ibuprofen', 'Painkiller'),
        ('Metformin', 'Diabetes'),
        ('Calpol', 'Fever'),
        ('Delcon', 'Antibiotic'),
        ('Levolin', 'Painkiller'),
        ('Meftal', 'Diabetes'),

    ]

    # Insert the data if no rows exist
    c.execute('SELECT COUNT(*) FROM medicines')
    if c.fetchone()[0] == 0:
        c.executemany('''INSERT INTO medicines (name, category) VALUES (?, ?)''', medicines)

    conn.commit()  # Commit changes
    conn.close()   # Close the connection

if __name__ == "__main__":
    create_database()

