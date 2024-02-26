import os

# Function to update start_file_number and end_file_number in vs_valid.py
def update_vs_valid(start_number_increment, end_number_increment):
    vs_valid_file = "vs_valid.py"
    
    # Read the contents of vs_valid.py
    with open(vs_valid_file, "r") as f:
        lines = f.readlines()
    
    # Find and update the lines containing start_file_number and end_file_number
    new_lines = []
    for i, line in enumerate(lines):
        if i == 50:  # Line 51 (zero-based index)
            start_number = int(line.split("=")[-1].strip())
            new_start_number = start_number + start_number_increment
            new_line = line.replace(str(start_number), str(new_start_number))
            new_lines.append(new_line)
        elif i == 51:  # Line 52 (zero-based index)
            end_number = int(line.split("=")[-1].strip())
            new_end_number = end_number + end_number_increment
            new_line = line.replace(str(end_number), str(new_end_number))
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    # Write the updated lines back to vs_valid.py
    with open(vs_valid_file, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    # Increment start_file_number by 100 and end_file_number by 100
    update_vs_valid(start_number_increment=100, end_number_increment=100)
