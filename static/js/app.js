/* KodaGrid — Main JS
   Handles: page loader · counter animations · scroll reveal
            nav scroll effect · image lazy‑load enhancement
            progress bars · live chat · coding games
   ----------------------------------------------------------------- */

/* ── Page loader ─────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("loaded");
    initCounters();
    initScrollReveal();
    initNavScroll();
    initProgressBars();
    initImageEnhancements();
    initThemeToggle();
    initLangPicker();
    applyTranslations();
    initClickableCards();
});

/* ── Clickable cards (data-href) ─────────────────────────────────── */
function initClickableCards() {
    document.querySelectorAll(".cs-clickable-card[data-href]").forEach(card => {
        card.addEventListener("click", e => {
            if (e.target.closest("a, button")) return;
            window.location.href = card.dataset.href;
        });
    });
}

/* ── Animated counters ───────────────────────────────────────────── */
function initCounters() {
    const counters = document.querySelectorAll("[data-count]");
    const easeFn = (t) => 1 - Math.pow(1 - t, 3);

    const animateCounter = (el) => {
        const target = Number(el.dataset.count || "0");
        const duration = 1400;
        const start = performance.now();
        const tick = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            const value = Math.floor(target * easeFn(progress));
            el.textContent = value.toLocaleString();
            if (progress < 1) requestAnimationFrame(tick);
            else {
                el.textContent = target.toLocaleString();
                el.closest(".stat-item")?.classList.add("counter-done");
            }
        };
        requestAnimationFrame(tick);
    };

    if ("IntersectionObserver" in window) {
        const obs = new IntersectionObserver((entries, o) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    o.unobserve(entry.target);
                }
            });
        }, { threshold: 0.35 });
        counters.forEach((c) => obs.observe(c));
    } else {
        counters.forEach(animateCounter);
    }
}

/* ── Theme toggle ────────────────────────────────────────────────── */
function initThemeToggle() {
    const html    = document.getElementById("html-root");
    const btn     = document.getElementById("theme-toggle-btn");
    const iconEl  = document.getElementById("theme-icon");
    const favicon = document.getElementById("site-favicon");
    if (!html || !btn || !iconEl) return;

    const syncUI = (theme) => {
        const nextTheme = theme === "dark" ? "light" : "dark";
        iconEl.innerHTML = theme === "dark"
            ? '<circle cx="12" cy="12" r="4"></circle><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"></path>'
            : '<path d="M20.9 13A9 9 0 0 1 11 3.1 9 9 0 1 0 20.9 13Z"></path>';
        const label = `Switch to ${nextTheme} mode`;
        btn.setAttribute("aria-label", label);
        btn.title = label;
        if (favicon) {
            favicon.href = favicon.dataset[`${theme}Href`];
        }
    };

    const current = html.dataset.theme === "dark" ? "dark" : "light";
    html.dataset.theme = current;
    syncUI(current);

    btn.addEventListener("click", () => {
        const next = html.dataset.theme === "dark" ? "light" : "dark";
        html.dataset.theme = next;
        try {
            localStorage.setItem("cs_theme", next);
        } catch (error) {
            // Keep the current theme usable when browser storage is unavailable.
        }
        syncUI(next);
    });
}

/* ── i18n ─────────────────────────────────────────────────────────── */
function applyTranslations() {
    const lang = document.documentElement.dataset.lang || "en";
    const i18n = window.CS_I18N || {};
    const dict = i18n[lang] || i18n.en || {};

    /* text content */
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const val = dict[el.dataset.i18n] ?? i18n.en?.[el.dataset.i18n];
        if (val !== undefined) el.textContent = val;
    });

    /* input / textarea placeholders */
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const val = dict[el.dataset.i18nPlaceholder] ?? i18n.en?.[el.dataset.i18nPlaceholder];
        if (val !== undefined) el.placeholder = val;
    });

    /* aria-labels that need translation */
    document.querySelectorAll("[data-i18n-label]").forEach(el => {
        const val = dict[el.dataset.i18nLabel] ?? i18n.en?.[el.dataset.i18nLabel];
        if (val !== undefined) el.setAttribute("aria-label", val);
    });

    /* set <html lang="…"> for accessibility */
    document.documentElement.lang = lang;
}

