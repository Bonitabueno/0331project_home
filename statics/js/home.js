// ================================
// HOME PAGE FUNCTIONALITY
// ================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ================================
    // Initialize AOS (Animate On Scroll)
    // ================================
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100
        });
    }
    
    // ================================
    // Project Cards Hover Effect
    // ================================
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.zIndex = '10';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.zIndex = '1';
        });
    });
    
    // ================================
    // Parallax Effect for Hero Orbs
    // ================================
    const heroOrbs = document.querySelectorAll('.gradient-orb');
    
    if (heroOrbs.length > 0) {
        window.addEventListener('mousemove', (e) => {
            const mouseX = e.clientX / window.innerWidth;
            const mouseY = e.clientY / window.innerHeight;
            
            heroOrbs.forEach((orb, index) => {
                const speed = (index + 1) * 10;
                const x = (mouseX - 0.5) * speed;
                const y = (mouseY - 0.5) * speed;
                
                orb.style.transform = `translate(${x}px, ${y}px)`;
            });
        });
    }
    
    // ================================
    // Smooth Reveal on Scroll
    // ================================
    const revealElements = document.querySelectorAll('[data-aos]');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('aos-animate');
            }
        });
    }, {
        threshold: 0.1
    });
    
    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
    
    // ================================
    // Dynamic Year in Footer
    // ================================
    const currentYear = new Date().getFullYear();
    const yearElements = document.querySelectorAll('.footer-bottom p');
    yearElements.forEach(el => {
        if (el.textContent.includes('2026')) {
            el.textContent = el.textContent.replace('2026', currentYear);
        }
    });
    
    // ================================
    // Add loading state to external links
    // ================================
    const externalLinks = document.querySelectorAll('a[target="_blank"]');
    externalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add visual feedback
            this.style.opacity = '0.6';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 200);
        });
    });
    
    // ================================
    // Hero CTA Button Ripple Effect
    // ================================
    const ctaButtons = document.querySelectorAll('.btn-primary, .btn-outline');
    
    ctaButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add ripple CSS dynamically
    const style = document.createElement('style');
    style.textContent = `
        .btn {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});


document.addEventListener('DOMContentLoaded', async function() {
    const grid = document.getElementById('featured-grid');
    if (!grid) {
        console.error('featured-grid not found!');
        return;
    }
    try {
        const response = await fetch('https://raw.githubusercontent.com/Bonitabueno/0331project/refs/heads/main/0331project_home/projects.json');
        const projects = await response.json();
        
        grid.innerHTML = projects.map((project, index) => {
            
            const isDisabled = !project.externalLink || project.externalLink === '#';
            const linkIcon = isDisabled ? '<i class="fas fa-lock"></i>' : '<i class="fas fa-external-link-alt"></i>';
            const linkClass = isDisabled ? 'project-link project-link-disabled' : 'project-link';
            const linkTarget = isDisabled ? '' : 'target="_blank"';
            const linkTitle = isDisabled ? 'Coming Soon' : 'Visit Site';

            return `
            <article class="project-card" data-aos="fade-up" data-aos-delay="${index * 100}">
                <div class="project-image">
                    <div class="project-image-placeholder">
                        <i class="fas ${project.icon} fa-3x"></i>
                    </div>
                </div>
                <div class="project-content">
                    <div class="project-header">
                        <h3 class="project-title">${project.title}</h3>
                        <span class="badge badge-${project.status}">
                            <i class="fas ${project.status === 'live' ? 'fa-circle' : 'fa-code'}"></i> 
                            ${project.status === 'live' ? 'Live' : 'Dev'}
                        </span>
                    </div>
                    <p class="project-description">${project.description}</p>
                    <div class="project-meta">
                        <div class="project-tech">
                            ${project.tags.map(tag => `<span class="tech-tag">${tag}</span>`).join('')}
                        </div>
                        <a href="${project.externalLink}" class="${linkClass}" ${linkTarget} title="${linkTitle}">
                            ${linkIcon}
                        </a>
                    </div>
                </div>
            </article>
            `;
        }).join('');

        if (typeof AOS !== 'undefined') {
            AOS.refresh();
        }
    } catch (error) {
        console.error('Error loading projects:', error);
    }
});