from collections import defaultdict
from heapq import *

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf")

# if __name__ == "__main__":
#     edges = [
#         ("1", "2", 20),
#         ("2", "3", 20),
#         ("3", "4", 10),
#         ("4", "5", 20),
#         ("5", "6", 20),
#         ("1", "7", 15),
#         ("2", "8", 10),
#         ("3", "9", 10),
#         ("4", "10",20),
#         ("5", "11",15),
#         ("6", "12",20),
#         ("7", "8", 20),
#         ("8", "9", 10),
#         ("9", "10", 20),
#         ("10", "11", 15),
#         ("11", "12", 20),
#         ("7", "13", 20),
#         ("8", "14", 15),
#         ("9", "15", 20),
#         ("10", "16", 20),
#         ("11", "17", 20),
#         ("12", "18", 15),
#         ("13", "14", 10),
#         ("15", "16", 10),
#         ("16", "17", 10),
#         ("17", "18", 20),
#         ("13", "19", 15),
#         ("14", "20", 10),
#         ("15", "21", 10),
#         ("16", "22", 15),
#         ("17", "23", 15),
#         ("18", "24", 20),
#     ]
#
#     print("=== Dijkstra ===")
#     # print(edges)
#     print("2 -> 20:")
#     print(dijkstra(edges, "2", "20"))
#     # print("F -> G:")
#     # print(dijkstra(edges, "F", "G"))