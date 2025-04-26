from QAP import QAP
from taboo import TabooSearch

for i in range(10):
    qap = QAP('data/tai100a.dat', tenure=8)
    TS = TabooSearch(qap, iterations=1000)
    best = TS.run()
    print(f"Best Solution: {best[0]}, {best[2]}")