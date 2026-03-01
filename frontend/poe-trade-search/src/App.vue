<template>
  <div class="app">
    <header class="header">
      <h1>⚔️ Path of Exile Trade Search</h1>
      <div class="status" :class="{ 'status-online': apiHealthy }">
        {{ apiHealthy ? '🟢 API Online' : '🔴 API Offline' }}
      </div>
    </header>

    <div class="container">
      <!-- Opportunities Section -->
      <div class="opportunities-section">
        <h2>💰 Arbitrage Opportunities</h2>
        <button @click="fetchOpportunities" :disabled="loadingOpportunities" class="btn-primary">
          {{ loadingOpportunities ? 'Calculating...' : '♻️ Find Profitable Flips' }}
        </button>
        
        <div v-if="opportunities.length > 0" class="opportunities-table">
          <div class="table-header">
            <span>Rule</span>
            <span>Profit</span>
            <span>ROI</span>
            <span>Risk</span>
            <span>Tags</span>
          </div>
          <div 
            v-for="opp in opportunities" 
            :key="opp.name" 
            class="table-row clickable"
            @click="showBreakdown(opp)"
          >
            <span class="opp-name">{{ opp.name }}</span>
            <span class="opp-profit" :class="{ 'positive': opp.profit > 0 }">{{ opp.profit.toFixed(1) }}c</span>
            <span class="opp-roi">{{ opp.roi.toFixed(0) }}%</span>
            <span class="opp-risk">{{ opp.risk.toFixed(1) }}</span>
            <span class="opp-tags">
              <span v-for="tag in opp.tags" :key="tag" class="tag">{{ tag }}</span>
            </span>
          </div>
        </div>
      </div>

      <!-- Breakdown Modal -->
      <div v-if="selectedOpportunity" class="modal-overlay" @click.self="closeBreakdown">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ selectedOpportunity.name }} Breakdown</h3>
            <button @click="closeBreakdown" class="btn-close">×</button>
          </div>
          
          <div v-if="selectedOpportunity.breakdown" class="breakdown-content">
            <div class="breakdown-section">
              <h4>Ingredients (Cost)</h4>
              <table class="breakdown-table">
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Qty</th>
                    <th>Unit Cost</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in selectedOpportunity.breakdown.ingredients" :key="item.name">
                    <td>{{ item.name }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ item.unit_cost?.toFixed(1) }}c</td>
                    <td>{{ item.total_cost?.toFixed(1) }}c</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr>
                    <td colspan="3"><strong>Total Cost</strong></td>
                    <td><strong>{{ selectedOpportunity.breakdown.cost.toFixed(1) }}c</strong></td>
                  </tr>
                </tfoot>
              </table>
            </div>

            <div class="breakdown-section">
              <h4>Outcomes (Revenue)</h4>
              <table class="breakdown-table">
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Prob</th>
                    <th>Unit Value</th>
                    <th>Expected</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in selectedOpportunity.breakdown.products" :key="item.name">
                    <td>{{ item.name }}</td>
                    <td>{{ (item.probability * 100).toFixed(0) }}%</td>
                    <td>{{ item.unit_value?.toFixed(1) }}c</td>
                    <td>{{ item.expected_revenue?.toFixed(1) }}c</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr>
                    <td colspan="3"><strong>Total Expected Revenue</strong></td>
                    <td><strong>{{ selectedOpportunity.breakdown.revenue.toFixed(1) }}c</strong></td>
                  </tr>
                </tfoot>
              </table>
            </div>

            <div class="breakdown-summary">
              <div class="summary-item">
                <span>Raw Profit:</span>
                <span :class="{ 'positive': selectedOpportunity.breakdown.profit > 0 }">
                  {{ selectedOpportunity.breakdown.profit.toFixed(1) }}c
                </span>
              </div>
              <div class="summary-item">
                <span>Multiplier:</span>
                <span>{{ selectedOpportunity.breakdown.multiplier.toFixed(4) }}</span>
              </div>
              <div class="summary-item highlight">
                <span>Scaled Profit:</span>
                <span :class="{ 'positive': selectedOpportunity.breakdown.scaled_profit > 0 }">
                  {{ selectedOpportunity.breakdown.scaled_profit.toFixed(1) }}c
                </span>
              </div>
            </div>
          </div>
          <div v-else class="no-data">
            No breakdown data available.
          </div>
        </div>
      </div>

      <!-- Search Builder Section -->
      <div class="search-builder">
        <h2>Build Search Query</h2>
        
        <div class="form-group">
          <label>Base Type</label>
          <select v-model="currentSearch.type" class="input">
            <option value="">Select base type...</option>
            <option v-for="type in baseTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Prefixes</label>
          <div class="mod-list">
            <div v-for="(prefix, index) in currentSearch.prefixes" :key="'prefix-' + index" class="mod-item">
              <input 
                v-model="currentSearch.prefixes[index]" 
                type="text" 
                class="input mod-input"
                placeholder="e.g., 25% increased effect"
              />
              <button @click="removePrefix(index)" class="btn-remove">❌</button>
            </div>
          </div>
          <button @click="addPrefix" class="btn-add">+ Add Prefix</button>
          <div class="common-mods">
            <span class="label-small">Common:</span>
            <button 
              v-for="mod in commonPrefixes" 
              :key="mod"
              @click="addPrefixFromTemplate(mod)"
              class="btn-template"
            >
              {{ mod }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>Suffixes</label>
          <div class="mod-list">
            <div v-for="(suffix, index) in currentSearch.suffixes" :key="'suffix-' + index" class="mod-item">
              <input 
                v-model="currentSearch.suffixes[index]" 
                type="text" 
                class="input mod-input"
                placeholder="e.g., 61% reduced Effect of Curses"
              />
              <button @click="removeSuffix(index)" class="btn-remove">❌</button>
            </div>
          </div>
          <button @click="addSuffix" class="btn-add">+ Add Suffix</button>
          <div class="common-mods">
            <span class="label-small">Common:</span>
            <button 
              v-for="mod in commonSuffixes" 
              :key="mod"
              @click="addSuffixFromTemplate(mod)"
              class="btn-template"
            >
              {{ mod }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>Filters</label>
          <div class="filters-grid">
            <div class="filter-item">
              <label class="label-small">Corrupted</label>
              <select v-model="currentSearch.misc.filters.corrupted.option" class="input input-small">
                <option value="">Any</option>
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </div>
            <div class="filter-item">
              <label class="label-small">Quality Min</label>
              <input 
                v-model.number="currentSearch.misc.filters.quality.min" 
                type="number" 
                class="input input-small"
                min="0"
                max="30"
              />
            </div>
            <div class="filter-item">
              <label class="label-small">Quality Max</label>
              <input 
                v-model.number="currentSearch.misc.filters.quality.max" 
                type="number" 
                class="input input-small"
                min="0"
                max="30"
              />
            </div>
          </div>
        </div>

        <div class="actions">
          <button @click="executeSearch" :disabled="searching" class="btn-primary">
            {{ searching ? '🔍 Searching...' : '🔍 Search' }}
          </button>
          <button @click="clearSearch" class="btn-secondary">
            🗑️ Clear
          </button>
          <button @click="addToBatch" class="btn-secondary">
            📋 Add to Batch
          </button>
        </div>
      </div>

      <!-- Results Section -->
      <div class="results-section">
        <h2>Search Results</h2>
        
        <div v-if="searching" class="loading">
          <div class="spinner"></div>
          <p>Searching...</p>
        </div>

        <div v-else-if="error" class="error-message">
          <strong>Error:</strong> {{ error }}
        </div>

        <div v-else-if="searchResults" class="results">
          <div class="results-header">
            <h3>Found {{ searchResults.count }} items</h3>
            <div class="price-stats" v-if="searchResults.count > 0">
              <span>Min: {{ minPrice }}c</span>
              <span>Avg: {{ avgPrice }}c</span>
              <span>Max: {{ maxPrice }}c</span>
            </div>
          </div>

          <div class="results-list">
            <div 
              v-for="item in searchResults.results" 
              :key="item.id"
              class="result-item"
            >
              <div class="item-info">
                <div class="item-name">{{ item.item?.name || 'Unknown Item' }}</div>
                <div class="item-type">{{ item.item?.typeLine || currentSearch.type }}</div>
              </div>
              <div class="item-price" v-if="item.chaos_price">
                {{ item.chaos_price.toFixed(1) }} chaos
              </div>
              <div class="item-seller">
                {{ item.listing?.account?.name || 'Unknown' }}
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>No results yet. Configure a search and click "Search" to begin.</p>
        </div>
      </div>
    </div>

    <!-- Batch Search Section -->
    <div class="batch-section" v-if="batchSearches.length > 0">
      <h2>Batch Searches ({{ batchSearches.length }})</h2>
      
      <div class="batch-list">
        <div 
          v-for="(search, index) in batchSearches" 
          :key="'batch-' + index"
          class="batch-item"
        >
          <div class="batch-info">
            <strong>{{ search.type }}</strong>
            <div class="batch-mods">
              <span v-if="search.prefixes.length">{{ search.prefixes.length }} prefixes</span>
              <span v-if="search.suffixes.length">{{ search.suffixes.length }} suffixes</span>
            </div>
          </div>
          <button @click="removeBatchSearch(index)" class="btn-remove">Remove</button>
        </div>
      </div>

      <div class="batch-actions">
        <button @click="executeBatchSearch" :disabled="batchSearching" class="btn-primary">
          {{ batchSearching ? '🔍 Searching All...' : '🔍 Execute All Searches' }}
        </button>
        <button @click="clearBatch" class="btn-secondary">
          🗑️ Clear Batch
        </button>
      </div>

      <!-- Batch Results -->
      <div v-if="batchResults.length > 0" class="batch-results">
        <h3>Batch Results</h3>
        <div 
          v-for="result in batchResults" 
          :key="result.id"
          class="batch-result-item"
        >
          <div class="batch-result-header">
            <strong>{{ result.type }}</strong>
            <span class="count-badge">{{ result.count }} found</span>
          </div>
          <div v-if="result.success && result.listings?.length" class="price-stats">
            <span>Min: {{ getBatchMinPrice(result.listings) }}c</span>
            <span>Avg: {{ getBatchAvgPrice(result.listings) }}c</span>
            <span>Max: {{ getBatchMaxPrice(result.listings) }}c</span>
          </div>
          <div v-else-if="!result.success" class="error-text">
            Error: {{ result.error }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      apiHealthy: false,
      searching: false,
      batchSearching: false,
      loadingOpportunities: false,
      error: null,
      searchResults: null,
      batchResults: [],
      opportunities: [],
      selectedOpportunity: null,
      
      currentSearch: {
        type: '',
        prefixes: [],
        suffixes: [],
        misc: {
          filters: {
            corrupted: {
              option: 'false'
            },
            quality: {
              min: 20,
              max: 20
            }
          }
        }
      },

      batchSearches: [],

      baseTypes: [
        'Sapphire Flask',
        'Ruby Flask',
        'Topaz Flask',
        'Granite Flask',
        'Quicksilver Flask',
        'Silver Flask',
        'Amethyst Flask',
        'Jade Flask',
        'Diamond Flask',
        'Basalt Flask',
        'Bismuth Flask',
        'Quartz Flask',
        'Sulphur Flask',
        'Aquamarine Flask',
        'Stibnite Flask',
        'Corundum Flask'
      ],

      commonPrefixes: [
        '25% increased effect',
        '31% chance to gain a Flask Charge when you deal a Critical Strike',
        'Gains 3 Charges when you are hit by an Enemy'
      ],

      commonSuffixes: [
        '61% reduced Effect of Curses on you during Effect',
        '56% increased Armour during Effect',
        '56% increased Evasion Rating during Effect',
        '15% increased Attack Speed during Effect',
        '15% increased Cast Speed during Effect',
        '12% increased Movement Speed during Effect',
        '18% additional Elemental Resistances during Effect',
        '50% increased Critical Strike Chance during Effect',
        '51% Chance to Avoid being Stunned during Effect'
      ]
    };
  },

  computed: {
    minPrice() {
      if (!this.searchResults?.results?.length) return 0;
      const prices = this.searchResults.results
        .map(r => r.chaos_price)
        .filter(p => p);
      return prices.length ? Math.min(...prices).toFixed(1) : 0;
    },

    avgPrice() {
      if (!this.searchResults?.results?.length) return 0;
      const prices = this.searchResults.results
        .map(r => r.chaos_price)
        .filter(p => p);
      if (!prices.length) return 0;
      const sum = prices.reduce((a, b) => a + b, 0);
      return (sum / prices.length).toFixed(1);
    },

    maxPrice() {
      if (!this.searchResults?.results?.length) return 0;
      const prices = this.searchResults.results
        .map(r => r.chaos_price)
        .filter(p => p);
      return prices.length ? Math.max(...prices).toFixed(1) : 0;
    }
  },

  mounted() {
    this.checkApiHealth();
  },

  methods: {
    async checkApiHealth() {
      try {
        const response = await axios.get('/api/health');
        this.apiHealthy = response.data.status === 'ok';
      } catch (error) {
        this.apiHealthy = false;
        console.error('API health check failed:', error);
      }
    },

    showBreakdown(opp) {
      this.selectedOpportunity = opp;
    },

    closeBreakdown() {
      this.selectedOpportunity = null;
    },

    async fetchOpportunities() {
      this.loadingOpportunities = true;
      try {
        const response = await axios.get('/api/opportunities');
        this.opportunities = response.data;
      } catch (error) {
        alert('Failed to fetch opportunities: ' + error.message);
      } finally {
        this.loadingOpportunities = false;
      }
    },

    addPrefix() {
      this.currentSearch.prefixes.push('');
    },

    removePrefix(index) {
      this.currentSearch.prefixes.splice(index, 1);
    },

    addPrefixFromTemplate(mod) {
      if (!this.currentSearch.prefixes.includes(mod)) {
        this.currentSearch.prefixes.push(mod);
      }
    },

    addSuffix() {
      this.currentSearch.suffixes.push('');
    },

    removeSuffix(index) {
      this.currentSearch.suffixes.splice(index, 1);
    },

    addSuffixFromTemplate(mod) {
      if (!this.currentSearch.suffixes.includes(mod)) {
        this.currentSearch.suffixes.push(mod);
      }
    },

    clearSearch() {
      this.currentSearch = {
        type: '',
        prefixes: [],
        suffixes: [],
        misc: {
          filters: {
            corrupted: {
              option: 'false'
            },
            quality: {
              min: 20,
              max: 20
            }
          }
        }
      };
      this.searchResults = null;
      this.error = null;
    },

    async executeSearch() {
      this.searching = true;
      this.error = null;
      
      try {
        const response = await axios.post('/api/search', this.currentSearch);
        this.searchResults = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || error.message;
        this.searchResults = null;
      } finally {
        this.searching = false;
      }
    },

    addToBatch() {
      if (!this.currentSearch.type) {
        alert('Please select a base type first');
        return;
      }
      
      // Deep clone the current search
      const searchCopy = JSON.parse(JSON.stringify(this.currentSearch));
      searchCopy.id = `search-${Date.now()}`;
      this.batchSearches.push(searchCopy);
    },

    removeBatchSearch(index) {
      this.batchSearches.splice(index, 1);
    },

    clearBatch() {
      this.batchSearches = [];
      this.batchResults = [];
    },

    async executeBatchSearch() {
      this.batchSearching = true;
      this.batchResults = [];

      try {
        const response = await axios.post('/api/batch-search', {
          searches: this.batchSearches
        });
        
        this.batchResults = response.data.results;
      } catch (error) {
        alert('Batch search failed: ' + (error.response?.data?.error || error.message));
      } finally {
        this.batchSearching = false;
      }
    },

    getBatchMinPrice(listings) {
      if (!listings?.length) return 0;
      const prices = listings.map(l => l.chaos_price).filter(p => p);
      return prices.length ? Math.min(...prices).toFixed(1) : 0;
    },

    getBatchAvgPrice(listings) {
      if (!listings?.length) return 0;
      const prices = listings.map(l => l.chaos_price).filter(p => p);
      if (!prices.length) return 0;
      return (prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(1);
    },

    getBatchMaxPrice(listings) {
      if (!listings?.length) return 0;
      const prices = listings.map(l => l.chaos_price).filter(p => p);
      return prices.length ? Math.max(...prices).toFixed(1) : 0;
    }
  }
};
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: #1a1a1a;
}

