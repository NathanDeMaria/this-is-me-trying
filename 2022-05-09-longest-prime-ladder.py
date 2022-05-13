"""
https://fivethirtyeight.com/features/can-you-build-the-longest-ladder/
"""
import logging
import networkx as nx


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()


def _is_prime(n: int) -> bool:
    """
    Horribly inefficient, but works
    """
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True

def _get_primes(digits: int) -> list[int]:
    return [i for i in range(10 ** (digits - 1), 10 ** digits) if _is_prime(i)]


def _has_edge(a: str, b: str) -> bool:
    if a == b:
        return False
    assert len(a) == len(b)
    return sum([a[i] == b[i] for i in range(len(a))]) == len(a) - 1


def get_longest_prime_ladder(n_digits: int) -> list[int]:
    primes = [str(p) for p in _get_primes(n_digits)]
    logger.info(f"{len(primes)=}")
    graph = nx.Graph()
    graph.add_nodes_from(range(len(primes)))
    for i, p1 in enumerate(primes):
        for j, p2 in enumerate(primes):
            if i > j:
                edge = _has_edge(p1, p2)
                if edge:
                    graph.add_edge(i, j)
                    graph.add_edge(j, i)
                
    
    paths = nx.all_pairs_shortest_path(graph)
    longest_path = []
    longest_length = 0
    for _, paths_from_root in paths:
        for _, path_between in paths_from_root.items():
            if len(path_between) > longest_length:
                longest_length = len(path_between)
                longest_path = path_between
    
    return [int(primes[i]) for i in longest_path]
    


if __name__ == '__main__':
    for n in range(3, 7):
        logger.info(f"Starting {n}")
        print(get_longest_prime_ladder(n))
        logger.info(f"Done with {n}")
