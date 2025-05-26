import os

import numpy as np
import pandas as pd

def rank_it(best_improvements):
    # Create a dictionary to hold rankings per file (test)
    file_rankings = {}

    # First, collect all final values per file per case
    file_case_scores = {}

    for case_name, files in best_improvements.items():
        for file_name, runs in files.items():
            final_values = []
            for run in runs:
                if run:
                    final_values.append(run[-1][1])
            if final_values:
                avg_final = np.mean(final_values)
                file_case_scores.setdefault(file_name, {})[case_name] = avg_final

    # Now, compute rankings per file
    for file_name, case_values in file_case_scores.items():
        df = pd.DataFrame(list(case_values.items()), columns=['Case', 'Average Final Value'])
        df['Rank'] = df['Average Final Value'].rank(method='min')
        df.sort_values('Rank', inplace=True)
        file_rankings[file_name] = df

    # Display rankings for each file
    for file_name, df in file_rankings.items():
        print(f"\nRanking for {file_name}:\n")
        print(df.to_string(index=False))
    
    # Create CSV files for each test file's ranking
    csv_output_dir = "results/csv_rankings"
    os.makedirs(csv_output_dir, exist_ok=True)

    csv_file_paths = []

    for file_name, df in file_rankings.items():
        safe_file_name = file_name.replace(".", "_") + ".csv"
        csv_path = os.path.join(csv_output_dir, safe_file_name)
        df.to_csv(csv_path, index=False)
        csv_file_paths.append(csv_path)