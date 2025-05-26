import argparse
import os
import json
from copy import deepcopy as cp

from QAP import QAP, NeighType
from taboo import TabooSearch

def parse_args():
    args = argparse.ArgumentParser(description="Taboo Search for QAP")
    args.add_argument("test_all", nargs="?", const=True, default=False, 
                        help="Run all tests if specified")
    args.add_argument("-f", "--file", type=str, default="tai12a.dat",
                        help="Path to the data file")
    args.add_argument("-t", "--tenure", type=int, default=5,
                        help="Tenure for the Taboo search")
    args.add_argument("-i", "--iterations", type=int, default=1000,
                        help="Number of iterations for the Taboo search")
    # Argument for number of runs - default to 10
    args.add_argument("-r", "--runs", type=int, default=10,
                        help="Number of runs for the Taboo search")
    # Not used, but kept for compatibility
    args.add_argument("-s", "--seed", type=int, default=0,
                        help="Random seed for the Taboo search")
    return args.parse_args()

best_solutions = {
    "tai12a.dat": 224416,
    "tai12b.dat": 39464925,
    "tai15a.dat": 388214,
    "tai17a.dat": 491812,
    "tai100a.dat": 21052466,
}

def load_configurations(filename):
    """
    Load configurations from a JSON file.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        dict: A dictionary containing the configurations.
    """
    with open(filename, "r") as f:
        configurations = json.load(f)
    return configurations

def save_results_to_markdown(filename, results):
    """
    Save the results of the Taboo Search runs to a markdown file.

    Args:
        filename (str): The name of the markdown file to save.
        results (list of dict): A list of dictionaries containing run results.
    """
    markdown_file = filename.replace(".dat", "_results.md")
    with open(markdown_file, "w") as f:
        for conf_res in results.keys():
            # Write the header
            f.write(f"# Results for QAP for {conf_res}\n\n")
            header = "| Algorithm <br> TabooSearch |" + "|".join(f" Run {i+1} " for i in range(10)) + "|"
            f.write(header + "\n")
            tlines = '|'.join(['-'*len(x) for x in header.split("|")])
            f.write(tlines + "\n")        
            # Write each result row
            for res in results[conf_res].keys():
                results_line = f"| {res} | " + "|".join(f"{result}" for result in results[conf_res][res]) + "|"
                f.write(results_line + "\n")
                
            f.write("\n")
    print(f"Results saved to {markdown_file}")

def save_best_improvements_to_json(filename, best_improvements):
    """
    Save the best improvements to a JSON file.

    Args:
        filename (str): The name of the JSON file to save.
        best_improvements (dict): A dictionary containing the best improvements.
    """
    with open(filename, "w") as f:
        json.dump(best_improvements, f, indent=4)
    print(f"Best improvements saved to {filename}")

if __name__ == "__main__":
    args = parse_args()
    test_all = args.test_all
    filename=args.file
    tenure=args.tenure
    iterations=args.iterations
    runs=args.runs
    configs = load_configurations("configs.json")
    
    if test_all:
        results = {f: [] for f in best_solutions.keys()}
        conf_best_improvements = {f: cp(results) for f in configs.keys()}
        conf_results = {f: cp(results) for f in configs.keys()}
    else:
        results = {filename: []}
        conf_best_improvements = {"case1": cp(results)}
        conf_results = {"case1": cp(results)}

    for con_r in conf_results.keys():
        results = conf_results[con_r]
        best_improvements = conf_best_improvements[con_r]
        for f in results.keys():
            neigh_type = configs[con_r]["neigh_type"]
            if neigh_type == 0:
                neigh_type = NeighType.SWAP
            elif neigh_type == 1:
                neigh_type = NeighType.REVERSE
            elif neigh_type == 2:
                neigh_type = NeighType.ADHOC

            use_frequencies = configs[con_r]["use_frequencies"]
            iterations = configs[con_r]["iterations"]
            tenure = configs[con_r]["tenure"]
            
            data_filepath = os.path.join("data", f)
            if not os.path.exists(data_filepath):
                print(f"File {data_filepath} does not exist.")
                exit(1)
            if f not in best_solutions:
                print(f"File {f} not in best solutions dictionary.")
                exit(1)

            print(f"Running Taboo Search for QAP on \"{f}\" for test case {con_r}")
            print(f"Best known solution: {best_solutions[f]}")

            for i in range(runs):
                # Setup and run Taboo Search on the QAP instance
                qap = QAP(data_filepath, tenure=tenure, neigh_type=neigh_type, use_frequencies=use_frequencies)
                TS = TabooSearch(qap, iterations=iterations)
                best = TS.run()
                
                results[f].append(best[2])
                best_improvements[f].append(TS.tracked_bests)

                # Result and statistics
                print(" " + "-" * 92)
                print(f"| {'Run:':<5}{i+1:<5}| {'Iterations:':<12}{iterations:<7}| {'Tenure:':<8}{tenure:<4}| {'Best Fitness:':<14}{best[2]:<10} | diff: {best[2] - best_solutions[f]:<10} |")
                if len(best[0]) > 20:
                    print(f"| Best solution: {', '.join([str(b+1) for b in best[0][:18]])+', ...':<75} |")
                else:
                    print(f"| Best solution: {', '.join([str(b+1) for b in best[0]]):<76}|")
            
            # Final statistics
            print(" " + "-" * 92)
            print("Average best fitness: ", sum(results[f])//runs)
            print(f"Best fitness found {min(results[f])}, best known {best_solutions[f]}, diff: {min(results[f]) - best_solutions[f]}")
            print()

    save_results_to_markdown("results.md", conf_results)
    save_best_improvements_to_json("best_improvements.json", conf_best_improvements)
