from functools import lru_cache
from typing import List, Tuple, Dict
import os
import time

# ---------- helpers de bitboard ----------
def bit_index(r: int, c: int, cols: int) -> int:
    return r * cols + c

def bits_from_cells(cells: List[Tuple[int, int]], cols: int) -> int:
    bits = 0
    for r, c in cells:
        bits |= 1 << bit_index(r, c, cols)
    return bits

def neighbors_mask_for_cells(cells: List[Tuple[int, int]], rows: int, cols: int) -> int:
    mask = 0
    for r, c in cells:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr = r + dr
                cc = c + dc
                if 0 <= rr < rows and 0 <= cc < cols:
                    mask |= 1 << bit_index(rr, cc, cols)
    return mask

# ---------- generate placements: store as two parallel tuples of ints (bits, adj) ----------
def generate_placements_for_length(length: int, rows: int, cols: int):
    bits_list = []
    adj_list = []
    for r in range(rows):
        for c in range(cols):
            if c + length <= cols:
                cells = [(r, c + i) for i in range(length)]
                bits = bits_from_cells(cells, cols)
                adj = neighbors_mask_for_cells(cells, rows, cols)
                bits_list.append(bits)
                adj_list.append(adj)
            if r + length <= rows and length > 1:
                cells = [(r + i, c) for i in range(length)]
                bits = bits_from_cells(cells, cols)
                adj = neighbors_mask_for_cells(cells, rows, cols)
                bits_list.append(bits)
                adj_list.append(adj)
    return tuple(bits_list), tuple(adj_list)

# ---------- contador single-thread (otimizado) ----------
def count_fleet_configurations(rows: int, cols: int, fleet: List[int], allow_touch: bool = True) -> int:
    # agrupa frota por comprimento
    freq: Dict[int, int] = {}
    for L in fleet:
        freq[L] = freq.get(L, 0) + 1
    lengths = tuple(sorted(freq.keys()))
    counts_init = tuple(freq[L] for L in lengths)

    # precompute placements alinhados ao índice de 'lengths'
    placements_by_len_bits = []
    placements_by_len_adj = []
    for L in lengths:
        bits_arr, adj_arr = generate_placements_for_length(L, rows, cols)
        placements_by_len_bits.append(bits_arr)
        placements_by_len_adj.append(adj_arr)
    placements_by_len_bits = tuple(placements_by_len_bits)
    placements_by_len_adj = tuple(placements_by_len_adj)

    total_cells = rows * cols

    @lru_cache(maxsize=None)
    def dfs(counts_local: Tuple[int, ...], occ_mask_local: int) -> int:
        # terminal
        if all(c == 0 for c in counts_local):
            return 1
        # poda por células livres
        free = total_cells - occ_mask_local.bit_count()
        needed = sum(L * c for L, c in zip(lengths, counts_local))
        if free < needed:
            return 0

        # escolhe tipo com menos colocações válidas (contagem rápida)
        best_i = None
        best_cnt = None
        for i, (L, c) in enumerate(zip(lengths, counts_local)):
            if c == 0:
                continue
            bits_arr = placements_by_len_bits[i]
            adj_arr = placements_by_len_adj[i]
            cnt = 0
            if allow_touch:
                for b in bits_arr:
                    if (b & occ_mask_local) == 0:
                        cnt += 1
            else:
                for b, a in zip(bits_arr, adj_arr):
                    if (b & occ_mask_local) == 0 and (a & occ_mask_local) == 0:
                        cnt += 1
            if cnt == 0:
                return 0
            if best_cnt is None or cnt < best_cnt:
                best_cnt = cnt
                best_i = i
                if cnt == 1:
                    break

        # expande apenas o tipo escolhido (segunda passagem, sem alocar listas)
        total = 0
        bits_arr = placements_by_len_bits[best_i]
        adj_arr = placements_by_len_adj[best_i]
        counts_list = list(counts_local)
        for b, a in zip(bits_arr, adj_arr):
            if (b & occ_mask_local) != 0:
                continue
            if not allow_touch and (a & occ_mask_local) != 0:
                continue
            counts_list[best_i] -= 1
            total += dfs(tuple(counts_list), occ_mask_local | b)
            counts_list[best_i] += 1
        return total

    return dfs(counts_init, 0)


# ---------- exemplo ----------
if __name__ == "__main__":
    rows, cols = 10, 10
    fleet = [5, 4, 3, 2]
    allow_touch = True

    # ajuste conforme capacidade da sua máquina
    print(f"Tabuleiro: {rows}x{cols}, frota: {fleet}, allow_touch={allow_touch}")
    t0 = time.perf_counter()
    total = count_fleet_configurations(rows, cols, fleet, allow_touch=allow_touch)
    t1 = time.perf_counter()
    print(f"Configurações: {total}")
    print(f"Tempo: {t1 - t0:.3f}s")
