import subprocess

# Compile the C program
compile_process = subprocess.run(["gcc", "hello.c", "-o", "hello"], capture_output=True, text=True)

if compile_process.returncode != 0:
    print("Compilation failed!")
    print(compile_process.stderr)
    exit(1)

# Run the compiled program
run_process = subprocess.run(["./hello"], capture_output=True, text=True)

# Check output
expected_output = "Hello, World!\n"
expected_exit_code = 42

if run_process.stdout == expected_output and run_process.returncode == expected_exit_code:
    print("Test Passed!")
else:
    print("Test Failed!")
    print(f"Expected output: {expected_output}")
    print(f"Actual output: {run_process.stdout}")
    print(f"Expected exit code: {expected_exit_code}")
    print(f"Actual exit code: {run_process.returncode}")
