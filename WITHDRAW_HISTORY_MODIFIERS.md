# Withdrawal History Modifiers Documentation

## Overview

Created 6 withdrawal history screenshot modifiers using the new rendering logic with `text_draw_execute()` from `_text_line_render/text_draw.py`. Clean PIL-based rendering without legacy cv2/matplotlib dependencies.

## Files Created

### Bybit Modifiers (6 transactions each)

1. **bybit_clp_withdraw_history_modifier.py** + test
   - Currency: CLP (Chilean Peso)
   - Transactions: 6
   - Currency display: "CLP"

2. **bybit_mxn_withdraw_history_modifier.py** + test
   - Currency: MXN (Mexican Peso)
   - Transactions: 6
   - Currency display: "MXN"

3. **bybit_ved_withdraw_history_modifier.py** + test
   - Currency: VED (Venezuelan Bolívar)
   - Transactions: 6
   - Currency display: "Bs" (VED → Bs conversion)

### MEXC Modifiers (4 transactions each)

4. **mexc_clp_withdraw_history_modifier.py** + test
   - Currency: CLP (Chilean Peso)
   - Transactions: 4
   - Currency display: "CLP"

5. **mexc_mxn_withdraw_history_modifier.py** + test
   - Currency: MXN (Mexican Peso)
   - Transactions: 4
   - Currency display: "MXN"

6. **mexc_ecu_withdraw_history_modifier.py** + test
   - Currency: ECU (Ecuadorian)
   - Transactions: 4
   - Currency display: "USD" (ECU → USD conversion, MEXC only)

## Technical Details

### Preserved from Original

✅ **Coordinates:**
- Y positions: `[845, 1010, 1177, 1340, 1504, 1666]` (Bybit - 6 rows)
- Y positions: `[845, 1010, 1177, 1340]` (MEXC - 4 rows)
- X positions:
  - Time: `416`
  - Account: `937`
  - Bank: `1387`
  - Amount (right-aligned): `2341`

✅ **Font Configuration:**
- Font size: `72` (increased for better readability)
- Font family: `"fonts/OpenSans-Semibold.ttf"`
- Text color: `(255, 255, 255)` (pure white)
- Kerning: `1.0`

✅ **Calculation Logic:**
- Y centering: `y_pos - fs // 2` (preserved "845 - fs / 2" pattern)

✅ **Business Logic:**
- Add `"****"` to account numbers
- Currency conversions:
  - VED → "Bs" (Bybit)
  - ECU → "USD" (MEXC only)
  - MXN → "MXN" (unchanged)
  - CLP → "CLP" (unchanged)

### New Rendering Approach

🆕 **Uses PIL Image + text_draw_execute():**
```python
base_img = text_draw_execute(
    base_image=base_img,
    font_sz=fs,
    text=text_content,
    position=(x, y),
    alignment='left',  # or 'right' for amounts
    font_family=font_family,
    text_color=white_color,
    kerning=kr_default
)
```

🆕 **Image resize pattern:**
```python
width, height = base_img.size
new_size = (int(width * 0.7), int(height * 0.7))
base_img_resized = base_img.resize(new_size, Image.LANCZOS)
base_img_resized.convert("RGB").save(output_path, quality=85, optimize=True)
```

❌ **Removed:**
- cv2 usage
- matplotlib visualization
- `reduce_image_size_by_half()` function
- `editor.execute()` and `editor_center.execute()`

## Function Parameters

### Bybit (6 transactions)

```python
def render_bybit_XXX_withdraw_history(
    tran_1: str,           # Transaction 1 amount
    tran_2: str,           # Transaction 2 amount
    tran_3: str,           # Transaction 3 amount
    tran_4: str,           # Transaction 4 amount
    tran_5: str,           # Transaction 5 amount
    tran_6: str,           # Transaction 6 amount
    lead_bank: str,        # Bank name (all 6 rows)
    lead_number: str,      # Account number (rows 1-5)
    persa_number: str,     # Account number (row 6)
    time_in_description: str,  # Time (e.g., "Hace un mes")
    template_path: str = "templates/...",
    output_path: str = "output/result.png"
) -> str:
```

### MEXC (4 transactions)

