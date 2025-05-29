// scrolls to top when logo is clicked
document.addEventListener('DOMContentLoaded', function () {
    const logo = document.getElementById('logo');
    const arrow = document.querySelector('.arrow-up');

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    logo.addEventListener('click', scrollToTop);
    arrow.addEventListener('click', scrollToTop);
});

// VECTOR SVG MOVING WITH THE MOUSE

// Select the header element
const homeElement = document.getElementById('header');
// Select the #dots2 element
const dots = document.querySelector("#dots2");

// Add event listeners
homeElement.addEventListener('mousemove', move);


function move(event) {
    // Get the mouse coordinates
    let mouseX = event.clientX / 30;
    let mouseY = event.clientY / 30;
    // Update the position of the SVG
    dots.style.left = mouseX + 'px';
    dots.style.top = mouseY + 'px';
}


// NAV ANIMATION 

document.addEventListener('DOMContentLoaded', function () {
    var contentSections = document.querySelectorAll('.content-section');
    var navigationLinks = document.querySelectorAll('nav a');

    // Add click event listener to each navigation link
    navigationLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default behavior
            smoothScroll(link.getAttribute('href'));
        });
    });

    // Add scroll event listener to window
    window.addEventListener('scroll', function () {
        updateNavigation();
    });

    // Update navigation on page load
    updateNavigation();

    // FUNCTIONS
    function updateNavigation() {
        var windowHeight = window.innerHeight;
        var windowScrollTop = window.pageYOffset;

        contentSections.forEach(function (section) {
            var sectionTop = section.getBoundingClientRect().top + windowScrollTop;
            var sectionHeight = section.offsetHeight;
            var sectionName = section.id;
            var navigationMatch = document.querySelector('nav a[href="#' + sectionName + '"]');

            if (sectionTop - windowHeight / 2 < windowScrollTop &&
                sectionTop + sectionHeight - windowHeight / 2 > windowScrollTop) {
                navigationMatch.classList.add('active-section');
            } else {
                navigationMatch.classList.remove('active-section');
            }
        });
    }

    function smoothScroll(target) {
        var targetElement = document.querySelector(target);
        if (targetElement) {
            var targetOffset = targetElement.getBoundingClientRect().top + window.pageYOffset;
            window.scrollTo({
                top: targetOffset,
                behavior: 'smooth'
            });
        }
    }
});

// ADDING AND REMOVING CLASSES FOR EASE-IN AND EASE-OUT EFFECT WHEN IN VIEWPORT

document.addEventListener('DOMContentLoaded', function () {
    const projects = document.querySelectorAll('.projects .project');

    function checkVisibility(element) {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;

        // Check if the element is in the viewport
        const isVisible = (elementTop <= window.innerHeight && elementBottom >= 0);

        return isVisible;
    }

    function handleScroll() {
        projects.forEach(project => {
            if (checkVisibility(project)) {
                project.classList.add('visible');
            } else {
                project.classList.remove('visible');
            }
        });
    }

    // Initial check
    handleScroll();

    // Listen for scroll event
    window.addEventListener('scroll', handleScroll);
});

document.addEventListener('DOMContentLoaded', function () {
    const leftSection = document.querySelector('.left-section');
    const rightSection = document.querySelector('.right-section');
    const aboutMe = document.querySelector('.section-title-left');
    const skillsTitle = document.querySelector('.section-title-right');
    const skills = document.querySelectorAll('.skills .skill');
    const toolsTitle = document.querySelector('.section-title-tools');
    const cards = document.querySelector('.cards');
    const contact = document.querySelector('.contact');


    function checkVisibility(element) {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;

        // Check if the element is in the viewport
        const isVisible = (elementTop <= window.innerHeight && elementBottom >= 0);

        return isVisible;
    }

    function handleScroll() {
        if (checkVisibility(aboutMe)) {
            aboutMe.classList.add('visible');
        } else {
            aboutMe.classList.remove('visible');
        }
        if (checkVisibility(skillsTitle)) {
            skillsTitle.classList.add('visible');
        } else {
            skillsTitle.classList.remove('visible');
        }
        if (checkVisibility(leftSection)) {
            leftSection.classList.add('visible');
        } else {
            leftSection.classList.remove('visible');
        }

        if (checkVisibility(rightSection)) {
            rightSection.classList.add('visible');
        } else {
            rightSection.classList.remove('visible');
        }

        skills.forEach((skill, index) => {
            setTimeout(() => {
                if (checkVisibility(skill)) {
                    skill.classList.add('visible');
                } else {
                    skill.classList.remove('visible');
                }
            }, index * 600); // Delay each item by 600ms
        });
        if (checkVisibility(toolsTitle)) {
            toolsTitle.classList.add('visible');
        } else {
            toolsTitle.classList.remove('visible');
        }
        if (checkVisibility(cards)) {
            cards.classList.add('visible');
        } else {
            cards.classList.remove('visible');
        }
        if (checkVisibility(contact)) {
            contact.classList.add('visible');
        } else {
            contact.classList.remove('visible');
        }
    }

    // Initial check
    handleScroll();

    // Listen for scroll event
    window.addEventListener('scroll', handleScroll);
});

// ADDING GRADIENT BORDERS TO TOOLS ON MOUSEOVER
document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mouseover', function () {
            this.classList.add('border-gradient-purple');
        });

        card.addEventListener('mouseout', function () {
            this.classList.remove('border-gradient-purple');
            // Resetting border-image-slice to initial state

        });
    });
});


