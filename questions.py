from db import db

def get_questions(course_id):
	sql = """SELECT id, question, answer, course_id FROM questions
			 WHERE course_id=:course_id AND visible=1"""
	result = db.session.execute(sql, {"course_id":course_id})
	questions = result.fetchall()
	return questions

def get_question(question_id):
	sql = "SELECT id, question, answer, course_id FROM questions WHERE id=:question_id"
	result = db.session.execute(sql, {"question_id":question_id})
	question = result.fetchall()
	return question

def add_question(course_id, question, answer):
	sql = """INSERT INTO questions (course_id, question, answer, visible)
			 VALUES (:course_id, :question, :answer, 1) returning id"""
	db.session.execute(sql, {"course_id":course_id, "question":question, "answer":answer})
	db.session.commit()
	return True

def add_answer(user_id, question_id, answer):
	sql = "SELECT answer FROM questions WHERE id=:question_id"
	correct = db.session.execute(sql, {"question_id":question_id}).fetchone()[0]
	sql="""SELECT a.result FROM answers a, questions q WHERE user_id=:user_id AND
	 		question_id=:question_id AND a.result=1"""
	result = db.session.execute(sql,{"user_id":user_id,"question_id":question_id}).fetchall()
	if not result or result == 0:
		if answer.lower() == correct.lower():
			result = 1
		else:
			result = 0
		sql = """INSERT INTO answers (user_id, question_id, answer, result)
				 VALUES (:user_id, :question_id,:answer, :result)"""
		db.session.execute(sql, {"user_id":user_id,"question_id":question_id,
								"answer":answer, "result":result})
		db.session.commit()
	else:
		db.session.execute(sql, {"user_id":user_id, "question_id":question_id,
								"answer":answer, "result":result})
		db.session.commit()

def get_course(question_id):
	sql = "SELECT course_id FROM questions WHERE id=:id"
	result = db.session.execute(sql, {"id":question_id}).fetchone()
	return result

def delete_question(question_id):
	sql = "UPDATE questions SET visible='0' WHERE id=:question_id"
	db.session.execute(sql, {"question_id":question_id})
	db.session.commit()
	return True
