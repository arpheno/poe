# PoE Trade Search - Vue Frontend

A modern Vue.js frontend for executing Path of Exile trade searches with the same functionality as `flasks.py`.

## Features

- 🔍 **Build Complex Queries**: Specify base types, prefixes, suffixes, and filters
- 📊 **Real-time Results**: See search results with price statistics (min/avg/max)
- 📋 **Batch Searching**: Queue multiple searches and execute them all at once
- 🎨 **Modern UI**: Dark theme optimized for PoE aesthetics
- ⚡ **Fast**: Built with Vue 3 and Vite for instant feedback

## Quick Start

### 1. Install Dependencies

```bash
cd frontend/poe-trade-search
npm install
```

### 2. Start the Backend API

In a separate terminal:

```bash
cd /Users/swozny/Projects/poe

# Install Python dependencies if needed
source .venv/bin/activate
pip install flask flask-cors

# Start the Flask API
python poe/api/search_api.py
```

The API will run on `http://localhost:5000`

### 3. Start the Vue Frontend

```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

### 4. Make Sure the Proxy is Running

The backend needs your proxy to be running:

```bash
# In another terminal
python poe/proxy/main.py
```

This runs on `http://localhost:8999`

## Usage

### Single Search

1. **Select a Base Type**: Choose from the dropdown (e.g., "Sapphire Flask")
2. **Add Prefixes**: Click "+ Add Prefix" or use the common templates
3. **Add Suffixes**: Click "+ Add Suffix" or use the common templates
4. **Set Filters**: Configure corrupted status and quality range
5. **Click Search**: Execute the search and see results instantly

### Batch Search

1. Configure a search as above
2. Click "Add to Batch"
3. Repeat for multiple different searches
4. Click "Execute All Searches" to run them all
5. See aggregated results with price statistics

## API Endpoints

The Flask backend provides these endpoints:

### `GET /api/health`
Check if the API is running and which league is configured.

### `POST /api/search`
Execute a single search.

**Request:**
```json
{
  "type": "Sapphire Flask",
  "prefixes": ["25% increased effect"],
  "suffixes": ["61% reduced Effect of Curses on you during Effect"],
  "misc": {
    "filters": {
      "corrupted": {"option": "false"},
      "quality": {"min": 20, "max": 20}
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "count": 15,
  "results": [
    {
      "id": "...",
      "chaos_price": 12.5,
      "item": {...},
      "listing": {...}
    }
  ]
}
```

### `POST /api/batch-search`
Execute multiple searches in batch.

**Request:**
```json
{
  "searches": [
    {
      "id": "search-1",
      "type": "Sapphire Flask",
      "prefixes": ["25% increased effect"],
      "suffixes": ["61% reduced Effect of Curses"],
      "misc": {...}
    }
  ]
}
```

## Project Structure

```
frontend/poe-trade-search/
├── index.html           # HTML entry point
├── package.json         # Dependencies
├── vite.config.js      # Vite configuration
└── src/
    ├── main.js         # Vue app initialization
    └── App.vue         # Main application component

poe/api/
└── search_api.py       # Flask backend API
```

## Configuration

### Backend Configuration

Edit `poe/api/search_api.py` to change:
- `PROXY_BASE_URL`: Default is `http://localhost:8999`
- `LEAGUE`: Imported from `poe.constants`

### Frontend Configuration

Edit `vite.config.js` to change:
- Frontend port (default: 3000)
- API proxy settings

## Development

### Backend Development

The Flask API auto-reloads on changes when run with `debug=True`.

To add new endpoints:
1. Add route handler in `search_api.py`
2. Update frontend API calls in `App.vue`

### Frontend Development

Vite provides HMR (Hot Module Replacement) for instant updates.

Key files:
- `App.vue`: Main component with all UI logic
- Styles are scoped to the component

## Example Queries

The frontend comes pre-configured with common flask mods:

**Prefixes:**
- 25% increased effect
- 31% chance to gain a Flask Charge when you deal a Critical Strike
- Gains 3 Charges when you are hit by an Enemy

**Suffixes:**
- 61% reduced Effect of Curses on you during Effect
- 56% increased Armour during Effect
- 56% increased Evasion Rating during Effect
- 15% increased Attack Speed during Effect
- 15% increased Cast Speed during Effect
- 12% increased Movement Speed during Effect
- 18% additional Elemental Resistances during Effect
- 50% increased Critical Strike Chance during Effect
- 51% Chance to Avoid being Stunned during Effect

## Troubleshooting

### API not responding
- Check that Flask API is running: `http://localhost:5000/api/health`
- Check that proxy is running: `http://localhost:8999`
- Check browser console for CORS errors

### No search results
- Verify the proxy has access to Path of Exile API
- Check that mod text matches exactly what's in the trade API
- Look at the query in the response to debug

### Frontend won't start
```bash
# Clear node modules and reinstall
rm -rf node_modules
npm install
```

## Extending

### Adding New Base Types

Edit `baseTypes` array in `App.vue`:

```javascript
baseTypes: [
  'Sapphire Flask',
  'Ruby Flask',
  // Add more...
]
```

### Adding New Filter Options

1. Add to `currentSearch.misc.filters` in data
2. Add UI controls in the template
3. Backend will automatically use them

### Custom Styling

All styles are in the `<style scoped>` section of `App.vue`. The theme uses:
- Background: `#1a1a1a`
- Primary: `#d4af37` (gold)
- Secondary: `#3a3a3a`

## Performance

- **Frontend**: Vue 3 with Vite for near-instant HMR
- **Backend**: Flask with caching of trade stats
- **Proxy**: Rate-limited to respect PoE API limits

## License

Part of the larger PoE project.
