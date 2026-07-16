"""
seed_data.py
Run once to populate the database with:
  - admin user
  - sample student
  - 50+ FAQs across all categories
"""

from models.db import init_db, get_db
from utils.helpers import hash_password

ADMIN_EMAIL = "admin@campus.edu"
ADMIN_PASS = "admin123"
STUDENT_EMAIL = "student@campus.edu"
STUDENT_PASS = "student123"

FAQS = [
    # FEES
    ("What is the semester fee for MCA?", "The semester fee for MCA is ₹45,000 per semester, which includes tuition, lab, and library charges.", "fees"),
    ("When is the fee due date?", "The fee due date is typically within the first two weeks of each semester. Late payment attracts a fine of ₹100 per day.", "fees"),
    ("What are the payment modes for fee?", "Fees can be paid online via the college portal (net banking/UPI/card) or by DD at the accounts office.", "fees"),
    ("Is there any hostel fee?", "Hostel fee is ₹25,000 per semester, inclusive of mess charges. It must be paid at the time of enrollment.", "fees"),
    ("What is the examination fee?", "The examination fee is ₹1,500 per semester and is included in the main fee challan.", "fees"),
    ("Can I get a fee receipt?", "Yes, fee receipts are available on the student portal under 'My Payments' section after payment confirmation.", "fees"),
    ("Is there a fee concession for meritorious students?", "Yes, students scoring above 80% receive a 20% concession on tuition fees, subject to approval.", "fees"),
    # EXAM
    ("When are the semester exams?", "Semester exams are held in November–December for odd semesters and April–May for even semesters.", "exam"),
    ("How do I get my admit card?", "Admit cards are available on the student portal 10 days before the exam. Download and print before the exam date.", "exam"),
    ("What is the minimum attendance required?", "Minimum 75% attendance is required to be eligible to appear in semester exams.", "exam"),
    ("When are results declared?", "Results are usually declared within 30 days after the last exam. Check the college website or portal.", "exam"),
    ("How can I apply for re-evaluation?", "Submit the re-evaluation form available at the exam section within 7 days of result declaration with a fee of ₹500 per paper.", "exam"),
    ("What is the grading system?", "The college follows a 10-point CGPA grading system. O=10, A+=9, A=8, B+=7, B=6, C=5, F=0.", "exam"),
    ("Can I get a back paper form?", "Back paper forms are available at the exam section within 15 days of result announcement. Fee is ₹800 per paper.", "exam"),
    # TIMETABLE
    ("Where can I find the class timetable?", "The class timetable is posted on the department notice board and available on the student portal under 'Timetable'.", "timetable"),
    ("What are the college timings?", "College timings are Monday to Saturday, 9:00 AM to 5:00 PM. Lunch break is from 1:00 PM to 2:00 PM.", "timetable"),
    ("What time do MCA classes start?", "MCA classes start at 9:30 AM and end at 4:30 PM with a one-hour lunch break at 1:00 PM.", "timetable"),
    ("How many periods are there per day?", "There are 6 periods per day, each of 50 minutes duration.", "timetable"),
    ("Is there a lab session schedule?", "Lab sessions are scheduled twice a week, usually on Tuesday and Thursday afternoons from 2:00 PM to 5:00 PM.", "timetable"),
    # HOSTEL
    ("What are the hostel rules?", "Hostel rules include: no guests after 8 PM, lights out by 11 PM, no ragging, proper ID at gate, warden permission for outing.", "hostel"),
    ("What is the hostel curfew timing?", "The hostel curfew is 9:00 PM on weekdays and 10:00 PM on weekends. Late entry requires prior warden permission.", "hostel"),
    ("Is the mess food good?", "The hostel mess serves nutritious vegetarian and non-vegetarian meals. The menu changes weekly and is reviewed by the hostel committee.", "hostel"),
    ("Who is the hostel warden?", "The Boys Hostel Warden is Mr. Ramesh Kumar (Ext: 204). The Girls Hostel Warden is Ms. Priya Sharma (Ext: 205).", "hostel"),
    ("How do I apply for hostel accommodation?", "Fill the hostel allotment form at the administrative office during the first week of the academic year. Seats are allotted on merit basis.", "hostel"),
    ("Is Wi-Fi available in the hostel?", "Yes, hostel rooms have free Wi-Fi from 6:00 AM to 11:00 PM daily. Speed is 50 Mbps shared.", "hostel"),
    # LIBRARY
    ("What are the library timings?", "The library is open Monday to Saturday from 8:30 AM to 8:00 PM. On Sundays it is open from 10:00 AM to 5:00 PM.", "library"),
    ("How many books can I issue at once?", "Students can issue up to 3 books at a time for a period of 14 days. Reference books cannot be issued.", "library"),
    ("What is the fine for late return?", "The fine for late return is ₹2 per book per day after the due date.", "library"),
    ("Can I renew a book?", "Yes, books can be renewed once online via the library portal or in person at the counter, if no one else has reserved it.", "library"),
    ("Does the library have digital resources?", "Yes, the library provides access to INFLIBNET N-LIST, IEEE Xplore, and Springer databases for e-journals and e-books.", "library"),
    ("Who is the librarian?", "The chief librarian is Dr. Anita Verma. You can contact her at library@campus.edu or visit the library counter.", "library"),
    # ADMISSION
    ("What is the eligibility for MCA admission?", "Candidates must have a BCA, B.Sc. (CS/IT/Maths), or any graduation with Mathematics as a subject with minimum 50% marks.", "admission"),
    ("When does admission for MCA open?", "MCA admissions open in June every year. The entrance exam is held in July and counselling in August.", "admission"),
    ("Is there an entrance exam for MCA?", "Yes, admission is based on the state-level MCA entrance exam (NIMCET / state CET). Direct admission is available for management quota.", "admission"),
    ("What documents are required for admission?", "Required documents: 10th & 12th marksheets, graduation certificate, character certificate, migration certificate, passport photos, ID proof.", "admission"),
    ("Is there a management quota?", "Yes, 20% seats are available under management quota. Contact the admissions office for details.", "admission"),
    # FACULTY
    ("Who is the HOD of MCA?", "The Head of the MCA Department is Dr. Sunil Gupta. Office: Room 301, Block B. Email: hod.mca@campus.edu", "faculty"),
    ("Who teaches Machine Learning in MCA?", "Machine Learning is taught by Prof. Neha Singh. Contact: neha.singh@campus.edu, Room 305.", "faculty"),
    ("How do I contact a faculty member?", "Faculty contact details are available on the department website. You can also visit during office hours: 10 AM – 12 PM daily.", "faculty"),
    ("What are the faculty office hours?", "Faculty are available for student consultation from 10:00 AM to 12:00 PM on all working days.", "faculty"),
    ("Who teaches Python in MCA?", "Python Programming is taught by Mr. Ajay Mehta. Contact: ajay.mehta@campus.edu, Room 308.", "faculty"),
    # DEPARTMENT
    ("Where is the MCA department office?", "The MCA department office is located in Block B, Room 301. Office hours are 9 AM to 5 PM on working days.", "department"),
    ("What is the principal's contact?", "Principal Dr. Ramesh Patel can be reached at principal@campus.edu or at Ext: 100. Office is in the main administrative block.", "department"),
    ("Where is the admin office?", "The administrative office is on the ground floor of the main building. It is open from 9 AM to 4 PM on weekdays.", "department"),
    ("How do I get a bonafide certificate?", "Apply for a bonafide certificate at the administrative office with your student ID. It is issued within 2 working days.", "department"),
    ("Where can I get a migration certificate?", "Migration certificates are issued by the exam section on request. Submit a written application with required documents.", "department"),
    # SCHOLARSHIP
    ("What scholarships are available?", "Available scholarships: State Merit Scholarship, National SC/ST Scholarship, OBC Scholarship, and college merit award for toppers.", "scholarship"),
    ("How do I apply for a scholarship?", "Fill the scholarship form available at the student welfare office. Attach income certificate, marksheets, and caste certificate if applicable.", "scholarship"),
    ("When is the scholarship form deadline?", "Scholarship forms must be submitted by October 31 for the current academic year. Late applications are not accepted.", "scholarship"),
    ("What is the merit scholarship amount?", "The merit scholarship covers 50% of tuition fees for students ranking in the top 5% of their class.", "scholarship"),
    # NOTICE
    ("How do I check college notices?", "College notices are posted on the main notice board, department notice boards, and the college website under 'Announcements'.", "notice"),
    ("When is the next holiday?", "For updated holiday lists, check the academic calendar on the college website or visit the administrative office.", "notice"),
    ("How do I report ragging?", "Ragging is strictly prohibited. Report any incident to the anti-ragging committee at 1800-180-5522 or antiharassment@campus.edu.", "notice"),
]


