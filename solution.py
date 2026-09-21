import os
import sys
import time
from collections import defaultdict, deque


class SearchTimeout(Exception):
    pass


def load_fragments(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found.")

    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    fragments = []
    for line_idx, line in enumerate(raw_lines, 1):
        if len(line) < 2:
            print(f"[Warning] Line {line_idx} ('{line}') length is < 2 characters and was skipped.")
            continue
        if not line.isdigit():
            print(f"[Warning] Line {line_idx} ('{line}') contains non-digit characters and was skipped.")
            continue
        fragments.append(line)

    return fragments


def build_graph(fragments):
    n = len(fragments)
    adj = defaultdict(list)

    prefix_map = defaultdict(list)
    for idx, frag in enumerate(fragments):
        prefix_map[frag[:2]].append(idx)

    for i, frag in enumerate(fragments):
        suffix = frag[-2:]
        for j in prefix_map[suffix]:
            if i != j:
                adj[i].append(j)

    return adj


def assemble_puzzle(fragments, path):
    if not path:
        return ""
    
    result = fragments[path[0]]
    for idx in path[1:]:
        result += fragments[idx][2:]
    return result


def find_longest_chain(fragments, time_budget=20.0):
    n = len(fragments)
    if n == 0:
        return []
    if n == 1:
        return [0]

    sys.setrecursionlimit(max(2000, n + 500))

    adj = build_graph(fragments)

    in_degrees = [0] * n
    for u in range(n):
        for v in adj[u]:
            in_degrees[v] += 1

    best_path = []
    best_sequence = ""
    visited = [False] * n

    deadline = time.time() + time_budget
    step_count = 0

    def check_time_limit():
        nonlocal deadline
        if time.time() > deadline:
            print(f"\n[TIME] {time_budget:.0f} seconds elapsed. Current record: {len(best_path)} fragments.")
            try:
                ans = input("Continue search for another 20 seconds? (y/n, default 'y'): ").strip().lower()
                if ans in ("", "y", "yes", "1"):
                    deadline = time.time() + time_budget
                    print("[+] Continuing search...\n")
                    return
                else:
                    raise SearchTimeout()
            except (EOFError, KeyboardInterrupt):
                raise SearchTimeout()

    def get_reachable_count(start_node):
        q = deque([start_node])
        seen = {start_node}

        while q:
            curr = q.popleft()
            for nxt in adj[curr]:
                if not visited[nxt] and nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)

        return len(seen) - 1

    def dfs(current, current_path):
        nonlocal best_path, best_sequence, step_count

        step_count += 1
        if (step_count & 1023) == 0:
            check_time_limit()

        curr_len = len(current_path)
        best_len = len(best_path)

        if curr_len > best_len:
            best_path = list(current_path)
            best_sequence = assemble_puzzle(fragments, best_path)
            print(f"  [+] New length record: {best_len + 1} fragments!")
        elif curr_len == best_len and curr_len > 0:
            candidate_seq = assemble_puzzle(fragments, current_path)
            if candidate_seq > best_sequence:
                best_path = list(current_path)
                best_sequence = candidate_seq
                print(f"  [+] Found larger numeric value for length {curr_len}!")

        candidates = [v for v in adj[current] if not visited[v]]
        candidates.sort(key=lambda v: sum(1 for w in adj[v] if not visited[w]))

        for next_node in candidates:
            if curr_len + (n - curr_len) <= len(best_path):
                continue

            upper_bound = curr_len + 1 + get_reachable_count(next_node)
            if upper_bound < len(best_path):
                continue

            visited[next_node] = True
            current_path.append(next_node)

            dfs(next_node, current_path)

            current_path.pop()
            visited[next_node] = False

    start_nodes = sorted(range(n), key=lambda i: (in_degrees[i], -len(adj[i])))

    print(f"Starting optimized search among {n} fragments...")
    print(f"Time limit: {time_budget:.0f} sec. (Ctrl + C to stop immediately)\n")

    try:
        for start in start_nodes:
            check_time_limit()
            if 1 + get_reachable_count(start) < len(best_path):
                continue

            visited[start] = True
            dfs(start, [start])
            visited[start] = False

    except (KeyboardInterrupt, SearchTimeout):
        print("\n[!] Search stopped. Recording best found result...")

    return best_path


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "fragments.txt"

    try:
        fragments = load_fragments(filepath)
        print(f"Loaded valid fragments: {len(fragments)} from file '{filepath}'")

        best_indices = find_longest_chain(fragments, time_budget=20.0)
        print(f"\nBest found length: {len(best_indices)} fragments.")

        final_sequence = assemble_puzzle(fragments, best_indices)
        print(f"Resulting string length: {len(final_sequence)} characters.")
        print("\nResulting numeric sequence:")
        print(final_sequence)

    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)
