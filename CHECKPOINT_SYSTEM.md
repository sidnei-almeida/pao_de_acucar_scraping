# 🔄 Checkpoint & Crash Recovery System

## Overview

The checkpoint system was designed to solve frequent browser crashes that occurred while collecting URLs from massive categories (10,000+ items). The browser would crash after ~1 hour of continuous scrolling because of excessive memory usage.

## Original Problem

```
Scroll 248 - Total products: 10,406
ERROR - Error collecting URLs: Message: tab crashed
```

**Impact:**
- Loss of ~1 hour of scraping
- Loss of 10,406 collected URLs
- Required restarting from scratch

## Implemented Solution

### 1. **Checkpoint system (batched saves)**

The scraper automatically persists progress every **1,000 products**.

**Generated file:** `urls_checkpoint_{categoria}.json`

**Checkpoint structure:**
```json
{
  "urls": [...],                 // List of collected products
  "num_scrolls": 248,            // Number of scroll iterations
  "posicao_scroll": 125000,      // Current scroll position
  "timestamp": "2025-10-16T...", // Checkpoint timestamp
  "total_produtos": 10406        // Total products stored
}
```

### 2. **Periodic browser restarts**

The browser is restarted every **100 scrolls** (~4,200 products) to free memory.

**Flow:**
1. Save checkpoint with current position
2. Close the browser (release memory)
3. Spin up a new browser instance
4. Reload the page
5. Fast-scroll to the previous position
6. Continue harvesting

**Benefit:** Prevents memory buildup that leads to crashes

### 3. **Automatic crash recovery**

When a crash happens, the system:

1. **Detects the error:** `"tab crashed"` or `"session deleted"`
2. **Saves an emergency checkpoint** (if needed)
3. **Reloads the latest checkpoint** automatically
4. **Restarts the browser** after 10 seconds
5. **Resumes scraping** from the last saved state

**Retries:** Up to 3 automatic attempts before giving up

## Configuration

Defined in `url_collector.py` inside `coletar_urls()`:

```python
BATCH_SIZE = 1000           # Save checkpoint every 1000 products
RESTART_INTERVAL = 100      # Restart browser every 100 scrolls
MAX_RETRY_CRASHES = 3       # Up to 3 retries after crashes
```

## Usage

### Standard collection

```bash
python main.py
# Choose: 3 (Custom Collection)
# Category: 14 (Food - All Items, 10,000+ products)
# Mode: 2 (Full)
```

**During the run you’ll see:**
```
✨ New products: +42 (total: 1000)
✅ Checkpoint saved: 1000 products, 24 scrolls

✨ New products: +42 (total: 2000)
✅ Checkpoint saved: 2000 products, 48 scrolls

🔄 Restarting browser to free memory (scroll 100)
⏩ Returning to position 42350
```

### Crash recovery

If a crash happens you’ll see:
```
💥 Tab crashed! (attempt 1/3)
⚠️  Error: Message: tab crashed
✅ Checkpoint saved: 5432 products, 130 scrolls
⏳ Waiting 10 seconds before retrying...
📦 Checkpoint loaded: 5432 products, 130 scrolls
🔄 Resuming collection (currently 5432 products)
```

### Resuming after interruption

If you stop the script (Ctrl+C) or the browser crashes:

1. Run `python main.py` again
2. Select the **same category**
3. The system will automatically resume:
```
⚠️  Previous checkpoint found! Resuming from last state...
📦 Checkpoint loaded: 7891 products, 189 scrolls
📊 Continuing with 7891 products already collected
```

## Logging

Every action is captured in the logs:

```
2025-10-16 05:46:33 - INFO - New products found: 42 (total: 10070)
2025-10-16 05:46:33 - INFO - Scroll 240 - Total products: 10070
2025-10-16 05:46:35 - INFO - ✅ Checkpoint saved: 10000 products, 240 scrolls
2025-10-16 05:47:00 - INFO - 🔄 Restarting browser to free memory (scroll 200)
```