def seed():
    init_db()
    conn = get_db()

    # Create admin
    existing_admin = conn.execute("SELECT id FROM users WHERE email=?", (ADMIN_EMAIL,)).fetchone()
    if not existing_admin:
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            ("Administrator", ADMIN_EMAIL, hash_password(ADMIN_PASS), "admin"),
        )
        print(f"[+] Admin created: {ADMIN_EMAIL} / {ADMIN_PASS}")
    else:
        print("[=] Admin already exists.")

    # Create sample student
    existing_student = conn.execute("SELECT id FROM users WHERE email=?", (STUDENT_EMAIL,)).fetchone()
    if not existing_student:
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            ("Rahul Sharma", STUDENT_EMAIL, hash_password(STUDENT_PASS), "student"),
        )
        print(f"[+] Student created: {STUDENT_EMAIL} / {STUDENT_PASS}")
    else:
        print("[=] Student already exists.")

    # Insert FAQs
    existing_faqs = conn.execute("SELECT COUNT(*) as c FROM faqs").fetchone()["c"]
    if existing_faqs == 0:
        conn.executemany(
            "INSERT INTO faqs (question, answer, category) VALUES (?, ?, ?)",
            FAQS,
        )
        print(f"[+] Inserted {len(FAQS)} FAQs.")
    else:
        print(f"[=] FAQs already present ({existing_faqs} rows). Skipping.")

    conn.commit()
    conn.close()
    print("\n[OK] Database seeding complete.")
    print("    Admin  : admin@campus.edu / admin123")
    print("    Student: student@campus.edu / student123")


if __name__ == "__main__":
    seed()
