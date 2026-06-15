"""
Seed comprehensive lessons for all major programming languages + Scratch + Robotics.
Run: python manage.py seed_lessons
"""
from django.core.management.base import BaseCommand

from academy.models import Lesson, LearningPath


PATHS = [
    # (title, category, level, duration, skill_stack, lessons_list)
    # lessons_list: list of (title, objective, content, exercise, quiz_q, project, notes, mins)

    # ── SCRATCH ──────────────────────────────────────────────────────────────────
    ("Scratch for Kids", "programming", "beginner", "4 weeks", "Scratch, Block-based coding, MIT", [
        ("Welcome to Scratch", "Understand the Scratch interface and how blocks work.",
         "Scratch is a visual programming language made by MIT Media Lab. Instead of typing code, you snap together colourful blocks — like LEGO for code!\n\n**Key parts of the Scratch screen:**\n- Stage (where your sprite lives)\n- Sprite list (your characters)\n- Block palette (all your coding blocks)\n- Scripts area (where you build programs)\n- Green flag (runs your program)\n\n**Block categories:**\n- 🔵 Motion — move, turn, go to position\n- 🟣 Looks — say, show, change costume\n- 🔴 Sound — play sound, set volume\n- 🟡 Events — when flag clicked, when key pressed\n- 🟠 Control — if, repeat, wait\n- 🩵 Sensing — touching?, mouse-x\n\nEverything is drag-and-drop. You cannot break anything!",
         "Open Scratch at scratch.mit.edu. Drag a 'move 10 steps' block. Click it. Watch Scratch the cat move!",
         "What colour are Motion blocks in Scratch?", "Build a cat that walks across the screen when the green flag is clicked.",
         "Scratch was created at MIT and is used by over 100 million people worldwide.", 30),

        ("Making Things Move", "Animate sprites using Motion and Events blocks.",
         "**Motion blocks** control where and how your sprite moves.\n\n```\nwhen green flag clicked\nrepeat 10\n  move 20 steps\n  wait 0.1 seconds\n```\n\n**Key Motion blocks:**\n- `move N steps` — moves the sprite forward\n- `turn 15 degrees` — rotates\n- `go to x: 0 y: 0` — jumps to centre\n- `glide 1 secs to x: 200 y: 0` — smooth movement\n- `if on edge, bounce` — bounces off walls\n\n**Coordinates:** the stage uses x (left–right) and y (up–down). The centre is x:0, y:0.",
         "Make your sprite walk from the left edge to the right edge, then bounce back.",
         "Which block makes a sprite bounce off the stage edges?",
         "Create an animation of a cat chasing a mouse around the screen.",
         "Use 'set rotation style: left-right' so your sprite doesn't flip upside down!", 35),

        ("Costumes and Looks", "Use costumes to create animation frames.",
         "**Costumes** are like animation frames — switch between them quickly to create the illusion of movement.\n\n```\nwhen green flag clicked\nforever\n  next costume\n  wait 0.1 seconds\n```\n\n**Looks blocks:**\n- `switch costume to [name]`\n- `next costume`\n- `say Hello! for 2 seconds` — speech bubble\n- `think Hmm... for 2 seconds`\n- `set size to 50 %` — make sprite bigger/smaller\n- `change color effect by 25` — colour shift\n\nYou can draw your own costumes in the costume editor using paint tools.",
         "Give your sprite 3 costumes and make it cycle through them every 0.2 seconds.",
         "What is the Scratch block that cycles to the next costume?",
         "Create a character with a walk cycle — draw 4 costumes showing different leg positions.",
         "The costume editor has vector (smooth) and bitmap (pixel) drawing modes.", 35),

        ("Sounds and Music", "Add sound effects and music to a Scratch project.",
         "**Sound blocks** let you play recorded sounds or even music notes.\n\n```\nwhen this sprite clicked\nplay sound [Meow] until done\n```\n\n**Sound blocks:**\n- `play sound [name]`\n- `play sound [name] until done`\n- `stop all sounds`\n- `set volume to 80 %`\n- `play note 60 for 0.5 beats` — musical notes!\n\n**Record your own:** click the microphone icon in the Sounds tab to record your voice.\n\n**MIDI Notes:** 60 = Middle C, 62 = D, 64 = E, 65 = F, 67 = G",
         "Make a sprite play a different sound when clicked vs when the arrow keys are pressed.",
         "Which Scratch block plays a musical note?",
         "Compose a short 8-note melody using 'play note' blocks.",
         "Scratch has over 100 built-in sounds including instruments, animals, and sound effects!", 30),

        ("My First Game", "Build a complete interactive game in Scratch.",
         "**Building a catching game:**\n\n1. Create a basket sprite at the bottom\n2. Create a falling object sprite\n3. Use forever + change y by -5 to make it fall\n4. Reset position when it reaches bottom: if y < -170, go to x: random y: 170\n5. Detect catching: if touching basket, score += 1\n6. Use a Variable for score\n\n**Variables:** click 'Make a Variable' in the Variables category. This stores your score.\n\n```\nwhen green flag clicked\nset [Score] to 0\nforever\n  change y by -5\n  if touching [Basket] then\n    change [Score] by 1\n    go to x: pick random -200 to 200  y: 170\n  end\nend\n```",
         "Add a timer that counts down from 30. When it hits zero, stop the game.",
         "How do you create a score counter in Scratch?",
         "Build a complete 'Catch the Fruit' game with score, timer, and multiple falling objects.",
         "Share your project on scratch.mit.edu — over 100 million kids will be able to play it!", 60),
    ]),

    # ── PYTHON ───────────────────────────────────────────────────────────────────
    ("Python Programming", "programming", "beginner", "8 weeks", "Python 3, pip, IDLE, VS Code", [
        ("Hello Python", "Write and run your first Python program.",
         "Python is one of the most popular programming languages in the world. It powers Instagram, YouTube, NASA, and thousands of startups.\n\n**Why Python?**\n- Reads almost like English\n- Runs on any computer\n- Used for web, AI, data science, automation, games\n- Huge community and free resources\n\n**Your first program:**\n```python\nprint('Hello, CodeSavannah!')\n```\n\nRun it with: `python hello.py`\n\n**print()** — outputs text to the screen\n**Strings** — text wrapped in quotes: `'like this'` or `\"like this\"`\n\n**Comments** — notes that Python ignores:\n```python\n# This is a comment\nprint('Python ignores the line above')\n```",
         "Write a program that prints your name, your country, and your favourite programming language on three separate lines.",
         "Which function prints output in Python?",
         "Write a 'Personal Info Card' program that prints a formatted profile about yourself.",
         "Python was created by Guido van Rossum in 1991. The name comes from Monty Python, not the snake!", 30),

        ("Variables and Data Types", "Store and manipulate data using Python variables.",
         "**Variables** are containers that store data.\n\n```python\nname = 'Amara'\nage = 17\ngpa = 3.85\nis_student = True\n\nprint(name, 'is', age, 'years old')\n```\n\n**Data types:**\n| Type | Example | Use |\n|------|---------|-----|\n| `str` | `'hello'` | Text |\n| `int` | `42` | Whole numbers |\n| `float` | `3.14` | Decimals |\n| `bool` | `True` | Yes/No |\n\n**Type checking:** `type(name)` → `<class 'str'>`\n\n**Type conversion:**\n```python\nage_str = str(age)      # int → string\nnum = int('42')         # string → int\nprice = float('9.99')  # string → float\n```\n\n**f-strings** (the modern way to format):\n```python\nprint(f'{name} scored {gpa} GPA')\n```",
         "Create variables for a student: name, age, grade, GPA. Print a formatted school report using f-strings.",
         "What data type stores True or False values in Python?",
         "Build a 'Currency Converter' that stores exchange rates as variables and converts between KES, USD, and EUR.",
         "Variable names cannot start with a number and cannot contain spaces. Use_underscores instead.", 35),

        ("Conditionals and Loops", "Control program flow with if/else and loops.",
         "**if / elif / else:**\n```python\nscore = 85\n\nif score >= 90:\n    print('A — Excellent!')\nelif score >= 80:\n    print('B — Very Good!')\nelif score >= 70:\n    print('C — Good')\nelif score >= 60:\n    print('D — Pass')\nelse:\n    print('F — Needs improvement')\n```\n\n**Comparison operators:** `==` `!=` `>` `<` `>=` `<=`\n**Logical operators:** `and`, `or`, `not`\n\n**for loop:**\n```python\nfor i in range(1, 11):\n    print(f'{i} x 5 = {i * 5}')\n```\n\n**while loop:**\n```python\ncount = 0\nwhile count < 5:\n    print(f'Count: {count}')\n    count += 1\n```\n\n**break** — exits the loop early\n**continue** — skips to next iteration",
         "Write a FizzBuzz program: for numbers 1–100, print 'Fizz' if divisible by 3, 'Buzz' if by 5, 'FizzBuzz' if both.",
         "Which keyword exits a loop early in Python?",
         "Build a 'Number Guessing Game' where the computer picks a random number and the player guesses it.",
         "Python uses indentation (spaces) to define code blocks — no curly braces like Java or JavaScript!", 45),

        ("Functions", "Write reusable code blocks using def.",
         "**Functions** let you write code once and use it many times.\n\n```python\ndef greet(name, time_of_day='morning'):\n    return f'Good {time_of_day}, {name}!'\n\nprint(greet('Grace'))\nprint(greet('Brian', 'evening'))\n```\n\n**Parts of a function:**\n- `def` — keyword to define\n- `greet` — function name\n- `(name, time_of_day)` — parameters\n- `return` — sends a value back\n\n**Lambda (one-line functions):**\n```python\nsquare = lambda x: x ** 2\nprint(square(9))  # 81\n```\n\n**Scope:** variables inside functions are local — they don't exist outside.\n\n```python\ndef calculate_bmi(weight_kg, height_m):\n    bmi = weight_kg / (height_m ** 2)\n    if bmi < 18.5:   return 'Underweight'\n    elif bmi < 25:   return 'Normal'\n    elif bmi < 30:   return 'Overweight'\n    else:            return 'Obese'\n```",
         "Write a function `is_prime(n)` that returns True if n is prime, False otherwise. Test it on 7, 12, and 97.",
         "What keyword is used to send a value back from a Python function?",
         "Build a 'Scientific Calculator' with separate functions for add, subtract, multiply, divide, power, and square root.",
         "Functions with no return statement return None automatically.", 40),

        ("Lists and Dictionaries", "Organise data in Python collections.",
         "**Lists** — ordered, changeable collections:\n```python\nstudents = ['Amara', 'Brian', 'Grace', 'Kofi']\n\nprint(students[0])        # Amara (0-indexed)\nstudents.append('Zara')   # add to end\nstudents.remove('Brian')  # remove\nstudents.sort()           # alphabetical\nprint(len(students))      # 4\n```\n\n**List comprehension:**\n```python\nsquares = [x**2 for x in range(1, 11)]\nevens   = [x for x in range(1, 21) if x % 2 == 0]\n```\n\n**Dictionaries** — key:value pairs:\n```python\nstudent = {\n    'name':  'Grace',\n    'age':   16,\n    'grade': 'Form 3',\n    'gpa':   3.9\n}\n\nprint(student['name'])         # Grace\nstudent['school'] = 'CSA'      # add key\nprint(student.get('phone', 'N/A'))  # safe access\n\nfor key, value in student.items():\n    print(f'{key}: {value}')\n```",
         "Create a list of 5 African cities. Sort them alphabetically. Print the longest city name.",
         "How do you access the value of key 'name' in a dictionary called `person`?",
         "Build a 'Contact Book' app that stores names and phone numbers in a dictionary, with add, search, and delete functions.",
         "Python lists can hold mixed types: [1, 'hello', True, 3.14] is perfectly valid.", 45),

        ("File Handling and Modules", "Read/write files and use Python's standard library.",
         "**Writing files:**\n```python\nwith open('notes.txt', 'w') as f:\n    f.write('CodeSavannah Academy\\n')\n    f.write('Python is awesome!\\n')\n```\n\n**Reading files:**\n```python\nwith open('notes.txt', 'r') as f:\n    content = f.read()\nprint(content)\n\n# Line by line:\nwith open('notes.txt', 'r') as f:\n    for line in f:\n        print(line.strip())\n```\n\n**Modes:** `'r'` read, `'w'` write, `'a'` append, `'rb'` binary read\n\n**Useful modules:**\n```python\nimport random\nimport math\nimport os\nimport datetime\n\nprint(random.randint(1, 100))\nprint(math.sqrt(144))          # 12.0\nprint(os.getcwd())             # current folder\nprint(datetime.date.today())\n```\n\n**Installing external libraries:** `pip install requests`",
         "Write a program that saves your daily mood to a log file. Each run should append today's date and mood rating (1–10).",
         "What file mode appends new content without deleting existing content?",
         "Build a 'Expense Tracker' that saves transactions to a CSV file and reads them back to show totals.",
         "Always use `with open()` — it automatically closes the file even if an error occurs.", 45),

        ("Python for the Web with Django", "Understand how Python powers web applications.",
         "**Django** is a Python web framework used by Instagram, Pinterest, and NASA.\n\n**Django architecture (MVT):**\n- **Model** — Python class = database table\n- **View** — Python function = business logic\n- **Template** — HTML file = what users see\n\n```python\n# models.py\nfrom django.db import models\n\nclass Student(models.Model):\n    name  = models.CharField(max_length=150)\n    email = models.EmailField(unique=True)\n    grade = models.CharField(max_length=20)\n    \n    def __str__(self):\n        return self.name\n```\n\n```python\n# views.py\nfrom django.shortcuts import render\nfrom .models import Student\n\ndef student_list(request):\n    students = Student.objects.all()\n    return render(request, 'students.html', {'students': students})\n```\n\n```html\n<!-- students.html -->\n{% for student in students %}\n  <p>{{ student.name }} — {{ student.grade }}</p>\n{% endfor %}\n```\n\n**Quick start:**\n```bash\npip install django\ndjango-admin startproject mysite\ncd mysite\npython manage.py runserver\n```",
         "Create a Django model for a `BlogPost` with title, content, author, and date_published fields.",
         "What does MVT stand for in Django?",
         "Build a personal blog with Django: create posts, list posts, and view individual posts.",
         "Django's admin panel at /admin/ is automatically generated from your models — no extra code needed!", 60),
    ]),

    # ── JAVASCRIPT ───────────────────────────────────────────────────────────────
    ("JavaScript", "web", "beginner", "7 weeks", "JavaScript ES6+, DOM, Browser APIs", [
        ("JavaScript Foundations", "Understand variables, types, and operators.",
         "JavaScript runs in every browser and powers interactive websites.\n\n```javascript\n// Variables\nconst name = 'CodeSavannah';  // never changes\nlet score = 0;                 // can change\n\n// Types\nconsole.log(typeof 42);        // number\nconsole.log(typeof 'hello');   // string\nconsole.log(typeof true);      // boolean\nconsole.log(typeof null);      // object (historic bug!)\nconsole.log(typeof undefined); // undefined\n\n// Template literals\nconst msg = `Welcome to ${name}!`;\nconsole.log(msg);\n\n// Numbers\nconsole.log(10 / 3);   // 3.333...\nconsole.log(10 % 3);   // 1 (remainder)\nconsole.log(2 ** 8);   // 256 (power)\n```",
         "Write a script that converts Celsius to Fahrenheit and prints the result using a template literal.",
         "Which JS keyword declares a variable that can be reassigned?",
         "Build a tip calculator: ask for bill amount and tip percentage, output the tip and total.",
         "Use const by default; only use let when you know the value will change.", 35),

        ("DOM Manipulation", "Make web pages interactive with JavaScript.",
         "The **DOM (Document Object Model)** is a tree of HTML elements that JavaScript can read and modify.\n\n```javascript\n// Select elements\nconst heading = document.getElementById('title');\nconst btn     = document.querySelector('.submit-btn');\nconst cards   = document.querySelectorAll('.card');\n\n// Modify content\nheading.textContent = 'New Title';\nheading.innerHTML   = '<strong>Bold Title</strong>';\n\n// Modify style\nheading.style.color    = 'var(--accent)';\nheading.style.fontSize = '2rem';\n\n// Add/remove classes\nbtn.classList.add('active');\nbtn.classList.remove('hidden');\nbtn.classList.toggle('dark');\n\n// Create & append elements\nconst p = document.createElement('p');\np.textContent = 'New paragraph';\ndocument.body.appendChild(p);\n```",
         "Create an HTML page with a button. Each click changes the page background to a random colour.",
         "What method selects the first element matching a CSS selector?",
         "Build a 'To-Do List' app: add items, mark complete, delete items — all without page reload.",
         "innerHTML is powerful but dangerous with user input — it can cause XSS attacks. Prefer textContent.", 45),

        ("Functions and Arrow Functions", "Master modern JavaScript function syntax.",
         "```javascript\n// Function declaration\nfunction greet(name) {\n    return `Hello, ${name}!`;\n}\n\n// Function expression\nconst greet2 = function(name) {\n    return `Hi, ${name}!`;\n};\n\n// Arrow function (ES6+)\nconst greet3 = (name) => `Hey, ${name}!`;\n\n// Arrow with multiple statements\nconst calculateTax = (amount, rate = 0.16) => {\n    const tax = amount * rate;\n    return { amount, tax, total: amount + tax };\n};\n\n// Higher-order functions\nconst numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];\n\nconst evens   = numbers.filter(n => n % 2 === 0);\nconst doubled = numbers.map(n => n * 2);\nconst sum     = numbers.reduce((acc, n) => acc + n, 0);\n```",
         "Write an arrow function `fibonacci(n)` that returns the nth Fibonacci number.",
         "What is the shorter syntax for writing functions in JavaScript ES6?",
         "Build an array manipulation toolkit: functions for finding max, min, average, and unique values.",
         "Arrow functions do not have their own 'this' — important for class methods and event handlers.", 40),

        ("Async JavaScript and Fetch API", "Work with APIs and asynchronous code.",
         "JavaScript uses **async/await** to handle operations that take time (API calls, file reads).\n\n```javascript\n// Fetch data from a public API\nasync function getWeather(city) {\n    try {\n        const response = await fetch(\n            `https://api.open-meteo.com/v1/forecast?latitude=1.29&longitude=36.82&current=temperature_2m`\n        );\n        const data = await response.json();\n        return data.current.temperature_2m;\n    } catch (error) {\n        console.error('Failed:', error.message);\n    }\n}\n\n// Call it\ngetWeather('Nairobi').then(temp => {\n    document.getElementById('temp').textContent = `${temp}°C`;\n});\n```\n\n**Promises:**\n```javascript\nconst delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));\nawait delay(1000); // pause 1 second\n```",
         "Fetch data from the JSONPlaceholder API (jsonplaceholder.typicode.com/posts/1) and display the title and body on a webpage.",
         "What keyword makes a function that can use await?",
         "Build a weather dashboard that fetches and displays real-time temperature data from a public API.",
         "Always wrap fetch() calls in try/catch — APIs can fail, be offline, or return unexpected data.", 50),
    ]),

    # ── HTML ─────────────────────────────────────────────────────────────────────
    ("HTML5", "web", "beginner", "3 weeks", "HTML5, Semantic HTML, Accessibility", [
        ("HTML Foundations", "Understand the building blocks of every web page.",
         "**HTML (HyperText Markup Language)** defines the structure and content of web pages.\n\n```html\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>My First Page</title>\n</head>\n<body>\n    <h1>Welcome to CodeSavannah!</h1>\n    <p>This is my first web page.</p>\n    <a href=\"https://codesavannah.ac\">Visit us</a>\n</body>\n</html>\n```\n\n**Core tags:**\n| Tag | Purpose |\n|-----|---------|\n| `<h1>–<h6>` | Headings |\n| `<p>` | Paragraph |\n| `<a href>` | Link |\n| `<img src alt>` | Image |\n| `<ul><li>` | Bullet list |\n| `<ol><li>` | Numbered list |\n| `<div>` | Container block |\n| `<span>` | Container inline |",
         "Build an HTML page about your favourite topic with at least one heading, two paragraphs, an image, and a list.",
         "Which attribute makes an image accessible to screen readers?",
         "Build a personal profile page with your name, photo, bio, skills list, and contact links.",
         "Always include `lang` on the `<html>` tag — screen readers use it to pronounce content correctly.", 30),

        ("Semantic HTML", "Use meaningful HTML5 elements for better accessibility and SEO.",
         "**Semantic HTML** uses tags that describe their content's meaning.\n\n```html\n<header>\n    <nav>\n        <a href=\"/\">Home</a>\n        <a href=\"/courses\">Courses</a>\n    </nav>\n</header>\n\n<main>\n    <article>\n        <header>\n            <h1>Python Tutorial</h1>\n            <time datetime=\"2025-06-01\">June 1, 2025</time>\n        </header>\n        <p>Python is a beginner-friendly language...</p>\n        <section>\n            <h2>Variables</h2>\n            <p>Variables store data...</p>\n        </section>\n    </article>\n\n    <aside>\n        <h2>Related Articles</h2>\n    </aside>\n</main>\n\n<footer>\n    <p>&copy; 2025 CodeSavannah Academy</p>\n</footer>\n```\n\n**Why semantic HTML?**\n- Search engines rank it higher\n- Screen readers navigate it correctly\n- Other developers understand it faster",
         "Rewrite a non-semantic `<div>` heavy page using proper semantic tags.",
         "Which HTML5 element represents the main content of a page?",
         "Build a blog article page using article, section, aside, header, and footer tags correctly.",
         "Google's algorithm specifically rewards pages that use proper semantic HTML structure.", 35),

        ("HTML Forms", "Build user input forms with validation.",
         "```html\n<form method=\"post\" action=\"/submit\">\n    <label for=\"email\">Email Address</label>\n    <input type=\"email\" id=\"email\" name=\"email\"\n           placeholder=\"you@example.com\" required>\n    \n    <label for=\"password\">Password</label>\n    <input type=\"password\" id=\"password\" name=\"password\"\n           minlength=\"8\" required>\n    \n    <label for=\"level\">Skill Level</label>\n    <select id=\"level\" name=\"level\">\n        <option value=\"\">Choose...</option>\n        <option value=\"beginner\">Beginner</option>\n        <option value=\"intermediate\">Intermediate</option>\n        <option value=\"advanced\">Advanced</option>\n    </select>\n    \n    <label>\n        <input type=\"checkbox\" name=\"terms\" required>\n        I agree to the Terms\n    </label>\n    \n    <button type=\"submit\">Sign Up</button>\n</form>\n```\n\n**Input types:** text, email, password, number, date, file, checkbox, radio, range",
         "Build a registration form for a coding event with: name, email, age, t-shirt size, programming language preference, and a submit button.",
         "Which input attribute makes a field required before form submission?",
         "Build a multi-section survey form with fieldsets, legends, and at least 5 different input types.",
         "Add autocomplete='off' on password fields to prevent browsers storing sensitive passwords.", 40),
    ]),

    # ── CSS ──────────────────────────────────────────────────────────────────────
    ("CSS3 Design", "web", "beginner", "4 weeks", "CSS3, Flexbox, Grid, Animations", [
        ("CSS Fundamentals", "Style HTML with selectors, properties, and values.",
         "```css\n/* Selector types */\nh1        { color: navy; }         /* element */\n.card     { padding: 24px; }       /* class */\n#hero     { height: 80vh; }        /* id */\na:hover   { color: cyan; }         /* pseudo-class */\np::first-line { font-weight: bold; } /* pseudo-element */\ndiv > p   { margin: 0; }           /* child combinator */\n\n/* Box model */\n.box {\n    width: 300px;\n    padding: 20px;           /* inside */\n    border: 2px solid #333;  /* border */\n    margin: 16px auto;       /* outside, centered */\n    box-sizing: border-box;  /* padding included in width */\n}\n\n/* Custom properties (variables) */\n:root {\n    --primary: #1341a8;\n    --accent: #00d4f5;\n    --radius: 8px;\n}\n\n.btn {\n    background: var(--primary);\n    border-radius: var(--radius);\n}\n```",
         "Style a navigation bar: horizontal layout, logo left, links right, hover colour change.",
         "Which CSS unit is relative to the root font size?",
         "Build and fully style a product card with image, title, description, price, and 'Add to Cart' button.",
         "Always set box-sizing: border-box on *,*::before,*::after — it makes layout calculations far more intuitive.", 40),

        ("Flexbox and Grid", "Create modern responsive layouts.",
         "**Flexbox** — 1-dimensional layout:\n```css\n.nav {\n    display: flex;\n    align-items: center;\n    justify-content: space-between;\n    gap: 16px;\n    flex-wrap: wrap;\n}\n\n.card-grid {\n    display: flex;\n    flex-wrap: wrap;\n    gap: 24px;\n}\n.card { flex: 1 1 280px; }  /* grow, shrink, base width */\n```\n\n**CSS Grid** — 2-dimensional layout:\n```css\n.layout {\n    display: grid;\n    grid-template-columns: repeat(3, minmax(0, 1fr));\n    grid-template-rows: auto;\n    gap: 24px;\n}\n\n/* Holy Grail layout */\n.page {\n    display: grid;\n    grid-template-areas:\n        'header  header  header'\n        'sidebar main    aside'\n        'footer  footer  footer';\n    grid-template-columns: 240px 1fr 200px;\n}\n.header  { grid-area: header;  }\n.sidebar { grid-area: sidebar; }\n.main    { grid-area: main;    }\n```",
         "Build a 3-column card grid using CSS Grid that collapses to 1 column on mobile.",
         "Which CSS property creates a grid layout?",
         "Recreate the CodeSavannah stats band layout using CSS Grid with 6 equal columns.",
         "Flexbox is best for 1-direction UI components (navbars, button groups). Grid is best for page layouts.", 45),

        ("Animations and Transitions", "Add motion to web pages.",
         "**Transitions** — smooth property changes:\n```css\n.btn {\n    background: var(--primary);\n    transform: translateY(0);\n    transition: background 200ms ease, transform 200ms ease;\n}\n\n.btn:hover {\n    background: var(--primary-dark);\n    transform: translateY(-3px);\n}\n```\n\n**Keyframe animations:**\n```css\n@keyframes fadeInUp {\n    from {\n        opacity: 0;\n        transform: translateY(24px);\n    }\n    to {\n        opacity: 1;\n        transform: none;\n    }\n}\n\n.hero-title {\n    animation: fadeInUp 700ms cubic-bezier(0.22, 1, 0.36, 1) both;\n}\n\n@keyframes pulse {\n    0%, 100% { transform: scale(1); opacity: 1; }\n    50%       { transform: scale(1.05); opacity: 0.8; }\n}\n```\n\n**CSS transforms:**\n```css\ntranslate(x, y)  /* move */\nscale(n)         /* resize */\nrotate(deg)      /* spin */\nskewX(deg)       /* slant */\n```",
         "Add entrance animations to a landing page: hero fades in, cards slide up one by one with delay.",
         "Which CSS property creates a keyframe animation sequence?",
         "Build an animated loading spinner, a pulsing button, and a card with a hover flip effect.",
         "Use `will-change: transform` on heavily animated elements to hint the browser to use GPU acceleration.", 45),
    ]),

    # ── JAVA ─────────────────────────────────────────────────────────────────────
    ("Java Programming", "programming", "intermediate", "10 weeks", "Java 17, Maven, OOP, Collections", [
        ("Java Basics", "Understand Java syntax, types, and the JVM.",
         "Java is one of the most widely used languages — it powers Android, enterprise banking, and Spring web apps.\n\n```java\npublic class HelloWorld {\n    public static void main(String[] args) {\n        String name = \"CodeSavannah\";\n        int year = 2025;\n        double version = 1.0;\n        boolean isAwesome = true;\n        \n        System.out.println(\"Hello from \" + name + \"!\");\n        System.out.printf(\"Year: %d, Version: %.1f%n\", year, version);\n    }\n}\n```\n\n**Primitive types:** `int`, `long`, `double`, `float`, `char`, `boolean`, `byte`, `short`\n\n**Compile and run:**\n```bash\njavac HelloWorld.java\njava HelloWorld\n```\n\nOr use an IDE like IntelliJ IDEA (free Community edition).",
         "Write a Java program that prints the multiplication table (1–12) for a number entered by the user.",
         "What method is the entry point of every Java application?",
         "Build a 'Student Grade Calculator' that reads marks for 5 subjects and computes the average and grade.",
         "Java is statically typed — you must declare a variable's type. This catches errors at compile time, not runtime.", 40),

        ("OOP in Java", "Apply encapsulation, inheritance, and polymorphism.",
         "```java\npublic class Student {\n    private String name;\n    private int age;\n    private double gpa;\n    \n    // Constructor\n    public Student(String name, int age, double gpa) {\n        this.name = name;\n        this.age  = age;\n        this.gpa  = gpa;\n    }\n    \n    // Getter\n    public String getName() { return name; }\n    \n    // Method\n    public String getGrade() {\n        if (gpa >= 3.7) return \"A\";\n        if (gpa >= 3.0) return \"B\";\n        if (gpa >= 2.0) return \"C\";\n        return \"F\";\n    }\n    \n    @Override\n    public String toString() {\n        return name + \" (GPA: \" + gpa + \", Grade: \" + getGrade() + \")\";\n    }\n}\n\n// Inheritance\npublic class GraduateStudent extends Student {\n    private String thesis;\n    \n    public GraduateStudent(String name, int age, double gpa, String thesis) {\n        super(name, age, gpa);\n        this.thesis = thesis;\n    }\n}\n```",
         "Create a `BankAccount` class with deposit, withdraw, and getBalance methods. Add input validation.",
         "Which Java keyword calls a parent class constructor?",
         "Build a library management system with Book, Member, and Library classes including borrowing logic.",
         "The `final` keyword prevents inheritance (class) or overriding (method) or reassignment (variable).", 50),
    ]),

    # ── C++ ──────────────────────────────────────────────────────────────────────
    ("C++ Programming", "programming", "intermediate", "10 weeks", "C++17, STL, Pointers, OOP", [
        ("C++ Foundations", "Write and compile C++ programs.",
         "C++ is the language of performance — used in game engines, operating systems, trading systems, and embedded hardware.\n\n```cpp\n#include <iostream>\n#include <string>\n\nint main() {\n    std::string name = \"CodeSavannah\";\n    int count = 10;\n    double price = 9.99;\n    \n    std::cout << \"Welcome to \" << name << \"!\" << std::endl;\n    std::cout << \"Count: \" << count << std::endl;\n    \n    // Input\n    std::cout << \"Enter your name: \";\n    std::cin >> name;\n    std::cout << \"Hello, \" << name << \"!\" << std::endl;\n    \n    return 0;\n}\n```\n\n**Compile:** `g++ -std=c++17 -o hello hello.cpp`\n\n**Variables:** declared with type — `int`, `double`, `std::string`, `bool`, `char`\n\n**Namespaces:** `using namespace std;` lets you write `cout` instead of `std::cout`",
         "Write a C++ program that reads 5 integers and prints their sum, average, min, and max.",
         "What does `#include <iostream>` do in C++?",
         "Build a simple ATM simulator with balance checking, deposit, and withdrawal operations.",
         "C++ gives direct memory control — with great power comes great responsibility. Always free what you allocate!", 40),

        ("Pointers and Memory", "Understand C++ memory management.",
         "```cpp\n#include <iostream>\n\nint main() {\n    int x = 42;\n    int* ptr = &x;     // pointer to x\n    \n    std::cout << x;    // value: 42\n    std::cout << &x;   // address: 0x7fff...\n    std::cout << ptr;  // same address\n    std::cout << *ptr; // dereference: 42\n    \n    *ptr = 100;        // change x through pointer\n    std::cout << x;    // 100\n    \n    // Dynamic allocation\n    int* arr = new int[10];\n    arr[0] = 1;\n    arr[1] = 2;\n    delete[] arr;       // ALWAYS free!\n    \n    // Smart pointers (modern C++)\n    auto smart = std::make_unique<int>(42);\n    // auto-freed when goes out of scope\n    \n    return 0;\n}\n```",
         "Write a function that swaps two integers using pointers (not references).",
         "What operator dereferences a pointer to access the value at that memory address?",
         "Implement a simple linked list with insert, delete, and print operations using raw pointers.",
         "Prefer smart pointers (unique_ptr, shared_ptr) over raw pointers in modern C++ to avoid memory leaks.", 55),
    ]),

    # ── SQL ──────────────────────────────────────────────────────────────────────
    ("SQL and Databases", "databases", "beginner", "5 weeks", "SQL, PostgreSQL, MySQL, SQLite", [
        ("SQL Foundations", "Query databases with SELECT, WHERE, and JOIN.",
         "**SQL (Structured Query Language)** is used to communicate with databases.\n\n```sql\n-- Create a table\nCREATE TABLE students (\n    id         SERIAL PRIMARY KEY,\n    name       VARCHAR(150) NOT NULL,\n    email      VARCHAR(200) UNIQUE NOT NULL,\n    grade      VARCHAR(20),\n    gpa        DECIMAL(3,2),\n    enrolled_at DATE DEFAULT CURRENT_DATE\n);\n\n-- Insert data\nINSERT INTO students (name, email, grade, gpa)\nVALUES ('Amara Osei', 'amara@example.com', 'Form 3', 3.85);\n\n-- Query data\nSELECT name, gpa\nFROM students\nWHERE gpa >= 3.5\nORDER BY gpa DESC\nLIMIT 10;\n\n-- Update\nUPDATE students SET gpa = 3.90 WHERE name = 'Amara Osei';\n\n-- Delete\nDELETE FROM students WHERE id = 5;\n```",
         "Write a query that returns all students with a GPA above 3.0, sorted alphabetically by name.",
         "Which SQL clause filters rows based on a condition?",
         "Design and query a school database with tables for students, teachers, courses, and enrolments.",
         "SQL keywords are case-insensitive (select = SELECT) but conventionally written in uppercase for readability.", 40),

        ("JOINs and Aggregation", "Combine tables and summarise data.",
         "```sql\n-- INNER JOIN — only matching rows from both tables\nSELECT s.name, c.title, e.grade\nFROM enrolments e\nINNER JOIN students s ON s.id = e.student_id\nINNER JOIN courses  c ON c.id = e.course_id;\n\n-- LEFT JOIN — all rows from left, matching from right\nSELECT s.name, COUNT(e.id) AS courses_taken\nFROM students s\nLEFT JOIN enrolments e ON e.student_id = s.id\nGROUP BY s.name\nHAVING COUNT(e.id) > 2;\n\n-- Aggregation\nSELECT \n    grade,\n    COUNT(*)          AS student_count,\n    AVG(gpa)          AS avg_gpa,\n    MAX(gpa)          AS top_gpa,\n    MIN(gpa)          AS lowest_gpa\nFROM students\nGROUP BY grade\nORDER BY avg_gpa DESC;\n\n-- Subquery\nSELECT name FROM students\nWHERE gpa > (SELECT AVG(gpa) FROM students);\n```",
         "Write a query that shows each course title, its teacher name, and the number of enrolled students.",
         "Which SQL keyword is used to group rows that have the same values?",
         "Build a reporting query that shows the top 3 courses by average student GPA.",
         "INDEX your JOIN columns! Without indexes, JOINs on large tables scan every row — extremely slow.", 50),
    ]),

    # ── REACT ────────────────────────────────────────────────────────────────────
    ("React", "web", "intermediate", "8 weeks", "React 18, Hooks, JSX, Vite", [
        ("React Foundations", "Build UI components with JSX and props.",
         "React is a JavaScript library for building component-based UIs.\n\n```jsx\n// A functional component\nfunction CourseCard({ title, level, instructor }) {\n    return (\n        <div className=\"card\">\n            <span className={`tag tag-${level}`}>{level}</span>\n            <h2>{title}</h2>\n            <p>by {instructor}</p>\n            <button className=\"btn btn-primary\">Enrol Now</button>\n        </div>\n    );\n}\n\n// Using the component\nfunction App() {\n    return (\n        <main>\n            <h1>CodeSavannah Courses</h1>\n            <CourseCard\n                title=\"Python for Beginners\"\n                level=\"Beginner\"\n                instructor=\"Amina W.\"\n            />\n        </main>\n    );\n}\n\nexport default App;\n```\n\n**Setup:** `npm create vite@latest my-app -- --template react`",
         "Create a UserProfile component that accepts name, avatar URL, bio, and skills as props and renders them.",
         "What is the file extension for React components that contain JSX?",
         "Build a course listing page with CourseCard components rendered from an array of course data.",
         "JSX looks like HTML but compiles to JavaScript. className instead of class, htmlFor instead of for.", 45),

        ("State and Hooks", "Manage dynamic data with useState and useEffect.",
         "```jsx\nimport { useState, useEffect } from 'react';\n\nfunction Counter() {\n    const [count, setCount] = useState(0);\n    const [name, setName]   = useState('');\n    \n    // Side effects (data fetching, subscriptions)\n    useEffect(() => {\n        document.title = `Count: ${count}`;\n    }, [count]); // runs whenever count changes\n    \n    return (\n        <div>\n            <h2>Count: {count}</h2>\n            <button onClick={() => setCount(c => c + 1)}>+1</button>\n            <button onClick={() => setCount(c => c - 1)}>−1</button>\n            <input\n                value={name}\n                onChange={e => setName(e.target.value)}\n                placeholder=\"Your name\"\n            />\n            <p>Hello, {name || 'stranger'}!</p>\n        </div>\n    );\n}\n```\n\n**Other hooks:** `useRef`, `useContext`, `useMemo`, `useCallback`, `useReducer`",
         "Build a shopping cart component: add items, remove items, show total price — all using useState.",
         "What React hook subscribes to side effects like data fetching?",
         "Build a real-time search filter that filters a list of 50 items as you type in a text box.",
         "Never mutate state directly. Always use the setter function: setCount(count + 1), not count++.", 50),
    ]),

    # ── CYBERSECURITY ────────────────────────────────────────────────────────────
    ("Cybersecurity Fundamentals", "cybersecurity", "intermediate", "8 weeks", "Networking, OWASP, Kali Linux, CTF", [
        ("Security Basics", "Understand the CIA triad and threat landscape.",
         "**The CIA Triad:**\n- **C**onfidentiality — data is private and only accessible to authorised users\n- **I**ntegrity — data is accurate and hasn't been tampered with\n- **A**vailability — systems are up and accessible when needed\n\n**Common attack types:**\n| Attack | What it does |\n|--------|--------------|\n| Phishing | Tricks users into revealing credentials |\n| SQL Injection | Injects SQL code into database queries |\n| XSS | Injects JavaScript into web pages |\n| MITM | Intercepts communication between two parties |\n| DDoS | Overwhelms a server with traffic |\n| Ransomware | Encrypts files and demands payment |\n\n**OWASP Top 10** — the most critical web vulnerabilities, updated every few years by the Open Web Application Security Project.\n\n**Defence:** defence in depth — multiple layers of security so no single failure causes a breach.",
         "Research a real-world data breach (e.g., LinkedIn 2021, Facebook 2019). Which CIA properties were violated?",
         "What does the 'I' in the CIA triad stand for?",
         "Set up a CTF (Capture The Flag) challenge account on picoCTF.org and complete 5 beginner challenges.",
         "95% of security breaches are caused by human error — social engineering is more dangerous than any exploit.", 45),

        ("Ethical Hacking Intro", "Use security tools responsibly and legally.",
         "**IMPORTANT:** Ethical hacking means testing systems you own or have explicit written permission to test. Unauthorised hacking is illegal.\n\n**The ethical hacking process:**\n1. Reconnaissance — gather info (nmap, shodan, whois)\n2. Scanning — find open ports and services\n3. Enumeration — identify specific vulnerabilities\n4. Exploitation — attempt to exploit (only on authorised targets!)\n5. Post-exploitation — understand impact\n6. Reporting — document findings professionally\n\n**Essential tools (on Kali Linux):**\n```bash\n# Network discovery\nnmap -sV -p 1-1000 192.168.1.0/24\n\n# Web testing proxy\nburpsuite\n\n# Password cracking (on your own hashes!)\nhashcat -m 0 hash.txt wordlist.txt\n\n# Web vulnerability scanner\nniktto -h http://localhost:8080\n```\n\n**Legal ways to practice:**\n- HackTheBox.com (virtual machines)\n- TryHackMe.com (guided labs)\n- picoCTF.org (competitions)",
         "Using Kali Linux in a VM, run `nmap localhost` and explain what each result means.",
         "What is the first phase of the ethical hacking methodology?",
         "Complete TryHackMe's 'Pre-Security' learning path (free) and document your progress.",
         "Bug bounty programs (HackerOne, Bugcrowd) pay researchers legally to find vulnerabilities in real companies.", 55),
    ]),

    # ── MACHINE LEARNING ─────────────────────────────────────────────────────────
    ("Machine Learning", "ai", "advanced", "12 weeks", "Python, scikit-learn, TensorFlow, pandas", [
        ("ML Foundations", "Understand what machine learning is and how models learn.",
         "**Machine Learning** trains computers to find patterns in data without being explicitly programmed.\n\n**Types of ML:**\n- **Supervised** — labelled data (spam/not-spam, cat/dog photos)\n- **Unsupervised** — unlabelled data, find hidden patterns (clustering customers)\n- **Reinforcement** — agent learns by trial and error (games, robots)\n\n**The ML workflow:**\n```\nData → Clean → Features → Train → Evaluate → Deploy\n```\n\n```python\n# Simple example with scikit-learn\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import accuracy_score\n\n# Load data\ndf = pd.read_csv('students.csv')\nX  = df[['hours_studied', 'prev_score']]\ny  = df['passed']  # 0 or 1\n\n# Split\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n\n# Train\nmodel = LogisticRegression()\nmodel.fit(X_train, y_train)\n\n# Evaluate\npredictions = model.predict(X_test)\nprint(f'Accuracy: {accuracy_score(y_test, predictions):.2%}')\n```",
         "Load the Iris dataset using `sklearn.datasets.load_iris()` and train a decision tree classifier. Print accuracy.",
         "What type of ML uses labelled data?",
         "Build a student performance predictor: given hours studied and sleep, predict if the student will pass.",
         "Garbage in, garbage out — data quality matters more than model complexity. Clean first, model second.", 60),
    ]),

    # ── FLUTTER ──────────────────────────────────────────────────────────────────
    ("Flutter Mobile Dev", "mobile", "intermediate", "10 weeks", "Flutter, Dart, Android/iOS, Firebase", [
        ("Flutter Foundations", "Build cross-platform mobile UIs with Flutter.",
         "Flutter is Google's UI toolkit for building natively compiled apps for mobile, web, and desktop from a single Dart codebase.\n\n```dart\nimport 'package:flutter/material.dart';\n\nvoid main() {\n    runApp(const MyApp());\n}\n\nclass MyApp extends StatelessWidget {\n    const MyApp({super.key});\n    \n    @override\n    Widget build(BuildContext context) {\n        return MaterialApp(\n            title: 'CodeSavannah',\n            theme: ThemeData(\n                colorScheme: ColorScheme.fromSeed(\n                    seedColor: const Color(0xFF1341a8),\n                ),\n                useMaterial3: true,\n            ),\n            home: const HomePage(),\n        );\n    }\n}\n\nclass HomePage extends StatelessWidget {\n    const HomePage({super.key});\n    \n    @override\n    Widget build(BuildContext context) {\n        return Scaffold(\n            appBar: AppBar(title: const Text('Home')),\n            body: const Center(\n                child: Text(\n                    'Welcome to CodeSavannah!',\n                    style: TextStyle(fontSize: 24),\n                ),\n            ),\n        );\n    }\n}\n```\n\n**Setup:** Install Flutter SDK, run `flutter create myapp`, open in VS Code.",
         "Build a counter app where tapping a button increments a number displayed on screen.",
         "What is the base class for Flutter widgets that do not change over time?",
         "Build a to-do list Flutter app with add, complete, and delete functionality using StatefulWidget.",
         "In Flutter, everything is a Widget — even padding, alignment, and styling are widgets, not properties.", 55),
    ]),

    # ── CLOUD AWS ────────────────────────────────────────────────────────────────
    ("Cloud Computing (AWS)", "cloud", "advanced", "10 weeks", "AWS, EC2, S3, Lambda, RDS, IAM", [
        ("AWS Foundations", "Navigate core AWS services and deploy a web app.",
         "Amazon Web Services is the world's largest cloud platform — 33% market share, used by Netflix, Airbnb, NASA.\n\n**Core concepts:**\n- **Region** — geographic area (us-east-1, af-south-1)\n- **Availability Zone** — data centre within a region\n- **IAM** — Identity and Access Management (who can do what)\n\n**Essential services:**\n| Service | Purpose |\n|---------|---------|\n| EC2 | Virtual servers |\n| S3 | Object storage (files, images, backups) |\n| RDS | Managed databases (PostgreSQL, MySQL) |\n| Lambda | Serverless functions |\n| CloudFront | CDN — fast global delivery |\n| Route 53 | DNS management |\n| ECS/EKS | Container orchestration |\n\n**Free tier:** AWS gives 750 hours/month of t2.micro EC2, 5GB S3, and 1M Lambda calls — free for 12 months.\n\n```bash\n# Install AWS CLI\npip install awscli\naws configure\n\n# Deploy a static site to S3\naws s3 sync ./build s3://my-site --delete\naws s3 website s3://my-site --index-document index.html\n```",
         "Create a free tier AWS account and deploy a static HTML page to S3 with public access enabled.",
         "What AWS service stores files and objects in the cloud?",
         "Deploy a Django application to an EC2 instance with Nginx, Gunicorn, and an RDS PostgreSQL database.",
         "Always enable MFA on your AWS root account and never use root credentials in your code.", 60),
    ]),
]


