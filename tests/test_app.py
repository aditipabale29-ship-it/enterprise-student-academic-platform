import pytest

from app.main import (
    app,
    students,
    faculty,
    courses,
    enrollments,
    grades,
)


@pytest.fixture
def client():
    students.clear()
    faculty.clear()
    courses.clear()
    enrollments.clear()
    grades.clear()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    students.clear()
    faculty.clear()
    courses.clear()
    enrollments.clear()
    grades.clear()


def add_student(client):
    return client.post(
        "/students",
        json={"id": "S001", "name": "Test Student"},
    )


def add_course(client, course_id, name, credits):
    return client.post(
        "/courses",
        json={
            "id": course_id,
            "name": name,
            "credits": credits,
        },
    )


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["status"] == "running"


def test_add_student(client):
    response = add_student(client)

    assert response.status_code == 201
    assert response.json["id"] == "S001"


def test_reject_duplicate_student(client):
    add_student(client)

    response = add_student(client)

    assert response.status_code == 400


def test_reject_enrollment_over_18_credits(client):
    add_student(client)
    add_course(client, "C101", "Python", 10)
    add_course(client, "C102", "Data Science", 9)

    first = client.post(
        "/enrollments",
        json={
            "student_id": "S001",
            "course_id": "C101",
            "semester": "Sem1",
        },
    )

    second = client.post(
        "/enrollments",
        json={
            "student_id": "S001",
            "course_id": "C102",
            "semester": "Sem1",
        },
    )

    assert first.status_code == 201
    assert second.status_code == 400
    assert "credit limit" in second.json["error"]


def test_reject_enrollment_for_unknown_student(client):
    add_course(client, "C101", "Python", 3)

    response = client.post(
        "/enrollments",
        json={
            "student_id": "UNKNOWN",
            "course_id": "C101",
            "semester": "Sem1",
        },
    )

    assert response.status_code == 404


def test_calculate_weighted_gpa(client):
    add_student(client)
    add_course(client, "C101", "Python", 3)
    add_course(client, "C102", "Data Science", 4)

    for course_id in ["C101", "C102"]:
        response = client.post(
            "/enrollments",
            json={
                "student_id": "S001",
                "course_id": course_id,
                "semester": "Sem1",
            },
        )
        assert response.status_code == 201

    client.post(
        "/grades",
        json={
            "student_id": "S001",
            "course_id": "C101",
            "semester": "Sem1",
            "grade_point": 8,
        },
    )

    client.post(
        "/grades",
        json={
            "student_id": "S001",
            "course_id": "C102",
            "semester": "Sem1",
            "grade_point": 9,
        },
    )

    response = client.get("/gpa/S001/Sem1")

    assert response.status_code == 200
    assert response.json["gpa"] == 8.57
