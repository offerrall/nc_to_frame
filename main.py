import re
from time import time
from cffi import FFI
import platform

ffi = FFI()


ffi.cdef(
"""
    void get_bounding_box(const char* file_path,
                          double* min_x,
                          double* max_x,
                          double* min_y,
                          double* max_y);
"""
)

if platform.system() == "Windows":
    lib = ffi.dlopen("nc_to_frame.dll")
else:
    lib = ffi.dlopen("./nc_to_frame.so")

def get_bounding_box(file_path: str):
    min_x = ffi.new("double *")
    max_x = ffi.new("double *")
    min_y = ffi.new("double *")
    max_y = ffi.new("double *")

    lib.get_bounding_box(file_path.encode('utf-8'), min_x, max_x, min_y, max_y)

    return round(min_x[0], 3), round(max_x[0], 3), round(min_y[0], 3), round(max_y[0], 3)

def python_get_bounding_box(file_path: str) -> tuple[float, float, float, float]:
    min_x: float = float('inf')
    max_x: float = float('-inf')
    min_y: float = float('inf')
    max_y: float = float('-inf')

    with open(file_path, 'r') as file:
        for line in file:
            x_match = re.search(r'X([-+]?[0-9]*\.?[0-9]+)', line)
            y_match = re.search(r'Y([-+]?[0-9]*\.?[0-9]+)', line)

            if x_match:
                x = float(x_match.group(1))
                min_x = min(min_x, x)
                max_x = max(max_x, x)

            if y_match:
                y = float(y_match.group(1))
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    return round(min_x, 3), round(max_x, 3), round(min_y, 3), round(max_y, 3)

def generate_framing_gcode(left: float,
                           right: float,
                           bottom: float,
                           top: float,
                           power: float = 10,
                           feed: int = 1000) -> list[str]:
    gcode: list[str] = [
        f"G0 X{left} Y{bottom}",
        f"M3 S{power:.3f} F{feed}",
        f"G1 Y{top}",
        f"G1 X{right}",
        f"G1 Y{bottom}",
        f"G1 X{left}",
        "M5",
        "G0 X0 Y0"
    ]
    return gcode

def process_input_file(input_path: str,
                       output_path: str = "framing.nc",
                       engine: callable = get_bounding_box
                       ) -> None:
    left, right, bottom, top = engine(input_path)
    gcode = generate_framing_gcode(left, right, bottom, top)

    print("Framing G-code generated in:", output_path)
    for line in gcode:
        print(line)


nc_file: str = "./test/giant.nc"

start: float = time()
process_input_file(nc_file)
end: float = time()
print(f"C Execution time: {end - start:.2f} seconds")

start: float = time()
process_input_file(nc_file, engine=python_get_bounding_box)
end: float = time()
print(f"Python Execution time: {end - start:.2f} seconds")
