"""
Create or update LearningPath + Lesson records for every course in the courses app.
LearningPath slugs are set to match Course slugs so CourseDetailView can look them up.

Run:  python manage.py setup_course_notes
Re-runnable safely (uses get_or_create).
"""
from django.core.management.base import BaseCommand
from academy.models import LearningPath, Lesson

# Each entry: (course_slug, title, category, level, duration, skill_stack, summary, lessons)
# lesson tuple: (title, order, objective, content, exercise, quiz_q, project, notes, mins)

COURSE_PATHS = [

    # ── WEB DEVELOPMENT ─────────────────────────────────────────────────────────
    ('web-development', 'Web Development', 'web', 'beginner', '10 weeks',
     'HTML5, CSS3, JavaScript, React, Django', 'Build real websites from scratch to full-stack.', [

        (1, 'HTML & Page Structure',
         'Build the skeleton of any web page using semantic HTML5.',
         """HTML (HyperText Markup Language) is the language of the web. Every page you visit is built on HTML.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Web Page</title>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/courses">Courses</a>
            <a href="/contact">Contact</a>
        </nav>
    </header>
    <main>
        <h1>Welcome to CodeSavannah!</h1>
        <p>We teach real-world coding skills.</p>
        <ul>
            <li>Python</li>
            <li>Web Development</li>
            <li>Cybersecurity</li>
        </ul>
    </main>
    <footer>
        <p>&copy; 2025 CodeSavannah Academy</p>
    </footer>
</body>
</html>
```

**Semantic elements** — use tags that describe meaning:
- `<header>` — top of page or section
- `<nav>` — navigation links
- `<main>` — primary content
- `<article>` — self-contained content
- `<section>` — thematic grouping
- `<aside>` — sidebar content
- `<footer>` — bottom of page or section

**Why semantics matter:**
- Search engines rank semantic pages higher
- Screen readers navigate by landmarks
- Your code is easier to maintain""",
         'Build an HTML profile page with header, nav, main (about + skills), and footer.',
         'Which HTML tag wraps the primary content of a page?',
         'Create a full HTML page for a local restaurant — menu, location, opening hours.',
         'Always add lang="en" on <html> and charset="UTF-8" in <head>. Missing these breaks internationalisation and encoding.', 35),

        (2, 'CSS Styling & Layout',
         'Style pages with CSS properties, Flexbox, and Grid.',
         """CSS (Cascading Style Sheets) controls how HTML looks.

```css
/* Variables — define once, use everywhere */
:root {
    --primary:  #1341a8;
    --accent:   #00d4f5;
    --radius:   8px;
}

/* Selectors */
body        { font-family: 'Segoe UI', sans-serif; margin: 0; }
.card       { padding: 24px; border-radius: var(--radius); }
#hero       { height: 80vh; }
a:hover     { color: var(--accent); }

/* Flexbox — 1D layout */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    height: 72px;
}

/* Grid — 2D layout */
.course-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
}

/* Responsive */
@media (max-width: 768px) {
    .navbar { flex-direction: column; height: auto; }
    .course-grid { grid-template-columns: 1fr; }
}
```

**Box model:** every element is a box — margin → border → padding → content.
Set `box-sizing: border-box` globally so padding doesn't add to declared width.""",
         'Style a card component: shadow, rounded corners, hover lift effect using transform.',
         'Which CSS property creates a 2-dimensional grid layout?',
         'Build a fully responsive landing page with a sticky navbar, hero, 3-column features, and footer.',
         'Use CSS custom properties (variables) for colours and spacing — changing a theme becomes a one-line edit.', 45),

        (3, 'JavaScript Interactivity',
         'Make pages dynamic with DOM manipulation and events.',
         """JavaScript brings pages to life. It runs in the browser and responds to user actions.

```javascript
// Select elements
const btn     = document.querySelector('#submit-btn');
const results = document.querySelector('#results');

// Listen for events
btn.addEventListener('click', () => {
    const input = document.querySelector('#search').value.trim();
    if (!input) return;
    results.innerHTML = `<p>You searched for: <strong>${input}</strong></p>`;
});

// Fetch data from an API
async function loadCourses() {
    const res  = await fetch('/api/courses/');
    const data = await res.json();
    data.forEach(course => {
        const card = document.createElement('article');
        card.className = 'card';
        card.innerHTML = `<h2>${course.title}</h2><p>${course.description}</p>`;
        document.querySelector('#grid').appendChild(card);
    });
}

loadCourses();
```

**Event types:** `click`, `submit`, `keydown`, `input`, `scroll`, `resize`, `DOMContentLoaded`

**localStorage** — persist data between sessions:
```javascript
localStorage.setItem('theme', 'dark');
const theme = localStorage.getItem('theme'); // 'dark'
```""",
         'Build a live character counter for a textarea — update a count badge on every keystroke.',
         'What DOM method attaches an event listener to an element?',
         'Build a to-do list app — add tasks, tick complete, delete, persist to localStorage.',
         'Use textContent to set text, never innerHTML with user-provided data — innerHTML with external input causes XSS attacks.', 45),

        (4, 'React Components & State',
         'Build component-based UIs with React and useState.',
         """React is JavaScript's most popular UI library. Instead of manipulating the DOM directly, you describe what the UI should look like and React updates it.

```jsx
import { useState } from 'react';

function CourseCard({ title, level, enrolled, onEnroll }) {
    return (
        <div className="card">
            <span className={`tag tag-${level}`}>{level}</span>
            <h2>{title}</h2>
            <button
                onClick={onEnroll}
                className={enrolled ? 'btn btn-success' : 'btn btn-primary'}
            >
                {enrolled ? '✓ Enrolled' : 'Enroll Now'}
            </button>
        </div>
    );
}

function CourseList() {
    const [courses, setCourses] = useState([
        { id: 1, title: 'Python Programming', level: 'beginner',  enrolled: false },
        { id: 2, title: 'Web Development',    level: 'beginner',  enrolled: false },
        { id: 3, title: 'Cybersecurity',      level: 'intermediate', enrolled: false },
    ]);

    const enroll = (id) => {
        setCourses(courses.map(c => c.id === id ? { ...c, enrolled: true } : c));
    };

    return (
        <div className="course-grid">
            {courses.map(c => (
                <CourseCard key={c.id} {...c} onEnroll={() => enroll(c.id)} />
            ))}
        </div>
    );
}
```

**Setup:** `npm create vite@latest my-app -- --template react && cd my-app && npm install && npm run dev`""",
         'Add a search input to CourseList that filters visible cards as you type.',
         'Which React hook stores component-local state?',
         'Build a full course browser with search, category filter, and enrol toggle using React.',
         "React re-renders only when state changes. Never mutate state directly — always call the setter function.", 50),

        (5, 'Django Full-Stack',
         'Build server-rendered web apps with Python and Django.',
         """Django is Python's most popular full-stack web framework — used by Instagram, Pinterest, and NASA.

```python
# models.py — defines database tables
from django.db import models

class Course(models.Model):
    title       = models.CharField(max_length=180)
    description = models.TextField()
    level       = models.CharField(max_length=20)
    instructor  = models.CharField(max_length=120)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

```python
# views.py — business logic
from django.views.generic import ListView, DetailView
from .models import Course

class CourseListView(ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'
```

```html
{# templates/courses/list.html #}
{% for course in courses %}
<article class="card">
    <h2>{{ course.title }}</h2>
    <p>{{ course.description|truncatewords:20 }}</p>
    <a href="{{ course.get_absolute_url }}">Learn more</a>
</article>
{% endfor %}
```

**Commands:**
```bash
python manage.py makemigrations  # detect model changes
python manage.py migrate         # apply to DB
python manage.py createsuperuser # admin login
python manage.py runserver       # start dev server
```""",
         'Add a `search` view that filters courses by title keyword from a GET parameter.',
         'What Django command applies pending database migrations?',
         'Build a blog with Django: Post model, list view, detail view, create form, admin panel.',
         "Django's admin (localhost:8080/admin/) auto-generates a full CRUD interface from your models — use it!", 60),
    ]),

    # ── PYTHON PROGRAMMING ──────────────────────────────────────────────────────
    ('python-programming', 'Python Programming', 'programming', 'beginner', '8 weeks',
     'Python 3, OOP, File I/O, Django, APIs', 'From zero to Python — syntax, logic, OOP, and real projects.', [

        (1, 'Python Basics',
         'Write and run Python programs using variables, types, and print.',
         """Python is the world's most popular language. It's readable, powerful, and used everywhere.

```python
# Variables and data types
name       = 'Amara'       # str  — text
age        = 17            # int  — whole number
gpa        = 3.85          # float — decimal
is_student = True          # bool — True/False

# Print with f-strings
print(f'{name} is {age} years old with a GPA of {gpa}')

# Type conversion
age_str = str(age)         # int → str
price   = float('9.99')   # str → float
count   = int('42')       # str → int

# User input
user_name = input('Enter your name: ')
print(f'Welcome, {user_name}!')

# Arithmetic operators
print(10 + 3)   # 13
print(10 - 3)   # 7
print(10 * 3)   # 30
print(10 / 3)   # 3.333...
print(10 // 3)  # 3   (floor division)
print(10 % 3)   # 1   (remainder)
print(2 ** 8)   # 256 (power)
```""",
         'Write a program that asks for your name and birth year, then prints your age.',
         'Which Python function reads input from the user?',
         'Build a Personal Info Card — ask for name, country, age, hobby, print a formatted card.',
         'Python was created by Guido van Rossum in 1991. The name comes from Monty Python, not the snake!', 30),

        (2, 'Control Flow',
         'Use if/elif/else and loops to control program logic.',
         """```python
# if / elif / else
score = int(input('Enter score: '))

if score >= 90:
    print('A — Excellent!')
elif score >= 80:
    print('B — Very Good')
elif score >= 70:
    print('C — Good')
elif score >= 60:
    print('D — Pass')
else:
    print('F — Retake required')

# for loop — iterate a range
for i in range(1, 11):
    print(f'{i} x 7 = {i * 7}')

# while loop — repeat until condition is false
attempts = 3
while attempts > 0:
    guess = input('Guess the number: ')
    if guess == '42':
        print('Correct!')
        break
    attempts -= 1
    print(f'{attempts} attempts left')

# Logical operators
age = 17
if age >= 13 and age <= 19:
    print('Teenager')

if not is_student:
    print('Not enrolled')
```

**break** — exit the loop immediately
**continue** — skip rest of current iteration
**pass** — do nothing (placeholder)""",
         'Write FizzBuzz: print numbers 1–100, but Fizz for multiples of 3, Buzz for 5, FizzBuzz for both.',
         'Which keyword immediately exits a loop in Python?',
         'Build a Number Guessing Game — computer picks random 1–100, player guesses with hints.',
         'Python uses indentation to define code blocks — no curly braces. 4 spaces is the standard.', 40),

        (3, 'Functions',
         'Write reusable, modular code with Python functions.',
         """```python
# Define and call a function
def greet(name, language='en'):
    if language == 'sw':
        return f'Habari, {name}!'
    return f'Hello, {name}!'

print(greet('Grace'))           # Hello, Grace!
print(greet('Brian', 'sw'))     # Habari, Brian!

# Multiple return values
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([5, 3, 9, 1, 7])
print(f'Min: {lo}, Max: {hi}')

# *args — variable positional arguments
def total(*numbers):
    return sum(numbers)

print(total(1, 2, 3, 4, 5))  # 15

# **kwargs — variable keyword arguments
def profile(**details):
    for key, value in details.items():
        print(f'{key}: {value}')

profile(name='Zara', school='CodeSavannah', grade='Form 4')

# Lambda — one-line function
square = lambda x: x ** 2
evens  = list(filter(lambda x: x % 2 == 0, range(1, 11)))
```""",
         'Write a function is_palindrome(text) that returns True if the text reads the same forwards and backwards.',
         'What keyword defines a function in Python?',
         'Build a Scientific Calculator with functions for +, -, *, /, power, sqrt, and factorial.',
         'Functions with no return statement return None automatically.', 40),

        (4, 'Lists, Dicts & Comprehensions',
         'Organise and process data with Python collections.',
         """```python
# Lists
students = ['Amara', 'Brian', 'Grace', 'Kofi', 'Zara']
students.append('Lena')       # add to end
students.insert(0, 'Aaron')   # add at index
students.remove('Brian')      # remove by value
students.sort()               # alphabetical sort
print(students[0])            # first item
print(students[-1])           # last item
print(students[1:3])          # slice

# List comprehensions
squares  = [x**2 for x in range(1, 11)]
evens    = [x for x in range(1, 21) if x % 2 == 0]
upper    = [s.upper() for s in students]

# Dictionaries
student = {
    'name':   'Grace Adhiambo',
    'grade':  'Form 3',
    'gpa':    3.9,
    'skills': ['Python', 'HTML', 'Robotics'],
}

print(student['name'])
print(student.get('email', 'N/A'))  # safe — returns default if key missing

student['email'] = 'grace@csa.ke'   # add new key

for key, value in student.items():
    print(f'{key}: {value}')

# Dict comprehension
grades = {'Amara': 85, 'Brian': 72, 'Grace': 94}
above_80 = {name: score for name, score in grades.items() if score >= 80}
```""",
         'Create a contact book dictionary. Add 5 contacts, search by name, delete one, print all remaining.',
         'How do you safely access a dictionary key that might not exist?',
         'Build a Student Records System using dictionaries — add, update, delete, display all records.',
         'Python lists can hold mixed types: [1, "hello", True, 3.14] is perfectly valid.', 45),

        (5, 'File I/O & Modules',
         'Read and write files, and use Python standard library modules.',
         """```python
# Writing a file
with open('students.txt', 'w') as f:
    f.write('Amara Osei,Form3,3.85\\n')
    f.write('Brian Otieno,Form2,3.20\\n')

# Reading a file
with open('students.txt', 'r') as f:
    for line in f:
        name, grade, gpa = line.strip().split(',')
        print(f'{name} — GPA: {gpa}')

# CSV with the csv module
import csv

with open('scores.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'score'])
    writer.writeheader()
    writer.writerow({'name': 'Grace', 'score': 94})
    writer.writerow({'name': 'Kofi',  'score': 88})

# Useful standard library modules
import random
import math
import os
import datetime

print(random.randint(1, 100))     # random integer
print(math.sqrt(144))             # 12.0
print(math.pi)                    # 3.14159...
print(os.getcwd())                # current directory
print(datetime.date.today())      # 2025-06-05

# Installing external libraries
# pip install requests
import requests
res  = requests.get('https://jsonplaceholder.typicode.com/posts/1')
data = res.json()
print(data['title'])
```""",
         'Write an expense tracker that saves each expense (name, amount, category) to a CSV file and reads it back.',
         'What file mode appends new data without deleting existing content?',
         'Build a daily journal app — entries stored in a text file, option to view all entries.',
         'Always use `with open()` — it closes the file even if an error occurs midway through.', 45),

        (6, 'OOP with Python',
         'Model real-world objects using classes, inheritance, and encapsulation.',
         """```python
class Student:
    school = 'CodeSavannah Academy'  # class attribute

    def __init__(self, name, grade, gpa):
        self.name  = name    # instance attributes
        self.grade = grade
        self.gpa   = gpa

    def get_letter_grade(self):
        if self.gpa >= 3.7:  return 'A'
        if self.gpa >= 3.0:  return 'B'
        if self.gpa >= 2.0:  return 'C'
        return 'F'

    def __str__(self):
        return f'{self.name} ({self.grade}) — {self.get_letter_grade()}'

    def __repr__(self):
        return f'Student(name={self.name!r}, gpa={self.gpa})'


# Inheritance
class GraduateStudent(Student):
    def __init__(self, name, gpa, thesis_title):
        super().__init__(name, 'Graduate', gpa)
        self.thesis = thesis_title

    def __str__(self):
        return f'{super().__str__()} | Thesis: {self.thesis}'


# Usage
s1 = Student('Grace', 'Form 3', 3.9)
s2 = GraduateStudent('Dr. Amara', 3.95, 'AI in African Education')
students = [s1, s2]

for student in students:
    print(student)

# Sort by GPA
students.sort(key=lambda s: s.gpa, reverse=True)
```

**Four pillars of OOP:**
- **Encapsulation** — bundle data and methods in a class
- **Abstraction** — hide complex details behind simple interfaces
- **Inheritance** — child class reuses parent class
- **Polymorphism** — same method name, different behaviour""",
         'Create a BankAccount class with deposit, withdraw, and balance property. Prevent negative balance.',
         'Which Python method is called when an object is created?',
         'Build a Library Management System — Book, Member, Library classes with borrowing and returning logic.',
         'Use @property to create computed attributes — they look like attributes but run code.', 50),
    ]),

    # ── CYBERSECURITY FOUNDATIONS ───────────────────────────────────────────────
    ('cybersecurity-foundations', 'Cybersecurity Foundations', 'cybersecurity', 'beginner', '8 weeks',
     'Networking, OWASP, Linux, CTF, Cryptography', 'Understand how attacks work — then learn to defend against them.', [

        (1, 'The CIA Triad & Threat Landscape',
         'Understand the core security principles and common attack types.',
         """Every cybersecurity decision comes back to three principles — the **CIA Triad**:

- **Confidentiality** — only authorised users can read the data
- **Integrity** — data is accurate and unmodified
- **Availability** — systems are up when needed

**Common attack types:**

| Attack | How it works | Defence |
|--------|-------------|---------|
| Phishing | Fake emails/sites steal credentials | MFA, training |
| SQL Injection | Malicious SQL via input fields | Parameterised queries |
| XSS | JavaScript injected into pages | Input sanitisation |
| MITM | Attacker intercepts traffic | TLS/HTTPS |
| DDoS | Flood server with requests | Rate limiting, CDN |
| Ransomware | Encrypts files, demands ransom | Backups, endpoint security |
| Brute Force | Try all password combinations | Account lockout, strong passwords |

**OWASP Top 10** — the most critical web vulnerabilities, published by the Open Web Application Security Project.

**Defence in depth** — don't rely on a single layer. Multiple controls mean a breach of one layer doesn't compromise everything.

**Principle of least privilege** — give users only the minimum access they need to do their job.""",
         'Research a real-world breach (e.g., LinkedIn 2021). Which CIA properties were violated?',
         'What does the A in the CIA triad stand for?',
         'Sign up at picoCTF.org and complete 5 beginner challenges. Document what you learned.',
         '95% of breaches involve human error — phishing and social engineering beat technical exploits most of the time.', 45),

        (2, 'Networking Fundamentals',
         'Understand how data moves across the internet.',
         """The internet is built on protocols — agreed standards for communication.

**Key protocols:**
| Protocol | Port | Use |
|----------|------|-----|
| HTTP | 80 | Web pages (unencrypted) |
| HTTPS | 443 | Secure web (TLS encrypted) |
| SSH | 22 | Secure remote shell |
| FTP | 21 | File transfer |
| DNS | 53 | Name → IP resolution |
| SMTP | 25/587 | Email sending |

**IP addresses:** unique numbers identifying devices (192.168.1.1 = local, 8.8.8.8 = Google DNS)

**TCP vs UDP:**
- TCP — reliable, ordered, slower (web, email)
- UDP — fast, no guarantee (video calls, games)

**Useful tools:**
```bash
# Scan open ports on a host
nmap -sV 192.168.1.1

# Trace the route packets take
traceroute google.com      # Linux/Mac
tracert google.com         # Windows

# Check DNS resolution
nslookup codesavannah.ac

# Capture network traffic (GUI)
wireshark
```

**Firewalls** filter traffic by IP, port, and protocol. Always run a host firewall and only open needed ports.""",
         'Run `nmap localhost` on your machine. List every open port and identify what service uses it.',
         'Which protocol encrypts web traffic on port 443?',
         'Set up Wireshark and capture your own HTTP traffic. Identify the request/response for a web page load.',
         'Never connect to public WiFi without a VPN — all unencrypted traffic is visible to anyone on the network.', 50),

        (3, 'Linux for Security',
         'Navigate Linux, manage permissions, and use security tools.',
         """Most servers run Linux. Security professionals live in the terminal.

```bash
# Navigation
ls -la              # list files with permissions
cd /etc/nginx       # change directory
pwd                 # print working directory
cat /etc/passwd     # read a file
grep 'root' /etc/passwd  # search in file

# File permissions: rwxrwxrwx (owner-group-others)
chmod 755 script.sh      # owner: rwx, group/others: r-x
chmod 600 private.key    # owner: rw only
chown amara:users file   # change owner

# Process management
ps aux               # list all processes
kill -9 1234         # force kill PID 1234
top                  # live process monitor
htop                 # better process monitor

# Network
ss -tulnp            # listening ports
curl -I https://codesavannah.ac  # HTTP headers
wget https://example.com/file.zip

# Log files (where attacks leave traces)
tail -f /var/log/auth.log    # live SSH login attempts
cat /var/log/syslog | grep error
```

**sudo** — run as root. Only use when necessary.
**SSH key authentication** — more secure than passwords for remote access.""",
         'On a Linux system, find all files modified in the last 24 hours using: `find / -mtime -1 2>/dev/null`',
         'What Linux command shows currently listening network ports?',
         'Harden a fresh Ubuntu server: disable root login, configure UFW firewall, set up fail2ban.',
         'Never run web servers or databases as root. Use dedicated service accounts with minimal permissions.', 50),

        (4, 'Web Security & OWASP',
         'Find and fix the most common web vulnerabilities.',
         """The OWASP Top 10 are the most critical web security risks.

**SQL Injection:**
```python
# VULNERABLE — never do this
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# SAFE — parameterised query
cursor.execute("SELECT * FROM users WHERE name = %s", [user_input])
# or Django ORM (always safe)
User.objects.filter(name=user_input)
```

**Cross-Site Scripting (XSS):**
```python
# VULNERABLE
return HttpResponse(f'<p>Hello {request.GET["name"]}</p>')

# SAFE — Django templates auto-escape
return render(request, 'hello.html', {'name': request.GET.get('name', '')})
# In template: {{ name }} is escaped, {{ name|safe }} is NOT
```

**Broken Authentication:**
- Never store plain-text passwords — use bcrypt/Argon2
- Enforce MFA on admin accounts
- Use secure session cookies (HttpOnly, Secure, SameSite=Strict)
- Implement account lockout after failed attempts

**Security headers:**
```python
# Django settings
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
```""",
         'Use the OWASP ZAP scanner on a test site (like http://testphp.vulnweb.com) and list vulnerabilities found.',
         'What type of attack injects malicious SQL into a database query?',
         'Set up a deliberately vulnerable app (DVWA or WebGoat) and exploit then patch 3 vulnerabilities.',
         'Django protects against XSS, CSRF, and SQL injection by default — only break these protections intentionally.', 55),

        (5, 'Cryptography Basics',
         'Understand hashing, encryption, and digital certificates.',
         """Cryptography is the foundation of all digital security.

**Hashing** — one-way transformation, same input always gives same output:
```python
import hashlib

text = 'my_password'
h    = hashlib.sha256(text.encode()).hexdigest()
print(h)  # 256-bit hex string

# For passwords, use bcrypt (salted, slow by design)
import bcrypt
password = b'my_password'
hashed   = bcrypt.hashpw(password, bcrypt.gensalt())
bcrypt.checkpw(password, hashed)  # True
```

**Symmetric encryption** — same key for encrypt/decrypt (AES):
```python
from cryptography.fernet import Fernet
key     = Fernet.generate_key()
f       = Fernet(key)
token   = f.encrypt(b'secret message')
message = f.decrypt(token)
```

**Asymmetric encryption** (public/private key pairs):
- Public key encrypts (anyone can send you messages)
- Private key decrypts (only you can read them)
- Used in HTTPS, SSH, code signing

**TLS/HTTPS** — certificate authorities (CAs) vouch that a public key belongs to a domain.

**Common hash algorithms:**
- MD5 — broken, never use for security
- SHA-1 — deprecated
- SHA-256 — acceptable
- bcrypt/Argon2 — best for passwords (slow by design)""",
         'Hash 5 different inputs with SHA-256 and observe that even one character change gives a completely different hash.',
         'Which cryptographic operation is one-way and cannot be reversed?',
         'Implement a simple password manager that stores encrypted entries in a local file.',
         "MD5 and SHA-1 are broken — don't use them for passwords or data integrity. Use SHA-256+ or bcrypt.", 50),
    ]),

    # ── CLOUD COMPUTING ─────────────────────────────────────────────────────────
    ('cloud-computing', 'Cloud Computing', 'cloud', 'intermediate', '10 weeks',
     'AWS, Azure, GCP, Docker, Kubernetes, Terraform', 'Deploy, scale, and manage applications in the cloud.', [

        (1, 'Cloud Concepts & AWS Fundamentals',
         'Understand cloud models and navigate core AWS services.',
         """**Cloud computing** delivers on-demand IT resources over the internet — servers, storage, databases, networking, and more.

**Service models:**
- **IaaS** (Infrastructure as a Service) — raw VMs and storage (AWS EC2, GCP Compute)
- **PaaS** (Platform as a Service) — managed platform, deploy code (Heroku, App Engine)
- **SaaS** (Software as a Service) — ready-to-use apps (Gmail, Salesforce)

**AWS core services:**
| Service | Purpose |
|---------|---------|
| EC2 | Virtual servers |
| S3 | Object storage (files, images, backups) |
| RDS | Managed databases (PostgreSQL, MySQL) |
| Lambda | Serverless functions |
| CloudFront | CDN — global fast delivery |
| Route 53 | DNS and domain management |
| IAM | Users, roles, and permissions |
| VPC | Private network |

**AWS free tier:** 750 hours/month EC2 t2.micro, 5GB S3, 1M Lambda requests — free for 12 months.

```bash
# Install and configure AWS CLI
pip install awscli
aws configure   # enter Access Key, Secret Key, region

# Deploy a static site to S3
aws s3 sync ./dist s3://my-bucket --delete
aws s3 website s3://my-bucket --index-document index.html
```""",
         'Create an AWS free-tier account and deploy a static HTML page to S3 with public access.',
         'What AWS service stores files and objects in the cloud?',
         'Deploy a static React app to S3 + CloudFront with a custom domain on Route 53.',
         'Always enable MFA on your AWS root account. Never commit AWS credentials to git.', 60),

        (2, 'Linux Servers & SSH',
         'Launch, configure, and secure a Linux virtual machine.',
         """```bash
# Launch EC2 instance (AWS Console or CLI)
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name my-key \
    --security-group-ids sg-12345

# Connect via SSH
ssh -i my-key.pem ubuntu@<PUBLIC-IP>

# Initial server setup
sudo apt update && sudo apt upgrade -y
sudo apt install nginx python3-pip git ufw -y

# Firewall
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Deploy a Django app
git clone https://github.com/you/myapp.git
cd myapp
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

**Nginx as reverse proxy** — sits in front of Gunicorn, handles SSL, static files, and load balancing.""",
         'Launch an EC2 t2.micro instance, SSH in, install Nginx, and verify the default page loads in a browser.',
         'What command securely connects to a remote Linux server?',
         'Deploy a Django app to EC2 with Nginx + Gunicorn + Let\'s Encrypt SSL certificate.',
         "Use an SSH config file (~/.ssh/config) to save connection aliases — `ssh myserver` beats typing the full command.", 55),

        (3, 'Docker & Containers',
         'Package and run applications with Docker containers.',
         """**Docker** packages your app and all its dependencies into an isolated container that runs identically anywhere.

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -d -p 8080:8000 --name myapp myapp:latest

# Check logs
docker logs myapp

# Shell into container
docker exec -it myapp bash
```

**Docker Compose** — run multiple services together:
```yaml
# docker-compose.yml
version: '3.9'
services:
  web:
    build: .
    ports: ['8000:8000']
    environment:
      - DATABASE_URL=postgresql://user:pass@db/mydb
    depends_on: [db]
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
  redis:
    image: redis:alpine
```

```bash
docker-compose up -d      # start all services
docker-compose logs -f    # follow logs
docker-compose down       # stop and remove
```""",
         'Containerise the CodeSavannah Django project using Docker. Verify `docker run` starts the server.',
         'What file defines how to build a Docker image?',
         'Create a docker-compose.yml that runs Django + PostgreSQL + Redis together.',
         "Add a .dockerignore file (like .gitignore) to exclude venv, __pycache__, .env from the image build.", 55),

        (4, 'Kubernetes Basics',
         'Orchestrate containers at scale with Kubernetes.',
         """**Kubernetes (K8s)** automates deploying, scaling, and managing containerised applications.

**Core concepts:**
- **Pod** — one or more containers running together (smallest deployable unit)
- **Deployment** — manages multiple identical pods and handles updates
- **Service** — stable network endpoint to reach pods
- **Ingress** — routes external HTTP traffic to services
- **ConfigMap / Secret** — configuration and sensitive data

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8000
        resources:
          requests: { cpu: '100m', memory: '128Mi' }
          limits:   { cpu: '500m', memory: '512Mi' }
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-svc
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs -f <pod-name>
kubectl scale deployment myapp --replicas=5
kubectl rollout undo deployment/myapp  # roll back
```""",
         'Deploy a simple Nginx pod to a local Minikube cluster and expose it via a NodePort service.',
         'What Kubernetes object ensures a set number of identical pods are always running?',
         'Deploy the CodeSavannah Django app to a Kubernetes cluster with 3 replicas and auto-scaling.',
         'Use Horizontal Pod Autoscaler (HPA) to automatically scale your pods based on CPU/memory usage.', 60),
    ]),

    # ── DATA SCIENCE ────────────────────────────────────────────────────────────
    ('data-science', 'Data Science', 'ai', 'intermediate', '10 weeks',
     'Python, pandas, NumPy, Matplotlib, scikit-learn, SQL', 'Turn raw data into insights and predictions.', [

        (1, 'Data Analysis with pandas',
         'Load, clean, and explore tabular data using pandas.',
         """**pandas** is Python's primary data analysis library — think Excel in code.

```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('students.csv')
df = pd.read_excel('grades.xlsx', sheet_name='Term2')

# Explore
print(df.shape)          # (rows, cols)
print(df.dtypes)         # column types
print(df.describe())     # stats: mean, std, min, max
print(df.head(10))       # first 10 rows
print(df.isnull().sum()) # missing values per column

# Select
df['name']                         # one column
df[['name', 'gpa']]                # multiple columns
df[df['gpa'] >= 3.5]               # filter rows
df.loc[0:4, 'name':'grade']        # label-based slice
df.iloc[0:4, 0:3]                  # integer slice

# Clean
df.dropna(inplace=True)            # remove rows with NaN
df['gpa'].fillna(df['gpa'].mean(), inplace=True)
df.drop_duplicates(inplace=True)
df['name'] = df['name'].str.strip().str.title()
df['age']  = df['age'].astype(int)

# Group and aggregate
summary = (df.groupby('grade')
             .agg(count=('name', 'count'),
                  avg_gpa=('gpa', 'mean'),
                  top_gpa=('gpa', 'max'))
             .reset_index())
print(summary)
```""",
         'Load a CSV of your choice, find and fill missing values, filter rows above the mean, and print summary stats.',
         'Which pandas method shows descriptive statistics like mean and standard deviation?',
         'Analyse a real dataset (Kaggle) — clean it, answer 5 business questions with code.',
         'Always call .copy() when creating a derived DataFrame to avoid SettingWithCopyWarning.', 55),

        (2, 'Data Visualisation',
         'Create clear charts and dashboards with Matplotlib and Seaborn.',
         """```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='darkgrid', palette='husl')

# Bar chart
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df['grade'], df['avg_gpa'], color='#1341a8')
ax.set_xlabel('Grade')
ax.set_ylabel('Average GPA')
ax.set_title('Average GPA by Grade — CodeSavannah 2025')
plt.tight_layout()
plt.savefig('gpa_chart.png', dpi=150)
plt.show()

# Scatter plot with regression line
sns.regplot(data=df, x='hours_studied', y='gpa', scatter_kws={'alpha': 0.5})
plt.title('Study Hours vs GPA')
plt.show()

# Heatmap (correlations)
corr = df[['gpa', 'hours_studied', 'attendance', 'assignments']].corr()
sns.heatmap(corr, annot=True, cmap='Blues', vmin=-1, vmax=1)
plt.show()

# Multiple subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].hist(df['gpa'], bins=20, color='#00d4f5')
axes[0].set_title('GPA Distribution')
axes[1].boxplot(df['gpa'])
axes[1].set_title('GPA Box Plot')
axes[2].pie(grade_counts, labels=grade_counts.index, autopct='%1.0f%%')
axes[2].set_title('Grade Distribution')
plt.tight_layout()
plt.show()
```""",
         'Create 4 different chart types from the same student dataset — bar, scatter, histogram, and pie.',
         'Which library is built on top of Matplotlib and provides a high-level interface for statistical charts?',
         'Build a dashboard of 6 charts analysing a public dataset like Kenya census data or football stats.',
         "Save figures with plt.savefig('file.png', dpi=150, bbox_inches='tight') for publication quality.", 45),

        (3, 'Machine Learning with scikit-learn',
         'Train, evaluate, and compare ML models for classification and regression.',
         """```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                              confusion_matrix)

# Load and prepare data
df = pd.read_csv('students.csv')
X  = df[['hours_studied', 'attendance', 'prev_score', 'sleep_hours']]
y  = df['passed']  # 0 = fail, 1 = pass

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# Train multiple models
models = {
    'Logistic Regression': LogisticRegression(),
    'Decision Tree':       DecisionTreeClassifier(max_depth=5),
    'Random Forest':       RandomForestClassifier(n_estimators=100),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    score = cross_val_score(model, X_train, y_train, cv=5).mean()
    print(f'{name}: CV accuracy = {score:.2%}')

# Best model evaluation
rf = models['Random Forest']
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))
print('Confusion matrix:')
print(confusion_matrix(y_test, y_pred))
```""",
         'Train a Decision Tree on the Iris dataset (sklearn.datasets.load_iris). Tune max_depth and report accuracy.',
         'What does cross-validation protect against?',
         'Build a student pass/fail predictor and deploy it as a Flask/Django web form.',
         'High accuracy on training data but low on test data = overfitting. Regularise or reduce model complexity.', 60),
    ]),

    # ── UI/UX DESIGN ────────────────────────────────────────────────────────────
    ('ui-ux-design', 'UI/UX Design', 'web', 'beginner', '8 weeks',
     'Figma, Design Systems, Accessibility, Prototyping', 'Design interfaces people love to use.', [

        (1, 'Design Fundamentals',
         'Apply the core principles of visual design: hierarchy, contrast, alignment, and proximity.',
         """Good design solves problems and communicates clearly. Before any tools, master the principles.

**Gestalt principles:**
- **Proximity** — elements close together are perceived as related
- **Similarity** — elements that look alike are grouped together
- **Continuity** — the eye follows lines and curves
- **Closure** — the mind fills in incomplete shapes
- **Figure/Ground** — distinguishing object from background

**Visual hierarchy:**
Size → Weight → Colour → Position → Space

```
BIG TITLE                 ← most important
Subtitle — second read    ← secondary
Body text reads here...   ← detail
small caption/label       ← least important
```

**Colour theory:**
- **Primary:** red, yellow, blue
- **Complementary:** opposite on colour wheel (high contrast)
- **Analogous:** adjacent on wheel (harmonious)
- **60/30/10 rule:** 60% dominant, 30% secondary, 10% accent

**Typography rules:**
- Maximum 2 font families per project
- Line height: 1.4–1.6× for body text
- Minimum 16px body text for readability
- Never fully justify text in narrow columns""",
         'Redesign a bad UI you encounter daily (a menu, a form, a dashboard). Explain your decisions.',
         'What design principle groups related elements close together?',
         'Create a complete colour palette and type scale for a fictional tech startup.',
         'Never use pure black (#000000) on white — use #1a1a2e or similar for softer, more readable text.', 40),

        (2, 'Figma for UI Design',
         'Use Figma to wireframe, prototype, and design production-ready interfaces.',
         """Figma is the industry-standard design tool — free for students and small teams.

**Figma workflow:**
1. Wireframe (low-fidelity sketches)
2. High-fidelity mockup (colours, typography, imagery)
3. Interactive prototype (clickable flows)
4. Developer handoff (inspect mode with CSS values)

**Key shortcuts:**
| Key | Action |
|-----|--------|
| F | Create Frame (artboard) |
| R | Rectangle |
| T | Text |
| L | Line |
| Ctrl+G | Group |
| Ctrl+Alt+G | Create Component |
| Ctrl+Shift+4 | Capture frame to clipboard |
| Alt+drag | Duplicate element |

**Components and variants:**
- Create a Button component with states: Default, Hover, Active, Disabled
- Use Auto Layout for responsive frames that adapt to content
- Build a Design System: colours, typography, spacing, components

**Accessibility in Figma:**
- Colour contrast ratio ≥ 4.5:1 for text (WCAG AA)
- Use Figma's Accessibility Annotations plugin
- Name layers meaningfully — they become accessible names in code""",
         'In Figma, design a mobile login screen with email input, password input, and a CTA button.',
         'What is the minimum colour contrast ratio for WCAG AA compliance?',
         'Design a full mobile app (5 screens) for a school management system in Figma with a working prototype.',
         'Use Figma\'s Inspect panel to copy exact CSS values — designers and developers can agree on spacing without guessing.', 45),

        (3, 'User Research & UX Process',
         'Research user needs, map journeys, and test designs with real users.',
         """Great UX starts before you open Figma. Talk to users first.

**The Double Diamond:**
```
Discover → Define → Develop → Deliver
(diverge)  (converge) (diverge) (converge)
```

**Research methods:**
- **User interviews** — open-ended 1:1 conversations
- **Surveys** — quantitative data at scale
- **Usability testing** — watch users complete tasks
- **Card sorting** — how users mentally organise content
- **Analytics** — where users drop off (Google Analytics, Hotjar)

**User Personas:**
```
Name: Amara, 16, Form 3 student
Goal: Find Python tutorials fast
Pain point: Too much text, no code examples
Device: Mobile phone, 2G internet
Quote: "I want to start coding, not read essays"
```

**User Journey Map:**
```
Stage:   Discovers → Registers → Starts Course → Gets Stuck → Asks for Help
Feeling: Excited    → Hopeful   → Motivated     → Frustrated → Grateful
Touch:   Google     → Homepage  → Course page   → Forum      → Chat
```

**Usability testing:**
- 5 users reveal 85% of usability problems (Nielsen's rule)
- Give tasks, not instructions: "Find a Python course" not "Click Courses"
- Observe silently. Note hesitations and errors.""",
         'Create a user persona for a CodeSavannah student and map their 5-step journey to completing a course.',
         'How many users does Nielsen\'s rule say are enough for usability testing?',
         'Conduct usability tests with 3 real people on your Figma prototype. Document changes made.',
         "Observing 5 users find the same issue is more valuable than 100 survey responses about it.", 45),
    ]),

    # ── DIGITAL MARKETING ───────────────────────────────────────────────────────
    ('digital-marketing', 'Digital Marketing', 'web', 'beginner', '8 weeks',
     'SEO, Google Ads, Social Media, Email, Analytics, Content Strategy', 'Grow online audiences and drive business results.', [

        (1, 'Digital Marketing Foundations',
         'Understand the digital marketing landscape and key channels.',
         """Digital marketing uses online channels to reach, engage, and convert customers.

**Core channels:**
| Channel | Best for | Cost |
|---------|----------|------|
| SEO | Long-term organic traffic | Time |
| Google Ads (PPC) | Immediate targeted traffic | Money |
| Social Media | Brand awareness, community | Time |
| Email Marketing | Retention, nurturing leads | Low |
| Content Marketing | Authority, SEO, trust | Time |
| Influencer | Reach new audiences fast | Money |

**The funnel:**
```
Awareness  → Interest  → Consideration  → Conversion → Loyalty
(Find you)   (Read you)   (Compare you)    (Buy/Sign)   (Return)
```

**Key metrics:**
- **CTR** (Click-Through Rate) — clicks ÷ impressions
- **CPC** (Cost Per Click) — ad spend ÷ clicks
- **CPA** (Cost Per Acquisition) — ad spend ÷ conversions
- **LTV** (Lifetime Value) — total revenue from one customer
- **Bounce Rate** — left without interacting
- **Conversion Rate** — % of visitors who complete a goal

**Tools:** Google Analytics, Google Search Console, SEMrush, Ahrefs, Mailchimp, Buffer/Hootsuite""",
         'Audit a real website\'s digital marketing presence — list their channels, estimate their strategy.',
         'What does CTR stand for in digital marketing?',
         'Create a 30-day digital marketing plan for a fictional Nairobi tech startup.',
         'Data beats opinion. Always A/B test before assuming what works.', 40),

        (2, 'SEO — Search Engine Optimisation',
         'Improve a website\'s visibility in Google search results.',
         """SEO = showing up in Google when people search for what you offer.

**On-page SEO:**
```html
<!-- Title tag — most important SEO element -->
<title>Python Programming Course | CodeSavannah Academy</title>

<!-- Meta description — shown in search results -->
<meta name="description" content="Learn Python from scratch in 8 weeks. Hands-on projects, mentorship, and career guidance. Join 5,000+ students at CodeSavannah Academy.">

<!-- Heading hierarchy — one H1 per page -->
<h1>Python Programming Course</h1>
<h2>What You'll Learn</h2>
<h3>Week 1: Variables & Data Types</h3>

<!-- Image alt text -->
<img src="python-class.jpg" alt="Students learning Python at CodeSavannah Academy, Nairobi">
```

**Technical SEO checklist:**
- HTTPS (Google ranks secure sites higher)
- Page speed < 3 seconds (use Google PageSpeed Insights)
- Mobile-first design
- Structured data (Schema.org JSON-LD)
- XML sitemap submitted to Google Search Console
- No broken links (404s hurt ranking)

**Off-page SEO:**
- Backlinks from high-authority sites = trust signals
- Local SEO: Google Business Profile for physical locations
- Social signals (shares, mentions)

**Keyword research:**
- Short-tail: "Python course" (high volume, competitive)
- Long-tail: "Python course for beginners in Nairobi" (lower volume, high intent)""",
         'Run a Google PageSpeed Insights test on a real website. List the top 3 improvements recommended.',
         'Which SEO element in the HTML head is most important for search ranking?',
         'Perform a full SEO audit of a website — on-page, technical, and backlink profile.',
         'Core Web Vitals (LCP, CLS, INP) are now official Google ranking signals — optimise them.', 50),

        (3, 'Social Media & Content Marketing',
         'Build an audience and drive traffic through content.',
         """Content marketing means creating valuable content that attracts and converts your target audience.

**Content types by platform:**
| Platform | Best content | Audience |
|----------|-------------|---------|
| LinkedIn | Thought leadership, case studies | Professionals |
| Instagram | Visual, reels, stories | Youth, lifestyle |
| TikTok | Short video, trending audio | Gen Z |
| YouTube | Tutorials, reviews | All ages |
| Twitter/X | Hot takes, news | Tech, media |
| Facebook | Community groups, events | 25–44 |

**The content calendar:**
```
Mon: Educational post (how-to)
Tue: Behind-the-scenes story
Wed: Student success story/testimonial
Thu: Industry news + opinion
Fri: Interactive (poll, question)
Sat: Inspirational quote + visual
Sun: Week in review / upcoming events
```

**Viral content formula:**
- Trigger an emotion (inspire, shock, entertain, teach)
- Be specific and actionable
- Tell a story, not a sales pitch
- Use visuals — posts with images get 2.3× more engagement

**Analytics — track what works:**
- Reach (unique accounts that saw it)
- Engagement rate (likes + comments + shares ÷ reach)
- Profile visits from post
- Link clicks to website""",
         'Create a 2-week social media content calendar for CodeSavannah Academy with captions and hashtags.',
         'Which social media metric shows the percentage of viewers who interacted with your content?',
         'Run a real 30-day social media campaign for a cause or project you care about. Report results.',
         'Post consistently at the same times. Platform algorithms favour accounts that post regularly.', 45),
    ]),

    # ── ROBOTICS ────────────────────────────────────────────────────────────────
    ('robotics-physical-computing', 'Robotics & Physical Computing', 'programming', 'beginner', '10 weeks',
     'Arduino, Python, Sensors, Motors, Raspberry Pi, MicroPython', 'Build physical devices that sense and respond to the world.', [

        (1, 'Introduction to Electronics',
         'Understand basic electronics: voltage, current, resistance, and circuits.',
         """Physical computing connects software to the physical world. Before writing code, understand the hardware.

**Ohm's Law:** V = I × R
- **V** — Voltage (volts) — electrical pressure
- **I** — Current (amps) — flow of electrons
- **R** — Resistance (ohms) — opposition to flow

**Components you'll use:**
| Component | Symbol | Purpose |
|-----------|--------|---------|
| LED | →|— | Light output |
| Resistor | zigzag | Limit current |
| Button | ——/ —— | Input switch |
| Capacitor | —||— | Store/smooth charge |
| Transistor | — | Switch/amplify |
| Motor | M | Motion |

**Circuit rules:**
- Series: same current, voltage divides → R_total = R1 + R2
- Parallel: same voltage, current divides → 1/R_total = 1/R1 + 1/R2

**Breadboard layout:**
- Horizontal rows are connected
- Power rails (+ and −) run vertically along edges
- Never connect + directly to − (short circuit!)

**LED resistor calculation:**
- Supply: 5V, LED forward voltage: 2V, desired current: 20mA
- R = (5 - 2) / 0.020 = 150Ω → use 220Ω (next standard value)""",
         'Build a simple LED circuit on a breadboard: one LED, one 220Ω resistor, 5V supply.',
         'What law relates voltage, current, and resistance?',
         'Build a traffic light circuit with 3 LEDs (red, amber, green) that cycle automatically.',
         'Always add a resistor in series with an LED — without one, the LED burns out instantly.', 40),

        (2, 'Arduino Programming',
         'Control hardware with C++ code on Arduino microcontrollers.',
         """Arduino is a beginner-friendly microcontroller platform — the "Hello World" of physical computing.

```cpp
// Blink an LED — the Hello World of hardware
const int LED_PIN = 13;

void setup() {
    // setup() runs once when power is applied
    pinMode(LED_PIN, OUTPUT);
    Serial.begin(9600);  // open serial monitor
}

void loop() {
    // loop() runs forever
    digitalWrite(LED_PIN, HIGH);  // LED on
    delay(500);                   // wait 500ms
    digitalWrite(LED_PIN, LOW);   // LED off
    delay(500);
    Serial.println("Blink!");
}
```

**Reading a button:**
```cpp
const int BTN_PIN = 2;
const int LED_PIN = 13;

void setup() {
    pinMode(BTN_PIN, INPUT_PULLUP);  // internal pull-up resistor
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    int state = digitalRead(BTN_PIN);
    if (state == LOW) {         // button pressed (LOW with pull-up)
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }
}
```

**Analog input (sensor reading):**
```cpp
int sensorValue = analogRead(A0);        // 0–1023
float voltage   = sensorValue * (5.0 / 1023.0);
Serial.println(voltage);
```""",
         'Wire an LED and button to Arduino. Pressing the button should toggle the LED on/off.',
         'What Arduino function sets a pin as input or output?',
         'Build a reaction time game: LED lights up randomly, player presses button, display reaction time in ms.',
         'Use Serial.println() liberally while debugging — it\'s the printf() of the physical world.', 50),

        (3, 'Sensors & Actuators',
         'Connect sensors (input) and actuators (output) to build interactive devices.',
         """Sensors convert physical world → electrical signal. Actuators convert electrical signal → physical action.

**Common sensors:**
| Sensor | Type | Use |
|--------|------|-----|
| HC-SR04 | Ultrasonic | Distance measurement |
| DHT22 | Temperature/Humidity | Weather station |
| PIR | Motion | Security, automation |
| LDR | Light | Day/night detection |
| MPU-6050 | Accelerometer/Gyro | Movement detection |
| MQ-2 | Gas | Smoke/LPG detection |

**Ultrasonic distance sensor (HC-SR04):**
```cpp
const int TRIG = 9;
const int ECHO = 10;

void setup() {
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
    Serial.begin(9600);
}

void loop() {
    // Send pulse
    digitalWrite(TRIG, LOW);  delayMicroseconds(2);
    digitalWrite(TRIG, HIGH); delayMicroseconds(10);
    digitalWrite(TRIG, LOW);

    // Measure echo time
    long duration = pulseIn(ECHO, HIGH);
    float distance = duration * 0.034 / 2;  // cm

    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
    delay(500);
}
```

**Servo motor:**
```cpp
#include <Servo.h>
Servo servo;

void setup() { servo.attach(9); }
void loop()  {
    servo.write(0);   delay(1000);
    servo.write(90);  delay(1000);
    servo.write(180); delay(1000);
}
```""",
         'Build a parking sensor: HC-SR04 measures distance, LED blinks faster as an object gets closer.',
         'What type of sensor measures distance using sound waves?',
         'Build a smart plant monitor: soil moisture sensor triggers a pump when dry.',
         'Debounce mechanical buttons in code — mechanical switches bounce 50–100 times on press. Add a 50ms delay or use a debounce library.', 50),

        (4, 'MicroPython & Raspberry Pi',
         'Run Python directly on microcontrollers and single-board computers.',
         """**MicroPython** is a lean Python implementation that runs on microcontrollers like ESP32 and Raspberry Pi Pico.

```python
# MicroPython on Raspberry Pi Pico
from machine import Pin, PWM
from time import sleep
import utime

# LED blink
led = Pin(25, Pin.OUT)  # onboard LED on Pico
while True:
    led.toggle()
    sleep(0.5)

# PWM for servo or LED brightness
pwm = PWM(Pin(15))
pwm.freq(50)   # 50Hz for servo

# 0° = 2000 (1ms), 90° = 4915 (1.5ms), 180° = 7864 (2ms)
pwm.duty_u16(4915)  # 90 degrees

# Read a button
btn = Pin(14, Pin.IN, Pin.PULL_UP)
while True:
    if not btn.value():  # pressed
        print('Button pressed!')
        sleep(0.1)       # debounce
```

**Raspberry Pi (full Linux computer):**
```python
# RPi GPIO (full Python)
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

for _ in range(5):
    GPIO.output(18, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(18, GPIO.LOW)
    time.sleep(0.5)

GPIO.cleanup()
```

Raspberry Pi can run a full web server, camera, keyboard, and display — it's a complete computer the size of a credit card.""",
         'Flash MicroPython to a Pico or ESP32 and run a blink program via Thonny IDE.',
         'What MicroPython class controls GPIO pins as input or output?',
         'Build a Pico W weather station that reads temperature/humidity and serves data over WiFi.',
         'The Raspberry Pi Pico W has built-in WiFi — you can host a tiny web server for sensor data with 10 lines of MicroPython.', 55),
    ]),

    # ── AI / MACHINE LEARNING ───────────────────────────────────────────────────
    ('ai-machine-learning', 'AI & Machine Learning', 'ai', 'advanced', '12 weeks',
     'Python, TensorFlow, PyTorch, scikit-learn, NLP, Computer Vision', 'Build intelligent systems that learn from data.', [

        (1, 'Machine Learning Foundations',
         'Understand what ML is, types of learning, and the standard workflow.',
         """Machine Learning trains computers to find patterns and make decisions from data.

**Types of ML:**
- **Supervised** — labelled training data (spam/not-spam, cat/dog)
- **Unsupervised** — find hidden patterns (clustering, dimensionality reduction)
- **Reinforcement** — agent learns by trial and error (games, robotics)

**The ML workflow:**
```
1. Define the problem (what are we predicting?)
2. Collect and label data
3. Explore and clean (EDA)
4. Feature engineering
5. Choose a model
6. Train
7. Evaluate
8. Tune hyperparameters
9. Deploy
10. Monitor in production
```

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load
X, y = load_iris(return_X_y=True)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test  = sc.transform(X_test)

# Train
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
print(f'Accuracy: {accuracy_score(y_test, clf.predict(X_test)):.2%}')
print(classification_report(y_test, clf.predict(X_test)))
```""",
         'Load the Wine dataset (sklearn.datasets.load_wine). Compare accuracy of 3 classifiers: Logistic Regression, Decision Tree, Random Forest.',
         'What type of ML uses labelled training data?',
         'Build a student performance predictor — given attendance, hours studied, and past scores, predict pass/fail.',
         'Garbage in, garbage out. Data quality beats model complexity every time. Clean first.', 60),

        (2, 'Neural Networks with TensorFlow',
         'Build and train neural networks using Keras / TensorFlow.',
         """Neural networks are inspired by the brain — layers of interconnected neurons that learn from data.

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# Load and preprocess MNIST (handwritten digits)
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32')  / 255.0

# Build model
model = keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax'),  # 10 digits
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Train
history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

# Evaluate
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_acc:.2%}')

# Predict
predictions = model.predict(X_test[:5])
print(np.argmax(predictions, axis=1))
```""",
         'Modify the MNIST network to classify the Fashion MNIST dataset. Target > 88% accuracy.',
         'What activation function outputs probabilities that sum to 1 for multi-class classification?',
         'Train a CNN to classify images from CIFAR-10 with at least 70% test accuracy.',
         'Start with the simplest model. A logistic regression often beats a deep net when you have < 1000 samples.', 65),
    ]),

    # ── MOBILE APP DEVELOPMENT ──────────────────────────────────────────────────
    ('mobile-app-development', 'Mobile App Development', 'mobile', 'intermediate', '12 weeks',
     'Flutter, Dart, Firebase, Android, iOS, REST APIs', 'Build cross-platform mobile apps for Android and iOS.', [

        (1, 'Flutter & Dart Basics',
         'Build your first cross-platform mobile UI with Flutter.',
         """Flutter is Google's framework for building beautiful apps for mobile, web, and desktop from a single codebase using the Dart language.

```dart
// main.dart
import 'package:flutter/material.dart';

void main() => runApp(const CodeSavannahApp());

class CodeSavannahApp extends StatelessWidget {
    const CodeSavannahApp({super.key});

    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            title: 'CodeSavannah',
            debugShowCheckedModeBanner: false,
            theme: ThemeData(
                colorScheme: ColorScheme.fromSeed(
                    seedColor: const Color(0xFF1341a8),
                    brightness: Brightness.dark,
                ),
                useMaterial3: true,
            ),
            home: const HomeScreen(),
        );
    }
}

class HomeScreen extends StatelessWidget {
    const HomeScreen({super.key});

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: const Text('CodeSavannah Academy'),
                backgroundColor: const Color(0xFF0c1a2e),
                foregroundColor: Colors.white,
            ),
            body: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                        const Text(
                            'Welcome back, Coder!',
                            style: TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.w900,
                            ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                            'Continue your Python journey.',
                            style: TextStyle(color: Colors.grey[400]),
                        ),
                    ],
                ),
            ),
            floatingActionButton: FloatingActionButton(
                onPressed: () {},
                child: const Icon(Icons.add),
            ),
        );
    }
}
```

**Setup:** Install Flutter SDK → `flutter create myapp` → `flutter run`""",
         'Build a profile card widget with name, avatar, bio, and a row of skill chips.',
         'In Flutter, what is the base class for widgets that never change?',
         'Build a CodeSavannah course browser app — list view of courses with tap to detail.',
         'In Flutter, everything is a Widget — even Padding, Align, and SizedBox are widgets, not properties.', 55),

        (2, 'State Management',
         'Manage dynamic app state with setState, Provider, and Riverpod.',
         """State in Flutter is data that can change and needs to cause a UI update when it does.

```dart
// StatefulWidget — local state
class EnrolmentButton extends StatefulWidget {
    final String courseTitle;
    const EnrolmentButton({super.key, required this.courseTitle});

    @override
    State<EnrolmentButton> createState() => _EnrolmentButtonState();
}

class _EnrolmentButtonState extends State<EnrolmentButton> {
    bool _enrolled = false;

    @override
    Widget build(BuildContext context) {
        return ElevatedButton.icon(
            onPressed: () {
                setState(() => _enrolled = !_enrolled);
            },
            icon: Icon(_enrolled ? Icons.check : Icons.school),
            label: Text(_enrolled ? 'Enrolled!' : 'Enrol Now'),
            style: ElevatedButton.styleFrom(
                backgroundColor: _enrolled
                    ? Colors.green
                    : Theme.of(context).colorScheme.primary,
            ),
        );
    }
}
```

**Provider** — share state across the widget tree:
```dart
// With Provider package
class CourseProvider extends ChangeNotifier {
    final List<Course> _enrolled = [];

    List<Course> get enrolled => List.unmodifiable(_enrolled);

    void enrol(Course course) {
        if (!_enrolled.contains(course)) {
            _enrolled.add(course);
            notifyListeners();  // rebuild widgets that listen
        }
    }
}

// In widget
final provider = context.watch<CourseProvider>();
final count = provider.enrolled.length;
```""",
         'Build a shopping cart widget using setState — add/remove items, show total count in AppBar badge.',
         'Which Flutter method triggers a widget rebuild with updated state?',
         'Build a complete to-do app with Provider state management — add, complete, delete, persist to SharedPreferences.',
         'Lift state up to the nearest common ancestor of all widgets that need it.', 50),

        (3, 'Firebase & Backend Integration',
         'Connect a Flutter app to Firebase for auth, database, and storage.',
         """Firebase is Google's mobile backend-as-a-service — authentication, real-time database, cloud storage, and more.

```dart
// Firebase Auth — email/password sign-in
import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
    final _auth = FirebaseAuth.instance;

    Future<UserCredential> signIn(String email, String password) {
        return _auth.signInWithEmailAndPassword(
            email: email, password: password
        );
    }

    Future<UserCredential> register(String email, String password) {
        return _auth.createUserWithEmailAndPassword(
            email: email, password: password
        );
    }

    Future<void> signOut() => _auth.signOut();

    Stream<User?> get authState => _auth.authStateChanges();
}

// Firestore — cloud NoSQL database
import 'package:cloud_firestore/cloud_firestore.dart';

class CourseService {
    final _db = FirebaseFirestore.instance;

    Future<void> saveCourse(Map<String, dynamic> course) {
        return _db.collection('courses').add(course);
    }

    Stream<QuerySnapshot> getCourses() {
        return _db.collection('courses')
            .orderBy('title')
            .snapshots();
    }
}

// In widget — real-time list
StreamBuilder<QuerySnapshot>(
    stream: CourseService().getCourses(),
    builder: (context, snapshot) {
        if (!snapshot.hasData) return CircularProgressIndicator();
        final docs = snapshot.data!.docs;
        return ListView.builder(
            itemCount: docs.length,
            itemBuilder: (_, i) => Text(docs[i]['title']),
        );
    },
)
```""",
         'Integrate Firebase Auth into a Flutter app — implement login, register, and sign out screens.',
         'What Firebase service provides real-time data synchronisation?',
         'Build a full Flutter + Firebase chat app with auth, Firestore messages, and user profiles.',
         'Use FirebaseAuth.instance.authStateChanges() to automatically rebuild your UI when login state changes.', 60),
    ]),

]