```python
def render_mexc_XXX_withdraw_history(
    tran_1: str,           # Transaction 1 amount
    tran_2: str,           # Transaction 2 amount
    tran_3: str,           # Transaction 3 amount
    tran_4: str,           # Transaction 4 amount
    lead_bank: str,        # Bank name (all rows)
    lead_number: str,      # Account number (rows 1-3)
    persa_number: str,     # Account number (row 4)
    time_in_description: str,  # Time (e.g., "Hace un mes")
    template_path: str = "templates/...",
    output_path: str = "output/result.png"
) -> str:
```

## Account Number Logic

### Bybit (6 transactions):
- Rows 1-5: Use `lead_number + "****"`
- Row 6: Use `persa_number + "****"`

### MEXC (4 transactions):
- Rows 1-3: Use `lead_number + "****"`
- Row 4: Use `persa_number + "****"`

## Usage Examples

### Bybit CLP Example

```python
from _modifiers_photo.bybit_clp_withdraw_history_modifier import render_bybit_clp_withdraw_history

result = render_bybit_clp_withdraw_history(
    tran_1="488.323",
    tran_2="241.579",
    tran_3="355.120",
    tran_4="612.890",
    tran_5="178.456",
    tran_6="523.789",
    lead_bank="Falabella",
    lead_number="1999659",       # Will display as "1999659****"
    persa_number="1509208",      # Will display as "1509208****"
    time_in_description="Hace un mes",
    template_path="templates/bybit_clp_withdraw_history.png",
    output_path="output/bybit_clp_result.png"
)
```

### MEXC MXN Example

```python
from _modifiers_photo.mexc_mxn_withdraw_history_modifier import render_mexc_mxn_withdraw_history

result = render_mexc_mxn_withdraw_history(
    tran_1="1,234.56",
    tran_2="987.65",
    tran_3="2,345.67",
    tran_4="456.78",
    lead_bank="BBVA Bancomer",
    lead_number="4152888",       # Will display as "4152888****"
    persa_number="9876543",      # Will display as "9876543****"
    time_in_description="Hace un mes",
    template_path="templates/mexc_mxn_withdraw_history.png",
    output_path="output/mexc_mxn_result.png"
)
```

## Template Requirements

Each modifier requires a corresponding template image:

### Bybit Templates
- `templates/bybit_clp_withdraw_history.png`
- `templates/bybit_mxn_withdraw_history.png`
- `templates/bybit_ved_withdraw_history.png`

### MEXC Templates
- `templates/mexc_clp_withdraw_history.png`
- `templates/mexc_mxn_withdraw_history.png`
- `templates/mexc_ecu_withdraw_history.png`

## Testing

All modifiers include test files with pytest:

```bash
# Test all withdraw history modifiers
cd _modifiers_photo
pytest test_bybit_clp_withdraw_history_modifier.py -v
pytest test_bybit_mxn_withdraw_history_modifier.py -v
pytest test_bybit_ved_withdraw_history_modifier.py -v
pytest test_mexc_clp_withdraw_history_modifier.py -v
pytest test_mexc_mxn_withdraw_history_modifier.py -v
pytest test_mexc_ecu_withdraw_history_modifier.py -v

# Or test all at once
pytest test_*_withdraw_history_modifier.py -v
```

Tests skip gracefully if template images are not found.

## Currency Conversion Reference

| Geo | Input Currency | Display Currency | Exchange | Notes |
|-----|---------------|------------------|----------|-------|
| CLP | CLP | CLP | Bybit, MEXC | No conversion |
| MXN | MXN | MXN | Bybit, MEXC | No conversion |
| VED | VED | Bs | Bybit only | VED → Bs conversion |
| ECU | ECU | USD | MEXC only | ECU → USD conversion |

## File Statistics

**Total files created:** 12
- **6 modifiers:** 3 Bybit + 3 MEXC
- **6 test files:** 3 Bybit tests + 3 MEXC tests

**All files validated:** ✅ Syntax check passed

## Next Steps

1. **Add template images** to `templates/` directory:
   - 3 Bybit templates (CLP, MXN, VED)
   - 3 MEXC templates (CLP, MXN, ECU)

2. **Adjust coordinates** if needed based on actual template layouts

3. **Test with real templates:**
   ```bash
   pytest _modifiers_photo/test_*_withdraw_history_modifier.py -v
   ```

4. **Integrate with bot handlers** (if needed)

---

**Created:** 2025-10-09
**Status:** ✅ Complete
**Rendering:** PIL Image + `text_draw_execute()`
**Focus:** Bybit & MEXC withdrawal history screenshots
