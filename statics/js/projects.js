// ================================
// PROJECTS PAGE FUNCTIONALITY
// ================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ================================
    // Initialize AOS
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
    // Global Variables
    // ================================
    const projectsGrid = document.getElementById('projectsGrid');
    const loadingState = document.getElementById('loadingState');
    const emptyState = document.getElementById('emptyState');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('searchInput');
    
    let allProjects = [];
    let currentFilter = 'all';
    let currentSearch = '';
    
    // ================================
    // Load Projects from JSON
    // ================================
    async function loadProjects() {
        try {
            const response = await fetch('https://raw.githubusercontent.com/Bonitabueno/0331project/refs/heads/main/0331project_home/projects.json');
            if (!response.ok) {
                throw new Error('Failed to load projects');
            }
            allProjects = await response.json();
            renderProjects();
            hideLoading();
        } catch (error) {
            console.error('Error loading projects:', error);
            showError();
        }
    }
    
    // ================================
    // Render Projects
    // ================================
    function renderProjects() {
        projectsGrid.innerHTML = '';
        
        let visibleCount = 0;
        
        allProjects.forEach((project, index) => {
            const card = createProjectCard(project, index);
            
            // Apply filters
            const categoryMatch = currentFilter === 'all' || project.status === currentFilter;
            const searchMatch = currentSearch === '' || 
                                project.title.toLowerCase().includes(currentSearch) || 
                                project.description.toLowerCase().includes(currentSearch) ||
                                project.tags.some(tag => tag.toLowerCase().includes(currentSearch));
            
            if (categoryMatch && searchMatch) {
                projectsGrid.appendChild(card);
                visibleCount++;
            }
        });
        
        // Show/hide empty state
        if (visibleCount === 0) {
            emptyState.style.display = 'block';
        } else {
            emptyState.style.display = 'none';
        }
        
        // Reinitialize AOS for new elements
        if (typeof AOS !== 'undefined') {
            AOS.refresh();
        }
    }
    
    // ================================
    // Create Project Card Element
    // ================================
    function createProjectCard(project, index) {
        const article = document.createElement('article');
        article.className = 'project-card';
        article.setAttribute('data-category', project.status);
        article.setAttribute('data-aos', 'fade-up');
        article.setAttribute('data-aos-delay', (index % 4) * 100);
        
        // [수정] status가 'dev'이거나, 링크가 없으면 비활성화 처리
        const isDisabled = project.status === 'dev' || project.externalLink === '#' || !project.externalLink;
        
        const statusBadge = project.status === 'live' 
            ? '<span class="badge badge-live"><i class="fas fa-circle"></i> Live</span>'
            : '<span class="badge badge-dev"><i class="fas fa-code"></i> Dev</span>';
        
        const linkIcon = isDisabled 
            ? '<i class="fas fa-lock"></i>'
            : '<i class="fas fa-external-link-alt"></i>';
        
        const linkClass = isDisabled 
            ? 'project-link project-link-disabled'
            : 'project-link';
        
        const linkTarget = isDisabled ? '' : 'target="_blank"';
        const linkTitle = isDisabled ? 'Coming Soon' : 'Visit Site';
        const finalHref = isDisabled ? '#' : project.externalLink;
        
        article.innerHTML = `
            <div class="project-image">
                <div class="project-image-placeholder">
                    <i class="fas ${project.icon} fa-3x"></i>
                </div>
            </div>
            <div class="project-content">
                <div class="project-header">
                    <h3 class="project-title">${project.title}</h3>
                    ${statusBadge}
                </div>
                <p class="project-description">
                    ${project.description}
                </p>
                <div class="project-meta">
                    <div class="project-tech">
                        ${project.tags.map(tag => `<span class="tech-tag">${tag}</span>`).join('')}
                    </div>
                    <a href="${finalHref}" class="${linkClass}" ${linkTarget} title="${linkTitle}">
                        ${linkIcon}
                    </a>
                </div>
            </div>
        `;
        
        // Add hover effect
        article.addEventListener('mouseenter', function() {
            this.style.zIndex = '10';
        });
        
        article.addEventListener('mouseleave', function() {
            this.style.zIndex = '1';
        });
        
        return article;
    }
    
    // ================================
    // Filter Functionality
    // ================================
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Update active state
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Get filter value
            currentFilter = this.getAttribute('data-filter');
            
            // Re-render projects
            renderProjects();
            
            // Scroll to projects section
            scrollToProjects();
        });
    });
    
    // ================================
    // Search Functionality
    // ================================
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            currentSearch = this.value.toLowerCase().trim();
            renderProjects();
        });
    }
    
    // ================================
    // URL Parameter Handling
    // ================================
    const urlParams = new URLSearchParams(window.location.search);
    const filterParam = urlParams.get('filter');
    
    if (filterParam) {
        const targetButton = document.querySelector(`[data-filter="${filterParam}"]`);
        if (targetButton) {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            targetButton.classList.add('active');
            currentFilter = filterParam;
        }
    }
    
    // ================================
    // Helper Functions
    // ================================
    function hideLoading() {
        if (loadingState) {
            loadingState.style.display = 'none';
        }
    }
    
    function showError() {
        if (loadingState) {
            loadingState.innerHTML = `
                <i class="fas fa-exclamation-triangle fa-3x" style="color: var(--accent-error); margin-bottom: 20px;"></i>
                <p>Failed to load projects. Please try again later.</p>
            `;
        }
    }
    
    function scrollToProjects() {
        const projectsSection = document.querySelector('.projects-section');
        if (projectsSection) {
            const offset = 200;
            const elementPosition = projectsSection.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - offset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    }
    
    // ================================
    // Keyboard Shortcuts
    // ================================
    document.addEventListener('keydown', function(e) {
        // Press '/' to focus search
        if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
            e.preventDefault();
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Press 'Escape' to clear search
        if (e.key === 'Escape') {
            if (searchInput && searchInput === document.activeElement) {
                searchInput.value = '';
                currentSearch = '';
                renderProjects();
                searchInput.blur();
            }
        }
    });
    
    // ================================
    // Ripple Effect for Buttons
    // ================================
    const addRippleEffect = (button, e) => {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    };
    
    // Add ripple to filter buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            addRippleEffect(this, e);
        });
    });
    
    // Add ripple CSS
    const style = document.createElement('style');
    style.textContent = `
        .filter-btn, .btn {
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
    // Initialize - Load Projects
    // ================================
    loadProjects();
});

