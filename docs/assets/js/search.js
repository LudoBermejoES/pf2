/**
 * Pathfinder 2 Player Core - Advanced Search System
 * Uses Lunr.js for full-text search with Spanish support
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

  async init() {
    await this.loadSearchIndex();
    this.bindEvents();
  }

  async loadSearchIndex() {
    try {
      const response = await fetch('/assets/js/search-index.json');
      if (!response.ok) throw new Error('Search index not found');

      this.searchData = await response.json();

      // Build Lunr index - documents must be added inside the callback
      const searchData = this.searchData;
      this.searchIndex = lunr(function() {
        this.ref('id');
        this.field('title', { boost: 10 });
        this.field('content');
        this.field('category', { boost: 5 });
        this.field('tags', { boost: 3 });

        // Spanish stemmer support (basic)
        this.pipeline.remove(lunr.stemmer);
        this.pipeline.remove(lunr.stopWordFilter);

        this.searchPipeline.remove(lunr.stemmer);
        this.searchPipeline.remove(lunr.stopWordFilter);

        // Add documents inside callback (required by Lunr)
        searchData.forEach((doc, index) => {
          this.add({
            id: index,
            title: doc.title,
            content: doc.content,
            category: doc.category,
            tags: doc.tags?.join(' ') || ''
          });
        });
      });

      console.log('Search index loaded:', this.searchData.length, 'documents');
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

    // Search input
    this.input?.addEventListener('input', () => {
      this.performSearch(this.input.value);
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
      // Search with wildcards for partial matches
      const searchQuery = query.trim().split(/\s+/).map(term => `${term}* ${term}`).join(' ');
      let results = this.searchIndex.search(searchQuery);

      // Filter by category if needed
      if (this.currentFilter !== 'all') {
        results = results.filter(result => {
          const doc = this.searchData[result.ref];
          return doc.category === this.currentFilter;
        });
      }

      this.searchResults = results.slice(0, 20); // Limit to 20 results
      this.selectedIndex = -1;

      if (this.searchResults.length === 0) {
        this.showNoResults(query);
      } else {
        this.renderResults(query);
      }
    } catch (error) {
      console.error('Search error:', error);
      // Fallback to simple search
      this.performSimpleSearch(query);
    }
  }

  performSimpleSearch(query) {
    const lowerQuery = query.toLowerCase();
    let results = this.searchData.filter(doc => {
      const matchTitle = doc.title.toLowerCase().includes(lowerQuery);
      const matchContent = doc.content.toLowerCase().includes(lowerQuery);
      const matchTags = doc.tags?.some(tag => tag.toLowerCase().includes(lowerQuery));
      return matchTitle || matchContent || matchTags;
    });

    if (this.currentFilter !== 'all') {
      results = results.filter(doc => doc.category === this.currentFilter);
    }

    this.searchResults = results.slice(0, 20).map((doc, i) => ({
      ref: this.searchData.indexOf(doc),
      score: doc.title.toLowerCase().includes(lowerQuery) ? 10 : 1
    }));

    this.selectedIndex = -1;

    if (this.searchResults.length === 0) {
      this.showNoResults(query);
    } else {
      this.renderResults(query);
    }
  }

  renderResults(query) {
    const html = this.searchResults.map((result, index) => {
      const doc = this.searchData[result.ref];
      const excerpt = this.getExcerpt(doc.content, query);
      const highlightedTitle = this.highlightMatch(doc.title, query);
      const highlightedExcerpt = this.highlightMatch(excerpt, query);

      return `
        <a href="${doc.url}" class="search-result-item" data-index="${index}">
          <span class="result-category">${this.getCategoryLabel(doc.category)}</span>
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
    const lowerContent = content.toLowerCase();
    const lowerQuery = query.toLowerCase().split(/\s+/)[0];
    const index = lowerContent.indexOf(lowerQuery);

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
    if (!query) return text;

    const words = query.trim().split(/\s+/);
    let result = text;

    words.forEach(word => {
      if (word.length < 2) return;
      const regex = new RegExp(`(${this.escapeRegExp(word)})`, 'gi');
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
      apendices: 'Apéndice'
    };
    return labels[category] || category;
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
            <li>Busca conjuros: <code>bola de fuego</code></li>
            <li>Busca clases: <code>guerrero</code></li>
            <li>Busca reglas: <code>flanqueo</code></li>
            <li>Busca acciones: <code>golpear</code></li>
          </ul>
        </div>
      </div>
    `;
  }

  showNoResults(query) {
    this.results.innerHTML = `
      <div class="search-no-results">
        <p>No se encontraron resultados para "<strong>${query}</strong>"</p>
        <p>Intenta con términos más generales o revisa la ortografía.</p>
      </div>
    `;
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
