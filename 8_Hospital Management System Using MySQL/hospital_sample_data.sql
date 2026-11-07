-- Hospital Management System : sample database
-- Run in MySQL:  SOURCE hospital_sample_data.sql;
-- (The Python program also creates the tables and doctors automatically.)

CREATE DATABASE IF NOT EXISTS hospital;
USE hospital;

CREATE TABLE IF NOT EXISTS doctors (
    doc_id INT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    department VARCHAR(30),
    fees INT
);

CREATE TABLE IF NOT EXISTS patients (
    pat_id INT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    age INT,
    gender CHAR(1),
    phone VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS appointments (
    app_id INT PRIMARY KEY AUTO_INCREMENT,
    pat_id INT,
    doc_id INT,
    app_date DATE,
    status VARCHAR(10) DEFAULT 'Booked',
    FOREIGN KEY (pat_id) REFERENCES patients(pat_id),
    FOREIGN KEY (doc_id) REFERENCES doctors(doc_id)
);

INSERT INTO doctors VALUES
(101, 'Dr. R.K. Sharma', 'Cardiology', 800),
(102, 'Dr. Meena Joshi', 'Pediatrics', 500),
(103, 'Dr. Anil Rawat', 'Orthopedics', 600),
(104, 'Dr. Sunita Bisht', 'General', 300),
(105, 'Dr. Vikas Pant', 'Cardiology', 700);

INSERT INTO patients VALUES
(1, 'Ramesh Negi', 45, 'M', '9876543210'),
(2, 'Kavya Bisht', 8, 'F', '9412345678'),
(3, 'Mohan Rawat', 67, 'M', '9758123456'),
(4, 'Sunita Joshi', 34, 'F', '9897011223');

INSERT INTO appointments (pat_id, doc_id, app_date, status) VALUES
(1, 101, '2026-11-10', 'Booked'),
(2, 102, '2026-11-10', 'Booked'),
(3, 101, '2026-11-11', 'Booked'),
(4, 104, '2026-11-11', 'Cancelled'),
(3, 103, '2026-11-12', 'Booked');

-- Some practice queries
-- SELECT * FROM doctors WHERE department = 'Cardiology';
-- SELECT department, COUNT(*) FROM doctors GROUP BY department;
-- SELECT p.name, d.name FROM appointments a, patients p, doctors d
--        WHERE a.pat_id = p.pat_id AND a.doc_id = d.doc_id;
