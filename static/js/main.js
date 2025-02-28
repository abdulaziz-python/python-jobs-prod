document.addEventListener('DOMContentLoaded', () => {
    // Handle form interactions and validation
    initializeForms();
    
    // Setup message dismissal
    setupMessageDismissal();
    
    // Enhance job search
    enhanceJobSearch();
    
    // Add mobile menu toggle
    setupMobileMenu();
    
    // Setup dark mode toggle
    setupDarkMode();
    
    // Add animation to job cards
    animateJobCards();
    
    // Initialize file inputs
    initializeFileInputs();
});

function initializeForms() {
    // Add focus and blur effects to form fields
    const formGroups = document.querySelectorAll('.form-group');
    
    formGroups.forEach(group => {
        const input = group.querySelector('input, select, textarea');
        if (!input) return;
        
        // Add focused class when input is focused
        input.addEventListener('focus', () => {
            group.classList.add('focused');
        });
        
        // Remove focused class when input loses focus
        input.addEventListener('blur', () => {
            if (input.value === '') {
                group.classList.remove('focused');
            }
        });
        
        // Check initial state on page load
        if (input.value !== '') {
            group.classList.add('focused');
        }
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Basic validation for required fields
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                const formGroup = field.closest('.form-group');
                
                if (field.value.trim() === '') {
                    isValid = false;
                    formGroup.classList.add('error');
                    
                    // Add error message if it doesn't exist yet
                    if (!formGroup.querySelector('.form-error')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.className = 'form-error';
                        errorMsg.textContent = 'Bu maydon to\'ldirilishi shart';
                        formGroup.appendChild(errorMsg);
                    }
                } else {
                    formGroup.classList.remove('error');
                    
                    // Remove error message if it exists
                    const errorMsg = formGroup.querySelector('.form-error');
                    if (errorMsg) {
                        formGroup.removeChild(errorMsg);
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            } else {
                // Show loading state on submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = `<span class="spinner"></span> Yuborilmoqda...`;
                    submitBtn.disabled = true;
                    
                    // Reset button state if form submission takes too long (for demo purposes)
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }, 8000);
                }
            }
        });
    });
}

function setupMessageDismissal() {
    // Add close buttons to messages
    const messages = document.querySelectorAll('.message');
    
    messages.forEach(message => {
        // Create close button if it doesn't exist
        if (!message.querySelector('.message-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'message-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.setAttribute('aria-label', 'Close message');
            
            closeBtn.addEventListener('click', () => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
            
            message.appendChild(closeBtn);
        }
        
        // Add entrance animation
        message.style.animation = 'slideIn 0.3s ease-out forwards';
        
        // Auto-dismiss success messages after 5 seconds
        if (message.classList.contains('message-success')) {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }, 5000);
        }
    });
}

function enhanceJobSearch() {
    const searchInput = document.querySelector('.search-form input[name="q"]');
    if (!searchInput) return;
    
    // Create suggestions container
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions';
    suggestionsContainer.style.display = 'none';
    searchInput.parentNode.appendChild(suggestionsContainer);
    
    // Add event listeners for search input
    searchInput.addEventListener('input', debounce(() => {
        const query = searchInput.value.trim();
        
        // Simple demo suggestions (in a real app, this would call an API)
        if (query.length >= 2) {
            // Demo function to simulate API call
            simulateSearchSuggestions(query, suggestionsContainer);
            suggestionsContainer.style.display = 'block';
        } else {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none';
        }
    }, 300));
    
    // Add keyboard navigation for suggestions
    searchInput.addEventListener('keydown', (e) => {
        const suggestions = suggestionsContainer.querySelectorAll('.search-suggestion');
        if (!suggestions.length) return;
        
        // Find currently focused suggestion
        const focused = suggestionsContainer.querySelector('.search-suggestion.focused');
        let index = -1;
        
        if (focused) {
            Array.from(suggestions).forEach((item, i) => {
                if (item === focused) index = i;
            });
        }
        
        // Arrow down
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (focused) focused.classList.remove('focused');
            
            // Focus next suggestion or first if at end
            index = (index + 1) % suggestions.length;
            suggestions[index].classList.add('focused');
            suggestions[index].scrollIntoView({ block: 'nearest' });
        }
        
        // Arrow up
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (focused) focused.classList.remove('focused');
            
            // Focus previous suggestion or last if at beginning
            index = (index - 1 + suggestions.length) % suggestions.length;
            suggestions[index].classList.add('focused');
            suggestions[index].scrollIntoView({ block: 'nearest' });
        }
        
        // Enter to select focused suggestion
        if (e.key === 'Enter' && focused) {
            e.preventDefault();
            searchInput.value = focused.textContent;
            suggestionsContainer.style.display = 'none';
        }
        
        // Escape to close suggestions
        if (e.key === 'Escape') {
            suggestionsContainer.style.display = 'none';
        }
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.style.display = 'none';
        }
    });
}

