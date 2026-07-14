-- ============================================================
-- Student Grade Management System
-- Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS student_grade_manager;

USE student_grade_manager;

-- ============================================================
-- Drop Existing Tables (Safe Recreation Order)
-- ============================================================

DROP TABLE IF EXISTS subject;
DROP TABLE IF EXISTS education_record;
DROP TABLE IF EXISTS students;

-- ============================================================
-- Students Table
-- ============================================================

CREATE TABLE students (

    student_id INT AUTO_INCREMENT PRIMARY KEY,

    password VARCHAR(255) NOT NULL,

    name VARCHAR(100) NOT NULL,

    father_name VARCHAR(100) NOT NULL,

    mother_name VARCHAR(100) NOT NULL,

    date_of_birth DATE NOT NULL,

    gender ENUM('Male', 'Female', 'Other') NOT NULL,

    phone VARCHAR(15) NOT NULL UNIQUE,

    email VARCHAR(100) NOT NULL UNIQUE,

    address TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ============================================================
-- Education Record Table
-- ============================================================

CREATE TABLE education_record (

    record_id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    record_type ENUM('School', 'College') NOT NULL,

    level VARCHAR(50) NOT NULL,

    organization VARCHAR(150) NOT NULL,

    category VARCHAR(100) NOT NULL,

    academic_year VARCHAR(20) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_student_record
        UNIQUE (student_id, record_type, level)

);



-- ============================================================
-- Subject Table
-- ============================================================

CREATE TABLE subject (

    subject_id INT AUTO_INCREMENT PRIMARY KEY,

    record_id INT NOT NULL,

    subject_name VARCHAR(150) NOT NULL,

    credit INT NOT NULL,

    grade ENUM('A+', 'A', 'A-' 'B', 'B-', 'C', 'C-', 'D', 'F') NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_record
        FOREIGN KEY (record_id)
        REFERENCES education_record(record_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_subject
        UNIQUE (record_id, subject_name)

);

-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX idx_student_name
ON students(name);

CREATE INDEX idx_record_student
ON education_record(student_id);

CREATE INDEX idx_subject_record
ON subject(record_id);

-- ============================================================
-- End of Schema
-- ============================================================

