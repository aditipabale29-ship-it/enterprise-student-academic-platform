import threading


class Database:
    """Thread-safe in-memory database for Student Academic Platform."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._init_db()
            return cls._instance

    def _init_db(self):
        self.students = {}
        self.faculty = {}
        self.courses = {}
        self.enrollments = []
        self.grades = []
        self._seed_initial_data()

    def _seed_initial_data(self):
        self.students["S101"] = {
            "student_id": "S101",
            "name": "Alice Johnson",
            "email": "alice@university.edu",
            "semester": 1,
            "total_credits": 0
        }

        self.faculty["F101"] = {
            "faculty_id": "F101",
            "name": "Dr. Robert Smith",
            "email": "robert.smith@university.edu"
        }

        self.courses["C101"] = {
            "course_id": "C101",
            "name": "Python Programming",
            "credits": 4,
            "faculty_id": "F101",
            "capacity": 30,
            "enrolled": 0
        }

        self.courses["C102"] = {
            "course_id": "C102",
            "name": "Data Structures",
            "credits": 4,
            "faculty_id": "F101",
            "capacity": 30,
            "enrolled": 0
        }

    def reset(self):
        """Restore initial database state for testing."""
        with self._lock:
            self.students.clear()
            self.faculty.clear()
            self.courses.clear()
            self.enrollments.clear()
            self.grades.clear()
            self._seed_initial_data()


db = Database()