function simulateSearchSuggestions(query, container) {
    // Demo suggestions - in a real app, this would fetch from an API
    const demoSuggestions = [
        `Python ${query}`,
        `Django ${query}`,
        `FastAPI ${query}`,
        `Flask ${query}`,
        `TensorFlow ${query}`
    ];
    
    container.innerHTML = '';
    
    demoSuggestions.forEach(suggestion => {
        const item = document.createElement('div');
        item.className = 'search-suggestion';
        item.textContent = suggestion;
        
        item.addEventListener('mouseover', () => {
            // Remove focused class from all suggestions
            container.querySelectorAll('.search-suggestion').forEach(s => {
                s.classList.remove('focused');
            });
            
            // Add focused class to current suggestion
            item.classList.add('focused');
        });
        
        item.addEventListener('click', () => {
            document.querySelector('.search-form input[name="q"]').value = suggestion;
            container.style.display = 'none';
            
            // Submit form if there's a search button
            const searchButton = document.querySelector('.search-form button[type="submit"]');
            if (searchButton) {
                searchButton.click();
            }
        });
        
        container.appendChild(item);
    });
}

function setupMobileMenu() {
    const header = document.querySelector('.header');
    if (!header) return;
    
    // Create mobile menu toggle
    const mobileMenuToggle = document.createElement('button');
    mobileMenuToggle.className = 'mobile-menu-toggle';
    mobileMenuToggle.setAttribute('aria-label', 'Toggle navigation menu');
    mobileMenuToggle.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
    `;
    
    const nav = header.querySelector('.nav');
    if (nav) {
        const headerInner = header.querySelector('.header-inner');
        if (headerInner) {
            headerInner.insertBefore(mobileMenuToggle, nav);
            
            // Add mobile styling and toggle functionality
            const mediaQuery = window.matchMedia('(max-width: 768px)');
            
            function handleMobileLayout(e) {
                if (e.matches) {
                    mobileMenuToggle.style.display = 'block';
                    nav.style.display = 'none';
                    nav.style.width = '100%';
                    nav.style.flexDirection = 'column';
                    nav.style.alignItems = 'center';
                    nav.style.padding = '1rem 0';
                    nav.style.marginTop = '1rem';
                    nav.style.borderTop = '1px solid var(--color-border)';
                } else {
                    mobileMenuToggle.style.display = 'none';
                    nav.style.display = 'flex';
                    nav.style.flexDirection = 'row';
                    nav.style.borderTop = 'none';
                    nav.style.padding = '0';
                    nav.style.marginTop = '0';
                }
            }
            
            // Initial check
            handleMobileLayout(mediaQuery);
            
            // Add listener for window resize
            mediaQuery.addEventListener('change', handleMobileLayout);
            
            // Toggle menu on click
            mobileMenuToggle.addEventListener('click', () => {
                if (nav.style.display === 'none' || !nav.style.display) {
                    nav.style.display = 'flex';
                    mobileMenuToggle.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    `;
                } else {
                    nav.style.display = 'none';
                    mobileMenuToggle.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="3" y1="12" x2="21" y2="12"></line>
                            <line x1="3" y1="6" x2="21" y2="6"></line>
                            <line x1="3" y1="18" x2="21" y2="18"></line>
                        </svg>
                    `;
                }
            });
        }
    }
}

function setupDarkMode() {
    // Check for saved theme preference or use the user's system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Default to dark mode
    if (savedTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    
    // Create dark mode toggle
    const header = document.querySelector('.header-inner');
    if (header) {
        const darkModeToggle = document.createElement('button');
        darkModeToggle.className = 'theme-toggle';
        darkModeToggle.setAttribute('aria-label', 'Toggle dark mode');
        
        // Set initial icon based on current theme
        const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
        darkModeToggle.innerHTML = isDarkMode ? 
            `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>` :
            `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
        
        // Add event listener for theme toggle
        darkModeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update icon
            darkModeToggle.innerHTML = newTheme === 'dark' ? 
                `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>` :
                `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
        });
        
        // Add to DOM
        const nav = header.querySelector('.nav');
        if (nav) {
            nav.appendChild(darkModeToggle);
        } else {
            header.appendChild(darkModeToggle);
        }
    }
}

function animateJobCards() {
    // Add entrance animation to job cards
    const jobCards = document.querySelectorAll('.job-card');
    jobCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        // Stagger the animations
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });
}

function initializeFileInputs() {
    // Enhance file inputs with preview and better UX
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        // Skip if already enhanced
        if (input.closest('.file-input-wrapper')) return;
        
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'file-input-wrapper';
        
        // Create button-like display
        const button = document.createElement('div');
        button.className = 'file-input-button';
        button.textContent = 'Fayl yuklash';
        
        // Create file name display
        const fileNameDisplay = document.createElement('div');
        fileNameDisplay.className = 'file-name-display';
        fileNameDisplay.textContent = 'Hech qanday fayl tanlanmagan';
        
        // Replace input with enhanced version
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(button);
        wrapper.appendChild(input);
        wrapper.after(fileNameDisplay);
        
        // Update file name display when file selected
        input.addEventListener('change', () => {
            if (input.files.length > 0) {
                fileNameDisplay.textContent = input.files[0].name;
            } else {
                fileNameDisplay.textContent = 'Hech qanday fayl tanlanmagan';
            }
        });
    });
}

// Utility function to debounce inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

