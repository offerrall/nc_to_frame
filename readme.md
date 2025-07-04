# nc_to_frame

Extracts the bounding box from `.nc` files and generates simple framing G-code for laser/CNC alignment.

---

## Installation

```bash
git clone https://github.com/offerrall/nc_to_frame
```

```bash
cd nc_to_frame
```

```bash
pip install .
```


```bash
pip install cffi
```

Compile the C extension:

- **Linux/macOS**:
  ```bash
  cd c_src && bash compile.sh
  ```

- **Windows**:
  ```cmd
  cd c_src && compile.bat
  ```

> ℹ️ To avoid falling back to the slower Python version, make sure the compiled `.so` (Linux) or `.dll` (Windows) is in your environment path:
>
> - Linux/macOS: set `LD_LIBRARY_PATH`
> - Windows: add to `PATH`

---

## Usage

```python
from nc_to_frame import get_bounding_box, generate_framing_gcode

# Step 1: Get bounding box
left, right, bottom, top = get_bounding_box("input.nc")

# Step 2: Generate framing G-code
gcode = generate_framing_gcode(left, right, bottom, top)

# Step 3: Output the result
for line in gcode:
    print(line)
```

---

## Output Example

```gcode
G0 X10.0 Y5.0
M3 S10.000 F1000
G1 Y25.0
G1 X50.0
G1 Y5.0
G1 X10.0
M5
G0 X0 Y0
```

---

## API

### `get_bounding_box(file_path) -> (min_x, max_x, min_y, max_y)`
Parses the `.nc` file and returns the bounding box as four floats.

### `generate_framing_gcode(left, right, bottom, top, power=10, feed=1000) -> list[str]`
Creates rectangular framing G-code from given bounds.

---

## License

MIT
