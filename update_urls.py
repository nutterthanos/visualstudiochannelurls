import os

# Function to update the for loop range in vs_valid.py
def update_vs_valid():
    vs_valid_file = "vs_valid.py"
    
    # Read the contents of vs_valid.py
    with open(vs_valid_file, "r") as f:
        lines = f.readlines()
    
    # Find and update the line containing the for loop
    new_lines = []
    for line in lines:
        if "for i in range(6, 10):" in line:
            new_line = "for i in range(11, 15):"  # Update range from 6 to 10 to 11 to 15
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    # Write the updated lines back to vs_valid.py
    with open(vs_valid_file, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    # Update the for loop range
    update_vs_valid()
