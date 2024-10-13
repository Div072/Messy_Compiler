import subprocess
import os

# Step 1: Run main.py
print("Running main.py...")
subprocess.run(['python3', 'main.py'])

# Step 2: Compile the generated.s file with gcc to produce a.out
print("Compiling generated.s with gcc...")
subprocess.run(['gcc', 'generated.s', '-o', 'a.out'])
subprocess.run(['gcc', 'main.c', '-o', 'b.out'])
# Step 3: Run the a.out executable
print("Executing a.out...")
result = subprocess.run(['./a.out'])
result2 = subprocess.run(['./b.out'])
# Step 4: Get the return value (exit code) of a.out using $? and echo it
return_code = result.returncode
return_code2 = result2.returncode
print(f"Return value of messy_compiler (exit code): {return_code}")
print(f"Return value of gcc (exit code): {return_code2}")

# Step 5: Clean up: remove a.out and generated.s
print("Cleaning up files...")
os.remove('a.out')
os.remove('b.out')
os.remove('generated.s')
print("Process complete!")