class Command(BaseCommand):
    help = 'Seed comprehensive lessons for all programming languages and technology tracks.'

    def handle(self, *args, **options):
        created_paths = 0
        created_lessons = 0

        for (title, category, level, duration, skill_stack, lessons_data) in PATHS:
            path, path_created = LearningPath.objects.get_or_create(
                title=title,
                defaults={
                    'category': category,
                    'level': level,
                    'duration': duration,
                    'skill_stack': skill_stack,
                    'summary': f'A comprehensive {level} track covering {skill_stack}.',
                    'is_featured': True,
                },
            )
            if path_created:
                created_paths += 1
                self.stdout.write(f'  Created path: {title}')

            for order, (l_title, objective, content, exercise, quiz_q, project, notes, mins) in enumerate(lessons_data, start=1):
                _, lesson_created = Lesson.objects.get_or_create(
                    learning_path=path,
                    title=l_title,
                    defaults={
                        'order': order,
                        'objective': objective,
                        'content': content,
                        'exercise_prompt': exercise,
                        'quiz_question': quiz_q,
                        'project_prompt': project,
                        'notes': notes,
                        'estimated_minutes': mins,
                    },
                )
                if lesson_created:
                    created_lessons += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {created_paths} new paths and {created_lessons} new lessons.'
        ))