function initLangPicker() {
    const picker  = document.getElementById("lang-picker");
    const btn     = document.getElementById("lang-picker-btn");
    const nameEl  = document.getElementById("lang-name");
    if (!picker || !btn || !nameEl) return;

    const options = [...picker.querySelectorAll(".lang-option")];
    const saved = options.some(option => option.dataset.lang === document.documentElement.dataset.lang)
        ? document.documentElement.dataset.lang
        : "en";
    const savedBtn = options.find(option => option.dataset.lang === saved);
    document.documentElement.dataset.lang = saved;

    const selectLanguage = (option) => {
        const lang = option.dataset.lang;
        document.documentElement.dataset.lang = lang;
        nameEl.textContent = option.dataset.label;
        options.forEach(item => {
            const selected = item === option;
            item.classList.toggle("active", selected);
            item.setAttribute("aria-selected", String(selected));
        });
        try {
            localStorage.setItem("cs_lang", lang);
        } catch (error) {
            // Translation remains available for this page when browser storage is unavailable.
        }
        applyTranslations();
    };

    if (savedBtn) selectLanguage(savedBtn);

    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        picker.classList.toggle("open");
        btn.setAttribute("aria-expanded", picker.classList.contains("open"));
    });
    document.addEventListener("click", () => { picker.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); });

    options.forEach(opt => {
        opt.addEventListener("click", () => {
            selectLanguage(opt);
            picker.classList.remove("open");
        });
    });
}

/* ── Scroll‑reveal (.reveal) ─────────────────────────────────────── */
function initScrollReveal() {
    const revealEls = document.querySelectorAll(".reveal");
    if (!revealEls.length) return;

    if ("IntersectionObserver" in window) {
        const obs = new IntersectionObserver((entries, o) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("revealed");
                    o.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });
        revealEls.forEach((el) => obs.observe(el));
    } else {
        revealEls.forEach((el) => el.classList.add("revealed"));
    }
}

/* ── Nav: add .scrolled class after 60px scroll ──────────────────── */
function initNavScroll() {
    const header = document.querySelector(".site-header");
    if (!header) return;
    const toggle = () => header.classList.toggle("scrolled", window.scrollY > 60);
    toggle();
    window.addEventListener("scroll", toggle, { passive: true });
}

