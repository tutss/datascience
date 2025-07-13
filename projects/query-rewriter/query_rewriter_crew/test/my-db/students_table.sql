CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    admission_date DATE NOT NULL,
    born_date DATE NOT NULL,
    program VARCHAR(50) NOT NULL,
    UNIQUE(name, admission_date, born_date, program)
);

-- # Sample data for this table below
-- INSERT INTO students (name, admission_date, born_date, program) VALUES
-- ('Anne Silva', '2020-01-01', '1994-03-01', 'Computer Science'),
-- ('Jane Smith', '2020-01-02', '1998-10-23', 'Mathematics'),
-- ('Mariana Lima', '2020-01-01', '1992-01-12', 'Physics'),
-- ('Jim Carrey', '2020-01-02', '2000-01-05', 'Mathematics'),
-- ('Kate McDonald', '2020-01-01', '2001-12-1', 'Computer Science'),
-- ('Lucas Steph', '2020-01-02', '1998-05-15', 'Mathematics'),
-- ('James K', '2020-01-01', '1995-04-20', 'Geography'),
-- ('Estefan Rodriguez', '2020-01-02', '1990-01-02', 'Geography'),
-- ('Li Dong', '2020-01-01', '1997-09-13', 'Physics'),
-- ('Abhishek T', '2020-01-02', '1997-07-17', 'Astronomy'),
-- ('Alice Johnson', '2020-01-03', '1990-01-03', 'Computer Science');

