import argparse
import os
import math

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

def save_results_to_markdown(filename, results):
    """
    Save the results of the Taboo Search runs to a markdown file.

    Args:
        filename (str): The name of the markdown file to save.
        results (list of dict): A list of dictionaries containing run results.
    """
    markdown_file = filename.replace(".dat", "_results.md")
    with open(markdown_file, "w") as f:
        # Write the header
        f.write(f"# Results for QAP\n\n")
        header = "| Algorithm <br> TabooSearch |" + "|".join(f" Run {i+1} " for i in range(10)) + "|"
        f.write(header + "\n")
        tlines = '|'.join(['-'*len(x) for x in header.split("|")])
        f.write(tlines + "\n")        
        # Write each result row
        for res in results.keys():
            results_line = f"| {res} | " + "|".join(f"{result}" for result in results[res]) + "|"
            f.write(results_line + "\n")
        
    print(f"Results saved to {markdown_file}")

if __name__ == "__main__":
    args = parse_args()
    test_all = args.test_all
    filename=args.file
    tenure=args.tenure
    iterations=args.iterations
    runs=args.runs
    
    if test_all:
        results = {f: [] for f in best_solutions.keys()}
    else:
        results = {filename: []}
    for f in results.keys():
        data_filepath = os.path.join("data", f)
        if not os.path.exists(data_filepath):
            print(f"File {data_filepath} does not exist.")
            exit(1)
        if f not in best_solutions:
            print(f"File {f} not in best solutions dictionary.")
            exit(1)

        print(f"Running Taboo Search for QAP on \"{f}\"")
        print(f"Best known solution: {best_solutions[f]}")

        for i in range(runs):
            # Setup and run Taboo Search on the QAP instance
            qap = QAP(data_filepath, tenure=tenure, neigh_type=NeighType.REVERSE)
            TS = TabooSearch(qap, iterations=iterations)
            best = TS.run()
            
            results[f].append(best[2])

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

    save_results_to_markdown("results.md", results)