/* ── Progress bar animation ──────────────────────────────────────── */
function initProgressBars() {
    const bars = document.querySelectorAll(".progress-track span[data-width]");
    if (!bars.length) return;
    const obs = new IntersectionObserver((entries, o) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.width = entry.target.dataset.width + "%";
                o.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    bars.forEach((b) => { b.style.width = "0%"; obs.observe(b); });
}

/* ── Lazy image fade‑in ──────────────────────────────────────────── */
function initImageEnhancements() {
    const imgs = document.querySelectorAll("img[loading='lazy']");
    imgs.forEach((img) => {
        img.style.transition = "opacity 500ms ease";
        img.style.opacity = img.complete ? "1" : "0";
        if (!img.complete) img.addEventListener("load", () => { img.style.opacity = "1"; });
    });
}


/* ================================================================
   LIVE CLASSROOM CHAT
   Call initChat(containerSelector, options) on the chat page.
   ================================================================ */
function initChat(containerSelector, options = {}) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    const { currentUser = "Student", userRole = "student", roomId = "general" } = options;
    const storageKey = `cs_chat_${roomId}`;

    /* mock messages persisted in sessionStorage so page refresh keeps them */
    const loadMessages = () => {
        try { return JSON.parse(sessionStorage.getItem(storageKey) || "[]"); }
        catch { return []; }
    };
    const saveMessages = (msgs) => sessionStorage.setItem(storageKey, JSON.stringify(msgs));

    let messages = loadMessages();

    /* seed with sample content the first time */
    if (!messages.length) {
        messages = [
            { user: "Trainer Amina", role: "trainer", text: "Welcome to today's session! We will be building a REST API with Django. 🐍", time: "9:00 AM" },
            { user: "Brian M.", role: "student", text: "So excited for this! I've been practising serialisers all week.", time: "9:01 AM" },
            { user: "Grace N.", role: "student", text: "Do we need to have completed the OOP lesson first?", time: "9:02 AM" },
            { user: "Trainer Amina", role: "trainer", text: "Great question Grace — yes, OOP basics are needed. Check the Resources tab if you need a refresher.", time: "9:03 AM" },
        ];
        saveMessages(messages);
    }

    const colorMap = { trainer: "var(--accent)", student: "var(--emerald)" };

    const renderMessage = (msg, isSelf) => {
        const div = document.createElement("div");
        div.className = `chat-bubble ${isSelf ? "chat-bubble-self" : "chat-bubble-other"}`;
        div.innerHTML = `
            ${!isSelf ? `<span class="chat-sender" style="color:${colorMap[msg.role] || "var(--muted)"};">${msg.user}${msg.role === "trainer" ? " 🎓" : ""}</span>` : ""}
            <p>${escapeHtml(msg.text)}</p>
            <span class="chat-time">${msg.time}</span>
        `;
        return div;
    };

    const escapeHtml = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

    const now = () => {
        const d = new Date();
        const h = d.getHours(), m = d.getMinutes();
        return `${h > 12 ? h - 12 : h || 12}:${String(m).padStart(2, "0")} ${h >= 12 ? "PM" : "AM"}`;
    };

    container.innerHTML = `
        <div class="chat-header">
            <div class="chat-header-info">
                <span class="chat-status-dot"></span>
                <strong id="chat-room-name">Classroom Chat</strong>
                <span class="chat-role-badge ${userRole}">${userRole === "trainer" ? "🎓 Trainer" : "👨‍💻 Student"}</span>
            </div>
            <span class="chat-member-count" id="chat-member-count">1 online</span>
        </div>
        <div class="chat-messages" id="chat-messages" aria-live="polite" aria-label="Chat messages"></div>
        <form class="chat-input-row" id="chat-form" autocomplete="off">
            <input id="chat-input" type="text" placeholder="Type a message…" maxlength="500" aria-label="Chat message">
            <button type="submit" class="btn btn-accent btn-small chat-send-btn" aria-label="Send">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            </button>
        </form>
    `;

    const msgBox = container.querySelector("#chat-messages");
    const form   = container.querySelector("#chat-form");
    const input  = container.querySelector("#chat-input");

    const scrollBottom = () => msgBox.scrollTo({ top: msgBox.scrollHeight, behavior: "smooth" });

    const renderAll = () => {
        msgBox.innerHTML = "";
        messages.forEach((m) => msgBox.appendChild(renderMessage(m, m.user === currentUser)));
        scrollBottom();
    };

    renderAll();

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        const msg = { user: currentUser, role: userRole, text, time: now() };
        messages.push(msg);
        if (messages.length > 120) messages.shift();
        saveMessages(messages);
        msgBox.appendChild(renderMessage(msg, true));
        scrollBottom();
        input.value = "";
        input.focus();
    });

    /* simulate a trainer reply after a few seconds (demo only) */
    const trainerReplies = [
        "Great progress! Keep it up. 💪",
        "Anyone else have questions? Don't be shy!",
        "Remember: every bug you fix makes you a better developer.",
        "Good thinking! That's exactly how it works.",
        "Check the exercises tab for practice problems on this topic.",
    ];
    let replyIdx = 0;
    const scheduleReply = () => {
        const delay = 12000 + Math.random() * 15000;
        setTimeout(() => {
            const msg = { user: "Trainer Amina", role: "trainer", text: trainerReplies[replyIdx % trainerReplies.length], time: now() };
            replyIdx++;
            messages.push(msg);
            saveMessages(messages);
            msgBox.appendChild(renderMessage(msg, false));
            scrollBottom();
            scheduleReply();
        }, delay);
    };
    scheduleReply();
}


/* ================================================================
   CODING GAMES ENGINE
   Call initGames(containerSelector) on the games page.
   ================================================================ */
