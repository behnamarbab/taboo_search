import argparse
import os
import math

from QAP import QAP
from taboo import TabooSearch

def parse_args():
    args = argparse.ArgumentParser(description="Taboo Search for QAP")
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

if __name__ == "__main__":
    args = parse_args()
    filename=args.file
    tenure=args.tenure
    iterations=args.iterations
    runs=args.runs
    
    filepath = os.path.join("data", filename)
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        exit(1)
    
    if filename not in best_solutions:
        print(f"File {filename} not in best solutions dictionary.")
        exit(1)

    print(f"Running Taboo Search for QAP on \"{filename}\"")
    print(f"Best known solution: {best_solutions[filename]}")
    sum = 0
    best_fitness = math.inf
    for i in range(runs):
        qap = QAP(filepath, tenure=tenure)
        TS = TabooSearch(qap, iterations=iterations)
        best = TS.run()
        if best[2] < best_fitness:
            best_fitness = best[2]
        sum += best[2]
        print(" " + "-" * 92)
        print(f"| {'Run:':<5}{i+1:<5}| {'Iterations:':<12}{iterations:<7}| {'Tenure:':<8}{tenure:<4}| {'Best Fitness:':<14}{best[2]:<10} | diff: {best[2] - best_solutions[filename]:<10} |")
        if len(best[0]) > 20:
            print(f"| Best solution: {', '.join([str(b+1) for b in best[0][:18]])+', ...':<75} |")
        else:
            print(f"| Best solution: {', '.join([str(b+1) for b in best[0]]):<76}|")
    print(" " + "-" * 92)
    print("Average best fitness: ", sum//runs)
    print(f"Best fitness found {best_fitness}, best known {best_solutions[filename]}, diff: {best_fitness - best_solutions[filename]}")
    