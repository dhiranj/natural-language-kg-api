import pandas as pd

# Load the dataset
file_path = 'top_1000_computer_scientists.csv'
top_1000_data = pd.read_csv(file_path)

# Step 1: Sort the dataset by rank (ascending order)
sorted_data = top_1000_data.sort_values(by="rank").reset_index(drop=True)

# Step 2: Divide the dataset into hierarchical levels
# Define the number of levels
num_levels = 3  # Example: top scientists, their students, and students' students

# Calculate the size of each level
level_size = len(sorted_data) // num_levels

# Assign levels
sorted_data['level'] = sorted_data.index // level_size

# Step 3: Create the teacher-student relationships
teacher_student_hierarchy = []

for level in range(num_levels - 1):  # Last level does not mentor others
    current_level = sorted_data[sorted_data['level'] == level]
    next_level = sorted_data[sorted_data['level'] == level + 1]
    
    # Shuffle the next level for random teacher-student assignments
    next_level_shuffled = next_level.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Match each teacher in the current level with students in the next level
    for i, teacher in current_level.iterrows():
        student_idx = i % len(next_level_shuffled)
        student = next_level_shuffled.iloc[student_idx]
        teacher_student_hierarchy.append({
            "teacher_id": teacher["author_id"],
            "teacher_name": teacher["author_name"],
            "student_id": student["author_id"],
            "student_name": student["author_name"]
        })

# Step 4: Convert the hierarchy into a DataFrame
teacher_student_df = pd.DataFrame(teacher_student_hierarchy)

# Optional: Save to a CSV file
output_file = 'teacher_student.csv'
teacher_student_df.to_csv(output_file, index=False)

print(f"The teacher-student hierarchy has been created and saved to '{output_file}'.")