function initGames(containerSelector) {
    const root = document.querySelector(containerSelector);
    if (!root) return;

    const games = [
        { id: "typer",    name: "Code Typer",     icon: "⌨️", desc: "Race the clock — type code snippets as fast as you can!" },
        { id: "bugfixer", name: "Bug Fixer",       icon: "🐛", desc: "Spot the bug in the code and select the fix before time runs out." },
        { id: "filler",   name: "Code Fill-In",   icon: "📝", desc: "Fill in the missing keyword to complete the function." },
        { id: "quiz",     name: "Tech Quiz",       icon: "🧠", desc: "Answer rapid-fire programming trivia to score points." },
    ];

    let activeGame = null;

    const renderMenu = () => {
        root.innerHTML = `
            <div class="games-menu">
                <h2 class="games-title">Choose Your Challenge</h2>
                <div class="games-grid">
                    ${games.map(g => `
                        <button class="game-card-btn" data-game="${g.id}" aria-label="Play ${g.name}">
                            <span class="game-icon">${g.icon}</span>
                            <h3>${g.name}</h3>
                            <p>${g.desc}</p>
                            <span class="btn btn-accent btn-small">Play Now</span>
                        </button>
                    `).join("")}
                </div>
            </div>
        `;
        root.querySelectorAll(".game-card-btn").forEach(btn => {
            btn.addEventListener("click", () => startGame(btn.dataset.game));
        });
    };

    const startGame = (id) => {
        activeGame = id;
        switch (id) {
            case "typer":    runTyperGame();    break;
            case "bugfixer": runBugFixerGame(); break;
            case "filler":   runFillerGame();   break;
            case "quiz":     runQuizGame();     break;
        }
    };

    const backBtn = () => `<button class="btn btn-ghost btn-small game-back-btn" onclick="">← Back to Games</button>`;

    const injectBack = () => {
        root.querySelector(".game-back-btn")?.addEventListener("click", () => {
            activeGame = null;
            renderMenu();
        });
    };

    /* ── TYPER GAME ── */
    const typerSnippets = [
        { code: "print('Hello, KodaGrid!')", lang: "Python" },
        { code: "const greet = (name) => `Hello, ${name}!`;", lang: "JavaScript" },
        { code: "for i in range(10):\n    print(i)", lang: "Python" },
        { code: "SELECT * FROM students WHERE active = 1;", lang: "SQL" },
        { code: "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)", lang: "Python" },
        { code: "const arr = [1,2,3].map(x => x * 2);", lang: "JavaScript" },
        { code: "<div class=\"hero\">\n  <h1>Learn to Code</h1>\n</div>", lang: "HTML" },
    ];

    function runTyperGame() {
        let snippet = typerSnippets[Math.floor(Math.random() * typerSnippets.length)];
        let startTime = null;
        let timerInterval = null;
        let timeLeft = 60;
        let score = 0;
        let streak = 0;

        const render = () => {
            root.innerHTML = `
                <div class="game-area">
                    ${backBtn()}
                    <h2 class="game-title">⌨️ Code Typer</h2>
                    <div class="game-hud">
                        <span class="hud-item">Score: <strong id="g-score">0</strong></span>
                        <span class="hud-item">Streak: <strong id="g-streak">0</strong></span>
                        <span class="hud-item">Time: <strong id="g-timer">60s</strong></span>
                    </div>
                    <div class="typer-card">
                        <p class="typer-lang">${snippet.lang}</p>
                        <pre class="typer-target" id="typer-target"><code>${escapeGameHtml(snippet.code)}</code></pre>
                        <textarea class="typer-input" id="typer-input" placeholder="Type the code above…" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="off"></textarea>
                        <div class="typer-accuracy" id="typer-accuracy">Start typing to begin the timer…</div>
                    </div>
                </div>
            `;
            injectBack();
            const input = root.querySelector("#typer-input");
            const timerEl = root.querySelector("#g-timer");
            const scoreEl = root.querySelector("#g-score");
            const streakEl = root.querySelector("#g-streak");
            const accuracyEl = root.querySelector("#typer-accuracy");

            input.addEventListener("input", () => {
                if (!startTime) {
                    startTime = Date.now();
                    timerInterval = setInterval(() => {
                        timeLeft--;
                        timerEl.textContent = timeLeft + "s";
                        if (timeLeft <= 0) endTyper();
                    }, 1000);
                }
                const typed = input.value;
                const target = snippet.code;
                let correct = 0;
                for (let i = 0; i < typed.length; i++) {
                    if (typed[i] === target[i]) correct++;
                }
                const pct = Math.round((correct / Math.max(target.length, 1)) * 100);
                accuracyEl.textContent = `Accuracy: ${pct}% (${typed.length}/${target.length} chars)`;
                if (typed === target) {
                    const elapsed = (Date.now() - startTime) / 1000;
                    const wpm = Math.round((target.length / 5) / (elapsed / 60));
                    streak++;
                    score += Math.max(10, wpm) + streak * 2;
                    scoreEl.textContent = score;
                    streakEl.textContent = streak;
                    snippet = typerSnippets[Math.floor(Math.random() * typerSnippets.length)];
                    input.value = "";
                    startTime = Date.now();
                    root.querySelector("#typer-target code").innerHTML = escapeGameHtml(snippet.code);
                    root.querySelector(".typer-lang").textContent = snippet.lang;
                    accuracyEl.textContent = "✅ Correct! Next snippet loaded.";
                }
            });

            const endTyper = () => {
                clearInterval(timerInterval);
                root.querySelector(".typer-card").innerHTML = `
                    <div class="game-result">
                        <h3>Time's Up! ⏱️</h3>
                        <p class="result-score">Score: <strong>${score}</strong></p>
                        <p>Best streak: ${streak}</p>
                        <button class="btn btn-accent" id="play-again">Play Again</button>
                    </div>
                `;
                root.querySelector("#play-again")?.addEventListener("click", runTyperGame);
            };
        };
        render();
    }

    /* ── BUG FIXER GAME ── */
    const bugChallenges = [
        { question: "What's wrong with this Python code?",
          code: "def greet(name)\n    print('Hello ' + name)",
          options: ["Missing colon after def greet(name)", "Missing quotes around name", "Should use f-string", "print should be Print"],
          correct: 0 },
        { question: "Which line causes an error?",
          code: "x = 10\ny = '5'\nresult = x + y\nprint(result)",
          options: ["Line 3: can't add int and str", "Line 1: wrong variable name", "Line 4: print syntax error", "Line 2: can't assign string"],
          correct: 0 },
        { question: "What's broken in this JavaScript?",
          code: "const nums = [1,2,3];\nnums.forEach(n => {\n  console.log(n * 2)\n}\n// missing bracket",
          options: ["Missing closing ) for forEach", "nums is const so can't iterate", "console.log is undefined", "Arrow function is wrong"],
          correct: 0 },
        { question: "Fix the SQL query:",
          code: "SELCT name, age FORM students WERE age > 18;",
          options: ["SELCT → SELECT, FORM → FROM, WERE → WHERE", "Missing semicolon", "age should be quoted", "Need ORDER BY clause"],
          correct: 0 },
        { question: "What's wrong here?",
          code: "for i in range(5):\nprint(i)",
          options: ["print(i) is not indented", "range should be range(0,5)", "Missing colon after range(5)", "for loop needs a list"],
          correct: 0 },
    ];

    function runBugFixerGame() {
        let idx = 0;
        let score = 0;
        let lives = 3;

        const render = () => {
            if (idx >= bugChallenges.length) {
                root.innerHTML = `<div class="game-area">${backBtn()}<div class="game-result"><h3>All bugs squashed! 🐛✅</h3><p class="result-score">Final score: <strong>${score}</strong></p><button class="btn btn-accent" id="play-again">Play Again</button></div></div>`;
                injectBack();
                root.querySelector("#play-again")?.addEventListener("click", runBugFixerGame);
                return;
            }
            const ch = bugChallenges[idx];
            root.innerHTML = `
                <div class="game-area">
                    ${backBtn()}
                    <h2 class="game-title">🐛 Bug Fixer</h2>
                    <div class="game-hud">
                        <span class="hud-item">Score: <strong>${score}</strong></span>
                        <span class="hud-item">Lives: <strong>${"❤️".repeat(lives)}</strong></span>
                        <span class="hud-item">Q: <strong>${idx+1}/${bugChallenges.length}</strong></span>
                    </div>
                    <div class="bug-card">
                        <p class="bug-question">${ch.question}</p>
                        <pre class="bug-code"><code>${escapeGameHtml(ch.code)}</code></pre>
                        <div class="bug-options">
                            ${ch.options.map((opt, i) => `<button class="bug-option" data-idx="${i}">${opt}</button>`).join("")}
                        </div>
                        <div class="bug-feedback" id="bug-feedback"></div>
                    </div>
                </div>
            `;
            injectBack();
            root.querySelectorAll(".bug-option").forEach(btn => {
                btn.addEventListener("click", () => {
                    const chosen = parseInt(btn.dataset.idx);
                    const fb = root.querySelector("#bug-feedback");
                    if (chosen === ch.correct) {
                        score += 10;
                        btn.classList.add("option-correct");
                        fb.textContent = "✅ Correct! Great debugging!";
                        fb.className = "bug-feedback feedback-correct";
                    } else {
                        lives--;
                        btn.classList.add("option-wrong");
                        root.querySelectorAll(".bug-option")[ch.correct].classList.add("option-correct");
                        fb.textContent = "❌ Not quite. The correct answer is highlighted.";
                        fb.className = "bug-feedback feedback-wrong";
                    }
                    root.querySelectorAll(".bug-option").forEach(b => b.disabled = true);
                    if (lives <= 0) {
                        setTimeout(() => {
                            root.innerHTML = `<div class="game-area">${backBtn()}<div class="game-result"><h3>Game Over 💔</h3><p class="result-score">Score: <strong>${score}</strong></p><button class="btn btn-accent" id="play-again">Try Again</button></div></div>`;
                            injectBack();
                            root.querySelector("#play-again")?.addEventListener("click", runBugFixerGame);
                        }, 1400);
                    } else {
                        setTimeout(() => { idx++; render(); }, 1400);
                    }
                });
            });
        };
        render();
    }

    /* ── CODE FILL-IN GAME ── */
    const fillChallenges = [
        { prompt: "Complete the Python for loop:", code: "___ i in range(10):", answer: "for", hint: "The keyword that starts a loop in Python" },
        { prompt: "Complete the function definition:", code: "___ greet(name):\n    return 'Hello ' + name", answer: "def", hint: "Defines a reusable block of code in Python" },
        { prompt: "Complete the JS arrow function:", code: "const add = (a, b) ___ a + b;", answer: "=>", hint: "The arrow in an arrow function" },
        { prompt: "Complete the SQL clause:", code: "SELECT * FROM students ___ age > 18;", answer: "WHERE", hint: "Filters rows based on a condition" },
        { prompt: "Complete the HTML tag:", code: "<___ class=\"hero\">\n  <h1>Welcome</h1>\n</___ >", answer: "div", hint: "A generic container element" },
        { prompt: "Complete the Python list comprehension:", code: "squares = [x**2 ___ x in range(10)]", answer: "for", hint: "The iteration keyword inside a list comp" },
        { prompt: "Complete the JavaScript conditional:", code: "___ (score > 50) {\n  console.log('Pass');\n}", answer: "if", hint: "Used for conditional logic" },
    ];

    function runFillerGame() {
        let idx = 0;
        let score = 0;

        const render = () => {
            if (idx >= fillChallenges.length) {
                root.innerHTML = `<div class="game-area">${backBtn()}<div class="game-result"><h3>All filled in! 🧩</h3><p class="result-score">Score: <strong>${score}/${fillChallenges.length * 10}</strong></p><button class="btn btn-accent" id="play-again">Play Again</button></div></div>`;
                injectBack();
                root.querySelector("#play-again")?.addEventListener("click", runFillerGame);
                return;
            }
            const ch = fillChallenges[idx];
            root.innerHTML = `
                <div class="game-area">
                    ${backBtn()}
                    <h2 class="game-title">📝 Code Fill-In</h2>
                    <div class="game-hud">
                        <span class="hud-item">Score: <strong>${score}</strong></span>
                        <span class="hud-item">Q: <strong>${idx+1}/${fillChallenges.length}</strong></span>
                    </div>
                    <div class="filler-card">
                        <p class="filler-prompt">${ch.prompt}</p>
                        <pre class="filler-code"><code>${escapeGameHtml(ch.code)}</code></pre>
                        <p class="filler-hint">💡 Hint: ${ch.hint}</p>
                        <div class="filler-input-row">
                            <input type="text" id="filler-input" class="filler-input" placeholder="Type your answer…" autocomplete="off" spellcheck="false">
                            <button class="btn btn-accent" id="filler-submit">Check</button>
                        </div>
                        <div class="filler-feedback" id="filler-feedback"></div>
                    </div>
                </div>
            `;
            injectBack();
            const input  = root.querySelector("#filler-input");
            const submit = root.querySelector("#filler-submit");
            const fb     = root.querySelector("#filler-feedback");

            const check = () => {
                const val = input.value.trim();
                if (val.toLowerCase() === ch.answer.toLowerCase()) {
                    score += 10;
                    fb.textContent = "✅ Correct! Well done.";
                    fb.className = "filler-feedback feedback-correct";
                } else {
                    fb.textContent = `❌ Not quite. The answer is: ${ch.answer}`;
                    fb.className = "filler-feedback feedback-wrong";
                }
                input.disabled = true; submit.disabled = true;
                setTimeout(() => { idx++; render(); }, 1300);
            };
            submit.addEventListener("click", check);
            input.addEventListener("keydown", (e) => { if (e.key === "Enter") check(); });
            input.focus();
        };
        render();
    }

    /* ── QUIZ GAME ── */
    const quizQs = [
        { q: "What does HTML stand for?", opts: ["HyperText Markup Language","HighText Machine Language","HyperText Machine Language","HyperText Markup Level"], a: 0 },
        { q: "Which language runs in a web browser?", opts: ["Java","Python","JavaScript","C++"], a: 2 },
        { q: "What symbol starts a comment in Python?", opts: ["//","/*","#","--"], a: 2 },
        { q: "What does CSS stand for?", opts: ["Computer Style Sheets","Creative Style Sheets","Cascading Style Sheets","Colorful Style Sheets"], a: 2 },
        { q: "Which keyword declares a variable in JavaScript (modern)?", opts: ["var","int","dim","let or const"], a: 3 },
        { q: "What does SQL stand for?", opts: ["Structured Query Language","Simple Query Logic","Sequential Query Language","Secure Query List"], a: 0 },
        { q: "Which of these is NOT a Python data type?", opts: ["int","float","char","list"], a: 2 },
        { q: "What is Git used for?", opts: ["Database management","Version control","Web hosting","Sending emails"], a: 1 },
        { q: "What does API stand for?", opts: ["Application Programming Interface","Advanced Protocol Integration","Application Processor Input","Automated Program Interface"], a: 0 },
        { q: "Which company created Django?", opts: ["Google","Facebook","The World Company (news site)","Microsoft"], a: 2 },
    ];

    function runQuizGame() {
        const shuffled = [...quizQs].sort(() => Math.random() - 0.5).slice(0, 7);
        let idx = 0;
        let score = 0;

        const render = () => {
            if (idx >= shuffled.length) {
                const pct = Math.round((score / (shuffled.length * 10)) * 100);
                root.innerHTML = `<div class="game-area">${backBtn()}<div class="game-result"><h3>Quiz Complete! 🧠</h3><p class="result-score">Score: <strong>${score}/${shuffled.length * 10}</strong> (${pct}%)</p><p>${pct >= 70 ? "🏆 Excellent work!" : pct >= 50 ? "👍 Good effort — keep studying!" : "📚 Review the lessons and try again."}</p><button class="btn btn-accent" id="play-again">Play Again</button></div></div>`;
                injectBack();
                root.querySelector("#play-again")?.addEventListener("click", runQuizGame);
                return;
            }
            const q = shuffled[idx];
            root.innerHTML = `
                <div class="game-area">
                    ${backBtn()}
                    <h2 class="game-title">🧠 Tech Quiz</h2>
                    <div class="game-hud">
                        <span class="hud-item">Score: <strong>${score}</strong></span>
                        <span class="hud-item">Q: <strong>${idx+1}/${shuffled.length}</strong></span>
                    </div>
                    <div class="quiz-card">
                        <p class="quiz-question">${q.q}</p>
                        <div class="quiz-options">
                            ${q.opts.map((opt, i) => `<button class="quiz-option" data-i="${i}">${opt}</button>`).join("")}
                        </div>
                        <div class="quiz-feedback" id="quiz-feedback"></div>
                    </div>
                </div>
            `;
            injectBack();
            root.querySelectorAll(".quiz-option").forEach(btn => {
                btn.addEventListener("click", () => {
                    const chosen = parseInt(btn.dataset.i);
                    const fb = root.querySelector("#quiz-feedback");
                    root.querySelectorAll(".quiz-option").forEach(b => b.disabled = true);
                    if (chosen === q.a) {
                        score += 10;
                        btn.classList.add("option-correct");
                        fb.textContent = "✅ Correct!";
                        fb.className = "quiz-feedback feedback-correct";
                    } else {
                        btn.classList.add("option-wrong");
                        root.querySelectorAll(".quiz-option")[q.a].classList.add("option-correct");
                        fb.textContent = `❌ The answer was: ${q.opts[q.a]}`;
                        fb.className = "quiz-feedback feedback-wrong";
                    }
                    setTimeout(() => { idx++; render(); }, 1300);
                });
            });
        };
        render();
    }

    const escapeGameHtml = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

    renderMenu();
}

