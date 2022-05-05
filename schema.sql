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