class Command(BaseCommand):
    help = ('Create or update LearningPath + Lesson records matching each Course slug. '
            'Safe to re-run — uses get_or_create throughout.')

    def handle(self, *args, **options):
        paths_created   = 0
        paths_updated   = 0
        lessons_created = 0

        for (course_slug, title, category, level, duration,
             skill_stack, summary, lessons_data) in COURSE_PATHS:

            path, created = LearningPath.objects.get_or_create(
                slug=course_slug,
                defaults={
                    'title':       title,
                    'category':    category,
                    'level':       level,
                    'duration':    duration,
                    'skill_stack': skill_stack,
                    'summary':     summary,
                    'is_featured': True,
                },
            )
            if created:
                paths_created += 1
                self.stdout.write(f'  + Created path: {title} (slug: {course_slug})')
            else:
                # Update fields in case content changed
                path.title       = title
                path.category    = category
                path.level       = level
                path.duration    = duration
                path.skill_stack = skill_stack
                path.summary     = summary
                path.is_featured = True
                path.save()
                paths_updated += 1
                self.stdout.write(f'  ~ Updated path: {title}')

            for (order, l_title, objective, content,
                 exercise, quiz_q, project, notes, mins) in lessons_data:

                lesson, l_created = Lesson.objects.get_or_create(
                    learning_path=path,
                    order=order,
                    defaults={
                        'title':            l_title,
                        'objective':        objective,
                        'content':          content,
                        'exercise_prompt':  exercise,
                        'quiz_question':    quiz_q,
                        'project_prompt':   project,
                        'notes':            notes,
                        'estimated_minutes': mins,
                    },
                )
                if l_created:
                    lessons_created += 1
                else:
                    lesson.title           = l_title
                    lesson.objective       = objective
                    lesson.content         = content
                    lesson.exercise_prompt = exercise
                    lesson.quiz_question   = quiz_q
                    lesson.project_prompt  = project
                    lesson.notes           = notes
                    lesson.estimated_minutes = mins
                    lesson.save()

        self.stdout.write(self.style.SUCCESS(
            f'\nDone — {paths_created} paths created, '
            f'{paths_updated} updated, '
            f'{lessons_created} new lessons created.'
        ))
        self.stdout.write(
            '\nRun the dev server and open any course detail page to see the lessons.'
        )
