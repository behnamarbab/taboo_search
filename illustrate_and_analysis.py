# Generate the graphs for the improvements of the best solutions found by the Taboo Search algorithm.
# The graphs will be saved in a directory named "bests_graphs".

import os
import json

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from ranking import rank_it

# TODO: Set an equal maximum range for each file. (tai12a be 350000) for instance, or the maximum of all different cases.
# TODO: ... needs preprocessing of the data to find the maximum range for each file.

best_solutions = {
    "tai12a.dat": 224416,
    "tai12b.dat": 39464925,
    "tai15a.dat": 388214,
    "tai17a.dat": 491812,
    "tai100a.dat": 21052466,
}

def find_ranges(best_improvements):
    """
    Finds the maximum range for each file in the best improvements dictionary.
    
    Args:
        best_improvements (dict): A dictionary containing the best improvements.
        
    Returns:
        dict: A dictionary with the maximum range for each file.
    """
    ranges = {}
    for case_name, files in best_improvements.items():
        for file_name, runs in files.items():
            min_range = 10**12
            max_range = 0
            for run in runs:
                mx_indx = min(5, len(run)-1)
                max_range = max(max_range, run[mx_indx][1])
                min_range = min(min_range, run[-1][1])
            ranges[file_name] = ((min_range*8)//9, max_range)
    return ranges

def get_configs(json_config_file):
    """
    Reads a JSON configuration file and returns the configurations.
    
    Args:
        json_config_file (str): The path to the JSON configuration file.
        
    Returns:
        dict: A dictionary containing the configurations.
    """
    with open(json_config_file, "r") as f:
        configs = json.load(f)
    return configs

def generate_best_graphs(best_improvements, output_dir="results"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    colors = cm.tab10.colors
    ranges = find_ranges(best_improvements)
    configs = get_configs("configs.json")

    for case_name, files in best_improvements.items():
        for file_name, runs in files.items():
            fig, ax = plt.subplots(figsize=(10, 5))  # wider to make space

            ax.set_yscale('log')
            ax.set_ylim(ranges[file_name][0], ranges[file_name][1])
            ax.set_xlim(0, 4000)

            info = configs[case_name]
            neigh_type = None
            if info['neigh_type'] == 0:
                neigh_type = "SWAP"
            elif info['neigh_type'] == 1:
                neigh_type = "REVERSE"
            elif info['neigh_type'] == 2:
                neigh_type = "ADHOC"
            printable_info = f'Neighbor Function: {neigh_type}\n' \
                             f'Use Frequency: {info["use_frequencies"]}\n' \
                             f'# Iterations: {info["iterations"]}\n' \
                             f'Tenure: {info["tenure"]}'

            # This adds the box to the right of the plot
            fig.text(0.79, 0.2, printable_info,
                     ha='left', va='center', fontsize=10,
                     bbox=dict(boxstyle="round", facecolor="white", alpha=0.6))

            all_y = []
            max_iteration = 0
            for i, run in enumerate(runs):
                x_vals = [point[0] for point in run]
                y_vals = [point[1] for point in run]
                ax.plot(x_vals, y_vals, label=f'Run {i+1}', color=colors[i], alpha=0.4)
                max_iteration = max(max_iteration, x_vals[-1])

                full_y = np.full(max_iteration + 1, y_vals[0])
                for j in range(1, len(x_vals)):
                    full_y[x_vals[j - 1]:x_vals[j] + 1] = y_vals[j - 1]
                full_y[x_vals[-1]:] = y_vals[-1]
                all_y.append(full_y)

            all_y = np.array(all_y)
            avg_y = np.mean(all_y, axis=0)
            std_y = np.std(all_y, axis=0)
            x_range = np.arange(max_iteration + 1)

            ax.plot(x_range, avg_y, color='black', label='Average', linewidth=2)
            ax.fill_between(x_range, avg_y - std_y, avg_y + std_y, color='gray', alpha=0.3, label='±1 Std Dev')
            
            ax.axhline(y=best_solutions[file_name], color='red', linestyle='--', label='Best Known Solution')
            

            ax.set_title(f'{case_name} - {file_name}')
            ax.set_xlabel('Iterations')
            ax.set_ylabel('Fitness Value')
            ax.legend(loc='upper left', bbox_to_anchor=(1.02, 0.9), borderaxespad=0., fontsize=9)

            plt.tight_layout(rect=[0, 0, 0.92, 1])  # make room for the right-side text box
            file_safe_name = f"{case_name}_{file_name.replace('.', '_')}.png"
            if not os.path.exists(os.path.join(output_dir, file_name.split('.')[0])):
                os.makedirs(os.path.join(output_dir, file_name.split('.')[0]))
            outpath = os.path.join(output_dir, file_name.split('.')[0], file_safe_name)
            fig.savefig(outpath)
            print(f"Saved graph for {case_name} - {file_name} as {file_safe_name}")
            plt.close(fig)

def run(best_improvements=None):
    # Load the best improvements from a JSON file
    if best_improvements is None:
        with open("results/best_improvements.json", "r") as f:
            best_improvements = json.load(f)

    # Generate and save the graphs
    generate_best_graphs(best_improvements)
    rank_it(best_improvements)
    print("Graphs generated and saved in 'results' directory.")

if __name__ == "__main__":
    run()