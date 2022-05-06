from db import db

def get_course_points(course_id, user_id):
    sql = """SELECT COALESCE(SUM(a.result),0)
             FROM answers a, courses c, questions q, users u
             WHERE c.id=q.course_id AND c.id=:course_id
             AND a.user_id=:user_id AND a.user_id=u.id
             AND a.question_id=q.id AND q.visible=1"""
    return db.session.execute(sql, {"course_id":course_id, "user_id":user_id}).fetchone()

def get_all_points():
    sql = """SELECT c.id, c.name, count(q.question)
             FROM courses c, questions q
             WHERE c.visible=1 AND q.visible=1
             AND c.id=q.course_id GROUP BY c.id ORDER BY name"""
    courses = db.session.execute(sql).fetchall()
    list = []
    for course in courses:
        sql = """SELECT u.id, u.name, COALESCE(SUM(a.result),0)
                 FROM answers a, courses c, users u, questions q
                 WHERE q.course_id=c.id AND q.id=a.question_id
                 AND u.id=a.user_id AND c.id=:course_id AND q.visible=1
                 GROUP BY u.id, u.name ORDER BY u.name"""

        results = db.session.execute(sql, {"course_id":course[0]}).fetchall()
        list.append((course[1], results, course[2]))
    return list