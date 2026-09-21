# Digital Puzzle Solution (PortaOne)

**[English Version](#english-version)** | **[Українська версія](#українська-версія)**

---

<a name="english-version"></a>
## English Version

### 1. Problem Formulation & Mathematical Model

* **Input**: A text file containing $N$ fragments (digit strings).
* **Connection Rule**: Fragment $A$ connects to fragment $B$ ($A \to B$) if the last 2 digits of $A$ match the first 2 digits of $B$ (`A[-2:] == B[:2]`).
* **Constraint**: Each fragment can be used in the sequence at most once.
* **Objective**: Find the longest sequence of fragments (and in case of equal length, the largest numerical value) and concatenate them into a single string with a 2-digit overlap.

#### Graph Theory Representation
The problem is modeled as finding the **Longest Simple Path** in a directed graph:
* **Vertices**: Fragment indices $0, 1, \dots, N-1$.
* **Directed Edges**: $(u, v)$ where `fragments[u][-2:] == fragments[v][:2]` and $u \neq v$.

Since the general Longest Simple Path problem is **NP-hard**, this solution combines exact graph search with advanced heuristics and pruning.

---

### 2. Key Algorithms & Optimizations

1. **Linear Graph Construction $O(N)$ via Prefix Hash Map**:
   Instead of comparing all pairs in $O(N^2)$, fragments are indexed by their 2-digit prefixes: `prefix_map[frag[:2]].append(idx)`. Looking up successors for any suffix takes $O(1)$ amortized time.

2. **DFS + Backtracking**:
   Explores the search tree while rolling back state (`visited[node] = False` and `path.pop()`), allowing fragments to be reconsidered in alternative candidate paths.

3. **Warnsdorff's Heuristic**:
   Candidates at each step are sorted in ascending order of their remaining unvisited outgoing exits:
   $$\text{score}(v) = \sum_{w \in \text{adj}[v]} [\text{not } visited[w]]$$
   The search prioritizes tight bottlenecks before they become unreachable dead ends, enabling the algorithm to rapidly reach deep, near-optimal paths.

4. **Two-Level Branch & Bound Pruning**:
   * **Level 1 ($O(1)$)**: Fast upper-bound check based on remaining unvisited nodes:
     $$\text{len}(path) + (N - \text{len}(path)) \le \text{len}(best\_path) \implies \text{prune}$$
   * **Level 2 (BFS Reachability)**: Computes the exact number of unvisited nodes reachable from the candidate. If the current length plus the reachable set cannot exceed the current record, the entire subtree is pruned.

5. **Tie-Breaking by Maximum Numerical Value**:
   When multiple valid sequences share the same maximum fragment count, preference is given to the sequence that is lexicographically larger as a number.

6. **Time Budgeting & Interactive Control**:
   * Runs in 20-second time budgets by default.
   * If the time expires before completing the search space, the user is interactively prompted to continue for another 20 seconds (`y`) or finish (`n`).
   * Supports immediate, graceful termination at any time via **Ctrl + C** (`KeyboardInterrupt`).
   * In non-interactive environments (pipes/automated test runners), it completes cleanly without hanging.

---

### 3. Function Reference

* **`load_fragments(filepath)`**: Reads and validates the input text file. Verifies file existence, strips whitespace, ignores empty lines, and validates that each fragment consists strictly of digits and has length $\ge 2$.
* **`build_graph(fragments)`**: Constructs the adjacency list `adj` using prefix indexing in $O(N)$ time and memory.
* **`assemble_puzzle(fragments, path)`**: Assembles the sequence of fragment indices into the final concatenated string (first piece fully, subsequent pieces without the first 2 digits).
* **`find_longest_chain(fragments, time_budget=20.0)`**: Main search coordinator. Adjusts recursion limits, ranks start nodes by `in-degree == 0`, executes Warnsdorff-guided DFS with reachability pruning, and manages time checks.

---

### 4. Usage Instructions

#### Run with default file (`fragments.txt`):
```powershell
py -3 solution.py
```

#### Run with a custom file:
```powershell
py -3 solution.py custom_fragments.txt
```

#### Interactive Controls:
* When prompted after 20 seconds:
  * Press **Enter** or type `y` to continue searching for another 20 seconds.
  * Type `n` to stop and output the current best sequence.
* Press **Ctrl + C** at any moment to stop the search immediately and print the best result.

---
---

<a name="українська-версія"></a>
## Українська версія

### 1. Постановка задачі та математична модель

* **Вхідні дані**: текстовий файл із $N$ фрагментів (числових рядків).
* **Правило з'єднання**: фрагмент $A$ з'єднується з фрагментом $B$ ($A \to B$), якщо останні 2 цифри числа $A$ збігаються з першими 2 цифрами числа $B$ (`A[-2:] == B[:2]`).
* **Обмеження**: кожен фрагмент може бути використаний у ланцюжку щонайбільше 1 раз.
* **Ціль**: знайти найдовшу послідовність фрагментів (а при рівній довжині — найбільше числове значення) і склеїти їх в один суцільний числовий рядок із перекриттям у 2 цифри.

#### Теорія графів
Задача формалізується як пошук **найдовшого простого шляху (Longest Simple Path)** в орієнтованому графі:
* **Вершини**: індекси фрагментів $0, 1, \dots, N-1$.
* **Орієнтовані ребра**: $(u, v)$, де `fragments[u][-2:] == fragments[v][:2]` та $u \neq v$.

Оскільки в загальному випадку задача про найдовший шлях є **NP-складною (NP-hard)**, для її ефективного розв'язання використано комбінацію точних та евристичних методів.

---

### 2. Ключові алгоритми та оптимізації

1. **Лінійна побудова графа $O(N)$ через хеш-таблицю префіксів**:
   Замість квадратичного порівняння $O(N^2)$ усіх пар чисел, фрагменти попередньо групуються у словник за першими двома цифрами `prefix_map[frag[:2]].append(idx)`. Пошук наступників для суфікса займає $O(1)$.

2. **DFS + Backtracking (глибинний пошук з поверненням)**:
   Дослідження дерева шляхів із відновленням стану (`visited[node] = False` та `path.pop()`), що дозволяє кожному фрагменту брати участь в альтернативних ланцюжках.

3. **Евристика Варнсдорфа (Warnsdorff's Rule)**:
   При виборі наступного фрагмента кандидати сортуються за зростанням кількості їхніх вільних виходів:
   $$\text{score}(v) = \sum_{w \in \text{adj}[v]} [\text{not } visited[w]]$$
   Алгоритм першочергово відвідує «вузькі місця» графа, не даючи їм перетворитися на недосяжні тупики, що дозволяє миттєво знаходити глибокі шляхи.

4. **Дворівневий метод гілок і меж (Branch & Bound Pruning)**:
   * **Рівень 1 ($O(1)$)**: швидка перевірка за загальною кількістю невідвіданих вершин:
     $$\text{len}(path) + (N - \text{len}(path)) \le \text{len}(best\_path) \implies \text{відсікання}$$
   * **Рівень 2 (BFS Reachability)**: підрахунок кількості невідвіданих вершин, які фізично досяжні з кандидата. Якщо поточна довжина + досяжні вершини не перевищують рекорд — піддерево відкидається.

5. **Tie-breaking за максимальним числовим значенням**:
   Якщо знайдено два різні шляхи однакової рекордної довжини, перевага віддається тому, чий склеєний рядок є лексикографічно більшим.

6. **Керування часом (Time Budget & Interactivity)**:
   * Пошук працює з квантом часу (за замовчуванням 20 секунд).
   * Після вичерпання часу користувач може продовжити пошук ще на 20 секунд (ввівши `y` або натиснувши Enter) або завершити та зафіксувати результат.
   * Підтримується негайне безпечне переривання через `Ctrl + C` (`KeyboardInterrupt`).
   * Якщо скрипт запущено у фоні чи через пайп (неінтерактивно), він коректно зупиняється без зависання.

---

### 3. Детальний опис функцій

* **`load_fragments(filepath)`**: зчитування та валідація вхідного файлу. Перевіряє існування файлу, ігнорує порожні рядки, перевіряє, що рядки складаються з цифр і мають довжину $\ge 2$.
* **`build_graph(fragments)`**: побудова списку суміжності `adj` через префіксне індексування за $O(N)$ за часом і пам'яттю.
* **`assemble_puzzle(fragments, path)`**: збирання фінального рядка за послідовністю індексів `path` (перший елемент повністю, наступні — без перших 2 цифр).
* **`find_longest_chain(fragments, time_budget=20.0)`**: головний координатор пошуку. Встановлює ліміт рекурсії, сортує старти за витоками (`in-degree == 0`), виконує DFS з Варнсдорфом та відсіканням гілок, керує часом і зупинкою.

---

### 4. Інструкція із запуску

#### Запуск за замовчуванням (з файлом `fragments.txt`):
```powershell
py -3 solution.py
```

#### Запуск із довільним файлом:
```powershell
py -3 solution.py custom_fragments.txt
```

#### Керування під час роботи:
* Після 20 секунд у консолі з'явиться запит:
  * Натисніть **Enter** або введіть `y` — пошук продовжиться ще на 20 секунд.
  * Введіть `n` — пошук завершиться, і буде виведено найкращий знайдений результат.
* У будь-який момент натисніть **Ctrl + C** для миттєвої зупинки та виведення рекорду.
