CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    quiz_date TEXT NOT NULL
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
);
