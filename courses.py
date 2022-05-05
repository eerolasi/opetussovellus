from flask import session
from db import db
import users

def get_courses():
    sql = "SELECT id, name, visible FROM courses WHERE visible=1 ORDER BY name"
    result = db.session.execute(sql).fetchall()
    return result

def get_course(course_id):
    sql = "SELECT id, name FROM courses WHERE id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    course = result.fetchone()
    session["course_id"] = course_id
    return course

def create_course(name):
	try:
		sql = "INSERT INTO courses (name, visible) VALUES (:name, 1) RETURNING id"
		db.session.execute(sql, {"name":name}).fetchone()[0]
		db.session.commit()
	except:
		return False
	return True

def delete_course(course_id):
	sql = "UPDATE courses SET visible='0' where id=:course_id"
	db.session.execute(sql, {"course_id":course_id})
	db.session.commit()
	return True

def add_description(course_id, description):
	sql = "INSERT INTO descriptions (course_id, description) VALUES (:course_id, :description)"
	db.session.execute(sql, {"course_id":course_id, "description":description})
	db.session.commit()
	return True

def get_description(course_id):
	sql = "SELECT description FROM descriptions WHERE course_id=:course_id ORDER BY id DESC"
	result = db.session.execute(sql, {"course_id":course_id})
	description = result.fetchone()
	return description