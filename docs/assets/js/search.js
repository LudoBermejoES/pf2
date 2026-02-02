/**
 * Pathfinder 2 Player Core - Advanced Search System
 * Uses MiniSearch for fuzzy full-text search with Spanish support
 */

class PF2Search {
  constructor() {
    this.searchIndex = null;
    this.searchData = [];
    this.modal = document.getElementById('searchModal');
    this.input = document.getElementById('searchInput');
    this.results = document.getElementById('searchResults');
    this.clearBtn = document.getElementById('searchClear');
    this.closeBtn = document.getElementById('searchClose');
    this.toggleBtn = document.querySelector('.search-toggle');
    this.filterBtns = document.querySelectorAll('.filter-btn');

    this.currentFilter = 'all';
    this.selectedIndex = -1;
    this.searchResults = [];

    this.init();
  }

  /**
   * Normalize text for search - removes accents/diacritics for Spanish
   * This allows "espadachin" to match "espadachín" and vice versa
   */
  normalizeText(text) {
    if (!text) return '';
    return text
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '') // Remove diacritics
      .toLowerCase();
  }

  async init() {
    await this.loadSearchIndex();
    this.bindEvents();
  }

  async loadSearchIndex() {
    try {
      const response = await fetch('/assets/js/search-index.json');
      if (!response.ok) throw new Error('Search index not found');

      this.searchData = await response.json();

      // Create MiniSearch instance with Spanish-optimized settings
      this.searchIndex = new MiniSearch({
        fields: ['title', 'content', 'category', 'tags', 'normalizedTitle', 'normalizedContent'],
        storeFields: ['title', 'url', 'category', 'content'],
        searchOptions: {
          boost: { title: 10, normalizedTitle: 8, tags: 5, category: 3 },
          fuzzy: 0.2, // Allow ~20% character errors (typos)
          prefix: true, // Enable prefix search
          combineWith: 'OR' // Match any term
        },
        // Custom tokenizer that handles Spanish better
        tokenize: (text) => {
          // Split on whitespace and punctuation, keep words of 2+ chars
          return text.toLowerCase().match(/[\p{L}\p{N}]{2,}/gu) || [];
        },
        // Process terms to normalize accents
        processTerm: (term) => this.normalizeText(term)
      });

      // Add documents with normalized versions for accent-insensitive search
      const documents = this.searchData.map((doc, index) => ({
        id: index,
        title: doc.title,
        content: doc.content,
        category: doc.category,
        tags: Array.isArray(doc.tags) ? doc.tags.join(' ') : (doc.tags || ''),
        url: doc.url,
        // Normalized versions for accent-insensitive matching
        normalizedTitle: this.normalizeText(doc.title),
        normalizedContent: this.normalizeText(doc.content)
      }));

      this.searchIndex.addAll(documents);

      console.log('MiniSearch index loaded:', this.searchData.length, 'documents');
    } catch (error) {
      console.error('Error loading search index:', error);
      this.showError('No se pudo cargar el índice de búsqueda.');
    }
  }

  bindEvents() {
    // Open modal
    this.toggleBtn?.addEventListener('click', () => this.open());

    // Close modal
    this.closeBtn?.addEventListener('click', () => this.close());
    this.modal?.querySelector('.search-modal-backdrop')?.addEventListener('click', () => this.close());

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      // Cmd/Ctrl + K to open search
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        this.open();
      }

      // Escape to close
      if (e.key === 'Escape' && this.modal?.classList.contains('active')) {
        this.close();
      }

      // Arrow navigation in results
      if (this.modal?.classList.contains('active')) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          this.navigateResults(1);
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          this.navigateResults(-1);
        } else if (e.key === 'Enter' && this.selectedIndex >= 0) {
          e.preventDefault();
          this.selectResult();
        }
      }
    });

    // Search input with debounce
    let debounceTimer;
    this.input?.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        this.performSearch(this.input.value);
      }, 100); // 100ms debounce for responsive feel
      this.clearBtn?.classList.toggle('visible', this.input.value.length > 0);
    });

    // Clear button
    this.clearBtn?.addEventListener('click', () => {
      this.input.value = '';
      this.input.focus();
      this.clearBtn.classList.remove('visible');
      this.showPlaceholder();
    });

    // Filter buttons
    this.filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        this.filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.currentFilter = btn.dataset.filter;
        if (this.input.value) {
          this.performSearch(this.input.value);
        }
      });
    });
  }

  open() {
    this.modal?.classList.add('active');
    this.input?.focus();
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.modal?.classList.remove('active');
    document.body.style.overflow = '';
    this.input.value = '';
    this.clearBtn?.classList.remove('visible');
    this.showPlaceholder();
  }

  performSearch(query) {
    if (!query.trim()) {
      this.showPlaceholder();
      return;
    }

    if (!this.searchIndex) {
      this.showError('El índice de búsqueda aún no está listo.');
      return;
    }

    try {
      // Search with MiniSearch - fuzzy and prefix enabled
      let results = this.searchIndex.search(query, {
        fuzzy: 0.25, // Slightly more tolerance for user queries
        prefix: true,
        combineWith: 'OR'
      });

      // Filter by category if needed
      if (this.currentFilter !== 'all') {
        results = results.filter(result => {
          return result.category === this.currentFilter;
        });
      }

      this.searchResults = results.slice(0, 20); // Limit to 20 results
      this.selectedIndex = -1;

      if (this.searchResults.length === 0) {
        // Try with more fuzzy tolerance
        results = this.searchIndex.search(query, {
          fuzzy: 0.4, // More tolerant for difficult queries
          prefix: true,
          combineWith: 'OR'
        });

        if (this.currentFilter !== 'all') {
          results = results.filter(result => result.category === this.currentFilter);
        }

        this.searchResults = results.slice(0, 20);

        if (this.searchResults.length === 0) {
          this.showNoResults(query);
        } else {
          this.renderResults(query);
        }
      } else {
        this.renderResults(query);
      }
    } catch (error) {
      console.error('Search error:', error);
      this.showError('Error al realizar la búsqueda.');
    }
  }

  renderResults(query) {
    const html = this.searchResults.map((result, index) => {
      const excerpt = this.getExcerpt(result.content, query);
      const highlightedTitle = this.highlightMatch(result.title, query);
      const highlightedExcerpt = this.highlightMatch(excerpt, query);

      return `
        <a href="${result.url}" class="search-result-item" data-index="${index}">
          <span class="result-category">${this.getCategoryLabel(result.category)}</span>
          <span class="result-title">${highlightedTitle}</span>
          <p class="result-excerpt">${highlightedExcerpt}</p>
        </a>
      `;
    }).join('');

    this.results.innerHTML = html;

    // Add hover handlers
    this.results.querySelectorAll('.search-result-item').forEach((item, index) => {
      item.addEventListener('mouseenter', () => {
        this.selectedIndex = index;
        this.updateSelection();
      });
    });
  }

  getExcerpt(content, query) {
    if (!content) return '';

    const normalizedContent = this.normalizeText(content);
    const normalizedQuery = this.normalizeText(query.split(/\s+/)[0]);
    const index = normalizedContent.indexOf(normalizedQuery);

    if (index === -1) {
      return content.substring(0, 150) + '...';
    }

    const start = Math.max(0, index - 50);
    const end = Math.min(content.length, index + 100);
    let excerpt = content.substring(start, end);

    if (start > 0) excerpt = '...' + excerpt;
    if (end < content.length) excerpt = excerpt + '...';

    return excerpt;
  }

  highlightMatch(text, query) {
    if (!query || !text) return text;

    const words = query.trim().split(/\s+/);
    let result = text;

    words.forEach(word => {
      if (word.length < 2) return;

      // Create regex that matches both accented and non-accented versions
      const normalizedWord = this.normalizeText(word);

      // Build a regex pattern that matches characters with or without accents
      let pattern = '';
      for (const char of normalizedWord) {
        const accentMap = {
          'a': '[aáàâäã]',
          'e': '[eéèêë]',
          'i': '[iíìîï]',
          'o': '[oóòôöõ]',
          'u': '[uúùûü]',
          'n': '[nñ]',
          'c': '[cç]'
        };
        pattern += accentMap[char] || this.escapeRegExp(char);
      }

      const regex = new RegExp(`(${pattern})`, 'gi');
      result = result.replace(regex, '<mark>$1</mark>');
    });

    return result;
  }

  escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  getCategoryLabel(category) {
    const labels = {
      introduccion: 'Intro',
      ascendencias: 'Ascendencia',
      clases: 'Clase',
      habilidades: 'Habilidad',
      dotes: 'Dote',
      equipo: 'Equipo',
      conjuros: 'Conjuro',
      reglas: 'Regla',
      apendices: 'Apéndice',
      ambientacion: 'Ambientación'
    };
    return labels[category] || category || 'General';
  }

  navigateResults(direction) {
    if (this.searchResults.length === 0) return;

    this.selectedIndex += direction;

    if (this.selectedIndex < 0) {
      this.selectedIndex = this.searchResults.length - 1;
    } else if (this.selectedIndex >= this.searchResults.length) {
      this.selectedIndex = 0;
    }

    this.updateSelection();
  }

  updateSelection() {
    this.results.querySelectorAll('.search-result-item').forEach((item, index) => {
      item.classList.toggle('selected', index === this.selectedIndex);
      if (index === this.selectedIndex) {
        item.scrollIntoView({ block: 'nearest' });
      }
    });
  }

  selectResult() {
    const selectedItem = this.results.querySelector('.search-result-item.selected');
    if (selectedItem) {
      window.location.href = selectedItem.href;
    }
  }

  showPlaceholder() {
    this.results.innerHTML = `
      <div class="search-placeholder">
        <div class="placeholder-icon">🔍</div>
        <p>Escribe para buscar en todo el contenido</p>
        <div class="search-tips">
          <p><strong>Consejos de búsqueda:</strong></p>
          <ul>
            <li>Busca clases: <code>espadachin</code> o <code>espadachín</code></li>
            <li>Busca conjuros: <code>bola de fuego</code></li>
            <li>Busca reglas: <code>flanqueo</code></li>
            <li>Tolera errores: <code>gerero</code> encuentra <code>guerrero</code></li>
          </ul>
        </div>
      </div>
    `;
  }

  showNoResults(query) {
    // Get suggestions using MiniSearch autoSuggest
    let suggestions = [];
    if (this.searchIndex) {
      try {
        suggestions = this.searchIndex.autoSuggest(query, {
          fuzzy: 0.3,
          prefix: true
        }).slice(0, 3);
      } catch (e) {
        console.warn('AutoSuggest error:', e);
      }
    }

    let suggestionsHtml = '';
    if (suggestions.length > 0) {
      suggestionsHtml = `
        <p>¿Quisiste decir?</p>
        <div class="search-suggestions">
          ${suggestions.map(s => `<button class="suggestion-btn" data-suggestion="${s.suggestion}">${s.suggestion}</button>`).join('')}
        </div>
      `;
    }

    this.results.innerHTML = `
      <div class="search-no-results">
        <p>No se encontraron resultados para "<strong>${this.escapeHtml(query)}</strong>"</p>
        ${suggestionsHtml}
        <p>Intenta con términos más generales o revisa la ortografía.</p>
      </div>
    `;

    // Add click handlers for suggestions
    this.results.querySelectorAll('.suggestion-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.input.value = btn.dataset.suggestion;
        this.performSearch(btn.dataset.suggestion);
      });
    });
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  showError(message) {
    this.results.innerHTML = `
      <div class="search-no-results">
        <p>${message}</p>
      </div>
    `;
  }
}

// Initialize search when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.pf2Search = new PF2Search();
});
