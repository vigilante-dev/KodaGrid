"""
Batch 6: Fix partial paths + HTML, CSS, JavaScript for Web, Next.js
"""
from django.core.management.base import BaseCommand
from academy.models import LearningPath, Lesson


def upsert(path, order, title, objective, content, exercise, quiz_q, project, notes, mins):
    qs = Lesson.objects.filter(learning_path=path, order=order)
    if qs.count() > 1:
        keep = qs.first().pk
        qs.exclude(pk=keep).delete()
        qs = Lesson.objects.filter(pk=keep)
    lesson = qs.first()
    if lesson:
        lesson.title = title; lesson.objective = objective
        lesson.content = content; lesson.exercise_prompt = exercise
        lesson.quiz_question = quiz_q; lesson.project_prompt = project
        lesson.notes = notes; lesson.estimated_minutes = mins
        lesson.save()
        return False
    Lesson.objects.create(
        learning_path=path, order=order, title=title, objective=objective,
        content=content, exercise_prompt=exercise, quiz_question=quiz_q,
        project_prompt=project, notes=notes, estimated_minutes=mins
    )
    return True


class Command(BaseCommand):
    help = 'Batch 6: Fix partial paths + HTML, CSS, JavaScript for Web, Next.js'

    def handle(self, *args, **options):
        created = updated = 0

        # ── NETWORKING (orders 1-3, order 1 had wrong C content) ──────────────
        p = LearningPath.objects.get(slug='networking')

        r = upsert(p, 1, 'Networking Fundamentals',
            'Understand the OSI model, TCP/IP, IP addressing, and how data travels across networks.',
            '''## How Networks Work

A **computer network** connects devices so they can share data. The internet is the world's largest network.

### The OSI Model (7 Layers)

| Layer | Name | Example |
|-------|------|---------|
| 7 | Application | HTTP, FTP, DNS |
| 6 | Presentation | SSL/TLS, encryption |
| 5 | Session | Login sessions |
| 4 | Transport | TCP, UDP |
| 3 | Network | IP addresses, routing |
| 2 | Data Link | MAC addresses, Ethernet |
| 1 | Physical | Cables, Wi-Fi signals |

### TCP/IP Address Structure

```
IPv4: 192.168.1.100
      |   |  | |
      |   |  | Host
      |   |  Subnet
      |   Network
      Class

Subnet mask: 255.255.255.0  (/24)
```

### Key Protocols

```
HTTP   - Hypertext Transfer Protocol (web pages, port 80)
HTTPS  - Secure HTTP (port 443)
DNS    - Domain Name System (name to IP, port 53)
DHCP   - Dynamic Host Configuration Protocol (auto IP assignment)
SSH    - Secure Shell (remote access, port 22)
FTP    - File Transfer Protocol (port 21)
SMTP   - Email sending (port 25 / 587)
```

### TCP vs UDP

```
TCP (Transmission Control Protocol)
- Connection-oriented (3-way handshake)
- Reliable: guarantees delivery
- Used by: HTTP, SSH, email
- Slower but accurate

UDP (User Datagram Protocol)
- Connectionless
- Fast but no delivery guarantee
- Used by: video streaming, DNS, gaming
```

### IP Subnetting Basics

```
Network:  192.168.1.0/24
Hosts:    192.168.1.1 - 192.168.1.254  (254 usable)
Broadcast: 192.168.1.255

Private ranges (RFC 1918):
  10.0.0.0/8        (10.x.x.x)
  172.16.0.0/12     (172.16.x.x - 172.31.x.x)
  192.168.0.0/16    (192.168.x.x)
```

### Ping and Traceroute

```bash
# Test connectivity
ping google.com
ping 8.8.8.8

# Trace route to destination
traceroute google.com    # Linux/Mac
tracert google.com       # Windows

# Show network interfaces
ip addr                  # Linux
ipconfig                 # Windows
ifconfig                 # Mac
```

### How DNS Works

```
You type: www.google.com
          |
          v
1. Check local cache
2. Ask DNS resolver (your ISP)
3. Ask root nameserver
4. Ask .com nameserver
5. Ask google.com nameserver
6. Get IP: 142.250.80.36
7. Connect to that IP
```''',
            'Use the `ping` command to test connectivity to 3 different hosts. Then use `ipconfig` (Windows) or `ip addr` (Linux) to find your machine\'s IP address and subnet mask.',
            'What protocol guarantees delivery by using a 3-way handshake? A) UDP  B) TCP  C) HTTP  D) DNS',
            'Build a simple network diagram: draw 4 computers connected to a switch, the switch connected to a router, and the router connected to the internet. Label each device with an example IP address. Identify which IPs are private and which are public.',
            'Private IP ranges are 10.x.x.x, 172.16-31.x.x, and 192.168.x.x. These are not routable on the public internet — NAT (Network Address Translation) maps them to a public IP.',
            50)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 2, 'Network Security & Protocols',
            'Learn about firewalls, VPNs, HTTPS, common attack vectors, and how to secure a network.',
            '''## Securing Networks

### Firewalls

A firewall filters traffic based on rules:

```
ALLOW  TCP  ANY         -> 443   (HTTPS in)
ALLOW  TCP  ANY         -> 22    (SSH in from trusted IPs)
DENY   ALL  ANY         -> ANY   (block everything else)
```

Types:
- **Packet filter**: checks IP/port headers
- **Stateful**: tracks connection state
- **Application (WAF)**: understands HTTP, SQL

### VPNs (Virtual Private Networks)

```
Remote Worker ──[encrypted tunnel]──> VPN Server ──> Internal Network
```

Common protocols:
- **OpenVPN**: open source, very secure
- **WireGuard**: modern, fast, minimal
- **IPsec**: built into routers/OS

### HTTPS and TLS

```
TLS Handshake (simplified):
1. Client: "Hello, I support TLS 1.3"
2. Server: "Hello, here's my certificate"
3. Client: verifies certificate
4. Both: generate session key
5. All data encrypted with AES-256
```

### Common Network Attacks

| Attack | Description | Defence |
|--------|-------------|---------|
| MITM | Intercept traffic | Use HTTPS/TLS |
| DNS spoofing | Fake DNS responses | DNSSEC |
| DDoS | Flood target with traffic | Rate limiting, CDN |
| ARP poisoning | Fake MAC addresses | Dynamic ARP inspection |
| Port scan | Find open services | Firewall, IDS |

### Network Monitoring Tools

```bash
# Scan network for open ports
nmap -sV 192.168.1.0/24

# Capture network traffic
tcpdump -i eth0 port 80

# Show open connections
netstat -tulnp          # Linux
netstat -an             # Windows

# Show routing table
route -n                # Linux
route print             # Windows
```

### Wireless Security

```
WEP   - Broken (DO NOT USE)
WPA   - Weak
WPA2  - Acceptable (use AES, not TKIP)
WPA3  - Current standard, use this
```

### Zero Trust Network Model

```
OLD: Trust inside, distrust outside
NEW: Trust nobody by default

Principles:
- Verify every user and device
- Least privilege access
- Assume breach
- Encrypt everything in transit
```''',
            'Set up a simple firewall rule: research how to block a specific IP address using Windows Firewall or Linux iptables. Write out the command or steps you would follow.',
            'What encryption standard is recommended for WPA2 wireless networks? A) TKIP  B) WEP  C) AES  D) MD5',
            'Research and document a real-world network breach (e.g., Target 2013, Mirai botnet). Identify: what vulnerability was exploited, what protocols failed, and what network security controls could have prevented it.',
            'WPA2 with AES is the minimum acceptable Wi-Fi security. WPA3 uses SAE (Simultaneous Authentication of Equals) which resists offline dictionary attacks.',
            55)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'Networking Project',
            'Design and document a small office network with security controls, IP addressing scheme, and protocol choices.',
            '''## Project: Design a Secure Office Network

### Scenario

You are hired to set up a network for a 10-person startup:
- 8 employee workstations
- 1 file/print server
- 1 web server (public-facing)
- Wi-Fi for guests
- Remote access for 3 remote workers

### Deliverables

**1. IP Addressing Plan**
```
WAN IP (public):     203.0.113.10
Router LAN IP:       10.0.0.1

VLAN 10 - Employees: 10.0.10.0/24
  Workstations:      10.0.10.10 - 10.0.10.20
  File server:       10.0.10.100

VLAN 20 - Servers:   10.0.20.0/24
  Web server:        10.0.20.10

VLAN 30 - Guest:     10.0.30.0/24
  DHCP pool:         10.0.30.100 - 10.0.30.200
```

**2. Security Controls**
```
Firewall rules:
- VLAN30 (guest) -> VLAN10 : DENY
- VLAN30 (guest) -> VLAN20 : DENY
- ANY           -> 10.0.20.10:443 : ALLOW
- 10.0.10.0/24  -> ANY           : ALLOW
- Remote VPN    -> 10.0.10.0/24  : ALLOW (authenticated)

Wi-Fi:
- Employee SSID: WPA3, VLAN10
- Guest SSID:    WPA2, VLAN30, bandwidth limited
```

**3. Documentation**
Create a diagram showing:
- Router, switch, VLANs
- Device placement per VLAN
- Firewall between VLANs and internet
- VPN endpoint

### Tools to Use
- **draw.io** (free) — network diagram tool
- **Packet Tracer** (Cisco, free) — simulate real networks
- **GNS3** — advanced network emulation''',
            'Use draw.io to create the network diagram for the scenario above. Include all VLANs, devices, and firewall rules.',
            'What is the purpose of VLANs in a network? A) Faster Wi-Fi  B) Segment traffic to improve security  C) Assign public IPs  D) Replace firewalls',
            'Extend the project: add a SIEM (Security Information and Event Management) plan. Identify what logs you would collect (firewall, DNS, authentication), how long to retain them, and what alerts to configure for suspicious activity.',
            'VLANs (Virtual LANs) segment broadcast domains logically without needing separate physical hardware. They are essential for isolating guest traffic from internal systems.',
            60)
        if r: created += 1
        else: updated += 1

        # ── DEEP LEARNING (fix order 1 placeholder + order 3) ──────────────────
        p = LearningPath.objects.get(slug='deep-learning')

        r = upsert(p, 1, 'Deep Learning Foundations',
            'Understand neurons, layers, activation functions, and how a neural network learns.',
            '''## What is Deep Learning?

Deep learning uses **neural networks** with many layers to learn patterns in data.

```
Input Layer  ->  Hidden Layers  ->  Output Layer
(features)       (learn patterns)   (prediction)
```

### The Artificial Neuron

```python
def neuron(inputs, weights, bias):
    # Weighted sum
    z = sum(w * x for w, x in zip(weights, inputs)) + bias
    # Activation
    return activation(z)

# Example: 3-input neuron
inputs  = [0.5, 0.8, 0.2]
weights = [0.4, -0.6, 0.9]
bias    = 0.1
z = (0.5*0.4) + (0.8*-0.6) + (0.2*0.9) + 0.1  # = -0.08
```

### Activation Functions

```python
import numpy as np

def relu(z):
    return np.maximum(0, z)        # Most common in hidden layers

def sigmoid(z):
    return 1 / (1 + np.exp(-z))   # Binary output (0-1)

def softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()             # Multi-class output (probabilities)

def tanh(z):
    return np.tanh(z)              # Range -1 to 1
```

### A Simple Neural Network with Keras

```python
import tensorflow as tf
from tensorflow import keras

# Build model
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')   # 10 classes
])

# Compile
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()
```

### How Networks Learn: Backpropagation

```
Forward pass:   input -> prediction
Loss:           compare prediction to truth
Backward pass:  compute gradients
Update:         weights = weights - lr * gradients
```

### The MNIST Example (28x28 handwritten digits)

```python
# Load data
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Preprocess
x_train = x_train.reshape(-1, 784) / 255.0
x_test  = x_test.reshape(-1, 784) / 255.0

# Train
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)

# Evaluate
loss, acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {acc:.4f}')   # ~98%
```

### Key Hyperparameters

| Parameter | What it controls |
|-----------|-----------------|
| Learning rate | Step size during gradient descent |
| Batch size | Samples per weight update |
| Epochs | Times through full dataset |
| Dropout | Fraction of neurons disabled (regularization) |
| Layers/neurons | Model capacity |''',
            'Build the MNIST classifier above in Google Colab or a local notebook. Record the training/validation accuracy per epoch. Try changing the number of hidden neurons from 128 to 64 and observe the effect on accuracy.',
            'What does the ReLU activation function output for a negative input? A) The negative value  B) Zero  C) One  D) Infinity',
            'Extend the MNIST classifier: add a third hidden layer, experiment with batch sizes (32, 128, 512), and plot training/validation accuracy curves. Report which configuration gave the best test accuracy.',
            'Overfitting is when a model memorizes training data but fails on new data. Dropout is the most common regularizer in deep learning — it randomly zeros neurons during training, forcing the network to learn redundant representations.',
            70)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'Deep Learning Project',
            'Build and deploy an image classifier or text classifier using a trained deep learning model.',
            '''## Project: Image Classifier with CNN

### Convolutional Neural Network (CNN)

CNNs are the standard architecture for image tasks:

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def build_cnn(num_classes):
    model = keras.Sequential([
        # Convolutional blocks
        layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)),
        layers.MaxPooling2D(),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, (3,3), activation='relu'),

        # Classifier head
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

model = build_cnn(10)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
```

### Train on CIFAR-10

```python
# 60,000 images in 10 classes (car, bird, cat, dog, ...)
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Normalize
x_train, x_test = x_train / 255.0, x_test / 255.0

# Data augmentation
datagen = keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
)
datagen.fit(x_train)

# Train
model.fit(datagen.flow(x_train, y_train, batch_size=64),
          epochs=20,
          validation_data=(x_test, y_test))
```

### Save and Load

```python
# Save
model.save('cifar10_cnn.h5')

# Load
loaded = keras.models.load_model('cifar10_cnn.h5')

# Predict on new image
import numpy as np
from PIL import Image

img = Image.open('test.jpg').resize((32, 32))
arr = np.array(img) / 255.0
arr = arr.reshape(1, 32, 32, 3)
predictions = loaded.predict(arr)
classes = ['airplane','auto','bird','cat','deer','dog','frog','horse','ship','truck']
print('Predicted:', classes[np.argmax(predictions)])
```

### Deliverables
1. Train model on CIFAR-10, achieve > 70% test accuracy
2. Plot training/validation curves
3. Show confusion matrix for test set
4. Predict on 5 new images from the web''',
            'Write the code to load the saved model and predict on 3 images you download from the internet. Print the class name and confidence score.',
            'What layer type extracts local features (edges, textures) from images? A) Dense  B) Conv2D  C) Flatten  D) Dropout',
            'Transfer learning: instead of training from scratch, use a pre-trained model (MobileNetV2, ResNet50) from `keras.applications`. Fine-tune only the top layers on a custom dataset of your choice (e.g., cats vs dogs). Compare accuracy and training time vs. training from scratch.',
            'Transfer learning uses weights pre-trained on ImageNet (1.2M images, 1000 classes). Fine-tuning only the last few layers takes minutes instead of hours and typically outperforms training from scratch on small datasets.',
            90)
        if r: created += 1
        else: updated += 1

        # ── PROMPT ENGINEERING (fix order 1 + order 3) ────────────────────────
        p = LearningPath.objects.get(slug='prompt-engineering')

        r = upsert(p, 1, 'Prompt Engineering Foundations',
            'Understand what prompt engineering is, why it matters, and master the core techniques for reliable AI outputs.',
            '''## What is Prompt Engineering?

Prompt engineering is the art of writing clear, structured instructions that get language models (LLMs) to produce exactly what you need.

### Why It Matters

```
Bad prompt:  "Write about Python"
Result:      Vague 3-paragraph overview

Good prompt: "Write a 5-step tutorial on Python list comprehensions
              for beginners aged 14-17. Include one code example per
              step. Use simple language."
Result:      Focused, structured, exactly right
```

### Core Principles

**1. Be Specific**
```
Instead of: "Summarize this"
Write:      "Summarize in 3 bullet points, each under 20 words,
             focusing on the main technical finding"
```

**2. Provide Context**
```
"You are a senior Python developer reviewing code written by
a junior. Review the following function and suggest 3 improvements
with explanations a beginner can understand."
```

**3. Specify Format**
```
"Return your response as valid JSON with keys:
 title (string), steps (array of strings), difficulty (easy/medium/hard)"
```

**4. Give Examples (Few-Shot)**
```
Classify the sentiment:
Text: "I love this course!" -> Positive
Text: "Terrible waste of time" -> Negative
Text: "The video quality was average" -> ?
```

### Prompt Templates

```python
# System + User structure (OpenAI / Claude)
prompt = {
    "system": "You are a coding tutor for African high school students.",
    "user": f"Explain {topic} in simple terms with a Kenyan context example."
}
```

### Chain of Thought

Asking the model to reason step by step dramatically improves accuracy:

```
Bad:  "What is 15% of 340?"

Good: "Calculate 15% of 340. Think step by step."
Reasoning: 10% of 340 = 34. 5% = 17. Total = 51.
```

### Temperature and Parameters

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0.2,   # 0 = deterministic, 1 = creative
    max_tokens=500,
    top_p=0.95,
)
```

| Temperature | Best for |
|-------------|---------|
| 0.0 - 0.3 | Code, facts, summaries |
| 0.5 - 0.7 | Explanations, analysis |
| 0.8 - 1.0 | Creative writing, brainstorming |''',
            'Write 3 versions of a prompt asking an AI to explain recursion: (1) a bad vague prompt, (2) a role+format prompt, and (3) a chain-of-thought prompt. Compare the types of responses each would produce.',
            'What technique dramatically improves AI accuracy on reasoning tasks by asking it to reason step-by-step? A) Zero-shot  B) Negative prompting  C) Chain of Thought  D) Temperature scaling',
            'Build a "prompt library" — a markdown file with 10 reusable prompt templates for common developer tasks: code review, bug explanation, test generation, documentation writing, commit message generation, and 5 more of your choice. Include an example output for each.',
            'Temperature controls randomness. For code generation, use temperature 0-0.2 to get deterministic, syntactically valid output. For creative tasks like story writing, use 0.7-1.0 for variety.',
            55)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'Prompt Engineering Project',
            'Build a real application that uses prompt engineering to power a useful AI feature.',
            '''## Project: AI-Powered Study Assistant

Build a Django or CLI app that uses an LLM API to help students learn.

### Features to Build

**1. Concept Explainer**
```python
def explain_concept(topic, student_level='high school'):
    prompt = f"""You are a patient coding tutor.

Explain '{topic}' to a {student_level} student in East Africa.
Use a relatable local analogy.
Include one short code example.
End with one question to check understanding.
Keep response under 200 words."""
    return ask_llm(prompt)
```

**2. Code Reviewer**
```python
def review_code(code, language='python'):
    prompt = f"""Review this {language} code written by a student.

```{language}
{code}
```

Provide:
1. What works well (1-2 sentences)
2. One specific bug or issue (with line reference)
3. One improvement suggestion
4. A corrected version

Be encouraging and educational."""
    return ask_llm(prompt)
```

**3. Quiz Generator**
```python
def generate_quiz(topic, num_questions=3, difficulty='beginner'):
    prompt = f"""Generate {num_questions} {difficulty} multiple-choice
questions about {topic}.

Format as JSON:
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct": "B",
    "explanation": "..."
  }}
]"""
    return ask_llm(prompt)
```

### Using OpenAI API

```python
from openai import OpenAI
client = OpenAI(api_key='your-key')

def ask_llm(prompt, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.4,
        max_tokens=600,
    )
    return response.choices[0].message.content
```

### Deliverables
1. Working CLI or web app with all 3 features
2. Prompt documentation: explain your design choices
3. Test each feature with 5 real inputs
4. Measure and report average response time''',
            'Implement the quiz generator and run it for 3 different topics. Format the output nicely in the terminal or as an HTML page.',
            'Which API parameter controls how creative vs. deterministic an LLM response is? A) max_tokens  B) top_k  C) temperature  D) frequency_penalty',
            'Add a fourth feature: a "study plan generator" that takes a topic and a number of weeks, then outputs a day-by-day study schedule with specific tasks, resources, and mini-projects. Use structured output (JSON) and render it as a formatted table.',
            'Always validate JSON output from LLMs before parsing — models occasionally produce malformed JSON. Use a try/except and a retry mechanism with a more explicit format instruction.',
            80)
        if r: created += 1
        else: updated += 1

        # ── BOOTSTRAP (fix orders 2-3) ──────────────────────────────────────
        p = LearningPath.objects.get(slug='bootstrap')

        r = upsert(p, 2, 'Bootstrap Components & Utilities',
            'Build responsive UIs with Bootstrap navigation, cards, forms, and utility classes.',
            '''## Bootstrap Components

### Navbar

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="#">CodeSavannah</a>
    <button class="navbar-toggler" type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link active" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Courses</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Contact</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

### Cards

```html
<div class="row row-cols-1 row-cols-md-3 g-4">
  {% for course in courses %}
  <div class="col">
    <div class="card h-100 shadow-sm">
      <img src="{{ course.image }}" class="card-img-top" alt="{{ course.title }}">
      <div class="card-body">
        <span class="badge bg-primary mb-2">{{ course.level }}</span>
        <h5 class="card-title">{{ course.title }}</h5>
        <p class="card-text text-muted">{{ course.description }}</p>
      </div>
      <div class="card-footer d-flex justify-content-between">
        <small class="text-muted">{{ course.duration }}</small>
        <a href="#" class="btn btn-sm btn-primary">Enroll</a>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
```

### Forms

```html
<form class="needs-validation" novalidate>
  <div class="mb-3">
    <label class="form-label">Email address</label>
    <input type="email" class="form-control" required>
    <div class="invalid-feedback">Please enter a valid email.</div>
  </div>
  <div class="mb-3">
    <label class="form-label">Course</label>
    <select class="form-select" required>
      <option value="">-- Choose --</option>
      <option>Python Programming</option>
      <option>Web Development</option>
    </select>
  </div>
  <button type="submit" class="btn btn-success w-100">Enroll Now</button>
</form>
```

### Utility Classes

```html
<!-- Spacing: m=margin, p=padding, 0-5 scale -->
<div class="mt-4 mb-2 px-3">...</div>

<!-- Flexbox -->
<div class="d-flex justify-content-between align-items-center gap-3">

<!-- Colors -->
<p class="text-primary">Blue</p>
<p class="text-success">Green</p>
<div class="bg-light p-3 rounded">Light background</div>

<!-- Display at breakpoints -->
<div class="d-none d-md-block">Hidden on mobile</div>
<div class="d-block d-md-none">Mobile only</div>
```''',
            'Build a course catalog page: a navbar with your academy name, a hero section with a heading and enroll button, and at least 3 course cards in a responsive grid. Use Bootstrap grid, cards, and utilities.',
            'Which Bootstrap class makes elements stack on mobile and show in a row on medium+ screens? A) d-block  B) flex-column  C) col-md-4  D) row-cols-1',
            'Build a complete landing page for CodeSavannah using only Bootstrap: navbar, hero with CTA, feature tiles (icons from Bootstrap Icons), a pricing table using Bootstrap cards, and a contact form. Make it mobile-responsive.',
            'Bootstrap Icons (icons.getbootstrap.com) are SVG icons you include via CDN. Use `<i class="bi bi-code-slash"></i>` format. They scale with font-size and accept text color classes.',
            60)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'Bootstrap Project',
            'Build a fully responsive multi-page website for a real organization using Bootstrap 5.',
            '''## Project: Academy Website with Bootstrap 5

### Requirements

Build a 3-page website:
1. **Home** — hero, features, courses preview, testimonials
2. **Courses** — searchable grid with filter buttons
3. **Contact** — form with validation

### Starter Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TechAcademy</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    .hero { min-height: 90vh; background: linear-gradient(135deg, #0d6efd, #0dcaf0); }
    .course-card:hover { transform: translateY(-4px); transition: .3s; }
  </style>
</head>
<body>
  <!-- NAVBAR -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">...</nav>

  <!-- HERO -->
  <section class="hero d-flex align-items-center text-white" style="margin-top:56px;">
    <div class="container text-center py-5">
      <h1 class="display-4 fw-bold">Transform Your Future Through Code</h1>
      <p class="lead">Africa's premier coding academy</p>
      <a href="courses.html" class="btn btn-light btn-lg me-2">Browse Courses</a>
      <a href="contact.html" class="btn btn-outline-light btn-lg">Get in Touch</a>
    </div>
  </section>

  <!-- FEATURES -->
  <section class="py-5 bg-light">
    <div class="container">
      <div class="row text-center g-4">
        <div class="col-md-4">
          <i class="bi bi-laptop fs-1 text-primary"></i>
          <h4 class="mt-3">Hands-On Learning</h4>
          <p class="text-muted">Build real projects from day one.</p>
        </div>
        <!-- more features -->
      </div>
    </div>
  </section>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Deliverables
1. All 3 pages built and linked
2. Fully responsive (test at 375px, 768px, 1280px)
3. At least 2 Bootstrap JS components (modal, carousel, or toast)
4. Custom CSS to brand it with your own color scheme
5. Valid HTML (check at validator.w3.org)''',
            'Test your website at 375px (iPhone SE) and 1440px (desktop). Take screenshots and identify any layout issues. Fix at least 2 issues using Bootstrap responsive utilities.',
            'Which Bootstrap JS component shows a dismissible temporary notification in the corner? A) Modal  B) Toast  C) Dropdown  D) Collapse',
            'Add a "dark mode" toggle to your website. Use Bootstrap 5\'s `data-bs-theme="dark"` attribute on `<html>` and a button that toggles it using 3 lines of JavaScript. Persist the preference in localStorage.',
            'Bootstrap 5 dropped jQuery as a dependency — it is now pure vanilla JS. The `data-bs-*` attributes handle most interactions without any JavaScript code.',
            90)
        if r: created += 1
        else: updated += 1

        # ── C PROGRAMMING (fix orders 2-3) ──────────────────────────────────
        p = LearningPath.objects.get(slug='c')

        r = upsert(p, 2, 'C Pointers and Memory Management',
            'Master pointers, dynamic memory allocation, and memory-safe programming in C.',
            '''## Pointers: The Heart of C

A pointer stores the memory address of another variable.

```c
#include <stdio.h>

int main() {
    int x = 42;
    int *ptr = &x;   // ptr holds the address of x

    printf("Value of x:   %d\\n", x);        // 42
    printf("Address of x: %p\\n", (void*)&x); // e.g. 0x7fff5fbff58c
    printf("ptr holds:    %p\\n", (void*)ptr); // same address
    printf("*ptr (deref): %d\\n", *ptr);      // 42

    *ptr = 100;   // modify x through ptr
    printf("x is now: %d\\n", x);            // 100
    return 0;
}
```

### Pointer Arithmetic

```c
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;    // points to arr[0]

printf("%d\\n", *p);      // 10
printf("%d\\n", *(p+1)); // 20
printf("%d\\n", *(p+2)); // 30

// Iterate with pointer
for (int i = 0; i < 5; i++) {
    printf("%d ", *(p + i));
}
```

### Dynamic Memory Allocation

```c
#include <stdlib.h>

int main() {
    int n = 5;

    // Allocate array on heap
    int *arr = malloc(n * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "malloc failed\\n");
        return 1;
    }

    // Use the array
    for (int i = 0; i < n; i++) {
        arr[i] = i * 10;
    }

    // Always free!
    free(arr);
    arr = NULL;   // prevent dangling pointer
    return 0;
}
```

### calloc and realloc

```c
// calloc: allocate + zero-initialize
int *a = calloc(10, sizeof(int));  // 10 ints, all zero

// realloc: resize existing allocation
int *b = malloc(5 * sizeof(int));
b = realloc(b, 10 * sizeof(int)); // grow to 10
if (!b) { /* handle error */ }
free(b);
```

### Common Memory Bugs

```c
// BUG 1: Dangling pointer
int *p = malloc(4);
free(p);
*p = 5;   // UNDEFINED BEHAVIOR — use after free

// BUG 2: Memory leak
void leak() {
    int *p = malloc(4);
    // forgot free(p) — memory leaks!
}

// BUG 3: Buffer overflow
char buf[8];
strcpy(buf, "this string is too long!");  // overflow!
// Safe alternative:
strncpy(buf, src, sizeof(buf) - 1);
buf[sizeof(buf)-1] = '\0';
```

### Valgrind: Memory Error Detector

```bash
gcc -g -o program program.c
valgrind --leak-check=full ./program
```''',
            'Write a C program that: (1) dynamically allocates an array of n integers (n from user input), (2) fills it with squares (arr[i] = i*i), (3) prints the array, (4) frees the memory. Verify with valgrind.',
            'What function deallocates memory allocated by malloc()? A) delete  B) free()  C) dispose()  D) release()',
            'Implement a dynamic stack using malloc/realloc: support push(), pop(), peek(), and isEmpty(). The stack should grow automatically when full. Write a main() that tests all operations.',
            'Rule of thumb: every malloc/calloc/realloc must have a corresponding free(). Use valgrind or AddressSanitizer (`gcc -fsanitize=address`) to catch memory bugs before they reach production.',
            65)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'C Project: Build a Text Adventure Game',
            'Apply C fundamentals to build a complete text-based adventure game with structs, files, and dynamic memory.',
            '''## Project: Text Adventure Game in C

### Game Structure

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ROOMS 10
#define NAME_LEN  64
#define DESC_LEN  256

typedef struct {
    int id;
    char name[NAME_LEN];
    char description[DESC_LEN];
    int north, south, east, west;  // room IDs, -1 = no exit
    int has_item;
    char item_name[NAME_LEN];
} Room;

typedef struct {
    char name[NAME_LEN];
    int current_room;
    int health;
    int inventory[10];
    int inv_count;
} Player;

// Global state
Room rooms[MAX_ROOMS];
Player player;
int num_rooms = 0;
```

### Room Setup

```c
void init_game() {
    // Room 0: Start
    rooms[0] = (Room){
        .id = 0,
        .name = "Main Gate",
        .description = "You stand at the entrance of the Savannah Academy.",
        .north = 1, .south = -1, .east = 2, .west = -1,
        .has_item = 1, .item_name = "keycard"
    };
    // Room 1: Library
    rooms[1] = (Room){
        .id = 1,
        .name = "Library",
        .description = "Rows of coding books line the walls.",
        .north = -1, .south = 0, .east = -1, .west = -1,
        .has_item = 0
    };
    num_rooms = 2;

    player = (Player){
        .name = "Coder", .current_room = 0,
        .health = 100, .inv_count = 0
    };
}
```

### Game Loop

```c
void move(char *direction) {
    Room *r = &rooms[player.current_room];
    int next = -1;
    if (strcmp(direction, "north") == 0) next = r->north;
    else if (strcmp(direction, "south") == 0) next = r->south;
    else if (strcmp(direction, "east") == 0)  next = r->east;
    else if (strcmp(direction, "west") == 0)  next = r->west;

    if (next == -1) printf("You can't go that way.\\n");
    else { player.current_room = next; look(); }
}

void look() {
    Room *r = &rooms[player.current_room];
    printf("\\n=== %s ===\\n%s\\n", r->name, r->description);
    if (r->has_item)
        printf("You see a %s here.\\n", r->item_name);
}

int main() {
    init_game();
    char cmd[64];
    look();
    while (1) {
        printf("\\n> ");
        fgets(cmd, sizeof(cmd), stdin);
        cmd[strcspn(cmd, "\\n")] = '\0';
        if (strcmp(cmd, "quit") == 0) break;
        else if (strncmp(cmd, "go ", 3) == 0) move(cmd + 3);
        else if (strcmp(cmd, "look") == 0) look();
        else printf("Commands: go <dir>, look, quit\\n");
    }
    return 0;
}
```

### Deliverables
1. At least 5 connected rooms
2. Items to pick up (inventory system)
3. One puzzle (need item X to unlock room Y)
4. Save/load game state to file using fwrite/fread''',
            'Add the "take" command that picks up an item from the current room and adds it to the player inventory array. Print a message confirming the pickup.',
            'Which C format specifier prints a pointer address? A) %d  B) %s  C) %p  D) %x',
            'Save and load game state: implement save_game() using fwrite() to write the Player struct and all Room structs to a binary file. Implement load_game() using fread(). Test that the game state is fully restored after loading.',
            'Binary file I/O with fwrite/fread is fast and compact but not portable across architectures (struct padding differs). For portable save files, consider a text format like JSON or CSV.',
            90)
        if r: created += 1
        else: updated += 1

        # ── FLASK (fix order 3) ─────────────────────────────────────────────
        p = LearningPath.objects.get(slug='flask')

        r = upsert(p, 3, 'Flask Project: REST API',
            'Build and deploy a complete Flask REST API with authentication, CRUD, and JSON responses.',
            '''## Flask REST API Project

### Project Structure

```
flask_api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── courses.py
│   └── config.py
├── run.py
└── requirements.txt
```

### App Factory Pattern

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
    app.config['JWT_SECRET_KEY'] = 'dev-secret-change-in-prod'

    db.init_app(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.courses import courses_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')

    with app.app_context():
        db.create_all()

    return app
```

### Models

```python
# app/models.py
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def set_password(self, raw): self.password = generate_password_hash(raw)
    def check_password(self, raw): return check_password_hash(self.password, raw)
    def to_dict(self): return {'id': self.id, 'username': self.username}

class Course(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    level       = db.Column(db.String(40), default='beginner')
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {'id': self.id, 'title': self.title,
                'description': self.description, 'level': self.level}
```

### Auth Routes

```python
# app/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .. import db
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token})
```

### Course CRUD

```python
# app/routes/courses.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Course

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])

@courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    data = request.get_json()
    course = Course(title=data['title'], description=data.get('description', ''),
                    level=data.get('level', 'beginner'),
                    user_id=get_jwt_identity())
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@courses_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    course.title = data.get('title', course.title)
    course.description = data.get('description', course.description)
    db.session.commit()
    return jsonify(course.to_dict())

@courses_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return '', 204
```''',
            'Test all 5 endpoints (register, login, list, create, update) using curl or the Requests library in Python. Include the JWT token in the Authorization header for protected routes.',
            'Which HTTP status code indicates a successfully created resource? A) 200  B) 201  C) 204  D) 400',
            'Add rate limiting to the API using Flask-Limiter: limit /api/auth/login to 5 attempts per minute per IP. Add input validation that returns descriptive 400 errors if required fields are missing. Document the API using Flasgger (Swagger UI).',
            'JWT tokens expire. Set a short expiry (15 minutes) for access tokens and implement a /refresh endpoint using Flask-JWT-Extended\'s refresh tokens. This follows the industry-standard two-token pattern.',
            90)
        if r: created += 1
        else: updated += 1

        # ── GENERATIVE AI (fix order 3) ─────────────────────────────────────
        p = LearningPath.objects.get(slug='generative-ai')

        r = upsert(p, 3, 'Generative AI Project',
            'Build a full-stack AI-powered application using an LLM API with a web interface.',
            '''## Project: AI Homework Helper

Build a web app that helps students with homework using the Claude or OpenAI API.

### Django + AI Integration

```python
# settings.py
ANTHROPIC_API_KEY = 'your-key-here'  # or use env var

# views.py
import anthropic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def ai_homework_help(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject  = data.get('subject', 'general')
        question = data.get('question', '')
        level    = data.get('level', 'high school')

        system_prompt = f"""You are a patient, encouraging tutor helping
{level} students in East Africa. When answering questions:
1. First check if the question is school-appropriate
2. Explain the concept clearly
3. Give a worked example if relevant
4. Ask one follow-up question to check understanding
Keep responses under 300 words."""

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=system_prompt,
            messages=[{"role": "user", "content": f"Subject: {subject}\\nQuestion: {question}"}]
        )

        return JsonResponse({
            'answer': message.content[0].text,
            'tokens_used': message.usage.input_tokens + message.usage.output_tokens
        })
```

### Frontend Chat Interface

```html
<div class="chat-container">
  <div id="chat-messages" class="messages-area"></div>
  <form id="chat-form" class="input-area">
    <select id="subject">
      <option>Mathematics</option>
      <option>Python Programming</option>
      <option>Physics</option>
    </select>
    <textarea id="question" placeholder="Ask your question..."></textarea>
    <button type="submit">Ask AI</button>
  </form>
</div>

<script>
document.getElementById('chat-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const question = document.getElementById('question').value;
  const subject  = document.getElementById('subject').value;

  // Show typing indicator
  appendMessage('user', question);
  appendMessage('ai', '...');

  const resp = await fetch('/ai/homework/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json',
               'X-CSRFToken': getCookie('csrftoken')},
    body: JSON.stringify({ question, subject })
  });
  const data = await resp.json();
  updateLastAIMessage(data.answer);
});

function appendMessage(role, text) {
  const div = document.createElement('div');
  div.className = `message message-${role}`;
  div.textContent = text;
  document.getElementById('chat-messages').appendChild(div);
}
</script>
```

### Conversation History

```python
# Store conversation in session for context
def ai_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        history = request.session.get('chat_history', [])
        history.append({"role": "user", "content": data['message']})

        # Keep last 10 turns to manage token usage
        if len(history) > 20:
            history = history[-20:]

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system="You are a helpful tutor.",
            messages=history
        )
        answer = response.content[0].text
        history.append({"role": "assistant", "content": answer})
        request.session['chat_history'] = history
        return JsonResponse({'answer': answer})
```

### Deliverables
1. Working Django app with AI chat endpoint
2. Subject selector (Math, Python, Science, English)
3. Conversation history (at least 5 turns remembered)
4. Loading spinner while waiting for AI response
5. Character/token usage counter displayed to user''',
            'Test the AI endpoint with 5 different homework questions. Record the response time and token usage. Identify which question type uses the most tokens.',
            'Which API parameter limits the maximum length of an AI response? A) temperature  B) max_tokens  C) top_p  D) stop',
            'Add content safety: before sending to the AI, check if the question contains inappropriate content using a simple keyword filter. Also implement a "report" button that saves flagged AI responses to the database for human review.',
            'Monitor your API costs by tracking token usage per user session. OpenAI and Anthropic both charge per million tokens. claude-haiku is cheapest at ~$0.25 per million input tokens — use it for high-volume features.',
            90)
        if r: created += 1
        else: updated += 1

        # ── MONGODB (fix orders 2-3) ──────────────────────────────────────
        p = LearningPath.objects.get(slug='mongodb')

        r = upsert(p, 2, 'MongoDB Queries and Aggregation',
            'Query MongoDB collections using find, filters, projections, and the aggregation pipeline.',
            '''## Querying MongoDB

### Basic find()

```javascript
// Find all documents
db.students.find()

// Find with filter
db.students.find({ grade: "Form 3" })

// Find one
db.students.findOne({ email: "alice@school.co.ke" })

// Comparison operators
db.students.find({ age: { $gt: 16 } })        // age > 16
db.students.find({ gpa: { $gte: 3.0 } })      // gpa >= 3.0
db.students.find({ score: { $lt: 50 } })      // score < 50
db.students.find({ level: { $in: ["Form 3", "Form 4"] } })
```

### Projections (select fields)

```javascript
// Return only name and email (exclude _id)
db.students.find({}, { name: 1, email: 1, _id: 0 })

// Exclude a field
db.students.find({}, { password: 0 })
```

### Sorting, Limiting, Skipping

```javascript
// Sort by gpa descending
db.students.find().sort({ gpa: -1 })

// Top 5
db.students.find().sort({ gpa: -1 }).limit(5)

// Pagination: page 3, 10 per page
db.students.find().skip(20).limit(10)
```

### Update Operations

```javascript
// Update one field
db.students.updateOne(
  { name: "Alice" },
  { $set: { gpa: 3.8 } }
)

// Increment a counter
db.courses.updateOne(
  { slug: "python-programming" },
  { $inc: { enrollment_count: 1 } }
)

// Add to array
db.students.updateOne(
  { name: "Alice" },
  { $push: { courses: "machine-learning" } }
)

// Update many
db.students.updateMany(
  { grade: "Form 4" },
  { $set: { eligible_for_certificate: true } }
)
```

### Aggregation Pipeline

```javascript
// Average GPA by grade
db.students.aggregate([
  { $group: {
      _id: "$grade",
      avgGPA: { $avg: "$gpa" },
      count:  { $sum: 1 }
  }},
  { $sort: { avgGPA: -1 } }
])

// Students with GPA > 3.0, grouped by course
db.students.aggregate([
  { $match: { gpa: { $gt: 3.0 } } },
  { $unwind: "$courses" },
  { $group: {
      _id: "$courses",
      topStudents: { $push: "$name" },
      count: { $sum: 1 }
  }},
  { $sort: { count: -1 } }
])
```

### Indexes

```javascript
// Create index for fast lookups
db.students.createIndex({ email: 1 }, { unique: true })
db.students.createIndex({ grade: 1, gpa: -1 })

// View indexes
db.students.getIndexes()

// Explain query (check if index is used)
db.students.find({ email: "alice@school.co.ke" }).explain("executionStats")
```''',
            'Write 5 MongoDB queries on a students collection: (1) find all with GPA > 3.5, (2) sort by name, limit 10, (3) update a specific student\'s GPA, (4) count students per grade using aggregation, (5) create an index on email.',
            'Which MongoDB operator appends a value to an array field? A) $set  B) $push  C) $inc  D) $pull',
            'Build a MongoDB-backed enrollment analytics dashboard: import a CSV of 100 student records into MongoDB using mongoimport, then write aggregation pipelines to compute (1) enrollment by course, (2) average GPA per grade, (3) top 10 students overall, and output the results as JSON.',
            'Indexes dramatically speed up read queries but slow down writes. Create indexes only on fields you query frequently. Compound indexes (multiple fields) follow left-prefix rules.',
            60)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'MongoDB Project: Content Management System',
            'Build a document-oriented CMS using MongoDB, PyMongo, and Flask with nested documents and search.',
            '''## Project: Blog CMS with MongoDB

### Document Schema Design

```python
# Unlike SQL, MongoDB allows nested documents
# article document:
{
    "_id": ObjectId("..."),
    "title": "Python for Beginners",
    "slug": "python-for-beginners",
    "author": {
        "name": "Mr. Kariuki",
        "email": "kariuki@academy.co.ke"
    },
    "content": "Full markdown content...",
    "tags": ["python", "beginners", "tutorial"],
    "category": "programming",
    "published": True,
    "created_at": datetime(2024, 6, 1),
    "stats": {
        "views": 1420,
        "likes": 89
    },
    "comments": [
        {
            "author": "Alice",
            "body": "Great tutorial!",
            "created_at": datetime(2024, 6, 2)
        }
    ]
}
```

### Flask + PyMongo Setup

```python
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import json

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['cms']
articles = db['articles']

@app.route('/api/articles')
def list_articles():
    query = {}
    tag = request.args.get('tag')
    if tag:
        query['tags'] = tag
    docs = list(articles.find(
        {**query, 'published': True},
        {'content': 0}
    ).sort('created_at', -1).limit(20))
    return dumps(docs)

@app.route('/api/articles/<slug>')
def get_article(slug):
    doc = articles.find_one_and_update(
        {'slug': slug},
        {'$inc': {'stats.views': 1}},
        return_document=True
    )
    if not doc:
        return jsonify({'error': 'Not found'}), 404
    return dumps(doc)
```

### Full-Text Search

```python
# Create text index
articles.create_index([('title', 'text'), ('content', 'text'), ('tags', 'text')])

@app.route('/api/search')
def search():
    q = request.args.get('q', '')
    results = list(articles.find(
        {'$text': {'$search': q}, 'published': True},
        {'score': {'$meta': 'textScore'}, 'content': 0}
    ).sort([('score', {'$meta': 'textScore'})]).limit(10))
    return dumps(results)
```

### Deliverables
1. CRUD API for articles (create, read, update, delete)
2. Full-text search endpoint
3. Add comment endpoint (append to embedded array)
4. View counter that increments on each read
5. Simple HTML frontend with search bar and article list''',
            'Add a DELETE endpoint for articles that also removes all comments. Test it ensures a 404 is returned for subsequent GET requests to the deleted slug.',
            'In MongoDB, what is the benefit of embedding comments directly inside an article document instead of a separate collection? A) Easier indexing  B) Atomic reads of article + comments in one query  C) Lower storage use  D) Faster writes',
            'Implement pagination using MongoDB cursor methods. The API should accept `page` and `per_page` query parameters and return a JSON response with `items`, `total`, `page`, and `pages` fields. Test with 50 seeded documents.',
            'Embedding vs. referencing: embed when you always read child data with parent (comments on a post). Reference when the child data is large, frequently updated independently, or shared (author profile).',
            90)
        if r: created += 1
        else: updated += 1

        # ── TAILWINDCSS (fix orders 2-3) ───────────────────────────────────
        p = LearningPath.objects.get(slug='tailwindcss')

        r = upsert(p, 2, 'TailwindCSS Layouts and Components',
            'Build responsive layouts and reusable UI components using Tailwind utility classes.',
            '''## Layout with TailwindCSS

### Flexbox Layout

```html
<!-- Navigation -->
<nav class="flex items-center justify-between px-6 py-4 bg-slate-900 text-white">
  <a href="/" class="text-xl font-bold text-emerald-400">CodeSavannah</a>
  <div class="hidden md:flex gap-6">
    <a href="/learn"    class="hover:text-emerald-400 transition-colors">Learn</a>
    <a href="/courses"  class="hover:text-emerald-400 transition-colors">Courses</a>
    <a href="/community" class="hover:text-emerald-400 transition-colors">Community</a>
  </div>
  <a href="/register"
     class="bg-emerald-500 hover:bg-emerald-600 px-4 py-2 rounded-lg font-semibold transition-colors">
    Get Started
  </a>
</nav>
```

### CSS Grid Layout

```html
<!-- 3-column card grid, 1-col on mobile -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
  <div class="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
    <div class="bg-gradient-to-br from-violet-500 to-purple-700 p-6 text-white">
      <span class="text-sm font-semibold uppercase tracking-wide">Programming</span>
      <h3 class="mt-2 text-lg font-bold">Python for Beginners</h3>
    </div>
    <div class="p-5">
      <p class="text-slate-600 text-sm">Master Python from zero to building real apps.</p>
      <div class="flex items-center justify-between mt-4">
        <span class="text-xs bg-emerald-100 text-emerald-700 px-2 py-1 rounded-full">Beginner</span>
        <a href="#"
           class="text-sm font-semibold text-violet-600 hover:underline">Start →</a>
      </div>
    </div>
  </div>
</div>
```

### Responsive Typography

```html
<h1 class="text-3xl md:text-5xl lg:text-6xl font-black text-slate-900 leading-tight">
  Transform Your Future<br>
  <span class="text-emerald-500">Through Code</span>
</h1>
<p class="mt-4 text-lg md:text-xl text-slate-600 max-w-2xl">
  Africa's premier coding academy for the next generation of developers.
</p>
```

### Dark Mode

```html
<!-- Toggle between dark/light with class on <html> -->
<html class="dark">
  <body class="bg-white dark:bg-slate-900 text-slate-900 dark:text-white">
    <div class="bg-slate-100 dark:bg-slate-800 rounded-xl p-6">
      <h2 class="text-slate-900 dark:text-white font-bold">Card Title</h2>
      <p class="text-slate-600 dark:text-slate-400">Body text adapts to theme.</p>
    </div>
  </body>
</html>
```

### Custom Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: ['./templates/**/*.html', './static/js/**/*.js'],
  theme: {
    extend: {
      colors: {
        'savannah': {
          50:  '#f0fdf4',
          500: '#22c55e',
          900: '#14532d',
        }
      },
      fontFamily: {
        'display': ['Inter', 'system-ui', 'sans-serif'],
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ]
}
```''',
            'Build a profile card component: avatar, name, role, stats (followers, courses, projects), and two action buttons. Make it responsive and include a dark mode version.',
            'Which Tailwind prefix applies styles only on medium screens and above? A) sm:  B) md:  C) lg:  D) xl:',
            'Build a complete landing page with TailwindCSS: hero (gradient background, headline, CTA), feature grid (3 columns on desktop), pricing table (3 tiers with highlighted middle), and footer. Use Tailwind\'s dark mode support.',
            'The @tailwindcss/typography plugin provides the "prose" class that styles raw HTML/markdown content beautifully — perfect for blog posts and documentation. Use `prose prose-lg dark:prose-invert` on your content container.',
            60)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'TailwindCSS Project: Admin Dashboard',
            'Build a full admin dashboard UI with TailwindCSS including sidebar, charts, and data tables.',
            '''## Project: Analytics Dashboard

### Dashboard Layout

```html
<div class="flex h-screen bg-slate-100 dark:bg-slate-900">

  <!-- Sidebar -->
  <aside class="w-64 bg-slate-900 text-white flex flex-col">
    <div class="p-6 border-b border-slate-700">
      <h1 class="text-xl font-bold text-emerald-400">CodeSavannah</h1>
      <p class="text-xs text-slate-400 mt-1">Admin Panel</p>
    </div>
    <nav class="flex-1 p-4 space-y-1">
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg
                         bg-emerald-600 text-white">
        <svg class="w-5 h-5"><!-- dashboard icon --></svg>
        Dashboard
      </a>
      <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg
                         text-slate-400 hover:bg-slate-800 hover:text-white transition-colors">
        <svg class="w-5 h-5"><!-- courses icon --></svg>
        Courses
      </a>
    </nav>
    <div class="p-4 border-t border-slate-700">
      <div class="flex items-center gap-3">
        <img src="/avatar.jpg" class="w-8 h-8 rounded-full">
        <div>
          <p class="text-sm font-semibold">Admin</p>
          <p class="text-xs text-slate-400">admin@academy.co.ke</p>
        </div>
      </div>
    </div>
  </aside>

  <!-- Main Content -->
  <main class="flex-1 overflow-y-auto">

    <!-- Top Bar -->
    <header class="bg-white dark:bg-slate-800 shadow-sm px-6 py-4 flex items-center justify-between">
      <h2 class="text-lg font-semibold text-slate-800 dark:text-white">Dashboard</h2>
      <div class="flex items-center gap-4">
        <button class="relative p-2 text-slate-500 hover:text-slate-700">
          <!-- Bell icon + notification dot -->
        </button>
        <img src="/avatar.jpg" class="w-8 h-8 rounded-full cursor-pointer">
      </div>
    </header>

    <!-- Stats Cards -->
    <div class="p-6 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-5 shadow-sm">
        <p class="text-sm text-slate-500">Total Students</p>
        <p class="text-3xl font-black text-slate-900 dark:text-white mt-1">2,847</p>
        <p class="text-sm text-emerald-500 mt-2">+12% this month</p>
      </div>
      <!-- more stat cards -->
    </div>

    <!-- Data Table -->
    <div class="px-6 pb-6">
      <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-700 flex items-center justify-between">
          <h3 class="font-semibold text-slate-800 dark:text-white">Recent Enrollments</h3>
          <button class="text-sm text-emerald-600 hover:underline">View all</button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-50 dark:bg-slate-700/50 text-slate-500 uppercase text-xs">
              <tr>
                <th class="px-6 py-3 text-left">Student</th>
                <th class="px-6 py-3 text-left">Course</th>
                <th class="px-6 py-3 text-left">Date</th>
                <th class="px-6 py-3 text-left">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
              <tr class="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
                <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">Alice Wanjiku</td>
                <td class="px-6 py-4 text-slate-600 dark:text-slate-400">Python Programming</td>
                <td class="px-6 py-4 text-slate-600 dark:text-slate-400">2024-06-01</td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs font-medium">Active</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </main>
</div>
```

### Deliverables
1. Full sidebar + main layout (responsive: sidebar collapses on mobile)
2. 4 stat cards with trend indicators
3. A data table with at least 5 rows
4. Dark mode toggle that persists in localStorage
5. One chart using Chart.js integrated with Tailwind colors''',
            'Make the sidebar collapsible on mobile: add a hamburger button in the top bar that toggles a CSS class to show/hide the sidebar using Tailwind transition utilities.',
            'Which Tailwind class makes an element sticky to the top of its scroll container? A) fixed  B) sticky  C) absolute  D) relative',
            'Add real-time interactivity: use Alpine.js (a lightweight JS framework that works beautifully with Tailwind) to implement: (1) sidebar toggle, (2) dropdown menus, (3) tab switching on the stats area. Alpine uses HTML attributes like x-data, x-show, and @click.',
            'Alpine.js is the perfect companion to Tailwind — it adds reactivity through HTML attributes without a build step. Include it via CDN: `<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>`',
            90)
        if r: created += 1
        else: updated += 1

        # ── NODEJS (fix order 3) ────────────────────────────────────────────
        p = LearningPath.objects.get(slug='nodejs')

        r = upsert(p, 3, 'Node.js Project: Real-Time App',
            'Build a real-time chat or live notification system using Node.js, Express, and Socket.io.',
            '''## Project: Real-Time Chat with Socket.io

### Setup

```bash
mkdir chat-app && cd chat-app
npm init -y
npm install express socket.io
```

### Server

```javascript
// server.js
const express = require('express');
const http    = require('http');
const { Server } = require('socket.io');
const path    = require('path');

const app    = express();
const server = http.createServer(app);
const io     = new Server(server);

app.use(express.static(path.join(__dirname, 'public')));

// Track connected users
const users = {};

io.on('connection', (socket) => {
    console.log('User connected:', socket.id);

    // User joins with username
    socket.on('user:join', (username) => {
        users[socket.id] = username;
        socket.broadcast.emit('user:joined', username);
        io.emit('users:list', Object.values(users));
        console.log(`${username} joined`);
    });

    // Handle chat message
    socket.on('message:send', (data) => {
        const message = {
            id:        Date.now(),
            username:  users[socket.id] || 'Anonymous',
            text:      data.text,
            room:      data.room || 'general',
            timestamp: new Date().toISOString(),
        };
        // Broadcast to all in room
        io.to(message.room).emit('message:received', message);
    });

    // Join a chat room
    socket.on('room:join', (room) => {
        socket.join(room);
        socket.emit('room:joined', room);
    });

    // Typing indicator
    socket.on('typing:start', (room) => {
        socket.to(room).emit('typing:show', users[socket.id]);
    });
    socket.on('typing:stop', (room) => {
        socket.to(room).emit('typing:hide', users[socket.id]);
    });

    socket.on('disconnect', () => {
        const username = users[socket.id];
        delete users[socket.id];
        io.emit('user:left', username);
        io.emit('users:list', Object.values(users));
    });
});

server.listen(3000, () => console.log('Chat server running on port 3000'));
```

### Client

```html
<!-- public/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <title>CodeSavannah Chat</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: sans-serif; margin: 0; display: flex; height: 100vh; }
    .sidebar { width: 220px; background: #1e293b; color: #fff; padding: 16px; }
    .chat    { flex: 1; display: flex; flex-direction: column; }
    .messages { flex: 1; overflow-y: auto; padding: 16px; }
    .message  { margin-bottom: 12px; }
    .message .username { font-weight: 700; color: #6366f1; }
    .input-bar { display: flex; padding: 12px; border-top: 1px solid #e2e8f0; }
    .input-bar input  { flex: 1; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; }
    .input-bar button { margin-left: 8px; background: #6366f1; color: #fff; border: none;
                        padding: 8px 16px; border-radius: 8px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="sidebar">
    <h3>Online Users</h3>
    <ul id="users-list"></ul>
    <h4 style="margin-top:16px;">Rooms</h4>
    <button onclick="joinRoom('general')">General</button>
    <button onclick="joinRoom('python')">Python</button>
  </div>
  <div class="chat">
    <div class="messages" id="messages"></div>
    <div id="typing-indicator" style="padding:4px 16px;font-size:.8rem;color:#94a3b8;height:20px;"></div>
    <div class="input-bar">
      <input id="msg" placeholder="Type a message..." />
      <button onclick="sendMessage()">Send</button>
    </div>
  </div>

  <script src="/socket.io/socket.io.js"></script>
  <script>
    const socket   = io();
    let currentRoom = 'general';

    // Join with username
    const username = prompt('Enter your username:');
    socket.emit('user:join', username);
    socket.emit('room:join', 'general');

    function sendMessage() {
      const text = document.getElementById('msg').value.trim();
      if (!text) return;
      socket.emit('message:send', { text, room: currentRoom });
      document.getElementById('msg').value = '';
      socket.emit('typing:stop', currentRoom);
    }

    function joinRoom(room) {
      currentRoom = room;
      socket.emit('room:join', room);
      document.getElementById('messages').innerHTML = '';
    }

    // Receive messages
    socket.on('message:received', (msg) => {
      const div = document.createElement('div');
      div.className = 'message';
      div.innerHTML = `<span class="username">${msg.username}</span>: ${msg.text}`;
      document.getElementById('messages').appendChild(div);
      div.scrollIntoView();
    });

    socket.on('users:list', (users) => {
      document.getElementById('users-list').innerHTML =
        users.map(u => `<li>${u}</li>`).join('');
    });

    let typingTimer;
    document.getElementById('msg').addEventListener('input', () => {
      socket.emit('typing:start', currentRoom);
      clearTimeout(typingTimer);
      typingTimer = setTimeout(() => socket.emit('typing:stop', currentRoom), 1500);
    });

    socket.on('typing:show', (user) => {
      document.getElementById('typing-indicator').textContent = `${user} is typing...`;
    });
    socket.on('typing:hide', () => {
      document.getElementById('typing-indicator').textContent = '';
    });

    document.getElementById('msg').addEventListener('keydown', e => {
      if (e.key === 'Enter') sendMessage();
    });
  </script>
</body>
</html>
```

### Deliverables
1. Working multi-room chat (at least 3 rooms)
2. Online users sidebar
3. Typing indicators
4. Message history loaded from array on join (last 20 messages)
5. Deployed to Railway or Render''',
            'Add a message history feature: store the last 20 messages per room in a JavaScript array on the server. When a user joins a room, emit the history to them immediately.',
            'What event does a Socket.io client listen for when connected to the server? A) start  B) open  C) connect  D) ready',
            'Upgrade the chat to a live notification system for the academy: broadcast announcements, new course availability, and student milestone notifications (first lesson completed). Use Socket.io namespaces to separate chat from notifications.',
            'Socket.io automatically falls back from WebSockets to long-polling when WebSockets are blocked by a proxy or firewall. This makes it much more reliable than raw WebSocket implementations for real-world deployment.',
            90)
        if r: created += 1
        else: updated += 1

        # ── ETHICAL HACKING (fix order 3) ──────────────────────────────────
        p = LearningPath.objects.get(slug='ethical-hacking')

        r = upsert(p, 3, 'Ethical Hacking Project: Capture the Flag',
            'Practice ethical hacking skills through a structured CTF challenge and write a professional penetration testing report.',
            '''## CTF Challenge & Pen Testing Report

### Setting Up a Safe Lab

```bash
# Install VirtualBox (free) and download:
# - Kali Linux: official attacker VM
# - Metasploitable2: intentionally vulnerable target
# - OWASP WebGoat: web app with built-in vulnerabilities

# Run both VMs on a Host-Only network (no internet access)
```

### Phase 1: Reconnaissance

```bash
# Passive recon — gather info without touching target
whois target.com
nslookup target.com
dig target.com MX

# OSINT — search engine tricks
site:target.com filetype:pdf
"target.com" inurl:admin
"target.com" "index of /"

# Active recon (legal only on systems you own/have permission)
nmap -sV -sC -O 192.168.1.100    # version + OS detection
nmap -p- 192.168.1.100           # all 65535 ports
```

### Phase 2: Vulnerability Scanning

```bash
# Nikto: web server scanner
nikto -h http://192.168.1.100

# Nessus / OpenVAS: comprehensive vuln scanner

# Manual web app testing:
# 1. Enumerate directories
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt

# 2. Test for SQL injection (legal targets only!)
sqlmap -u "http://target.com/item?id=1" --dbs --batch
```

### Phase 3: Exploitation (Authorized Systems Only)

```bash
# Metasploit Framework
msfconsole

# Search for exploits
msf> search vsftpd
msf> use exploit/unix/ftp/vsftpd_234_backdoor
msf> set RHOSTS 192.168.1.100
msf> run

# If successful: get a shell
msf> sessions -i 1
```

### Phase 4: Post-Exploitation & Persistence

```bash
# Once inside (authorized lab only):
whoami; id; hostname       # who are we?
cat /etc/passwd            # enumerate users
find / -perm -4000 2>/dev/null   # SUID binaries (privesc)
ls -la /home               # user directories
```

### Phase 5: The Penetration Testing Report

A professional pentest report includes:

```
EXECUTIVE SUMMARY
  - Tested system: Metasploitable2 lab
  - Date: [Date]
  - Tester: [Name]
  - Overall risk: CRITICAL

FINDINGS TABLE
  | ID | Severity | Title | CVSS | Status |
  |----|----------|-------|------|--------|
  | F1 | Critical | vsFTPd backdoor | 10.0 | Open |
  | F2 | High | Weak SSH credentials | 8.1 | Open |
  | F3 | Medium | Directory listing enabled | 5.3 | Open |

DETAILED FINDINGS
  F1: vsFTPd 2.3.4 Backdoor
  Description: ...
  Steps to reproduce: ...
  Evidence: [screenshot of shell access]
  Recommendation: Update vsFTPd to 3.0.5+
  References: CVE-2011-2523

REMEDIATION PRIORITY
  1. Patch vsFTPd immediately
  2. Change all default credentials
  3. Disable directory listing in web server config
```

### Deliverables
1. Complete recon of Metasploitable2 (nmap, nikto)
2. Identify and exploit at least 2 vulnerabilities
3. Write a professional 3-page pentest report with screenshots
4. Include remediation recommendations for each finding
5. Present findings to a classmate as if they are the client''',
            'Run nmap against Metasploitable2 and list all open ports and running services. For each service, research what vulnerabilities are commonly associated with that service version.',
            'What phase of penetration testing involves gathering information about the target without directly interacting with it? A) Exploitation  B) Post-exploitation  C) Passive reconnaissance  D) Enumeration',
            'BONUS: Set up OWASP WebGoat and complete 5 challenges: SQL Injection, XSS, Broken Authentication, Insecure Direct Object Reference, and CSRF. For each, document the vulnerability, proof of concept, and fix.',
            'Every penetration test MUST have written authorization from the system owner. Unauthorized access is illegal under the Computer Misuse and Cybercrimes Act in Kenya and similar laws globally. Always get a signed scope document first.',
            90)
        if r: created += 1
        else: updated += 1

        # ── HTML (fully placeholder) ─────────────────────────────────────
        p = LearningPath.objects.get(slug='html')

        r = upsert(p, 1, 'HTML Foundations: Structure and Semantics',
            'Write valid semantic HTML5 and understand how browsers interpret the DOM.',
            '''## HTML: The Skeleton of the Web

HTML (HyperText Markup Language) describes the **structure** of a web page. Every website you visit is built with HTML.

### Anatomy of an HTML Element

```html
<p class="intro">Hello, World!</p>
 ^              ^                ^
 opening tag    content          closing tag
     |
     └── attribute: name="value"
```

### A Valid HTML5 Document

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My First Page</title>
  <meta name="description" content="A page about coding in Kenya">
</head>
<body>
  <h1>Welcome to CodeSavannah</h1>
  <p>Africa's premier coding academy.</p>
</body>
</html>
```

### Headings and Text

```html
<h1>Main Page Title (one per page)</h1>
<h2>Section Heading</h2>
<h3>Sub-section</h3>

<p>A paragraph. <strong>Bold text.</strong> <em>Italic text.</em></p>
<p>Visit <a href="https://example.com">this link</a> for more.</p>
<p>Line break here<br>continues on next line.</p>
<hr>  <!-- horizontal rule -->
```

### Lists

```html
<!-- Unordered -->
<ul>
  <li>Python</li>
  <li>JavaScript</li>
  <li>Django</li>
</ul>

<!-- Ordered -->
<ol>
  <li>Install Python</li>
  <li>Write your first script</li>
  <li>Run it!</li>
</ol>

<!-- Description list -->
<dl>
  <dt>HTML</dt><dd>Structure of the page</dd>
  <dt>CSS</dt><dd>Styling and layout</dd>
</dl>
```

### Semantic HTML5 Tags

```html
<header>   <!-- site/section header -->
  <nav>    <!-- navigation links -->
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>  <!-- self-contained content (blog post) -->
    <h2>Learn Python in 30 Days</h2>
    <p>Published by <address>Mr. Kariuki</address></p>
  </article>

  <aside>  <!-- related sidebar content -->
    <h3>Related Courses</h3>
  </aside>
</main>

<footer>
  <p>&copy; 2024 CodeSavannah Academy</p>
</footer>
```

### Images and Links

```html
<!-- Always include alt text for accessibility -->
<img src="students-coding.jpg"
     alt="Students coding at CodeSavannah Academy"
     width="800" height="600"
     loading="lazy">

<!-- Link types -->
<a href="about.html">Relative link</a>
<a href="https://example.com" target="_blank" rel="noopener">External</a>
<a href="mailto:info@academy.co.ke">Email us</a>
<a href="tel:+254700000000">Call us</a>
<a href="#section-2">Jump to section</a>  <!-- anchor link -->
```

### Tables

```html
<table>
  <thead>
    <tr>
      <th scope="col">Course</th>
      <th scope="col">Level</th>
      <th scope="col">Duration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Python Programming</td>
      <td>Beginner</td>
      <td>6 weeks</td>
    </tr>
    <tr>
      <td>Web Development</td>
      <td>Intermediate</td>
      <td>8 weeks</td>
    </tr>
  </tbody>
</table>
```''',
            'Create a personal profile page in HTML: include your name, a photo (can be placeholder), a short bio, an unordered list of 5 programming skills, and a table with 3 courses you\'d like to take. Use semantic elements.',
            'Which HTML5 element should wrap the main navigation links of a website? A) <div class="nav">  B) <nav>  C) <menu>  D) <section>',
            'Build an HTML resume: use semantic elements (header, main, aside, section), headings hierarchy (h1 for name, h2 for sections), a skills table, an ordered list of work experience, and links to a portfolio and LinkedIn. Validate at validator.w3.org.',
            'Use one `<h1>` per page — it defines the main topic for search engines and screen readers. Use `<h2>`-`<h6>` for hierarchy, not for styling (use CSS for font size). This matters for SEO and accessibility.',
            45)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 2, 'HTML Forms and Multimedia',
            'Build accessible HTML forms and embed multimedia content including images, video, and audio.',
            '''## HTML Forms

Forms collect user input and send it to a server.

```html
<form action="/register" method="POST">
  <!-- Text inputs -->
  <label for="name">Full Name</label>
  <input type="text" id="name" name="name"
         placeholder="Alice Wanjiku"
         required minlength="2" maxlength="100">

  <label for="email">Email</label>
  <input type="email" id="email" name="email" required>

  <label for="password">Password</label>
  <input type="password" id="password" name="password"
         required minlength="8">

  <!-- Number -->
  <label for="age">Age</label>
  <input type="number" id="age" name="age" min="13" max="100">

  <!-- Date -->
  <label for="dob">Date of Birth</label>
  <input type="date" id="dob" name="dob">

  <!-- Select dropdown -->
  <label for="level">Level</label>
  <select id="level" name="level" required>
    <option value="">-- Choose your level --</option>
    <option value="beginner">Beginner</option>
    <option value="intermediate">Intermediate</option>
    <option value="advanced">Advanced</option>
  </select>

  <!-- Checkboxes (multiple selection) -->
  <fieldset>
    <legend>Interests</legend>
    <label><input type="checkbox" name="interest" value="python"> Python</label>
    <label><input type="checkbox" name="interest" value="web"> Web Dev</label>
    <label><input type="checkbox" name="interest" value="ai"> AI</label>
  </fieldset>

  <!-- Radio buttons (single selection) -->
  <fieldset>
    <legend>Experience</legend>
    <label><input type="radio" name="exp" value="none" required> No experience</label>
    <label><input type="radio" name="exp" value="some"> Some experience</label>
    <label><input type="radio" name="exp" value="pro"> Professional</label>
  </fieldset>

  <!-- Textarea -->
  <label for="bio">Short Bio</label>
  <textarea id="bio" name="bio" rows="4" maxlength="500"
            placeholder="Tell us about yourself..."></textarea>

  <!-- File upload -->
  <label for="cv">Upload CV</label>
  <input type="file" id="cv" name="cv" accept=".pdf,.doc">

  <!-- Submit -->
  <button type="submit">Register</button>
  <button type="reset">Clear</button>
</form>
```

### Form Validation Attributes

```html
required          <!-- field must be filled -->
minlength="3"     <!-- minimum character count -->
maxlength="50"    <!-- maximum character count -->
min="0"           <!-- minimum number value -->
max="100"         <!-- maximum number value -->
pattern="[A-Za-z]{3,}" <!-- regex pattern -->
type="email"      <!-- must be email format -->
type="url"        <!-- must be URL format -->
```

### Multimedia

```html
<!-- Responsive image with multiple sizes -->
<picture>
  <source srcset="hero-mobile.jpg" media="(max-width: 768px)">
  <source srcset="hero-desktop.jpg" media="(min-width: 769px)">
  <img src="hero-desktop.jpg" alt="Students coding" loading="lazy">
</picture>

<!-- Video -->
<video controls width="640" height="360" poster="thumbnail.jpg">
  <source src="intro.mp4"  type="video/mp4">
  <source src="intro.webm" type="video/webm">
  Your browser doesn't support video. <a href="intro.mp4">Download</a>
</video>

<!-- Audio -->
<audio controls>
  <source src="lecture.mp3" type="audio/mpeg">
  <a href="lecture.mp3">Download audio</a>
</audio>

<!-- Embed YouTube (iframe) -->
<iframe
  src="https://www.youtube.com/embed/dQw4w9WgXcQ"
  title="Intro to Python"
  width="560" height="315"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media"
  allowfullscreen
  loading="lazy">
</iframe>
```''',
            'Build a course registration form with all field types: text (name), email, select (course), radio (level), at least 2 checkboxes (interests), textarea (message), file upload (photo), and a submit button. All fields should have proper labels and validation attributes.',
            'Which HTML attribute makes a form field mandatory before the form can be submitted? A) mandatory  B) required  C) validate  D) nonempty',
            'Build a multi-step form for a coding assessment (3 steps: personal info, course selection, skill assessment). Use JavaScript to show/hide sections. Add a progress indicator at the top showing current step.',
            'Always link `<label>` to its `<input>` using matching `for` and `id` attributes. This increases the click target (clicking the label focuses the input) and is essential for screen reader accessibility.',
            50)
        if r: created += 1
        else: updated += 1

        r = upsert(p, 3, 'HTML Project: Build a Complete Website Structure',
            'Architect a multi-page HTML website using semantic markup, accessibility best practices, and proper metadata.',
            '''## Project: Academy Website in Pure HTML

Build 4 linked HTML pages with proper structure, semantics, and accessibility.

### Page 1: Home (index.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="CodeSavannah Academy — Learn coding in Kenya">
  <meta property="og:title" content="CodeSavannah Academy">
  <meta property="og:description" content="Africa's premier coding academy">
  <meta property="og:image" content="/img/og-image.jpg">
  <title>CodeSavannah Academy | Home</title>
  <link rel="icon" href="/favicon.ico">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a href="#main" class="skip-link">Skip to main content</a>

  <header>
    <nav aria-label="Main navigation">
      <a href="/" class="brand" aria-label="CodeSavannah Academy home">
        CodeSavannah Academy
      </a>
      <ul>
        <li><a href="/courses.html" aria-current="false">Courses</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section aria-labelledby="hero-heading">
      <h1 id="hero-heading">Transform Your Future Through Code</h1>
      <p>Africa's premier coding academy for the next generation.</p>
      <a href="/courses.html" class="cta-btn">Explore Courses</a>
    </section>

    <section aria-labelledby="features-heading">
      <h2 id="features-heading">Why CodeSavannah?</h2>
      <ul class="features-list">
        <li>
          <h3>Structured Learning Paths</h3>
          <p>From beginner to professional with hands-on projects.</p>
        </li>
        <!-- more features -->
      </ul>
    </section>
  </main>

  <footer>
    <p>&copy; <time datetime="2024">2024</time> CodeSavannah Academy</p>
    <nav aria-label="Footer navigation">
      <ul>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
        <li><a href="/privacy.html">Privacy</a></li>
      </ul>
    </nav>
  </footer>
</body>
</html>
```

### Deliverables

1. **Home page** (index.html) — hero, features, course preview
2. **Courses page** (courses.html) — table or list of courses with descriptions
3. **About page** (about.html) — team, mission, values
4. **Contact page** (contact.html) — contact form with all field types

**Accessibility requirements:**
- All images have descriptive alt text
- All form inputs have associated labels
- Color contrast ratio ≥ 4.5:1
- Keyboard navigation works throughout
- Skip-to-main link on every page

**Validation:**
- All 4 pages pass W3C HTML validation (validator.w3.org)
- No errors or warnings''',
            'Validate all 4 pages at validator.w3.org. Take screenshots of the validation results. Fix any errors found and document what you changed.',
            'Which meta tag tells search engines and social media platforms a summary of the page content? A) <meta name="keywords">  B) <meta name="description">  C) <meta charset>  D) <title>',
            'Add structured data (JSON-LD) to the home page to mark up your organization, and to the courses page to mark up each course as a Course schema (schema.org/Course). Test with Google\'s Rich Results Test tool.',
            'The `lang` attribute on `<html>` (e.g., `lang="en"` or `lang="sw"` for Swahili) is used by screen readers to choose the right voice and by translation tools. Always set it correctly.',
            60)
        if r: created += 1
        else: updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Batch 6 complete: {created} created, {updated} updated'
        ))
