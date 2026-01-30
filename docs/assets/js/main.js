/**
 * Pathfinder 2 Player Core - Main JavaScript
 * Handles navigation, sidebar, and table of contents
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initSidebar();
  initTableOfContents();
  initActiveLinks();
  initSmoothScroll();
});

/**
 * Mobile Navigation Toggle
 */
function initNavigation() {
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  const sidebar = document.querySelector('.sidebar');

  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navLinks?.classList.toggle('open');
      sidebar?.classList.toggle('open');

      // Animate hamburger menu
      navToggle.classList.toggle('active');
    });
  }

  // Close nav when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.main-nav') && !e.target.closest('.sidebar')) {
      navLinks?.classList.remove('open');
      sidebar?.classList.remove('open');
      navToggle?.classList.remove('active');
    }
  });
}

/**
 * Sidebar Collapsible Sections
 */
function initSidebar() {
  const sidebarSections = document.querySelectorAll('.sidebar-section');

  sidebarSections.forEach(section => {
    const heading = section.querySelector('.sidebar-heading');
    const links = section.querySelector('.sidebar-links');

    if (heading && links) {
      heading.style.cursor = 'pointer';
      heading.addEventListener('click', () => {
        section.classList.toggle('collapsed');
        links.style.display = section.classList.contains('collapsed') ? 'none' : 'block';
      });
    }
  });
}

/**
 * Generate Table of Contents from headings
 */
function initTableOfContents() {
  const tocContainer = document.getElementById('toc');
  const content = document.querySelector('.page-content');

  if (!tocContainer || !content) return;

  const headings = content.querySelectorAll('h2, h3');
  if (headings.length < 2) {
    tocContainer.parentElement?.remove();
    return;
  }

  const toc = document.createElement('ul');

  headings.forEach((heading, index) => {
    // Generate ID if not present
    if (!heading.id) {
      heading.id = `section-${index}`;
    }

    const li = document.createElement('li');
    li.style.paddingLeft = heading.tagName === 'H3' ? '1rem' : '0';

    const a = document.createElement('a');
    a.href = `#${heading.id}`;
    a.textContent = heading.textContent;

    li.appendChild(a);
    toc.appendChild(li);
  });

  tocContainer.appendChild(toc);

  // Highlight active section on scroll
  let ticking = false;

  const updateActiveSection = () => {
    const scrollPos = window.scrollY + 100;

    let activeHeading = null;
    headings.forEach(heading => {
      if (heading.offsetTop <= scrollPos) {
        activeHeading = heading;
      }
    });

    tocContainer.querySelectorAll('a').forEach(link => {
      link.classList.remove('active');
      if (activeHeading && link.getAttribute('href') === `#${activeHeading.id}`) {
        link.classList.add('active');
      }
    });

    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(updateActiveSection);
      ticking = true;
    }
  });

  updateActiveSection();
}

/**
 * Highlight active links in sidebar based on current URL
 */
function initActiveLinks() {
  const currentPath = window.location.pathname;
  const sidebarLinks = document.querySelectorAll('.sidebar-links a');

  sidebarLinks.forEach(link => {
    const linkPath = link.getAttribute('href');
    if (linkPath && currentPath.includes(linkPath.replace(/\/$/, ''))) {
      link.classList.add('active');

      // Expand parent section if collapsed
      const section = link.closest('.sidebar-section');
      if (section) {
        section.classList.remove('collapsed');
        const links = section.querySelector('.sidebar-links');
        if (links) links.style.display = 'block';
      }
    }
  });
}

/**
 * Smooth scroll for anchor links
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });

        // Update URL without scrolling
        history.pushState(null, '', targetId);
      }
    });
  });
}

/**
 * Convert action symbols in text
 * ◆ = 1 action, ◆◆ = 2 actions, ◆◆◆ = 3 actions, ↺ = reaction, ◇ = free
 */
function convertActionSymbols() {
  const content = document.querySelector('.page-content');
  if (!content) return;

  const symbolMap = {
    '◆◆◆': '<span class="action-cost action-3" title="3 acciones">3</span>',
    '◆◆': '<span class="action-cost action-2" title="2 acciones">2</span>',
    '◆': '<span class="action-cost action-1" title="1 acción">1</span>',
    '↺': '<span class="action-cost action-r" title="Reacción">R</span>',
    '◇': '<span class="action-cost action-f" title="Acción libre">F</span>'
  };

  // Process text nodes to avoid breaking HTML
  const walker = document.createTreeWalker(
    content,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );

  const textNodes = [];
  let node;
  while (node = walker.nextNode()) {
    for (const symbol of Object.keys(symbolMap)) {
      if (node.textContent.includes(symbol)) {
        textNodes.push(node);
        break;
      }
    }
  }

  textNodes.forEach(textNode => {
    let html = textNode.textContent;
    for (const [symbol, replacement] of Object.entries(symbolMap)) {
      html = html.split(symbol).join(replacement);
    }

    const span = document.createElement('span');
    span.innerHTML = html;
    textNode.parentNode.replaceChild(span, textNode);
  });
}

// Run action symbol conversion after page load
window.addEventListener('load', convertActionSymbols);
