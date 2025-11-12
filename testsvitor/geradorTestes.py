"""
Gera dois traces no formato do projeto (um endereço inteiro por linha):
 - trace_random_500.in: acessos randômicos
 - trace_sequential_500.in: acessos sequenciais (blocos repetidos)

Cada arquivo tem pelo menos 500 acessos.
"""
import random
from pathlib import Path

PAGE_SIZE = 4096            # mantém compatibilidade com o projeto
N_ACESSOS = 500             # número de acessos por trace (>= 500)
# Para trace sequencial: número de páginas distintas no working set
SEQ_WORKSET_PAGES = 100
# Para trace randômico: número máximo de páginas possíveis
RAND_PAGE_RANGE = 512
RANDOM_SEED = 42            # tornar reproduzível;

OUT_DIR = Path(".")
TRACE_SEQ_FN = OUT_DIR / "trace_sequential_500.in"
TRACE_RAND_FN = OUT_DIR / "trace_random_500.in"

def gen_sequential_addresses(n_accesses, workset_pages, page_size):
    """Gera acessos em páginas 0..workset_pages-1 repetidos até n_accesses."""
    addresses = []
    # repetimos blocos de 0..workset_pages-1 para criar locality
    i = 0
    while len(addresses) < n_accesses:
        page = i % workset_pages
        # adiciona um offset aleatório dentro da página para variar o endereço
        offset = random.randint(0, page_size - 1)
        addresses.append(page * page_size + offset)
        i += 1
    return addresses

def gen_random_addresses(n_accesses, page_range, page_size):
    """Gera n_accesses endereços com páginas uniformemente aleatórias em [0, page_range)."""
    addresses = []
    for _ in range(n_accesses):
        page = random.randint(0, page_range - 1)
        offset = random.randint(0, page_size - 1)
        addresses.append(page * page_size + offset)
    return addresses

def write_trace(path, addresses):
    with open(path, "w") as f:
        for a in addresses:
            f.write(f"{a}\n")
    print(f"Wrote {len(addresses)} addresses to: {path}")

def main():
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    seq_addrs = gen_sequential_addresses(N_ACESSOS, SEQ_WORKSET_PAGES, PAGE_SIZE)
    rand_addrs = gen_random_addresses(N_ACESSOS, RAND_PAGE_RANGE, PAGE_SIZE)

    write_trace(TRACE_SEQ_FN, seq_addrs)
    write_trace(TRACE_RAND_FN, rand_addrs)

    print("\nArquivos gerados:")
    print(f" - Sequencial: {TRACE_SEQ_FN}")
    print(f" - Randômico : {TRACE_RAND_FN}")

if __name__ == "__main__":
    main()
