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
        if "for i in range(1, 5):" in line:
            new_line = line.replace("for i in range(1, 5):", "for i in range(6, 10):")  # Update range from 1 to 5 to 6 to 10
            new_lines.append(new_line)
        else:
            # Increment each number in the for loop range by 5
            for i in range(1, 6):
                if str(i) in line:
                    updated_number = str(int(i) + 5)
                    line = line.replace(str(i), updated_number)
            new_lines.append(line)
    
    # Write the updated lines back to vs_valid.py
    with open(vs_valid_file, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    # Update the for loop range
    update_vs_valid()