.header {
  background: linear-gradient(135deg, #2d1b00 0%, #1a0f00 100%);
  border-bottom: 2px solid #4a3000;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.header h1 {
  color: #d4af37;
  font-size: 1.8rem;
  font-weight: 700;
}

.status {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  background: #2a2a2a;
  color: #888;
}

.status-online {
  background: #1a3a1a;
  color: #4ade80;
}

.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
}

.opportunities-section {
  background: #242424;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  grid-column: 1 / -1; /* Span full width */
}

.opportunities-table {
  margin-top: 1.5rem;
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 2fr;
  padding: 1rem;
  background: #2a2a2a;
  font-weight: 600;
  color: #d4af37;
  border-bottom: 2px solid #3a3a3a;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 2fr;
  padding: 1rem;
  border-bottom: 1px solid #3a3a3a;
  align-items: center;
  transition: background 0.2s;
}

.table-row:hover {
  background: #2a2a2a;
}

.opp-name {
  color: #e0e0e0;
  font-weight: 500;
}

.opp-profit {
  font-weight: 700;
  color: #888;
}

.opp-profit.positive {
  color: #4ade80;
}

.opp-roi {
  color: #9a9aff;
}

.opp-risk {
  color: #ff6b6b;
}

.opp-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background: #3a3a3a;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #ccc;
}