/* expose globally */
function initChatConnected(containerSelector, options = {}) {
    const container = document.querySelector(containerSelector);
    if (!container) return;
    const { currentUser = 'Student', userRole = 'student', roomId, apiUrl = '/chat/api/' } = options;
    let lastId = 0;
    const csrf = () => document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
    const request = async (url, payload) => {
        const response = await fetch(url, { credentials: 'same-origin', method: payload ? 'POST' : 'GET',
            headers: payload ? { 'Content-Type': 'application/json', 'X-CSRFToken': decodeURIComponent(csrf()) } : {},
            body: payload ? JSON.stringify(payload) : undefined });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Chat is unavailable.');
        return data;
    };
    container.innerHTML = `<div class="chat-header"><div class="chat-header-info"><span class="chat-status-dot"></span><strong>Classroom Chat</strong><span class="chat-role-badge ${userRole}">${userRole === 'trainer' ? 'Tutor' : 'Student'}</span></div></div><div class="chat-messages" aria-live="polite"></div><form class="chat-input-row" autocomplete="off"><input type="text" placeholder="Type a message…" maxlength="1000" aria-label="Chat message"><button type="submit" class="btn btn-accent btn-small chat-send-btn" aria-label="Send">Send</button></form>`;
    const messages = container.querySelector('.chat-messages');
    const input = container.querySelector('input');
    const append = item => {
        const bubble = document.createElement('div'); bubble.className = `chat-bubble ${item.mine ? 'chat-bubble-self' : 'chat-bubble-other'}`;
        if (!item.mine) { const sender = document.createElement('span'); sender.className = 'chat-sender'; sender.textContent = item.user; bubble.appendChild(sender); }
        const body = document.createElement('p'); body.textContent = item.text;
        const time = document.createElement('span'); time.className = 'chat-time'; time.textContent = new Date(item.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        bubble.append(body, time); messages.appendChild(bubble); messages.scrollTop = messages.scrollHeight;
    };
    const refresh = async () => {
        if (!roomId) return;
        try {
            const data = await request(`${apiUrl}?room=${encodeURIComponent(roomId)}&after=${lastId}`);
            data.messages.forEach(item => { append(item); lastId = Math.max(lastId, item.id); });
        } catch (error) { container.title = error.message; }
    };
    refresh();
    const timer = setInterval(refresh, 2500);
    container.querySelector('form').addEventListener('submit', event => {
        event.preventDefault();
        const text = input.value.trim();
        if (!text || !roomId) return;
        request(apiUrl, { room: roomId, text }).then(() => { input.value = ''; refresh(); })
            .catch(error => { container.title = error.message; });
    });
    window.addEventListener('pagehide', () => clearInterval(timer), { once: true });
}
window.initChat  = initChatConnected;
window.initGames = initGames;

/* ============================================================
   NAV DROPDOWNS — hover on desktop, click-toggle on mobile
   ============================================================ */
(function initNavDropdowns() {
    const isMobile = () => window.innerWidth < 900;

    document.querySelectorAll(".nav-dropdown").forEach(dd => {
        const btn = dd.querySelector(".nav-drop-btn");
        if (!btn) return;

        btn.addEventListener("click", e => {
            if (!isMobile()) return;
            e.stopPropagation();
            const open = dd.classList.toggle("open");
            btn.setAttribute("aria-expanded", open);
        });
    });

    /* close on outside click */
    document.addEventListener("click", e => {
        if (!e.target.closest(".nav-dropdown")) {
            document.querySelectorAll(".nav-dropdown.open").forEach(dd => {
                dd.classList.remove("open");
                const btn = dd.querySelector(".nav-drop-btn");
                if (btn) btn.setAttribute("aria-expanded", "false");
            });
        }
    });
})();
