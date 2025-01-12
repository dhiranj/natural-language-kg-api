import pandas as pd

def load_datasets(data_folder="datasets"):
    files = {
        "same_college_mapping": f"{data_folder}/same_college_results.csv",
        "author_mapping": f"{data_folder}/filtered_author_mapping.csv",
        "coauthor_mapping": f"{data_folder}/filtered_coauthor_mapping_top_1000.csv",
        "id_to_author_mapping": f"{data_folder}/id_to_author_mapping.csv",
        "teacher_student": f"{data_folder}/teacher_student.csv",
        "top_1000_scientists": f"{data_folder}/top_1000_computer_scientists.csv",
    }
    
    datasets = {name: pd.read_csv(path) for name, path in files.items()}
    return datasets