## Checkpoint files

**Location:** Project root  
**Pattern:** `urls_checkpoint_{categoria}.json`

**Examples:**
- `urls_checkpoint_alimentos_geral.json`
- `urls_checkpoint_bebidas.json`
- `urls_checkpoint_padaria.json`

**Auto-cleanup:**
- Removed automatically after a successful run
- Kept when a crash occurs for recovery

**Manual cleanup:**
```bash
# Start from scratch
rm urls_checkpoint_*.json
```

## Testing

### Simple test (checkpoint helpers)

```bash
python teste_checkpoint_simples.py
```

**Validates:**
- ✅ Checkpoint saving
- ✅ Checkpoint loading
- ✅ File cleanup
- ✅ Full lifecycle

### Full test (with browser)

```bash
python main.py
# Option 3: Custom Collection
# Category: Small one (e.g., Bakery)
# Mode: Test (5 products)
```

**Watch for:**
- Checkpoint messages
- Browser restart (if it hits 100 scrolls)
- Automatic recovery if the browser crashes

## Benefits

### Before

| Metric | Value |
|--------|-------|
| **Products lost in crash** | 10,406 (100%) |
| **Time lost** | ~1 hour |
| **Recovery process** | Manual, from scratch |
| **Memory stress** | High (led to crashes) |

### After

| Metric | Value |
|--------|-------|
| **Products lost in crash** | Max 1,000 (≈9%) |
| **Time lost** | Max ~5 minutes |
| **Recovery process** | Automatic |
| **Memory stress** | Low (periodic restarts) |

## Improvements Achieved

- **Loss reduction:** 91% fewer products lost  
- **Recovery:** Automatic instead of manual  
- **Reliability:** Up to 3 automated retries  
- **Transparency:** Detailed log trail for each action

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│ START COLLECTION                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Check for        │
                    │ existing         │
                    │ checkpoint       │
                    └──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 YES│                   │NO
                    ▼                   ▼
          ┌──────────────────┐  ┌──────────────────┐
          │ Load collected   │  │ Start from scratch│
          │ URLs             │  │ Empty list        │
          └──────────────────┘  └──────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌──────────────────┐
                    │ COLLECTION LOOP  │
                    └──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌────────────────────┐  ┌────────────────────┐
        │ Scroll & harvest   │  │ Every 100 scrolls: │
        │ products           │  │ restart browser    │
        └────────────────────┘  └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │ Every 1000         │
        │ products:          │
        │ Save checkpoint    │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │ End of category?   │
        │ No more products?  │
        └────────────────────┘
                    │
                 YES│
                    ▼
        ┌────────────────────┐
        │ SUCCESS            │
        │ Remove checkpoint  │
        │ Return URLs        │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │ END                │
        └────────────────────┘

        IF A CRASH OCCURS:
                    │
                    ▼
        ┌────────────────────┐
        │ Detect crash       │
        │ "tab crashed"      │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │ Save emergency     │
        │ checkpoint         │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │ Wait 10s           │
        │ Restart browser    │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │ Load checkpoint    │
        │ Resume collection  │
        └────────────────────┘
```

## Support Checklist

If something goes wrong:

1. **Inspect the logs:** `scraping_YYYYMMDD_HHMMSS.log`
2. **Check for existing checkpoints:** `ls urls_checkpoint_*.json`
3. **Run the helper test:** `python teste_checkpoint_simples.py`
4. **Clean old checkpoints if needed:** `rm urls_checkpoint_*.json`

## Technical Notes

- **Thread-safe:** No threading required; uses synchronous saves
- **Encoding:** UTF-8 to support accented characters
- **Format:** Pretty-printed JSON for easier debugging
- **Size:** ~8–9 KB per 1,000 products
- **Performance:** Saving takes <100 ms; no perceptible impact on scraping

