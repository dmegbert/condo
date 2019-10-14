from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from scrapers.j_and_m import get_j_and_m_condos
from scrapers.lino import get_lino_condos
from scrapers.tropical_coast import get_tropical_condos
from scrapers.island_west import get_island_condos
from mailer.sendy import send_condos


def main():
    condo_funcs = [get_lino_condos, get_j_and_m_condos, get_island_condos, get_tropical_condos]
    condos = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_condos) for get_condos in condo_funcs]
        for future in as_completed(futures):
            try:
                condos.append(future.result())
            except Exception as exc:
                print(exc)
    condos = [item for sublist in condos for item in sublist]
    with open('/Users/egbert/projects/condo/data/condos.json', 'w') as f:
        json.dump(condos, f)
    send_condos()


if __name__ == '__main__':
    main()
