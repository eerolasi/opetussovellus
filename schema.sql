CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	name TEXT UNIQUE,
	password TEXT,
	role INTEGER
);

CREATE TABLE courses (
	id SERIAL PRIMARY KEY,
	name TEXT UNIQUE,
	visible INTEGER
);

CREATE TABLE descriptions (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses,
	description TEXT
);

CREATE TABLE questions (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES courses,
	question TEXT,
	answer TEXT,
	visible INTEGER
);

CREATE TABLE answers (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	question_id INTEGER REFERENCES questions,
	answer TEXT,
	result INTEGER
);
