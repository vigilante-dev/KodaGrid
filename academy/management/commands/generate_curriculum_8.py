"""
Batch 8: C++, C#, Go, Kotlin, PHP, Ruby, Rust, Swift
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


def three_lesson_path(slug, lang_name, lesson1, lesson2, lesson3):
    """Helper to upsert 3 lessons for a path."""
    p = LearningPath.objects.get(slug=slug)
    results = []
    for order, data in enumerate([lesson1, lesson2, lesson3], start=1):
        r = upsert(p, order, *data)
        results.append(r)
    return results


class Command(BaseCommand):
    help = 'Batch 8: C++, C#, Go, Kotlin, PHP, Ruby, Rust, Swift'

    def handle(self, *args, **options):
        created = updated = 0

        # ── C++ ──────────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='cplusplus')
        for order, (title, obj, content, ex, quiz, proj, notes, mins) in enumerate([
            (
                'C++ Fundamentals',
                'Write, compile, and run C++ programs using variables, control flow, and functions.',
                '''## C++: Power and Performance

C++ extends C with object-oriented features. It powers game engines, operating systems, and high-frequency trading.

### Hello World

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string name = "CodeSavannah";
    cout << "Hello, " << name << "!" << endl;

    // cin for input
    int age;
    cout << "Enter your age: ";
    cin >> age;
    cout << "In 5 years you'll be " << (age + 5) << endl;

    return 0;
}
```

### Variables and Types

```cpp
int    count   = 42;
double price   = 9.99;
char   grade   = 'A';
bool   passed  = true;
string course  = "Python Programming";

// auto (type inference, C++11)
auto level = 3;        // int
auto score = 95.5;     // double

// Constants
const int MAX_STUDENTS = 30;
constexpr double PI = 3.14159;
```

### Control Flow

```cpp
// if-else
int score = 78;
if (score >= 90)      cout << "A";
else if (score >= 80) cout << "B";
else if (score >= 70) cout << "C";
else                  cout << "F";

// Range-based for (C++11)
vector<string> courses = {"Python", "C++", "Django"};
for (const string& c : courses) {
    cout << c << "\\n";
}

// While
int i = 0;
while (i < 5) {
    cout << i++ << " ";
}
```

### Functions

```cpp
#include <vector>
#include <algorithm>

// Pass by value
int square(int x) { return x * x; }

// Pass by reference (modify original)
void doubleValue(int& x) { x *= 2; }

// Pass by const reference (read-only, efficient for large objects)
double average(const vector<int>& nums) {
    if (nums.empty()) return 0.0;
    int sum = 0;
    for (int n : nums) sum += n;
    return static_cast<double>(sum) / nums.size();
}

// Default arguments
void greet(string name, string prefix = "Hello") {
    cout << prefix << ", " << name << "!\\n";
}

int main() {
    int x = 5;
    doubleValue(x);      // x is now 10

    vector<int> scores = {85, 92, 78, 96, 88};
    sort(scores.begin(), scores.end(), greater<int>());
    cout << "Top score: " << scores[0] << "\\n";
    cout << "Average: "   << average(scores) << "\\n";
    return 0;
}
```

### Compilation

```bash
# Compile
g++ -std=c++17 -Wall -o program program.cpp

# Run
./program       # Linux/Mac
program.exe     # Windows

# With optimizations (production)
g++ -std=c++17 -O2 -o program program.cpp
```''',
                'Write a grade calculator in C++: read 5 exam scores, compute average, and output the grade (A/B/C/D/F). Use a function for the grade calculation and pass-by-reference to store the result.',
                'What is the correct way to read a full line (including spaces) from stdin in C++? A) cin >> line  B) getline(cin, line)  C) scanf("%s", line)  D) fgets(line, stdin)',
                'Build a student records system in C++: a struct for Student (name, id, grades array), functions to add/remove/search students stored in a vector, and a main menu loop. Compile and test with 5 sample students.',
                'Always compile with -Wall to see all warnings. Treat warnings as errors during development using -Werror. Uninitialized variables and signed/unsigned comparison warnings catch real bugs.',
                55
            ),
            (
                'C++ OOP: Classes and Inheritance',
                'Design classes with constructors, access modifiers, inheritance, and polymorphism.',
                '''## Object-Oriented C++

### Classes

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

class Student {
private:
    string name;
    int    studentId;
    double gpa;

public:
    // Constructor
    Student(string n, int id, double g = 0.0)
        : name(n), studentId(id), gpa(g) {}

    // Copy constructor
    Student(const Student& other)
        : name(other.name), studentId(other.studentId), gpa(other.gpa) {}

    // Getters
    string getName()    const { return name; }
    int    getId()      const { return studentId; }
    double getGpa()     const { return gpa; }

    // Setters (with validation)
    void setGpa(double g) {
        if (g < 0.0 || g > 4.0)
            throw invalid_argument("GPA must be between 0 and 4");
        gpa = g;
    }

    // Method
    string getGrade() const {
        if (gpa >= 3.7) return "A";
        if (gpa >= 3.0) return "B";
        if (gpa >= 2.0) return "C";
        return "F";
    }

    // Overload << operator for printing
    friend ostream& operator<<(ostream& os, const Student& s) {
        os << s.name << " (ID:" << s.studentId << ", GPA:" << s.gpa << ")";
        return os;
    }
};
```

### Inheritance

```cpp
class Person {
protected:
    string name;
    int    age;
public:
    Person(string n, int a) : name(n), age(a) {}
    virtual void introduce() const {
        cout << "I am " << name << ", age " << age << ".\\n";
    }
    virtual ~Person() = default;  // virtual destructor
};

class Trainer : public Person {
    string specialty;
public:
    Trainer(string n, int a, string spec)
        : Person(n, a), specialty(spec) {}

    void introduce() const override {
        cout << "Trainer " << name << " specialises in " << specialty << ".\\n";
    }
};

// Polymorphism
void printInfo(const Person& p) {
    p.introduce();   // calls correct version
}

int main() {
    Student s("Alice", 101, 3.8);
    Trainer t("Mr. Kariuki", 35, "Python");

    cout << s << "\\n";
    printInfo(t);
    return 0;
}
```

### Smart Pointers (modern C++)

```cpp
#include <memory>

// unique_ptr: single owner (auto-deleted when out of scope)
auto student = make_unique<Student>("Bob", 102, 3.2);
cout << student->getName() << "\\n";
// No manual delete needed!

// shared_ptr: reference counted
auto s1 = make_shared<Student>("Carol", 103);
auto s2 = s1;  // both own it; deleted when both go out of scope
```''',
                'Implement a Shape hierarchy: a base class Shape with a virtual area() method, and derived classes Circle, Rectangle, and Triangle. Store a vector of Shape pointers and print the area of each using polymorphism.',
                'What keyword must be added to a base class function so derived classes can override it with different behavior? A) static  B) virtual  C) override  D) abstract',
                'Build a simple text-based bank account system using C++ classes: Account base class, CheckingAccount and SavingsAccount derived classes. Support deposit, withdraw (with overdraft protection for checking), and monthly interest (for savings). Use smart pointers.',
                'Rule of Three (or Five in modern C++): if you define a destructor, copy constructor, or copy assignment, you probably need all three (or five including move constructor and move assignment). Use the Rule of Zero if possible — rely on RAII types.',
                65
            ),
            (
                'C++ Project: Data Structures',
                'Implement classic data structures in C++ using templates and OOP.',
                '''## Project: Generic Data Structures

### Template Stack

```cpp
#include <iostream>
#include <vector>
#include <stdexcept>

template<typename T>
class Stack {
    vector<T> data;
public:
    void push(const T& value) { data.push_back(value); }

    T pop() {
        if (empty()) throw underflow_error("Stack is empty");
        T top = data.back();
        data.pop_back();
        return top;
    }

    const T& peek() const {
        if (empty()) throw underflow_error("Stack is empty");
        return data.back();
    }

    bool empty() const { return data.empty(); }
    size_t size() const { return data.size(); }
};

// Works with any type
Stack<int> intStack;
intStack.push(1); intStack.push(2); intStack.push(3);
while (!intStack.empty()) cout << intStack.pop() << " ";

Stack<string> strStack;
strStack.push("Python"); strStack.push("C++");
```

### Linked List

```cpp
template<typename T>
class LinkedList {
    struct Node {
        T data;
        Node* next;
        Node(T d) : data(d), next(nullptr) {}
    };
    Node* head = nullptr;
    int   count = 0;

public:
    ~LinkedList() { clear(); }

    void pushFront(const T& val) {
        Node* n = new Node(val);
        n->next = head;
        head = n;
        count++;
    }

    void pushBack(const T& val) {
        Node* n = new Node(val);
        if (!head) { head = n; }
        else {
            Node* cur = head;
            while (cur->next) cur = cur->next;
            cur->next = n;
        }
        count++;
    }

    void print() const {
        for (Node* cur = head; cur; cur = cur->next)
            cout << cur->data << " -> ";
        cout << "null\\n";
    }

    void clear() {
        while (head) {
            Node* next = head->next;
            delete head;
            head = next;
        }
        count = 0;
    }

    int size() const { return count; }
};
```

### Binary Search Tree

```cpp
struct BSTNode {
    int val;
    BSTNode* left  = nullptr;
    BSTNode* right = nullptr;
    BSTNode(int v) : val(v) {}
};

class BST {
    BSTNode* root = nullptr;

    BSTNode* insert(BSTNode* node, int val) {
        if (!node) return new BSTNode(val);
        if (val < node->val) node->left  = insert(node->left,  val);
        else                 node->right = insert(node->right, val);
        return node;
    }

    void inOrder(BSTNode* node) const {
        if (!node) return;
        inOrder(node->left);
        cout << node->val << " ";
        inOrder(node->right);
    }

public:
    void insert(int val)  { root = insert(root, val); }
    void inOrder() const  { inOrder(root); cout << "\\n"; }
};

int main() {
    BST tree;
    for (int v : {5, 3, 7, 1, 4, 6, 8}) tree.insert(v);
    tree.inOrder();  // 1 3 4 5 6 7 8
    return 0;
}
```

### Deliverables
1. Template Stack and Queue working with int and string
2. LinkedList with push, pop, search, and reverse
3. BST with insert, search, delete, and in-order traversal
4. Unit tests using `assert()` for each data structure
5. Time complexity analysis (Big-O) for each operation''',
                'Add a `reverse()` method to the LinkedList that reverses the nodes in place without creating a new list. Test with a list of 5 elements.',
                'What is the time complexity of searching for a value in a balanced Binary Search Tree? A) O(n)  B) O(log n)  C) O(1)  D) O(n log n)',
                'Implement a priority queue (min-heap) using a dynamic array. Support insert(), extractMin(), and peek(). Use it to implement Dijkstra\'s shortest path algorithm on a simple graph with 6 nodes.',
                'The STL (Standard Template Library) provides vector, list, stack, queue, map, set, and more — all optimized and tested. Use STL containers in production. Implement custom data structures only for learning or when performance demands it.',
                90
            ),
        ], start=1):
            r = upsert(p, order, title, obj, content, ex, quiz, proj, notes, mins)
            if r: created += 1
            else: updated += 1

        # ── C# ───────────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='csharp')
        for order, (title, obj, content, ex, quiz, proj, notes, mins) in enumerate([
            (
                'C# and .NET Fundamentals',
                'Write C# programs, understand types, control flow, and LINQ.',
                '''## C#: Microsoft\'s Modern Language

C# powers .NET web apps, Unity games, Windows apps, and cross-platform mobile apps.

### Program Structure

```csharp
using System;
using System.Collections.Generic;

namespace CodeSavannah;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, CodeSavannah!");

        var student = new Student("Alice", 3.8);
        Console.WriteLine(student);
    }
}
```

### Types and Variables

```csharp
// Value types
int    count   = 42;
double price   = 9.99;
bool   active  = true;
char   grade   = 'A';
decimal money  = 1000.50m;

// Reference types
string name    = "Alice";
int[]  scores  = { 85, 92, 78, 96 };
var    courses = new List<string> { "Python", "C#", "Django" };

// Nullable (C# 8+)
string? optionalName = null;
int? age = null;

// var (type inference)
var x = 42;         // int
var y = "hello";    // string
```

### Classes and Records

```csharp
// Regular class
public class Student
{
    public string Name { get; set; }
    public double Gpa  { get; private set; }

    public Student(string name, double gpa)
    {
        Name = name;
        Gpa  = gpa;
    }

    public string Grade => Gpa >= 3.7 ? "A" : Gpa >= 3.0 ? "B" : "C";

    public override string ToString() => $"{Name} (GPA: {Gpa:F1})";
}

// Record (immutable, value semantics, C# 9+)
public record Course(string Title, string Level, string Slug);

// Usage
var c = new Course("Python Programming", "Beginner", "python-programming");
var c2 = c with { Level = "Intermediate" };  // non-destructive copy
```

### LINQ

```csharp
var students = new List<Student>
{
    new("Alice", 3.9), new("Bob", 2.8),
    new("Carol", 3.5), new("Dave", 3.0)
};

// Filter + sort + project
var topStudents = students
    .Where(s => s.Gpa >= 3.0)
    .OrderByDescending(s => s.Gpa)
    .Select(s => new { s.Name, s.Grade })
    .ToList();

foreach (var s in topStudents)
    Console.WriteLine($"{s.Name}: {s.Grade}");

// Aggregate
double avg    = students.Average(s => s.Gpa);
double highest = students.Max(s => s.Gpa);
var    grouped = students.GroupBy(s => s.Grade);
```

### Async/Await

```csharp
using System.Net.Http;
using System.Text.Json;

async Task<List<Course>> FetchCoursesAsync(string query)
{
    using var http = new HttpClient();
    var url = $"https://api.example.com/courses?q={Uri.EscapeDataString(query)}";
    var json = await http.GetStringAsync(url);
    return JsonSerializer.Deserialize<List<Course>>(json)!;
}
```''',
                'Write a C# program that reads a list of 5 student names and GPAs from the console, stores them in a List<Student>, then uses LINQ to output (1) the top 2 by GPA, (2) the average GPA, (3) students with GPA < 3.0.',
                'What C# feature provides a concise way to query, filter, and transform collections? A) foreach  B) delegates  C) LINQ  D) generics',
                'Build a C# console library catalog: a List<Book> where Book is a record. Implement add, search by title/author (LINQ), delete by ISBN, and list by genre. Save to and load from a JSON file using System.Text.Json.',
                'C# records are perfect for DTOs (Data Transfer Objects) — they auto-generate Equals(), GetHashCode(), ToString(), and a with-expression for non-destructive updates. Use records for data that flows between layers.',
                55
            ),
            (
                'ASP.NET Core Web API',
                'Build REST APIs with ASP.NET Core, Entity Framework, and dependency injection.',
                '''## ASP.NET Core REST API

### Create a Project

```bash
dotnet new webapi -n CoursesApi --use-minimal-api
cd CoursesApi && dotnet run
```

### Minimal API (simple, modern)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseSqlite("Data Source=courses.db"));
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();

// GET /api/courses
app.MapGet("/api/courses", async (AppDbContext db, string? q) =>
{
    var courses = db.Courses.AsQueryable();
    if (!string.IsNullOrEmpty(q))
        courses = courses.Where(c => c.Title.Contains(q));
    return await courses.OrderBy(c => c.Title).ToListAsync();
});

// GET /api/courses/{slug}
app.MapGet("/api/courses/{slug}", async (string slug, AppDbContext db) =>
    await db.Courses.FirstOrDefaultAsync(c => c.Slug == slug) is Course course
        ? Results.Ok(course)
        : Results.NotFound());

// POST /api/courses
app.MapPost("/api/courses", async (CourseDto dto, AppDbContext db) =>
{
    var course = new Course { Title = dto.Title, Slug = dto.Slug, Level = dto.Level };
    db.Courses.Add(course);
    await db.SaveChangesAsync();
    return Results.Created($"/api/courses/{course.Slug}", course);
});

app.Run();
```

### Entity Framework Core Models

```csharp
using Microsoft.EntityFrameworkCore;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Course> Courses => Set<Course>();
}

public class Course
{
    public int    Id          { get; set; }
    public string Title       { get; set; } = "";
    public string Slug        { get; set; } = "";
    public string Level       { get; set; } = "beginner";
    public string Description { get; set; } = "";
}

public record CourseDto(string Title, string Slug, string Level, string Description);
```

### Migrations

```bash
dotnet add package Microsoft.EntityFrameworkCore.Sqlite
dotnet add package Microsoft.EntityFrameworkCore.Design

dotnet ef migrations add InitialCreate
dotnet ef database update
```''',
                'Add a PUT /api/courses/{slug} endpoint that updates a course, and a DELETE /api/courses/{slug} endpoint. Test all 5 CRUD endpoints using Swagger UI or curl.',
                'What ASP.NET Core class provides access to the database and tracks entity changes? A) Repository  B) DbContext  C) DataManager  D) UnitOfWork',
                'Add authentication to the API using JWT bearer tokens: implement /api/auth/register and /api/auth/login endpoints, and protect the POST/PUT/DELETE endpoints with [Authorize]. Use Microsoft.AspNetCore.Authentication.JwtBearer.',
                'Entity Framework Core\'s migrations track database schema changes in code. Always create a migration after changing models, and commit migrations to source control so the team can synchronize their databases.',
                65
            ),
            (
                'C# Project: Blazor Web App',
                'Build an interactive web application using Blazor WebAssembly with real-time updates.',
                '''## Project: Course Dashboard with Blazor

Blazor lets you write interactive browser UIs in C# instead of JavaScript.

### Setup

```bash
dotnet new blazorwasm -n CoursesDashboard
cd CoursesDashboard && dotnet run
```

### Component: CourseCard.razor

```razor
@* Components/CourseCard.razor *@
<div class="card">
    <div class="card-header bg-@CategoryColor">
        <span class="badge">@Course.Level</span>
    </div>
    <div class="card-body">
        <h5>@Course.Title</h5>
        <p>@Course.Description</p>
        <button class="btn btn-primary" @onclick="Enroll" disabled="@IsEnrolled">
            @(IsEnrolled ? "Enrolled" : "Enroll")
        </button>
    </div>
</div>

@code {
    [Parameter] public Course Course { get; set; } = default!;
    [Parameter] public EventCallback<Course> OnEnroll { get; set; }
    bool IsEnrolled { get; set; }

    async Task Enroll()
    {
        IsEnrolled = true;
        await OnEnroll.InvokeAsync(Course);
    }

    string CategoryColor => Course.Category switch
    {
        "programming" => "primary",
        "web"         => "success",
        "ai"          => "warning",
        _             => "secondary"
    };
}
```

### Page: Courses.razor

```razor
@page "/courses"
@inject HttpClient Http

<h1>Our Courses</h1>

@if (courses == null)
{
    <p>Loading...</p>
}
else
{
    <input @bind="searchQuery" @oninput="Filter" placeholder="Search..." class="form-control mb-3">

    <div class="row row-cols-1 row-cols-md-3 g-4">
        @foreach (var course in filtered)
        {
            <div class="col">
                <CourseCard Course="@course" OnEnroll="HandleEnroll" />
            </div>
        }
    </div>
}

@code {
    List<Course>? courses;
    List<Course>  filtered = new();
    string searchQuery = "";

    protected override async Task OnInitializedAsync()
    {
        courses  = await Http.GetFromJsonAsync<List<Course>>("api/courses") ?? new();
        filtered = courses;
    }

    void Filter()
    {
        filtered = courses!
            .Where(c => c.Title.Contains(searchQuery, StringComparison.OrdinalIgnoreCase))
            .ToList();
    }

    void HandleEnroll(Course course)
    {
        Console.WriteLine($"Enrolled in {course.Title}");
    }
}
```

### Deliverables
1. Course list with search filter
2. Course detail page with description and lessons
3. Enrollment state tracked in browser
4. Dark/light theme toggle
5. Deployed to GitHub Pages or Azure Static Web Apps''',
                'Add a favorites feature: a star button on each CourseCard that toggles the course into/out of a "My Favorites" list in a shared AppState service. Display the count in the navbar.',
                'In Blazor, which directive enables two-way data binding between a C# property and an HTML input? A) @bind  B) v-model  C) [(ngModel)]  D) data-bind',
                'Add a real-time notification system: use SignalR (ASP.NET\'s WebSocket library) to push live course enrollment counts to all connected Blazor clients. Display a live counter updating without page refresh.',
                'Blazor WebAssembly runs a real .NET runtime in the browser via WebAssembly. The initial download is ~2MB but then fully cached. Use Blazor Server for faster initial loads when network is unreliable.',
                90
            ),
        ], start=1):
            r = upsert(p, order, title, obj, content, ex, quiz, proj, notes, mins)
            if r: created += 1
            else: updated += 1

        # ── GO ───────────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='go')
        for order, (title, obj, content, ex, quiz, proj, notes, mins) in enumerate([
            (
                'Go Fundamentals',
                'Write Go programs using variables, functions, structs, and error handling.',
                '''## Go: Simple and Fast

Go (Golang) is a compiled language from Google used for web services, CLI tools, and cloud infrastructure.

```go
package main

import (
    "fmt"
    "strings"
)

func main() {
    name := "CodeSavannah"  // short variable declaration
    fmt.Printf("Hello, %s!\\n", name)

    greeting := greet(name, "Karibu")
    fmt.Println(greeting)
}

func greet(name, prefix string) string {
    return fmt.Sprintf("%s, %s!", prefix, strings.ToUpper(name))
}
```

### Types and Structs

```go
// Struct
type Student struct {
    Name string
    ID   int
    GPA  float64
}

// Method on struct
func (s Student) Grade() string {
    switch {
    case s.GPA >= 3.7: return "A"
    case s.GPA >= 3.0: return "B"
    default:           return "C"
    }
}

func (s *Student) UpdateGPA(gpa float64) {
    s.GPA = gpa
}

// Slices and maps
courses := []string{"Python", "Go", "Rust"}
registry := map[string]int{"Alice": 101, "Bob": 102}

// Iterate
for i, c := range courses { fmt.Printf("%d: %s\\n", i, c) }
for name, id := range registry { fmt.Printf("%s -> %d\\n", name, id) }
```

### Error Handling

```go
import (
    "errors"
    "fmt"
)

var ErrNotFound = errors.New("student not found")

func findStudent(id int, students []Student) (Student, error) {
    for _, s := range students {
        if s.ID == id {
            return s, nil
        }
    }
    return Student{}, fmt.Errorf("findStudent: id %d: %w", id, ErrNotFound)
}

// Caller always checks error
s, err := findStudent(999, students)
if err != nil {
    if errors.Is(err, ErrNotFound) {
        fmt.Println("Student does not exist")
    }
    return
}
fmt.Println(s.Name)
```

### Goroutines and Channels

```go
import (
    "fmt"
    "sync"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    fmt.Printf("Worker %d running\\n", id)
}

func main() {
    var wg sync.WaitGroup
    for i := 1; i <= 5; i++ {
        wg.Add(1)
        go worker(i, &wg)  // spawn goroutine
    }
    wg.Wait()
    fmt.Println("All workers done")
}
```''',
                'Write a Go program that reads student records from a CSV string (parse manually), stores them in a slice of Student structs, and outputs the top 3 by GPA and the class average.',
                'In Go, what is the conventional way to return an error from a function? A) throw exception  B) panic()  C) return (result, error)  D) fmt.Errorf() only',
                'Build a Go CLI tool using the cobra library: commands add, list, and complete for a to-do list. Persist data to a JSON file. Handle errors gracefully with descriptive messages.',
                'Go has no exceptions — errors are values returned explicitly. This makes error handling visible at every call site. The pattern `if err != nil { return ..., err }` is idiomatic Go and encourages thinking about failure paths.',
                55
            ),
            (
                'Go Web Services with net/http',
                'Build HTTP servers and REST APIs using Go\'s standard library and popular routers.',
                '''## Building HTTP Servers in Go

### Basic HTTP Server

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type Course struct {
    ID    int    `json:"id"`
    Title string `json:"title"`
    Level string `json:"level"`
}

var courses = []Course{
    {1, "Python Programming", "beginner"},
    {2, "Web Development",    "intermediate"},
}

func coursesHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(courses)
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /api/courses", coursesHandler)
    mux.HandleFunc("POST /api/courses", createCourse)

    log.Println("Listening on :8080")
    log.Fatal(http.ListenAndServe(":8080", mux))
}
```

### REST API with Chi Router

```go
import "github.com/go-chi/chi/v5"

r := chi.NewRouter()
r.Use(middleware.Logger)
r.Use(middleware.Recoverer)

r.Get("/api/courses",         listCourses)
r.Post("/api/courses",        createCourse)
r.Get("/api/courses/{slug}",  getCourse)
r.Put("/api/courses/{slug}",  updateCourse)
r.Delete("/api/courses/{slug}", deleteCourse)

func getCourse(w http.ResponseWriter, r *http.Request) {
    slug := chi.URLParam(r, "slug")
    for _, c := range courses {
        if c.Slug == slug {
            json.NewEncoder(w).Encode(c)
            return
        }
    }
    http.Error(w, "Not found", http.StatusNotFound)
}
```

### Database with sqlc + PostgreSQL

```go
// Generated type-safe SQL queries with sqlc
// queries.sql:
// -- name: GetCourse :one
// SELECT * FROM courses WHERE slug = $1;

// Generated Go code
course, err := db.GetCourse(ctx, slug)
```

### Concurrency Pattern: Worker Pool

```go
func processEnrollments(jobs []Enrollment) {
    jobChan    := make(chan Enrollment, len(jobs))
    resultChan := make(chan Result, len(jobs))

    // Start 5 workers
    for i := 0; i < 5; i++ {
        go func() {
            for job := range jobChan {
                result := processEnrollment(job)
                resultChan <- result
            }
        }()
    }

    // Send jobs
    for _, j := range jobs { jobChan <- j }
    close(jobChan)

    // Collect results
    for range jobs {
        r := <-resultChan
        log.Printf("Processed: %v", r)
    }
}
```''',
                'Build a Go REST API for a bookmarks service: GET /bookmarks, POST /bookmarks (create), DELETE /bookmarks/{id}. Store data in memory. Test with curl.',
                'What Go package provides the default HTTP multiplexer and request/response types? A) net/tcp  B) http/server  C) net/http  D) io/http',
                'Build a URL shortener service in Go: POST /shorten accepts a long URL and returns a short code, GET /:code redirects to the original URL. Track click counts. Use a PostgreSQL database with the pgx driver.',
                'Go\'s http.Server is production-ready out of the box. Set timeouts to prevent slow-loris attacks: ReadTimeout, WriteTimeout, and IdleTimeout. Deploy behind Nginx or Caddy for TLS termination.',
                60
            ),
            (
                'Go Project: Microservice',
                'Build and containerize a Go microservice with REST API, PostgreSQL, and Docker.',
                '''## Project: Course Enrollment Microservice

### Project Structure

```
enrollment-service/
├── cmd/server/main.go
├── internal/
│   ├── handler/  ← HTTP handlers
│   ├── service/  ← business logic
│   └── repo/     ← database layer
├── Dockerfile
└── docker-compose.yml
```

### Dockerfile

```dockerfile
# Multi-stage build
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o server ./cmd/server

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/server .
EXPOSE 8080
CMD ["./server"]
```

### docker-compose.yml

```yaml
version: "3.9"
services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgres://postgres:password@db:5432/enrollments
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB:       enrollments
      POSTGRES_USER:     postgres
      POSTGRES_PASSWORD: password
    volumes:
      - pg-data:/var/lib/postgresql/data

volumes:
  pg-data:
```

### Health Check and Middleware

```go
func main() {
    r := chi.NewRouter()

    // Middleware
    r.Use(middleware.RequestID)
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.Timeout(30 * time.Second))

    // Health check
    r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
        json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
    })

    r.Route("/api/enrollments", func(r chi.Router) {
        r.Get("/",          h.List)
        r.Post("/",         h.Create)
        r.Get("/{id}",      h.Get)
        r.Delete("/{id}",   h.Delete)
    })

    http.ListenAndServe(":8080", r)
}
```

### Deliverables
1. Full enrollment CRUD API with PostgreSQL
2. Input validation and descriptive error responses
3. Dockerized with docker-compose
4. Unit tests for service layer (go test ./...)
5. README with curl examples for every endpoint''',
                'Write a unit test for the enrollment service layer using Go\'s testing package. Mock the repository interface so no database is needed. Test happy path and error cases.',
                'What command runs all tests in a Go project? A) go check  B) go test ./...  C) go run test  D) go validate',
                'Add observability: instrument the service with Prometheus metrics (request count, latency histogram). Expose /metrics endpoint. Create a Grafana dashboard showing RPS, P99 latency, and error rate.',
                'Go binaries are statically linked by default — the Docker image only needs a minimal base like `scratch` or `alpine`. The multi-stage Dockerfile builds in the full Go image but ships only the ~10MB binary.',
                90
            ),
        ], start=1):
            r = upsert(p, order, title, obj, content, ex, quiz, proj, notes, mins)
            if r: created += 1
            else: updated += 1

        # ── KOTLIN ───────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='kotlin')
        for order, (title, obj, content, ex, quiz, proj, notes, mins) in enumerate([
            (
                'Kotlin Fundamentals',
                'Write Kotlin programs using null safety, data classes, lambdas, and extension functions.',
                '''## Kotlin: Modern JVM Language

Kotlin is Google\'s preferred language for Android. It is also used for server-side development with Ktor or Spring.

```kotlin
fun main() {
    val name = "CodeSavannah"   // immutable (val)
    var count = 0                // mutable (var)

    println("Hello, $name!")
    println("${name.length} characters")

    // Null safety
    val email: String? = null
    println(email?.uppercase() ?: "No email")
}
```

### Data Classes and When

```kotlin
data class Student(
    val name: String,
    val id: Int,
    val gpa: Double = 0.0
)

fun grade(gpa: Double) = when {
    gpa >= 3.7 -> "A"
    gpa >= 3.0 -> "B"
    gpa >= 2.0 -> "C"
    else       -> "F"
}

fun main() {
    val s = Student("Alice", 101, 3.8)
    val s2 = s.copy(gpa = 3.9)  // copy with changes
    println("${s.name}: ${grade(s.gpa)}")

    // Destructuring
    val (name, id, gpa) = s
    println("Name=$name, ID=$id")
}
```

### Collections and Lambdas

```kotlin
val students = listOf(
    Student("Alice", 1, 3.9),
    Student("Bob",   2, 2.7),
    Student("Carol", 3, 3.5)
)

// Functional operations
val top = students
    .filter { it.gpa >= 3.0 }
    .sortedByDescending { it.gpa }
    .map { "${it.name}: ${grade(it.gpa)}" }

top.forEach { println(it) }

val avg = students.averageBy { it.gpa }
```

### Extension Functions

```kotlin
fun String.toSlug() = this
    .lowercase()
    .replace(Regex("[^a-z0-9\\\\s-]"), "")
    .replace(Regex("\\\\s+"), "-")
    .trim('-')

fun Double.toGrade() = when {
    this >= 3.7 -> "A"
    this >= 3.0 -> "B"
    else        -> "C"
}

println("Python Programming".toSlug())   // python-programming
println(3.8.toGrade())                   // A
```

### Coroutines (async)

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

suspend fun fetchCourses(): List<String> {
    delay(100)  // simulates network call
    return listOf("Python", "Kotlin", "Android")
}

fun main() = runBlocking {
    val courses = fetchCourses()
    courses.forEach { println(it) }

    // Concurrent
    val (c1, c2) = awaitAll(
        async { fetchCourses() },
        async { fetchCourses() }
    )
}
```''',
                'Refactor a Java class to Kotlin: a Student class with name, GPA, and a method to compute the grade. Use a data class, when expression, and null-safe operators.',
                'In Kotlin, which keyword declares an immutable (read-only) variable? A) var  B) let  C) val  D) const',
                'Build a Kotlin command-line grade book: read student records from a CSV file, use data classes, filter/sort/group with Kotlin collection operators, and output a summary report to a new CSV file.',
                'Kotlin data classes auto-generate equals(), hashCode(), toString(), copy(), and componentN() functions. Use them for DTOs, API response models, and database entities. They remove significant boilerplate versus Java.',
                50
            ),
            (
                'Android Development with Kotlin',
                'Build Android apps using Jetpack Compose and modern Android architecture.',
                '''## Android with Jetpack Compose

### Composable Functions

```kotlin
import androidx.compose.material3.*
import androidx.compose.runtime.*

@Composable
fun CourseCard(course: Course, onEnroll: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        elevation = CardDefaults.cardElevation(4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = course.title,
                style = MaterialTheme.typography.headlineSmall
            )
            Text(
                text = course.level,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.secondary
            )
            Spacer(modifier = Modifier.height(12.dp))
            Button(onClick = onEnroll) {
                Text("Enroll Now")
            }
        }
    }
}

@Composable
fun CoursesScreen(viewModel: CoursesViewModel = viewModel()) {
    val courses by viewModel.courses.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    if (isLoading) {
        CircularProgressIndicator(modifier = Modifier.fillMaxSize().wrapContentSize())
    } else {
        LazyColumn {
            items(courses) { course ->
                CourseCard(course = course, onEnroll = { viewModel.enroll(course) })
            }
        }
    }
}
```

### ViewModel + StateFlow

```kotlin
class CoursesViewModel : ViewModel() {
    private val _courses = MutableStateFlow<List<Course>>(emptyList())
    val courses = _courses.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    init { loadCourses() }

    private fun loadCourses() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                _courses.value = repository.getCourses()
            } finally {
                _isLoading.value = false
            }
        }
    }
}
```

### Navigation

```kotlin
NavHost(navController, startDestination = "courses") {
    composable("courses") {
        CoursesScreen(onCourseClick = { slug ->
            navController.navigate("courses/$slug")
        })
    }
    composable("courses/{slug}") { backStackEntry ->
        val slug = backStackEntry.arguments?.getString("slug") ?: return@composable
        CourseDetailScreen(slug = slug)
    }
}
```''',
                'Create a simple Android app with Compose: a screen showing a hardcoded list of courses in a LazyColumn, each with a title, level, and an "Enroll" button that shows a Snackbar confirmation.',
                'In Jetpack Compose, which component efficiently renders a large list of items by only composing visible items? A) Column  B) RecyclerView  C) LazyColumn  D) ScrollView',
                'Build a complete Android course tracker app: browse courses fetched from an API (Retrofit), enroll in courses, and view enrolled courses in a "My Courses" tab. Persist enrollments with Room database. Implement proper ViewModel + Repository architecture.',
                'Prefer StateFlow over LiveData in new Android projects — it is Kotlin-native, works with coroutines, and supports composition. Use collectAsState() in Compose to subscribe to it.',
                70
            ),
            (
                'Kotlin Project: Ktor REST API',
                'Build a server-side REST API using Ktor, Exposed ORM, and PostgreSQL.',
                '''## Project: REST API with Ktor

### Setup

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "2.0.0"
    id("io.ktor.plugin") version "2.3.11"
    kotlin("plugin.serialization") version "2.0.0"
}

dependencies {
    implementation("io.ktor:ktor-server-netty:2.3.11")
    implementation("io.ktor:ktor-server-content-negotiation:2.3.11")
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.11")
    implementation("org.jetbrains.exposed:exposed-core:0.51.0")
    implementation("org.jetbrains.exposed:exposed-dao:0.51.0")
    implementation("org.jetbrains.exposed:exposed-jdbc:0.51.0")
    implementation("org.postgresql:postgresql:42.7.3")
}
```

### Application

```kotlin
// Application.kt
fun main() {
    embeddedServer(Netty, port = 8080) {
        install(ContentNegotiation) { json() }
        install(StatusPages) {
            exception<NotFoundException> { call, _ ->
                call.respond(HttpStatusCode.NotFound)
            }
        }
        Database.connect(
            url = System.getenv("DATABASE_URL") ?: "jdbc:postgresql://localhost/courses",
            driver = "org.postgresql.Driver"
        )
        transaction { SchemaUtils.create(CoursesTable) }
        routing {
            route("/api/courses") {
                get    { call.respond(CourseService.all())  }
                post   {
                    val dto = call.receive<CourseDto>()
                    call.respond(HttpStatusCode.Created, CourseService.create(dto))
                }
                get("/{slug}") {
                    val slug = call.parameters["slug"]!!
                    call.respond(CourseService.bySlug(slug) ?: throw NotFoundException())
                }
            }
        }
    }.start(wait = true)
}
```

### Exposed ORM

```kotlin
object CoursesTable : IntIdTable("courses") {
    val title = varchar("title", 180)
    val slug  = varchar("slug", 200).uniqueIndex()
    val level = varchar("level", 30).default("beginner")
}

class CourseEntity(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<CourseEntity>(CoursesTable)
    var title by CoursesTable.title
    var slug  by CoursesTable.slug
    var level by CoursesTable.level

    fun toDto() = CourseDto(id.value, title, slug, level)
}

object CourseService {
    fun all() = transaction { CourseEntity.all().map { it.toDto() } }

    fun bySlug(slug: String) = transaction {
        CourseEntity.find { CoursesTable.slug eq slug }.firstOrNull()?.toDto()
    }
    fun create(dto: CreateCourseDto) = transaction {
        CourseEntity.new {
            title = dto.title
            slug  = dto.slug
            level = dto.level
        }.toDto()
    }
}
```

### Deliverables
1. Full CRUD API with Ktor + Exposed + PostgreSQL
2. JWT authentication using `io.ktor:ktor-server-auth-jwt`
3. Request validation with `kotlinx.serialization`
4. Unit tests using `ktor-server-test-host`
5. Dockerfile and deploy to Railway or Render''',
                'Write integration tests for the GET /api/courses and POST /api/courses endpoints using Ktor\'s testApplication {} DSL. Assert status codes and response bodies.',
                'What Ktor plugin handles automatic JSON serialization and deserialization of request/response bodies? A) Authentication  B) ContentNegotiation  C) StatusPages  D) Sessions',
                'Add pagination to the GET /api/courses endpoint: accept ?page=1&per_page=10 query parameters and return a JSON object with items, total, page, and pages fields. Test with 50 seeded courses.',
                'Exposed supports two APIs: DSL (SQL-like queries) and DAO (object-mapping). Use DSL for complex queries and reporting; use DAO for simple CRUD. Mixing both in one project is common and fine.',
                85
            ),
        ], start=1):
            r = upsert(p, order, title, obj, content, ex, quiz, proj, notes, mins)
            if r: created += 1
            else: updated += 1

        # ── PHP ──────────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='php')
        for order, (title, obj, content, ex, quiz, proj, notes, mins) in enumerate([
            (
                'PHP Fundamentals',
                'Write PHP scripts, work with arrays, forms, and MySQL using PDO.',
                '''## PHP: Server-Side Web Scripting

PHP powers WordPress, Laravel, and millions of websites. It runs on Apache/Nginx servers.

### Syntax Basics

```php
<?php
$name = "CodeSavannah";
$count = 42;
$price = 9.99;
$active = true;

echo "Hello, $name!\\n";
echo "Count: {$count}\\n";

// Arrays
$courses = ["Python", "PHP", "JavaScript"];
$student = ["name" => "Alice", "gpa" => 3.8, "grade" => "Form 4"];

echo $courses[0] . "\\n";           // Python
echo $student["name"] . "\\n";      // Alice

// Loops
foreach ($courses as $i => $course) {
    echo "$i: $course\\n";
}

foreach ($student as $key => $value) {
    echo "$key = $value\\n";
}
```

### Functions

```php
function gradeFromGpa(float $gpa): string {
    return match(true) {
        $gpa >= 3.7 => "A",
        $gpa >= 3.0 => "B",
        $gpa >= 2.0 => "C",
        default     => "F",
    };
}

// Named arguments (PHP 8)
function createStudent(string $name, int $id, float $gpa = 0.0): array {
    return compact("name", "id", "gpa");
}

$s = createStudent(name: "Alice", id: 101, gpa: 3.8);
echo gradeFromGpa($s["gpa"]);
```

### Database with PDO

```php
$dsn = "mysql:host=localhost;dbname=academy;charset=utf8mb4";
$pdo = new PDO($dsn, "root", "password", [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);

// SELECT
$stmt = $pdo->prepare("SELECT * FROM courses WHERE level = :level ORDER BY title");
$stmt->execute([":level" => "beginner"]);
$courses = $stmt->fetchAll();

// INSERT
$stmt = $pdo->prepare("INSERT INTO courses (title, slug, level) VALUES (:title, :slug, :level)");
$stmt->execute([
    ":title" => "Django Web Framework",
    ":slug"  => "django",
    ":level" => "intermediate"
]);
$id = $pdo->lastInsertId();
```

### Handling Forms Securely

```php
// POST form
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name  = trim(htmlspecialchars($_POST["name"] ?? ""));
    $email = filter_input(INPUT_POST, "email", FILTER_VALIDATE_EMAIL);

    if (!$email) {
        $error = "Invalid email address.";
    } else {
        // Save to database with prepared statement (prevents SQL injection)
        $stmt = $pdo->prepare("INSERT INTO registrations (name, email) VALUES (?, ?)");
        $stmt->execute([$name, $email]);
        $success = "Registration complete!";
    }
}
?>

<form method="POST">
  <input name="name"  value="<?= htmlspecialchars($name ?? "") ?>">
  <input name="email" type="email">
  <button>Register</button>
</form>
```''',
                'Build a PHP contact form that validates name (required, min 2 chars), email (valid format), and message (required). On success, use PDO to save the submission to a contacts table. Show inline error messages without refreshing the page.',
                'Which PHP function prevents Cross-Site Scripting (XSS) by converting HTML special characters to entities? A) strip_tags()  B) htmlspecialchars()  C) addslashes()  D) sanitize()',
                'Build a PHP student grade tracker: a MySQL database with students and grades tables, CRUD forms for students, and a page showing each student\'s average grade. Use PDO prepared statements throughout. Include a session-based login for admin access.',
                'Always use PDO prepared statements — never concatenate user input into SQL strings. `$pdo->query("SELECT * FROM users WHERE id=" . $_GET["id"])` is vulnerable to SQL injection. Use `:named` or `?` placeholders instead.',
                55
            ),
            (
                'Laravel Framework',
                'Build web applications with Laravel\'s MVC architecture, Eloquent ORM, and Blade templates.',
                '''## Laravel: The PHP Framework

### Create a Project

```bash
composer create-project laravel/laravel academy
cd academy && php artisan serve
```

### Routing

```php
// routes/web.php
use App\\Http\\Controllers\\CourseController;

Route::get('/',          fn() => view('home'));
Route::resource('courses', CourseController::class);
// Creates: index, create, store, show, edit, update, destroy
```

### Controller

```bash
php artisan make:controller CourseController --resource
```

```php
// app/Http/Controllers/CourseController.php
class CourseController extends Controller
{
    public function index()
    {
        $courses = Course::withCount('lessons')
            ->orderBy('title')
            ->paginate(12);
        return view('courses.index', compact('courses'));
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'title' => 'required|min:3|max:180',
            'level' => 'required|in:beginner,intermediate,advanced',
            'description' => 'required|min:20',
        ]);
        $data['slug'] = Str::slug($data['title']);
        Course::create($data);
        return redirect()->route('courses.index')->with('success', 'Course created!');
    }
}
```

### Eloquent ORM

```php
// app/Models/Course.php
class Course extends Model
{
    protected $fillable = ['title', 'slug', 'level', 'description'];

    public function lessons()
    {
        return $this->hasMany(Lesson::class);
    }

    public function students()
    {
        return $this->belongsToMany(User::class, 'enrollments');
    }
}

// Queries
$courses     = Course::all();
$beginner    = Course::where('level', 'beginner')->get();
$withLessons = Course::with('lessons')->get();
$popular     = Course::withCount('students')->orderByDesc('students_count')->take(5)->get();
```

### Blade Templates

```blade
{{-- resources/views/courses/index.blade.php --}}
@extends('layouts.app')

@section('content')
<div class="container py-8">
    <h1>Courses</h1>
    <div class="grid grid-cols-3 gap-6">
        @foreach($courses as $course)
        <x-course-card :course="$course" />
        @endforeach
    </div>
    {{ $courses->links() }}
</div>
@endsection
```''',
                'Create a Laravel migration and model for a Lesson table (title, content, order, course_id). Seed 3 courses with 3 lessons each using DatabaseSeeder. Verify with php artisan tinker.',
                'Which Artisan command creates a new database migration file? A) php artisan db:migrate  B) php artisan make:migration  C) php artisan schema:create  D) php artisan db:seed',
                'Build a full Laravel blog: authentication (php artisan make:auth), posts with CRUD (title, body, category, published_at), comments (user + body), tags (many-to-many), and an RSS feed at /feed. Deploy to a free Laravel hosting service.',
                'Laravel\'s N+1 query problem: `$courses = Course::all(); foreach($courses as $c) echo $c->lessons->count()` fires one extra query per course. Fix with eager loading: `Course::with("lessons")->get()`.',
                65
            ),
            (
                'PHP Project: E-Commerce Cart',
                'Build a complete shopping cart system using PHP, MySQL, and sessions.',
                '''## Project: Course Marketplace

### Database Schema

```sql
CREATE TABLE courses (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(180) NOT NULL,
    slug        VARCHAR(200) UNIQUE NOT NULL,
    description TEXT,
    price       DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    level       ENUM("beginner","intermediate","advanced") DEFAULT "beginner",
    image       VARCHAR(255),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT,
    total      DECIMAL(10,2),
    status     ENUM("pending","paid","cancelled") DEFAULT "pending",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    order_id   INT REFERENCES orders(id),
    course_id  INT REFERENCES courses(id),
    price      DECIMAL(8,2),
    UNIQUE KEY (order_id, course_id)
);
```

### Cart Class

```php
class Cart {
    private PDO $db;

    public function __construct(PDO $db) {
        $this->db = $db;
        if (!isset($_SESSION["cart"])) {
            $_SESSION["cart"] = [];
        }
    }

    public function add(int $courseId): void {
        $_SESSION["cart"][$courseId] = true;
    }

    public function remove(int $courseId): void {
        unset($_SESSION["cart"][$courseId]);
    }

    public function items(): array {
        if (empty($_SESSION["cart"])) return [];
        $ids = implode(",", array_map("intval", array_keys($_SESSION["cart"])));
        $stmt = $this->db->query("SELECT * FROM courses WHERE id IN ($ids)");
        return $stmt->fetchAll();
    }

    public function total(): float {
        return array_sum(array_column($this->items(), "price"));
    }

    public function checkout(int $userId): int {
        $items = $this->items();
        if (empty($items)) throw new \\Exception("Cart is empty");

        $this->db->beginTransaction();
        try {
            $stmt = $this->db->prepare(
                "INSERT INTO orders (user_id, total, status) VALUES (?, ?, "pending")"
            );
            $stmt->execute([$userId, $this->total()]);
            $orderId = $this->db->lastInsertId();

            $stmt = $this->db->prepare(
                "INSERT INTO order_items (order_id, course_id, price) VALUES (?, ?, ?)"
            );
            foreach ($items as $item) {
                $stmt->execute([$orderId, $item["id"], $item["price"]]);
            }

            $this->db->commit();
            $_SESSION["cart"] = [];
            return $orderId;
        } catch (\\Throwable $e) {
            $this->db->rollBack();
            throw $e;
        }
    }
}
```

### Deliverables
1. Course catalog with add-to-cart buttons
2. Cart page (view, remove items, total)
3. Checkout that saves an order and clears the cart
4. Order history page for logged-in users
5. Basic Stripe integration for test payments''',
                'Implement a coupon code system: a coupons table with code, discount_percent, and expires_at. On the cart page, let users enter a code that reduces the total. Validate the code and expiry before applying.',
                'What PHP function starts or resumes a user session, enabling the $_SESSION superglobal? A) session_create()  B) session_start()  C) session_init()  D) session_open()',
                'Add email notifications using PHPMailer: send a confirmation email to the user on checkout with the order summary. Use Mailtrap for development to avoid sending real emails. Format the email as HTML.',
                'Always wrap related database operations in a transaction. If any step fails, rollBack() ensures no partial data is saved. This is critical for order checkout — a partial order is worse than no order.',
                90
            ),
        ], start=1):
            r = upsert(p, order, title, obj, content, ex, quiz, proj, notes, mins)
            if r: created += 1
            else: updated += 1

        # ── RUBY ─────────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='ruby')
        for order, (title, obj, content, ex, quiz, proj, notes, mins) in enumerate([
            (
                'Ruby Fundamentals',
                'Write Ruby programs using blocks, iterators, and object-oriented features.',
                '''## Ruby: Designed for Developer Happiness

Ruby\'s expressive syntax powers GitHub, Shopify, and Twitter (early days).

```ruby
# Variables and output
name    = "CodeSavannah"
count   = 42
price   = 9.99
active  = true
nothing = nil

puts "Hello, #{name}!"
puts "Count: #{count}"

# Symbols (lightweight strings, used as keys)
:beginner  :intermediate  :advanced
```

### Arrays and Hashes

```ruby
courses = ["Python", "Ruby", "Django"]
courses.push("React")
courses.unshift("HTML")         # add to front
courses.delete("React")

student = {
  name:  "Alice",
  gpa:   3.8,
  grade: "Form 4"
}
puts student[:name]   # Alice

# Iterators
courses.each { |c| puts c }
courses.map  { |c| c.upcase }
courses.select { |c| c.length > 4 }
courses.reject { |c| c.include?("a") }
```

### Classes

```ruby
class Student
  attr_accessor :name, :gpa
  attr_reader   :id

  def initialize(name, id, gpa: 0.0)
    @name = name
    @id   = id
    @gpa  = gpa
  end

  def grade
    case @gpa
    when 3.7..4.0 then "A"
    when 3.0..3.69 then "B"
    when 2.0..2.99 then "C"
    else "F"
    end
  end

  def to_s
    "#{@name} (GPA: #{@gpa}, Grade: #{grade})"
  end
end

s = Student.new("Alice", 101, gpa: 3.8)
puts s       # Alice (GPA: 3.8, Grade: A)
s.gpa = 3.9  # attr_accessor generates setter
```

### Blocks and Iterators

```ruby
# Blocks = anonymous functions
[1, 2, 3].each { |n| print "#{n} " }

[1,2,3,4,5].each_with_object([]) do |n, acc|
  acc << n * n if n.odd?
end
# => [1, 9, 25]

# Custom iterator
def repeat(n)
  n.times { |i| yield i }
end

repeat(3) { |i| puts "Iteration #{i}" }
```''',
                'Write a Ruby program that reads an array of student hashes, uses Ruby iterators (map, select, sort_by) to find the top 3 by GPA, compute the class average, and output a formatted report.',
                'In Ruby, which method returns a new array with only elements for which the block returns true? A) map  B) each  C) select  D) collect',
                'Build a Ruby CLI address book: classes for Contact and AddressBook, save/load to JSON file, and a simple REPL (read-eval-print loop) that supports add, search, list, and delete commands.',
                'Ruby\'s `symbol:value` hash syntax (`:key => value`) can be shortened to `key: value` when keys are symbols. This is the modern preferred style and matches JavaScript object notation.',
                50
            ),
            (
                'Ruby on Rails Basics',
                'Build a Rails app with MVC architecture, Active Record, and routes.',
                '''## Ruby on Rails: Convention over Configuration

### Create a Rails App

```bash
gem install rails
rails new academy --css tailwind --database postgresql
cd academy && bin/dev
```

### Generate a Resource

```bash
rails generate scaffold Course title:string slug:string:uniq level:string description:text
rails db:migrate
```

### Model Validations

```ruby
# app/models/course.rb
class Course < ApplicationRecord
  has_many :lessons, dependent: :destroy
  has_many :enrollments
  has_many :students, through: :enrollments, source: :user

  validates :title, presence: true, length: { minimum: 3, maximum: 180 }
  validates :slug,  presence: true, uniqueness: true
  validates :level, inclusion: { in: %w[beginner intermediate advanced] }

  before_validation :set_slug

  private

  def set_slug
    self.slug ||= title.parameterize
  end
end
```

### Controller

```ruby
# app/controllers/courses_controller.rb
class CoursesController < ApplicationController
  before_action :authenticate_user!, except: [:index, :show]

  def index
    @courses = Course.includes(:lessons).order(:title).page(params[:page]).per(12)
  end

  def show
    @course = Course.friendly.find(params[:id])
    @lessons = @course.lessons.order(:order)
  end

  def create
    @course = Course.new(course_params)
    if @course.save
      redirect_to @course, notice: "Course created!"
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def course_params
    params.require(:course).permit(:title, :level, :description)
  end
end
```

### Active Record Queries

```ruby
# All beginner courses, most popular first
Course.where(level: "beginner")
      .joins(:enrollments)
      .group("courses.id")
      .order("COUNT(enrollments.id) DESC")
      .limit(5)
```''',
                'Add a Lesson model to the Rails app (title, content, order, course_id). Create seeds with 3 courses and 3 lessons each. Write a scope on Lesson that orders by `order` column.',
                'In Rails, what is the name of the database migration generator command? A) rails db:create  B) rails generate migration  C) rails schema:load  D) rails db:seed',
                'Build a complete Rails course platform: User model with Devise authentication, Course and Lesson CRUD (admin only), student enrollment (join table), and a dashboard showing enrolled courses and progress. Deploy to Render.',
                'Rails Strong Parameters prevent mass-assignment vulnerabilities. Only attributes explicitly listed in `permit()` can be set from form data. Always use `params.require().permit()` in your controllers.',
                65
            ),
            (
                'Ruby Project: REST API with Sinatra',
                'Build a lightweight REST API using Sinatra and deploy it with Docker.',
                '''## Project: Courses API with Sinatra

Sinatra is a lightweight Ruby web framework — perfect for microservices.

### Setup

```bash
gem install sinatra sinatra-contrib sequel pg puma
# Gemfile
source "https://rubygems.org"
gem "sinatra"
gem "sinatra-contrib"
gem "sequel"
gem "pg"
gem "puma"
gem "jwt"
```

### Application

```ruby
# app.rb
require "sinatra"
require "sinatra/json"
require "sinatra/reloader"
require "sequel"
require "json"

DB = Sequel.connect(ENV.fetch("DATABASE_URL", "postgres://localhost/courses"))

DB.create_table?(:courses) do
  primary_key :id
  String :title, null: false
  String :slug,  null: false, unique: true
  String :level, default: "beginner"
  Text   :description
  Time   :created_at, default: Sequel::CURRENT_TIMESTAMP
end

Course = DB[:courses]

# Middleware
before do
  content_type :json
  @body = JSON.parse(request.body.read) rescue {}
end

# GET /api/courses
get "/api/courses" do
  q = params[:q]
  courses = q ? Course.where(Sequel.ilike(:title, "%#{q}%")) : Course.all
  json courses.to_a
end

# GET /api/courses/:slug
get "/api/courses/:slug" do
  course = Course.first(slug: params[:slug])
  halt 404, json(error: "Not found") unless course
  json course
end

# POST /api/courses
post "/api/courses" do
  halt 422, json(error: "Title required") if @body["title"].to_s.strip.empty?
  id = Course.insert(
    title:       @body["title"],
    slug:        @body["title"].downcase.gsub(/[^a-z0-9]+/, "-"),
    level:       @body["level"] || "beginner",
    description: @body["description"] || "",
    created_at:  Time.now
  )
  status 201
  json Course.first(id: id)
end

# DELETE /api/courses/:id
delete "/api/courses/:id" do
  count = Course.where(id: params[:id].to_i).delete
  halt 404, json(error: "Not found") if count == 0
  status 204
end
```

### JWT Authentication

```ruby
require "jwt"

SECRET = ENV.fetch("JWT_SECRET", "dev-secret")

def generate_token(user_id)
  payload = { sub: user_id, iat: Time.now.to_i, exp: 1.hour.from_now.to_i }
  JWT.encode(payload, SECRET, "HS256")
end

def authenticate!
  auth = request.env["HTTP_AUTHORIZATION"].to_s.split(" ").last
  payload, _header = JWT.decode(auth, SECRET, true, { algorithm: "HS256" })
  @current_user_id = payload["sub"]
rescue JWT::DecodeError
  halt 401, json(error: "Unauthorized")
end

post "/api/courses" do
  authenticate!
  # ... create course
end
```

### Deliverables
1. Full CRUD API with Sequel + PostgreSQL
2. JWT auth for write operations
3. Spec tests using `rspec` + `rack-test`
4. Dockerfile (Alpine + puma)
5. Deploy to Fly.io or Render''',
                'Write RSpec tests for the GET /api/courses and POST /api/courses endpoints. Test: empty list response, filtering by title, creating with valid data, and creating with missing title (422 error).',
                'What HTTP status code should a REST API return when a new resource is successfully created? A) 200  B) 201  C) 204  D) 302',
                'Add rate limiting to the API using the `rack-attack` gem: limit unauthenticated POST requests to 10 per minute per IP. Return 429 Too Many Requests with a Retry-After header.',
                'Sinatra\'s `halt` method immediately stops request processing and sends the given status/body. It\'s the Sinatra equivalent of Django\'s `HttpResponse` or Go\'s `return`. Use it liberally in early-return patterns.',
                80
            ),
        ], start=1):
            r = upsert(p, order, title, obj, content, ex, quiz, proj, notes, mins)
            if r: created += 1
            else: updated += 1

        # ── RUST ─────────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='rust')
        for order, (title, obj, content, ex, quiz, proj, notes, mins) in enumerate([
            (
                'Rust Fundamentals: Ownership and Safety',
                'Understand Rust\'s ownership system, borrowing rules, and why they prevent memory bugs at compile time.',
                '''## Rust: Memory Safety Without a Garbage Collector

Rust powers Firefox, Discord, Linux kernel, and Cloudflare Workers. It is consistently the most loved language in the Stack Overflow developer survey.

### Hello World

```bash
curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo new hello && cd hello && cargo run
```

```rust
fn main() {
    let name = String::from("CodeSavannah");
    println!("Hello, {}!", name);
    println!("Length: {} characters", name.len());
}
```

### Ownership — Rust\'s Core Concept

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;         // s1 is MOVED to s2 (s1 is no longer valid)
    // println!("{}", s1); // COMPILE ERROR: value moved

    let s3 = s2.clone(); // explicit deep copy
    println!("{} and {}", s2, s3);  // both valid
}
```

### Borrowing and References

```rust
fn calculate_length(s: &String) -> usize {
    s.len()   // borrow, don\'t take ownership
}

fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1);   // pass reference
    println!("{} has {} chars", s1, len);  // s1 still valid!
}

// Mutable reference
fn change(s: &mut String) {
    s.push_str(", world");
}

let mut s = String::from("hello");
change(&mut s);
println!("{}", s);  // hello, world
```

### Pattern Matching

```rust
let gpa: f64 = 3.8;
let grade = match gpa {
    g if g >= 3.7 => "A",
    g if g >= 3.0 => "B",
    g if g >= 2.0 => "C",
    _             => "F",
};

// Option type (no null pointers in Rust!)
let maybe_name: Option<String> = Some(String::from("Alice"));
match maybe_name {
    Some(name) => println!("Hello, {}!", name),
    None       => println!("No name provided"),
}

// Shorthand
let name = maybe_name.unwrap_or_else(|| String::from("Guest"));

// Result type (error handling)
let parsed: Result<i32, _> = "42".parse();
let number = parsed.unwrap_or(0);
```

### Structs and Traits

```rust
#[derive(Debug, Clone)]
struct Student {
    name: String,
    id:   u32,
    gpa:  f64,
}

impl Student {
    fn new(name: &str, id: u32, gpa: f64) -> Self {
        Self { name: name.to_string(), id, gpa }
    }

    fn grade(&self) -> &str {
        match self.gpa {
            g if g >= 3.7 => "A",
            g if g >= 3.0 => "B",
            _             => "C",
        }
    }
}

impl std::fmt::Display for Student {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{} (ID:{}, GPA:{:.1})", self.name, self.id, self.gpa)
    }
}

fn main() {
    let s = Student::new("Alice", 101, 3.8);
    println!("{} — Grade: {}", s, s.grade());
    println!("{:?}", s);  // Debug output
}
```''',
                'Write a Rust program that reads student data from a Vec<Student>, uses pattern matching to assign grades, and collects only students with GPA >= 3.0 into a new Vec. Print the results.',
                'In Rust, what happens when you assign one String variable to another (e.g., `let s2 = s1;`)? A) s1 and s2 both own the data  B) s1 is cloned automatically  C) s1 is moved and becomes invalid  D) s2 borrows from s1',
                'Build a Rust command-line word counter: read a text file, count total words, unique words, and the top 10 most frequent words. Use HashMap for counting. Handle file-not-found errors gracefully using the ? operator.',
                'The borrow checker rejects programs that would cause use-after-free or data races — at compile time, not at runtime. This makes Rust programs memory-safe without a garbage collector. When the compiler rejects your code, it\'s protecting you.',
                60
            ),
            (
                'Rust Systems Programming',
                'Build performant CLI tools and systems-level programs using Rust\'s standard library.',
                '''## Rust for Systems Programming

### Error Handling with the ? Operator

```rust
use std::fs;
use std::io;
use std::path::Path;

fn read_config(path: &Path) -> Result<String, io::Error> {
    let content = fs::read_to_string(path)?;  // ? propagates error up
    Ok(content)
}

fn main() {
    match read_config(Path::new("config.toml")) {
        Ok(config)  => println!("Config loaded: {} bytes", config.len()),
        Err(e)      => eprintln!("Error: {}", e),
    }
}
```

### CLI Tool with Clap

```rust
// Cargo.toml: clap = { version = "4", features = ["derive"] }
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "codesavannah", about = "Academy CLI")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// List all courses
    List { #[arg(short)] filter: Option<String> },
    /// Search for a course
    Search { query: String },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::List { filter } => list_courses(filter),
        Commands::Search { query } => search_courses(&query),
    }
}
```

### Concurrency with Threads

```rust
use std::thread;
use std::sync::{Arc, Mutex};

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for h in handles { h.join().unwrap(); }
    println!("Counter: {}", *counter.lock().unwrap()); // 10
}
```

### Async with Tokio

```rust
// Cargo.toml: tokio = { version = "1", features = ["full"] }
use tokio;
use reqwest;

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let courses: serde_json::Value = reqwest::get("https://api.example.com/courses")
        .await?
        .json()
        .await?;
    println!("{}", courses);
    Ok(())
}
```''',
                'Build a Rust CLI that recursively walks a directory and counts the number of files by extension (e.g., .py: 12, .html: 5). Use std::fs::read_dir and a HashMap.',
                'What is the Rust async runtime most commonly used for network and web applications? A) asyncio  B) tokio  C) rayon  D) async-std',
                'Build a Rust HTTP server using the Axum framework: GET /courses returns JSON from a Vec, POST /courses appends to a shared Arc<Mutex<Vec>>. Write integration tests with reqwest.',
                'Arc<Mutex<T>> is the pattern for shared mutable state across threads: Arc (Atomic Reference Counter) for shared ownership, Mutex for exclusive access. The compiler enforces correct usage — you can\'t accidentally have a data race.',
                65
            ),
            (
                'Rust Project: High-Performance Tool',
                'Build a production-quality Rust tool or web service demonstrating performance and safety.',
                '''## Project: Fast JSON Log Analyzer

Build a tool that reads and analyzes large JSON log files efficiently.

### Project Setup

```bash
cargo new log-analyzer
cd log-analyzer

# Cargo.toml
[dependencies]
serde         = { version = "1", features = ["derive"] }
serde_json    = "1"
clap          = { version = "4", features = ["derive"] }
rayon         = "1"   # parallel iteration
chrono        = "0.4"
colored       = "2"
```

### Log Entry Model

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct LogEntry {
    pub timestamp:   String,
    pub level:       String,
    pub message:     String,
    pub user_id:     Option<u64>,
    pub path:        Option<String>,
    pub status_code: Option<u16>,
    pub duration_ms: Option<f64>,
}

#[derive(Debug, Default)]
pub struct Stats {
    pub total:    usize,
    pub errors:   usize,
    pub warnings: usize,
    pub p50_ms:   f64,
    pub p99_ms:   f64,
    pub top_paths: Vec<(String, usize)>,
}
```

### Parallel Processing with Rayon

```rust
use rayon::prelude::*;
use std::collections::HashMap;
use std::sync::Mutex;

pub fn analyze(entries: Vec<LogEntry>) -> Stats {
    let path_counts = Mutex::new(HashMap::new());

    // Process in parallel
    let (errors, warnings): (usize, usize) = entries
        .par_iter()
        .map(|entry| {
            // Count paths
            if let Some(path) = &entry.path {
                let mut map = path_counts.lock().unwrap();
                *map.entry(path.clone()).or_insert(0) += 1;
            }
            (
                if entry.level == "ERROR" { 1 } else { 0 },
                if entry.level == "WARN"  { 1 } else { 0 },
            )
        })
        .reduce(|| (0, 0), |a, b| (a.0 + b.0, a.1 + b.1));

    // Compute latency percentiles
    let mut durations: Vec<f64> = entries.iter()
        .filter_map(|e| e.duration_ms)
        .collect();
    durations.sort_by(|a, b| a.partial_cmp(b).unwrap());

    let p50 = percentile(&durations, 0.50);
    let p99 = percentile(&durations, 0.99);

    // Sort paths by count
    let mut paths: Vec<_> = path_counts.into_inner().unwrap().into_iter().collect();
    paths.sort_by(|a, b| b.1.cmp(&a.1));

    Stats {
        total: entries.len(),
        errors,
        warnings,
        p50_ms: p50,
        p99_ms: p99,
        top_paths: paths.into_iter().take(10).collect(),
    }
}

fn percentile(sorted: &[f64], p: f64) -> f64 {
    if sorted.is_empty() { return 0.0; }
    let idx = ((sorted.len() as f64) * p) as usize;
    sorted[idx.min(sorted.len() - 1)]
}
```

### CLI Interface

```rust
#[derive(Parser)]
struct Cli {
    /// Path to log file (JSON lines format)
    file: PathBuf,
    /// Filter by log level
    #[arg(long)] level: Option<String>,
    /// Show entries after this time
    #[arg(long)] since: Option<String>,
}
```

### Deliverables
1. Parse and analyze a 100,000 line JSON log file
2. Output: total entries, error/warning counts, P50/P99 latency
3. Top 10 slowest paths
4. Filter by time range and log level
5. Benchmark against a Python equivalent (show the speedup)''',
                'Generate a test log file with 10,000 entries using a script. Run the analyzer and record the execution time. Then write the same analysis in Python and compare the runtime.',
                'What Rust crate enables easy parallel iteration over collections, similar to calling .iter() but using all CPU cores? A) tokio  B) crossbeam  C) rayon  D) async-std',
                'Add a --watch mode that monitors the log file for new entries using inotify (Linux) / kqueue (Mac) / ReadDirectoryChangesW (Windows) via the `notify` crate, and prints a live updating dashboard with current stats.',
                'Rust\'s ownership system means no garbage collector pauses. For latency-sensitive workloads (games, trading, real-time systems), this predictability is as important as raw throughput. That\'s why Discord moved from Go to Rust for voice.',
                90
            ),
        ], start=1):
            r = upsert(p, order, title, obj, content, ex, quiz, proj, notes, mins)
            if r: created += 1
            else: updated += 1

        # ── SWIFT ────────────────────────────────────────────────────────────
        p = LearningPath.objects.get(slug='swift')
        for order, (title, obj, content, ex, quiz, proj, notes, mins) in enumerate([
            (
                'Swift Fundamentals',
                'Write Swift programs using optionals, structs, enums, and closures.',
                '''## Swift: Apple\'s Modern Language

Swift powers iOS, macOS, watchOS, and tvOS apps. It is safe, fast, and expressive.

### Basics

```swift
import Foundation

let name = "CodeSavannah"    // constant (immutable)
var count = 42               // variable (mutable)
let pi = 3.14159

print("Hello, \\(name)!")    // string interpolation

// Types
let score: Double = 95.5
let active: Bool  = true
let levels: [String] = ["beginner", "intermediate", "advanced"]
let info: [String: Any] = ["name": "Alice", "gpa": 3.8]
```

### Optionals

```swift
// Optional = value might be absent
var email: String? = nil
email = "alice@academy.co.ke"

// Unwrap safely
if let e = email {
    print("Email: \\(e.uppercased())")
}

// Nil coalescing
let display = email ?? "No email"

// Guard (early exit)
func send(to email: String?) {
    guard let email = email else {
        print("No email address")
        return
    }
    print("Sending to \\(email)")
}

// Optional chaining
let length = email?.count  // Int? — safe even if nil
```

### Structs and Enums

```swift
struct Student {
    let name: String
    let id: Int
    var gpa: Double

    var grade: String {
        switch gpa {
        case 3.7...: return "A"
        case 3.0..<3.7: return "B"
        case 2.0..<3.0: return "C"
        default: return "F"
        }
    }

    mutating func updateGpa(_ newGpa: Double) {
        gpa = newGpa
    }
}

enum Level: String, CaseIterable {
    case beginner, intermediate, advanced, professional

    var displayName: String { rawValue.capitalized }
}

// Usage
var s = Student(name: "Alice", id: 101, gpa: 3.8)
print("\\(s.name): \\(s.grade)")
s.updateGpa(3.9)
```

### Closures

```swift
let students = [
    Student(name: "Alice", id: 1, gpa: 3.9),
    Student(name: "Bob",   id: 2, gpa: 2.7),
    Student(name: "Carol", id: 3, gpa: 3.5),
]

let topStudents = students
    .filter  { $0.gpa >= 3.0 }
    .sorted  { $0.gpa > $1.gpa }
    .map     { "\\($0.name): \\($0.grade)" }

topStudents.forEach { print($0) }

// Trailing closure syntax
topStudents.forEach { student in
    print(student)
}
```''',
                'Write a Swift playground that defines a Course struct (title, level, price), creates 5 courses, uses filter to find courses under $50, sorts by price, and prints the cheapest option.',
                'In Swift, what operator provides a default value when an optional is nil? A) || (or)  B) ?? (nil coalescing)  C) ?: (ternary)  D) ! (force unwrap)',
                'Build a Swift course catalog app (Playground or macOS command-line): a Course struct with ratings, a CourseLibrary struct using an array, methods to add/find/sort courses, and a simple text-based menu.',
                'Prefer structs over classes in Swift for value semantics (copied on assignment). Use classes when you need shared mutable state, inheritance, or Objective-C interoperability. Most Swift types should be structs.',
                50
            ),
            (
                'iOS App Development with SwiftUI',
                'Build iOS apps using SwiftUI declarative syntax and Combine for data flow.',
                '''## SwiftUI: Declarative iOS Development

### Views and State

```swift
import SwiftUI

struct Course: Identifiable {
    let id = UUID()
    var title: String
    var level: String
    var isEnrolled: Bool = false
}

struct CourseRow: View {
    @Binding var course: Course

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(course.title)
                    .font(.headline)
                Text(course.level)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            Spacer()
            Button(course.isEnrolled ? "Enrolled" : "Enroll") {
                course.isEnrolled.toggle()
            }
            .buttonStyle(.borderedProminent)
            .tint(course.isEnrolled ? .green : .blue)
        }
        .padding()
    }
}

struct CourseListView: View {
    @State private var courses = [
        Course(title: "Python Programming", level: "Beginner"),
        Course(title: "SwiftUI Mastery",    level: "Intermediate"),
        Course(title: "Machine Learning",   level: "Advanced"),
    ]
    @State private var searchText = ""

    var filtered: [Course] {
        searchText.isEmpty ? courses
            : courses.filter { $0.title.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        NavigationStack {
            List($filtered) { $course in
                CourseRow(course: $course)
            }
            .searchable(text: $searchText, prompt: "Search courses")
            .navigationTitle("Courses")
            .toolbar {
                Button("Add") { addCourse() }
            }
        }
    }

    func addCourse() {
        courses.append(Course(title: "New Course", level: "Beginner"))
    }
}
```

### ObservableObject + @StateObject

```swift
class CourseStore: ObservableObject {
    @Published var courses: [Course] = []
    @Published var isLoading = false

    func fetch() async {
        isLoading = true
        defer { isLoading = false }
        // Simulated network call
        try? await Task.sleep(nanoseconds: 1_000_000_000)
        courses = [Course(title: "Fetched Course", level: "Beginner")]
    }
}

struct ContentView: View {
    @StateObject private var store = CourseStore()

    var body: some View {
        Group {
            if store.isLoading {
                ProgressView("Loading courses...")
            } else {
                List(store.courses) { course in
                    Text(course.title)
                }
            }
        }
        .task { await store.fetch() }
    }
}
```''',
                'Create a SwiftUI course detail view: show title, level, description, a list of lesson titles, and an "Enroll" button that shows a confirmation alert. Use @State for the enrollment state.',
                'In SwiftUI, which property wrapper marks a value as the source of truth and causes the view to re-render when it changes? A) @Binding  B) @State  C) @Published  D) @ObservedObject',
                'Build a complete SwiftUI habit tracker app: habits with daily check-offs, a calendar view showing completion streaks, and local notifications reminding users to complete habits. Persist data with @AppStorage or Core Data.',
                'Use @State for local view state (toggle, text input). Use @StateObject to own an ObservableObject. Use @ObservedObject when a parent passes the object in. Use @EnvironmentObject for app-wide shared state.',
                70
            ),
            (
                'Swift Project: iOS App with Core Data',
                'Build a complete iOS app with persistent storage, network calls, and App Store-ready polish.',
                '''## Project: Course Progress Tracker iOS App

### Architecture: MVVM + Core Data

```
App/
├── Models/
│   ├── Course.swift          (struct for network/display)
│   ├── CourseProgress+CD.swift (Core Data NSManagedObject extension)
│   └── Persistence.swift     (Core Data stack)
├── ViewModels/
│   ├── CourseListVM.swift
│   └── CourseDetailVM.swift
├── Views/
│   ├── ContentView.swift
│   ├── CourseListView.swift
│   ├── CourseDetailView.swift
│   └── Components/
└── Services/
    └── APIService.swift
```

### Core Data Stack

```swift
// Persistence.swift
import CoreData

struct PersistenceController {
    static let shared = PersistenceController()

    let container: NSPersistentContainer

    init() {
        container = NSPersistentContainer(name: "Courses")
        container.loadPersistentStores { _, error in
            if let error { fatalError("CoreData: \\(error)") }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
    }
}

// Entity extension
extension CourseProgress {
    var progressPercent: Double {
        guard totalLessons > 0 else { return 0 }
        return Double(completedLessons) / Double(totalLessons) * 100
    }
}
```

### Network Layer

```swift
// Services/APIService.swift
import Foundation

struct APIService {
    static let base = URL(string: "https://api.codesavannah.com/")!

    static func courses(query: String = "") async throws -> [Course] {
        var url = base.appending(path: "api/courses/")
        if !query.isEmpty {
            url = url.appending(queryItems: [.init(name: "q", value: query)])
        }
        let (data, response) = try await URLSession.shared.data(from: url)
        guard (response as? HTTPURLResponse)?.statusCode == 200
        else { throw URLError(.badServerResponse) }
        return try JSONDecoder().decode([Course].self, from: data)
    }
}
```

### ViewModel

```swift
// ViewModels/CourseListVM.swift
import Foundation

@MainActor
class CourseListVM: ObservableObject {
    @Published var courses: [Course] = []
    @Published var isLoading = false
    @Published var errorMessage: String?

    func load(query: String = "") async {
        isLoading = true
        errorMessage = nil
        do {
            courses = try await APIService.courses(query: query)
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}
```

### App Entry Point

```swift
@main
struct CourseTrackerApp: App {
    let persistence = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\\..managedObjectContext, persistence.container.viewContext)
        }
    }
}
```

### Deliverables
1. Course list fetched from a real API with search
2. Course detail with lesson list and progress tracking
3. Core Data persistence of enrolled courses
4. Local push notifications for daily learning reminders
5. Polished UI with animations and loading states
6. Tested on both iPhone and iPad layouts''',
                'Implement a "favorites" feature using Core Data: a FavoriteCourse entity that stores course ID and title. Show a heart button on each course card that toggles the favorite state.',
                'What framework is used for persistent local storage in iOS/macOS Apple platform apps? A) SQLite  B) Realm  C) Core Data  D) UserDefaults',
                'Add a widget extension (WidgetKit) that shows the user\'s current streak (days of learning) on their home screen. Share data between the main app and widget using App Groups and @AppStorage.',
                'Always mark ViewModel classes with @MainActor in SwiftUI to ensure UI updates happen on the main thread. Without it, publishing changes from background async tasks causes runtime warnings in Xcode.',
                90
            ),
        ], start=1):
            r = upsert(p, order, title, obj, content, ex, quiz, proj, notes, mins)
            if r: created += 1
            else: updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Batch 8 complete: {created} created, {updated} updated'
        ))
