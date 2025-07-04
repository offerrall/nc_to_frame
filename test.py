from nc_to_frame import get_bounding_box, python_get_bounding_box, generate_framing_gcode

from time import time

nc_file: str = "./test/giant.nc"


def process_input_file(input_path: str,
                       output_path: str = "framing.nc",
                       engine: callable = get_bounding_box
                       ) -> None:
    left, right, bottom, top = engine(input_path)
    gcode = generate_framing_gcode(left, right, bottom, top)

    print("Framing G-code generated in:", output_path)
    for line in gcode:
        print(line)


start: float = time()
process_input_file(nc_file)
end: float = time()
print(f"C Execution time: {end - start:.2f} seconds")

start: float = time()
process_input_file(nc_file, engine=python_get_bounding_box)
end: float = time()
print(f"Python Execution time: {end - start:.2f} seconds")
