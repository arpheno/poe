# Development Tips - Trade Search Frontend

## Quick Commands Reference

```bash
# Get help
make help

# Install everything
make install-trade-search

# Start development
make trade-dev

# Check status
make trade-check

# View logs
make trade-logs

# Stop everything
make trade-stop
```

## Common Development Tasks

### Adding a New Filter

1. **Add to Vue component** (`frontend/poe-trade-search/src/App.vue`):
```javascript
// In data()
currentSearch: {
  misc: {
    filters: {
      // Add your new filter
      ilvl: { min: null, max: null }
    }
  }
}
```

2. **Add UI in template**:
```vue
<div class="filter-item">
  <label class="label-small">Item Level</label>
  <input v-model.number="currentSearch.misc.filters.ilvl.min" 
         type="number" class="input input-small" />
</div>
```

3. **Backend automatically handles it** - no changes needed!

### Adding a New Base Type

Edit `baseTypes` array in `App.vue`:

```javascript
baseTypes: [
  'Sapphire Flask',
  'Ruby Flask',
  // Add more
  'Your New Type',
]
```

### Debugging API Calls

Open browser DevTools → Network tab to see:
- Request payload
- Response data
- Status codes
- Timing

Or check backend logs:
```bash
make trade-logs
```

### Testing Backend Changes

```bash
# Make changes to poe/api/search_api.py
make trade-stop
make start-trade-api
# Flask auto-reloads on file changes in debug mode
```

### Testing Frontend Changes

Just save - Vite HMR updates instantly!

## Project Structure

```
poe/
├── Makefile                          # Build commands
│
├── poe/api/
│   └── search_api.py                # Flask API endpoints
│
├── poe/woke/
│   ├── mod_mapper.py                # Mod text → stat IDs
│   └── query_builder.py             # Build trade queries
│
└── frontend/poe-trade-search/
    ├── package.json                 # npm dependencies
    ├── vite.config.js              # Vite config
    ├── index.html                   # HTML entry
    └── src/
        ├── main.js                  # Vue initialization
        └── App.vue                  # Main component
            ├── <template>           # HTML structure
            ├── <script>             # Component logic
            └── <style scoped>       # Component styles
```

## Vue Component Breakdown

### Data Properties
- `apiHealthy` - API connection status
- `searching` - Loading state for single search
- `batchSearching` - Loading state for batch
- `searchResults` - Single search results
- `batchResults` - Batch search results
- `currentSearch` - Current query being built
- `batchSearches` - Queue of searches for batch

### Key Methods
- `executeSearch()` - POST to /api/search
- `executeBatchSearch()` - POST to /api/batch-search
- `addPrefix/Suffix()` - Manage mod lists
- `addToBatch()` - Add current search to batch queue
- `checkApiHealth()` - Ping /api/health

### Computed Properties
- `minPrice` - Minimum price from results
- `avgPrice` - Average price from results
- `maxPrice` - Maximum price from results

## Styling Guide

### Color Palette
```css
/* Background */
#1a1a1a  /* Main background */
#242424  /* Card background */
#3a3a3a  /* Border/divider */

/* Text */
#e0e0e0  /* Primary text */
#888     /* Secondary text */
#666     /* Muted text */

/* Accent */
#d4af37  /* Gold (primary) */
#9a9aff  /* Purple (links) */
#6ade6a  /* Green (success) */
#ff6b6b  /* Red (error) */
```

### Key CSS Classes
- `.btn-primary` - Main action button (gold)
- `.btn-secondary` - Secondary action (gray)
- `.btn-add` - Add mod button (green dashed)
- `.btn-remove` - Remove button (red)
- `.input` - All form inputs

## API Response Formats

### Single Search Response
```json
{
  "success": true,
  "count": 15,
  "results": [
    {
      "id": "abc123",
      "chaos_price": 12.5,
      "item": { "name": "...", "typeLine": "..." },
      "listing": {
        "price": { "amount": 12.5, "currency": "chaos" },
        "account": { "name": "PlayerName" }
      }
    }
  ],
  "query": { /* original query for debugging */ }
}
```

### Batch Search Response
```json
{
  "success": true,
  "results": [
    {
      "id": "search-1",
      "success": true,
      "type": "Sapphire Flask",
      "count": 10,
      "listings": [
        { "id": "...", "chaos_price": 15.0 }
      ]
    }
  ]
}
```

## Troubleshooting

### "Cannot connect to API"
```bash
make trade-check  # Check what's running
make trade-logs   # Look for errors
```

### "ModMapper not found"
The API needs your virtual environment:
```bash
source .venv/bin/activate
make start-trade-api
```

### "Port already in use"
```bash
lsof -i :5000  # Find what's using the port
kill -9 <PID>  # Kill it
```

### Vite not updating
```bash
# Hard refresh browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
# Or restart Vite:
cd frontend/poe-trade-search
npm run dev
```

## Performance Tips

### Frontend
- Vue DevTools to inspect component state
- Use Vue's reactivity system (avoid direct array mutations)
- Computed properties are cached

### Backend
- Flask debug mode enables auto-reload
- Use `mod_mapper` cache to avoid re-fetching stats
- Batch searches reduce total API calls

### Proxy
- Respects PoE API rate limits automatically
- Logs show rate limit status
- Don't bypass the proxy!

## Git Workflow

```bash
# Stage your changes
git add frontend/poe-trade-search/
git add poe/api/search_api.py
git add Makefile

# Commit
git commit -m "feat: add Vue trade search frontend"

# Push
git push origin adds-rules
```

## Testing Checklist

Before committing:
- [ ] `make trade-check` shows all services running
- [ ] Can execute a single search
- [ ] Can execute a batch search
- [ ] Results show correct prices
- [ ] Error handling works (try invalid mod)
- [ ] UI is responsive
- [ ] No console errors in browser DevTools

## Useful Keyboard Shortcuts

### In Terminal
- `Ctrl+C` - Stop foreground process
- `Ctrl+Z` - Suspend process
- `make trade-logs` then `Ctrl+C` - View logs and exit

### In Browser DevTools
- `Cmd+Opt+I` (Mac) or `F12` (Windows) - Open DevTools
- `Cmd+K` (Mac) or `Ctrl+L` (Windows) - Clear console
- Network tab → Filter by XHR to see API calls

### In VS Code
- `Cmd+P` - Quick file open
- `Cmd+Shift+F` - Search across files
- `F12` on a function - Go to definition

## Next Steps

1. Try running: `make trade-dev`
2. Open http://localhost:3000
3. Build a search query
4. Execute and see results
5. Try batch search with multiple queries

## Getting Help

- Check logs: `make trade-logs`
- Check service status: `make trade-check`
- Read docs: `QUICKSTART_TRADE_SEARCH.md`
- Full details: `docs/VUE_TRADE_SEARCH_IMPLEMENTATION.md`
