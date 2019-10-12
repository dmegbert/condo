from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from scrapers.tropical_coast import get_tropical_condos
from scrapers.island_west import get_island_condos


def main():
    tropical_condos = get_tropical_condos()
    island_condos = get_island_condos()
    with open('data/condos.json', 'w') as f:
        json.dump([*tropical_condos, *island_condos], f)


if __name__ == '__main__':
    main()