.search-builder,
.results-section {
  background: #242424;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

h2 {
  color: #d4af37;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  border-bottom: 2px solid #4a3000;
  padding-bottom: 0.5rem;
}

h3 {
  color: #e0e0e0;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  color: #d4af37;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.label-small {
  font-size: 0.85rem;
  color: #999;
}

.input {
  width: 100%;
  padding: 0.75rem;
  background: #1a1a1a;
  border: 2px solid #3a3a3a;
  border-radius: 6px;
  color: #e0e0e0;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.input-small {
  width: auto;
  padding: 0.5rem;
}

.mod-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.mod-item {
  display: flex;
  gap: 0.5rem;
}

.mod-input {
  flex: 1;
}

.btn-remove {
  padding: 0.5rem 0.75rem;
  background: #3a1a1a;
  border: none;
  border-radius: 6px;
  color: #ff6b6b;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: #4a2020;
}

.btn-add {
  width: 100%;
  padding: 0.75rem;
  background: #2a3a2a;
  border: 2px dashed #4a6a4a;
  border-radius: 6px;
  color: #6ade6a;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-add:hover {
  background: #3a4a3a;
  border-color: #6ade6a;
}

.common-mods {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
  align-items: center;
}

.btn-template {
  padding: 0.4rem 0.75rem;
  background: #2a2a3a;
  border: 1px solid #4a4a6a;
  border-radius: 4px;
  color: #9a9aff;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-template:hover {
  background: #3a3a4a;
  border-color: #9a9aff;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary {
  flex: 1;
  padding: 1rem;
  background: linear-gradient(135deg, #d4af37 0%, #b8941e 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a1a;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 1rem;
  background: #3a3a3a;
  border: 2px solid #5a5a5a;
  border-radius: 8px;
  color: #e0e0e0;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #4a4a4a;
  border-color: #7a7a7a;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #3a3a3a;
}

.price-stats {
  display: flex;
  gap: 1.5rem;
  color: #d4af37;
  font-weight: 600;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 600px;
  overflow-y: auto;
}

.result-item {
  background: #1a1a1a;
  border: 1px solid #3a3a3a;
  border-radius: 6px;
  padding: 1rem;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  align-items: center;
  transition: all 0.2s;
}

.result-item:hover {
  border-color: #d4af37;
  transform: translateX(4px);
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-name {
  color: #e0e0e0;
  font-weight: 600;
}

.item-type {
  color: #888;
  font-size: 0.9rem;
}

.item-price {
  color: #d4af37;
  font-weight: 700;
  font-size: 1.1rem;
}

.item-seller {
  color: #9a9aff;
  font-size: 0.9rem;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #3a3a3a;
  border-top-color: #d4af37;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  background: #3a1a1a;
  border: 2px solid #6a2a2a;
  border-radius: 6px;
  padding: 1rem;
  color: #ff6b6b;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.batch-section {
  background: #242424;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem;
  max-width: 1800px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.batch-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.batch-item {
  background: #1a1a1a;
  border: 1px solid #3a3a3a;
  border-radius: 6px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-info strong {
  color: #d4af37;
  display: block;
  margin-bottom: 0.5rem;
}

.batch-mods {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #888;
}

.batch-actions {
  display: flex;
  gap: 1rem;
}

.batch-results {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #3a3a3a;
}

.batch-result-item {
  background: #1a1a1a;
  border: 1px solid #3a3a3a;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.batch-result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.count-badge {
  background: #2a3a2a;
  color: #6ade6a;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.error-text {
  color: #ff6b6b;
  font-size: 0.9rem;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #242424;
  border: 2px solid #4a3000;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #3a3a3a;
  padding-bottom: 1rem;
}

.modal-header h3 {
  margin: 0;
  color: #d4af37;
}

.btn-close {
  background: none;
  border: none;
  color: #888;
  font-size: 2rem;
  cursor: pointer;
  line-height: 1;
}

.btn-close:hover {
  color: #fff;
}

.breakdown-section {
  margin-bottom: 2rem;
}

.breakdown-section h4 {
  color: #e0e0e0;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.breakdown-table {
  width: 100%;
  border-collapse: collapse;
  background: #1a1a1a;
  border-radius: 6px;
  overflow: hidden;
}

.breakdown-table th,
.breakdown-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #3a3a3a;
}

.breakdown-table th {
  background: #2a2a2a;
  color: #d4af37;
  font-weight: 600;
}

.breakdown-table td {
  color: #ccc;
}

.breakdown-table tfoot td {
  background: #2a2a2a;
  color: #d4af37;
  border-top: 2px solid #4a3000;
}

.breakdown-summary {
  display: flex;
  justify-content: flex-end;
  gap: 2rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #3a3a3a;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.summary-item span:first-child {
  color: #888;
  font-size: 0.9rem;
}

.summary-item span:last-child {
  color: #e0e0e0;
  font-weight: 700;
  font-size: 1.2rem;
}

.summary-item.highlight span:last-child {
  color: #d4af37;
  font-size: 1.5rem;
}

.positive {
  color: #4ade80 !important;
}

.clickable {
  cursor: pointer;
}
</style>
