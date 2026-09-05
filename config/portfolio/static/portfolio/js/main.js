document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    // =====================================================
    // 1. DUAL-THEME ENGINE
    // =====================================================
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    function setTheme(newTheme) {
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("site_theme", newTheme);
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", function () {
            const current = document.documentElement.getAttribute("data-theme") || "dark";
            const target = current === "dark" ? "light" : "dark";
            setTheme(target);
        });
    }

    // =====================================================
    // 2. BACK TO TOP
    // =====================================================
    const backToTop = document.getElementById("backToTop");
    window.addEventListener("scroll", function () {
        if (window.scrollY > 350) {
            backToTop?.classList.add("show");
        } else {
            backToTop?.classList.remove("show");
        }
    }, { passive: true });

    if (backToTop) {
        backToTop.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // =====================================================
    // 3. ULTRA-SMOOTH SIDE-HIDE PROJECT FILTER
    // =====================================================
    const filterBtns = document.querySelectorAll(".project-filter-btn");
    const projectCards = Array.from(document.querySelectorAll(".project-item"));
    let isTransitioning = false;

    filterBtns.forEach((btn) => {
        btn.addEventListener("click", function () {
            if (this.classList.contains("active") || isTransitioning) return;

            isTransitioning = true;
            filterBtns.forEach((b) => b.classList.remove("active"));
            this.classList.add("active");

            const filter = this.getAttribute("data-filter");

            // Slide exiting cards out to the left
            projectCards.forEach((card) => {
                const isFeatured = card.getAttribute("data-featured") === "true";
                const willStay = filter === "all" || (filter === "featured" && isFeatured);

                if (!willStay) {
                    card.classList.remove("slide-active");
                    card.classList.add("slide-out-left");
                }
            });

            // Swap layout and slide matching cards in from the right
            setTimeout(() => {
                projectCards.forEach((card, index) => {
                    const isFeatured = card.getAttribute("data-featured") === "true";
                    const willShow = filter === "all" || (filter === "featured" && isFeatured);

                    if (willShow) {
                        card.style.display = "";
                        card.classList.remove("slide-out-left");
                        card.classList.add("slide-prep-right");

                        void card.offsetWidth; // Reflow

                        setTimeout(() => {
                            card.classList.remove("slide-prep-right");
                            card.classList.add("slide-active");
                        }, index * 40);
                    } else {
                        card.style.display = "none";
                    }
                });

                setTimeout(() => {
                    isTransitioning = false;
                }, 300);
            }, 260);
        });
    });

    // =====================================================
    // 4. INTERACTIVE POKE-AROUND TERMINAL CONSOLE
    // =====================================================
    const cliInput = document.getElementById("cliInput");
    const terminalLog = document.getElementById("terminalLog");

    function appendTerminal(htmlContent) {
        if (!terminalLog) return;
        const entry = document.createElement("div");
        entry.className = "terminal-entry";
        entry.innerHTML = htmlContent;
        terminalLog.appendChild(entry);
        terminalLog.scrollTop = terminalLog.scrollHeight;
    }

    // Interactive jump trigger for terminal action links
    window.jumpToSection = function (sectionId) {
        const target = document.getElementById(sectionId);
        if (target) {
            target.scrollIntoView({ behavior: "smooth" });
        }
    };

    function runCliCommand(rawText) {
        const cmd = rawText.trim().toLowerCase();
        appendTerminal(`<div class="log-cmd-echo"><span class="prompt-sym">$</span> ${rawText}</div>`);

        if (!cmd) return;

        switch (cmd) {
            case "help":
            case "-help":
            case "--help":
            case "?":
                appendTerminal(`
                    <div class="terminal-response-box">
                        <div class="resp-title">Available Commands:</div>
                        <div class="resp-item"><code>skills</code> — Technical stack summary</div>
                        <div class="resp-item"><code>projects</code> — Portfolio builds snapshot</div>
                        <div class="resp-item"><code>experience</code> — Career overview</div>
                        <div class="resp-item"><code>education</code> — Academic credentials</div>
                        <div class="resp-item"><code>training</code> — Active technical training</div>
                        <div class="resp-item"><code>contact</code> — Direct communication</div>
                        <div class="resp-item"><code>whoami</code> — Identity overview</div>
                        <div class="resp-item"><code>clear</code> — Wipe console log</div>
                    </div>
                `);
                break;

            case "clear":
            case "cls":
                if (terminalLog) terminalLog.innerHTML = "";
                break;

            case "whoami":
                const bioName = document.querySelector(".hero-headline")?.textContent.replace(/\s+/g, ' ').trim() || "Developer";
                const bioRole = document.querySelector(".console-text")?.textContent.trim() || "Software Engineer";
                appendTerminal(`
                    <div class="terminal-response-box">
                        <div><strong>${bioName}</strong> — <span class="text-teal">${bioRole}</span></div>
                        <div class="text-muted small mt-1">Specialized in building full-stack applications with robust backend systems.</div>
                        <div class="mt-2"><button type="button" onclick="jumpToSection('about')" class="term-btn">View Full Bio ↗</button></div>
                    </div>
                `);
                break;

            case "skills":
            case "stack":
                appendTerminal(`
                    <div class="terminal-response-box">
                        <div class="small">Core engineering stack focused on <strong>Python</strong>, <strong>Django</strong>, <strong>Flask</strong>, relational databases (<strong>Oracle/SQL</strong>), and modern reactive frontends.</div>
                        <div class="mt-2"><button type="button" onclick="jumpToSection('skills')" class="term-btn">View Full Skills ↗</button></div>
                    </div>
                `);
                break;

            case "projects":
            case "work":
                const projectCount = document.querySelectorAll(".project-card-v2").length || "production";
                appendTerminal(`
                    <div class="terminal-response-box">
                        <div class="small">Engineered ${projectCount} applications spanning booking platforms, library management, and backend automation systems.</div>
                        <div class="mt-2"><button type="button" onclick="jumpToSection('projects')" class="term-btn">View All Projects ↗</button></div>
                    </div>
                `);
                break;

            case "experience":
            case "exp":
                appendTerminal(`
                    <div class="terminal-response-box">
                        <div class="small">Hands-on software development involving schema architecture, API endpoints, and scalable asynchronous workflows.</div>
                        <div class="mt-2"><button type="button" onclick="jumpToSection('experience')" class="term-btn">View Experience ↗</button></div>
                    </div>
                `);
                break;

            case "education":
            case "edu":
                const firstEdu = document.querySelector(".edu-degree")?.textContent.trim() || "Engineering Degree";
                const firstInst = document.querySelector(".edu-institution")?.textContent.trim() || "University";
                appendTerminal(`
                    <div class="terminal-response-box">
                        <div class="small">Formal academic background: <strong>${firstEdu}</strong> at ${firstInst}.</div>
                        <div class="mt-2"><button type="button" onclick="jumpToSection('education')" class="term-btn">View Credentials ↗</button></div>
                    </div>
                `);
                break;

            case "training":
            case "courses":
                appendTerminal(`
                    <div class="terminal-response-box">
                        <div class="small">Continuous technical training in Python full-stack engineering, containerization (Docker), and asynchronous processing.</div>
                        <div class="mt-2"><button type="button" onclick="jumpToSection('training')" class="term-btn">View Courses ↗</button></div>
                    </div>
                `);
                break;

            case "contact":
            case "email":
                const directEmail = document.querySelector(".bento-info-tile[href^='mailto:']")?.getAttribute("href")?.replace("mailto:", "") || "Available on form";
                appendTerminal(`
                    <div class="terminal-response-box">
                        <div class="small">Reach out directly via email at <strong class="text-teal">${directEmail}</strong>.</div>
                        <div class="mt-2"><button type="button" onclick="jumpToSection('contact')" class="term-btn">Open Contact Form ↗</button></div>
                    </div>
                `);
                break;

            default:
                appendTerminal(`
                    <div class="text-danger small font-monospace">
                        bash: command not found: "${cmd}". Type "<code>help</code>" to view all available commands.
                    </div>
                `);
                break;
        
        }
    }

    if (cliInput) {
        cliInput.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                e.stopPropagation();
                const val = this.value;
                runCliCommand(val);
                this.value = "";
            }
        });
    }
});