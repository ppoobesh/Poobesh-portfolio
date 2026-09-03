document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // ELEMENTS
    // =====================================================

    const navbar = document.getElementById("mainNavbar");
    const navbarMenu = document.getElementById("navbarMenu");

    const navLinks = document.querySelectorAll(
        '#mainNavbar .nav-link[href^="#"]'
    );

    const sections = document.querySelectorAll(
        "main section[id]"
    );

    const backToTop = document.getElementById("backToTop");

    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");


    // =====================================================
    // SMOOTH NAVIGATION
    // =====================================================

    navLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const targetId = this.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const targetSection =
                document.querySelector(targetId);

            if (!targetSection) {
                return;
            }

            event.preventDefault();

            const navbarHeight =
                navbar ? navbar.offsetHeight : 0;

            const targetPosition =
                targetSection.getBoundingClientRect().top +
                window.scrollY -
                navbarHeight -
                10;

            window.scrollTo({
                top: targetPosition,
                behavior: "smooth"
            });


            // Close Bootstrap mobile navbar
            if (
                navbarMenu &&
                navbarMenu.classList.contains("show")
            ) {

                const collapse =
                    bootstrap.Collapse.getOrCreateInstance(
                        navbarMenu
                    );

                collapse.hide();
            }

        });

    });

    // =====================================================
    // PREMIUM PROJECT FILTER - FLIP LAYOUT
    // =====================================================

    const projectFilterButtons =
        document.querySelectorAll(".project-filter-btn");

    const projectItems =
        Array.from(
            document.querySelectorAll(".project-item")
        );

    let projectFilterRunning = false;


    function shouldShowProject(project, filter) {

        if (filter === "all") {
            return true;
        }

        if (filter === "featured") {

            return (
                project.getAttribute("data-featured")
                === "true"
            );

        }

        return true;
    }


    // =====================================================
    // GET CURRENT PROJECT POSITIONS
    // =====================================================

    function getProjectPositions() {

        const positions = new Map();

        projectItems.forEach(function (project) {

            if (
                !project.classList.contains(
                    "project-hidden"
                )
            ) {

                positions.set(
                    project,
                    project.getBoundingClientRect()
                );

            }

        });

        return positions;
    }


    // =====================================================
    // RUN FLIP ANIMATION
    // =====================================================

    function animateProjectFilter(selectedFilter) {

        if (projectFilterRunning) {
            return;
        }

        projectFilterRunning = true;


        // ---------------------------------------------
        // STEP 1
        // Record current card positions
        // ---------------------------------------------

        const firstPositions =
            getProjectPositions();


        // ---------------------------------------------
        // STEP 2
        // Find cards leaving and entering
        // ---------------------------------------------

        const leavingProjects = [];
        const enteringProjects = [];
        const stayingProjects = [];


        projectItems.forEach(function (project) {

            const shouldShow =
                shouldShowProject(
                    project,
                    selectedFilter
                );

            const currentlyHidden =
                project.classList.contains(
                    "project-hidden"
                );


            if (
                shouldShow &&
                currentlyHidden
            ) {

                enteringProjects.push(
                    project
                );

            }

            else if (
                !shouldShow &&
                !currentlyHidden
            ) {

                leavingProjects.push(
                    project
                );

            }

            else if (
                shouldShow &&
                !currentlyHidden
            ) {

                stayingProjects.push(
                    project
                );

            }

        });


        // ---------------------------------------------
        // STEP 3
        // Fade out cards that are leaving
        // ---------------------------------------------

        leavingProjects.forEach(
            function (project) {

                project.classList.add(
                    "project-leaving"
                );

            }
        );


        // ---------------------------------------------
        // STEP 4
        // Wait for fade-out
        // ---------------------------------------------

        setTimeout(function () {


            // Hide leaving cards

            leavingProjects.forEach(
                function (project) {

                    project.classList.add(
                        "project-hidden"
                    );

                    project.classList.remove(
                        "project-leaving"
                    );

                }
            );


            // -----------------------------------------
            // Prepare entering cards BEFORE showing
            // -----------------------------------------

            enteringProjects.forEach(
                function (project) {

                    project.classList.add(
                        "project-entering"
                    );

                    project.classList.remove(
                        "project-hidden"
                    );

                }
            );


            // Force browser layout calculation

            void document.body.offsetHeight;


            // -----------------------------------------
            // Record new positions
            // -----------------------------------------

            const lastPositions =
                getProjectPositions();


            // -----------------------------------------
            // FLIP existing cards
            // -----------------------------------------

            projectItems.forEach(function (project) {

                if (
                    project.classList.contains(
                        "project-hidden"
                    )
                ) {
                    return;
                }


                const first =
                    firstPositions.get(project);

                const last =
                    lastPositions.get(project);


                if (!first || !last) {
                    return;
                }


                const deltaX =
                    first.left -
                    last.left;

                const deltaY =
                    first.top -
                    last.top;


                if (
                    deltaX !== 0 ||
                    deltaY !== 0
                ) {

                    project.style.transition =
                        "none";

                    project.style.transform =
                        `translate3d(
                        ${deltaX}px,
                        ${deltaY}px,
                        0
                    )`;

                }

            });


            // Force transform state to render

            void document.body.offsetHeight;


            // -----------------------------------------
            // Animate cards into new positions
            // -----------------------------------------

            requestAnimationFrame(function () {

                requestAnimationFrame(function () {


                    projectItems.forEach(
                        function (project) {

                            if (
                                project.classList.contains(
                                    "project-hidden"
                                )
                            ) {
                                return;
                            }


                            project.style.transition =
                                "";

                            project.style.transform =
                                "";

                        }
                    );


                    // ---------------------------------
                    // Animate entering cards
                    // ---------------------------------

                    enteringProjects.forEach(
                        function (project, index) {

                            setTimeout(function () {

                                project.classList.remove(
                                    "project-entering"
                                );

                                project.classList.add(
                                    "project-visible"
                                );

                            }, index * 70);

                        }
                    );


                    // ---------------------------------
                    // Remove helper visible class
                    // ---------------------------------

                    setTimeout(function () {

                        enteringProjects.forEach(
                            function (project) {

                                project.classList.remove(
                                    "project-visible"
                                );

                            }
                        );


                        projectFilterRunning = false;

                    }, 700);

                });

            });

        }, 320);

    }


    // =====================================================
    // FILTER BUTTON EVENTS
    // =====================================================

    projectFilterButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const selectedFilter =
                        this.getAttribute(
                            "data-filter"
                        );


                    if (
                        this.classList.contains(
                            "active"
                        )
                    ) {
                        return;
                    }


                    projectFilterButtons.forEach(
                        function (filterButton) {

                            filterButton.classList.remove(
                                "active"
                            );

                        }
                    );


                    this.classList.add(
                        "active"
                    );


                    animateProjectFilter(
                        selectedFilter
                    );

                }
            );

        }
    );



    // =====================================================
    // ACTIVE NAVIGATION
    // =====================================================

    function updateActiveNavigation() {

        const navbarHeight =
            navbar ? navbar.offsetHeight : 0;

        const scrollPosition =
            window.scrollY +
            navbarHeight +
            120;

        let currentSection = "";


        sections.forEach(function (section) {

            const sectionTop =
                section.offsetTop;

            const sectionHeight =
                section.offsetHeight;

            if (
                scrollPosition >= sectionTop &&
                scrollPosition <
                sectionTop + sectionHeight
            ) {

                currentSection =
                    section.getAttribute("id");

            }

        });


        navLinks.forEach(function (link) {

            link.classList.remove("active");


            if (
                link.getAttribute("href") ===
                "#" + currentSection
            ) {

                link.classList.add("active");

            }

        });

    }


    window.addEventListener(
        "scroll",
        updateActiveNavigation
    );

    window.addEventListener(
        "resize",
        updateActiveNavigation
    );

    updateActiveNavigation();


    // =====================================================
    // NAVBAR SCROLLED STATE
    // =====================================================

    function updateNavbar() {

        if (!navbar) {
            return;
        }

        if (window.scrollY > 30) {

            navbar.classList.add(
                "navbar-scrolled"
            );

        } else {

            navbar.classList.remove(
                "navbar-scrolled"
            );

        }

    }


    window.addEventListener(
        "scroll",
        updateNavbar
    );

    updateNavbar();


    // =====================================================
    // REVEAL ANIMATIONS
    // =====================================================

    const revealElements =
        document.querySelectorAll(".reveal");


    if ("IntersectionObserver" in window) {

        const revealObserver =
            new IntersectionObserver(
                function (entries, observer) {

                    entries.forEach(
                        function (entry) {

                            if (entry.isIntersecting) {

                                entry.target
                                    .classList
                                    .add("visible");

                                observer.unobserve(
                                    entry.target
                                );

                            }

                        }
                    );

                },
                {
                    threshold: 0.12
                }
            );


        revealElements.forEach(
            function (element) {

                revealObserver.observe(
                    element
                );

            }
        );

    } else {

        revealElements.forEach(
            function (element) {

                element.classList.add(
                    "visible"
                );

            }
        );

    }


    // =====================================================
    // SKILL PROGRESS
    // =====================================================

    const skillCards =
        document.querySelectorAll(".skill-card");


    if ("IntersectionObserver" in window) {

        const skillObserver =
            new IntersectionObserver(
                function (entries, observer) {

                    entries.forEach(
                        function (entry) {

                            if (
                                entry.isIntersecting
                            ) {

                                const progressBar =
                                    entry.target
                                        .querySelector(
                                            ".skill-progress"
                                        );

                                if (progressBar) {

                                    let width =
                                        parseInt(
                                            progressBar
                                                .dataset
                                                .width,
                                            10
                                        );

                                    if (
                                        isNaN(width)
                                    ) {

                                        width = 0;

                                    }

                                    width =
                                        Math.min(
                                            100,
                                            Math.max(
                                                0,
                                                width
                                            )
                                        );

                                    progressBar
                                        .style
                                        .width =
                                        width + "%";

                                }

                                observer.unobserve(
                                    entry.target
                                );

                            }

                        }
                    );

                },
                {
                    threshold: 0.35
                }
            );


        skillCards.forEach(
            function (card) {

                skillObserver.observe(
                    card
                );

            }
        );

    } else {

        skillCards.forEach(function (card) {

            const progressBar =
                card.querySelector(
                    ".skill-progress"
                );

            if (progressBar) {

                let width =
                    parseInt(
                        progressBar.dataset.width,
                        10
                    );

                if (isNaN(width)) {
                    width = 0;
                }

                width =
                    Math.min(
                        100,
                        Math.max(
                            0,
                            width
                        )
                    );

                progressBar.style.width =
                    width + "%";
            }

        });

    }


    // =====================================================
    // THEME TOGGLE
    // =====================================================

    const savedTheme =
        localStorage.getItem(
            "portfolio-theme"
        );


    if (savedTheme === "light") {

        document.documentElement
            .setAttribute(
                "data-theme",
                "light"
            );

        if (themeIcon) {

            themeIcon.className =
                "bi bi-sun-fill";

        }

    } else {

        document.documentElement
            .removeAttribute(
                "data-theme"
            );

        if (themeIcon) {

            themeIcon.className =
                "bi bi-moon-stars-fill";

        }

    }


    if (themeToggle) {

        themeToggle.addEventListener(
            "click",
            function () {

                const currentTheme =
                    document.documentElement
                        .getAttribute(
                            "data-theme"
                        );


                if (
                    currentTheme === "light"
                ) {

                    document.documentElement
                        .removeAttribute(
                            "data-theme"
                        );

                    localStorage.setItem(
                        "portfolio-theme",
                        "dark"
                    );

                    if (themeIcon) {

                        themeIcon.className =
                            "bi bi-moon-stars-fill";

                    }

                } else {

                    document.documentElement
                        .setAttribute(
                            "data-theme",
                            "light"
                        );

                    localStorage.setItem(
                        "portfolio-theme",
                        "light"
                    );

                    if (themeIcon) {

                        themeIcon.className =
                            "bi bi-sun-fill";

                    }

                }

            }
        );

    }


    // =====================================================
    // BACK TO TOP
    // =====================================================

    function updateBackToTop() {

        if (!backToTop) {
            return;
        }

        if (window.scrollY > 500) {

            backToTop.classList.add(
                "show"
            );

        } else {

            backToTop.classList.remove(
                "show"
            );

        }

    }


    window.addEventListener(
        "scroll",
        updateBackToTop
    );

    updateBackToTop();


    if (backToTop) {

        window.addEventListener("scroll", () => {
            if (window.scrollY > 500) {
                backToTop.classList.add("show");
            } else {
                backToTop.classList.remove("show");
            }
        });

        backToTop.addEventListener(
            "click",
            function () {

                window.scrollTo({
                    top: 0,
                    behavior: "smooth"
                });

            }
        );

    }

});