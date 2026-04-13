
import csv
import io
import random
import time
import urllib.request
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple

DATASET_URL = "https://data.buenosaires.gob.ar/dataset/arbolado-publico-lineal/resource/ecf38a47-563f-42c1-9bd4-7cedf35d536b/download"

# 1
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self, root):
        self.root = Node(root)

    def insert(self, value: Any) -> Node:
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return current.left
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return current.right
                current = current.right
            else:
                return current


    def search(self, value): 
        current = self.root
        while current is not None:
            if value == current.value:
                return current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return None

# 3 con recursion
def height(node: Node) -> int:
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


# 3 de forma iterativa
def height2(root: Node) -> int:
    if root is None:
        return -1

    stack = [(root, 0)]
    max_height = 0

    while stack:
        node, current_height = stack.pop()
        max_height = max(max_height, current_height)

        if node.left:
            stack.append((node.left, current_height + 1))
        if node.right:
            stack.append((node.right, current_height + 1))

    return max_height

def printTree(node: Node, prefix: str = "", is_left: bool = True) -> None:
    if node is not None:
        print(prefix + ("├── " if is_left else "└── ") + str(node.value))
        printTree(node.left, prefix + ("│   " if is_left else "    "), True)
        printTree(node.right, prefix + ("│   " if is_left else "    "), False)

# 2 y 5
def generarDatos(size: int, ordered: bool = False) -> BinaryTree:
    data = random.sample(range(1, size * 10 + 1), size)
    duplicate = random.choice(data)
    print("elemento repetido ", duplicate)
    insert_pos = random.randint(0, len(data))
    data.insert(insert_pos, duplicate)
    if ordered:
        data.sort()

    tree = BinaryTree(data[0])
    for number in data[1:]:
        tree.insert(number)

    return tree



# 6

def build_balanced_tree(sorted_values: List[Any]) -> Optional[BinaryTree]:
    if len(sorted_values) == 0:
        return None

    middle = len(sorted_values) // 2
    tree = BinaryTree(sorted_values[middle])

    def insert_middle(low: int, high: int) -> None:
        if low > high:
            return

        current_middle = (low + high) // 2
        tree.insert(sorted_values[current_middle])
        insert_middle(low, current_middle - 1)
        insert_middle(current_middle + 1, high)

    insert_middle(0, middle - 1)
    insert_middle(middle + 1, len(sorted_values) - 1)
    return tree


def parse_int(value: str) -> Optional[int]:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def normalize_species(name: str) -> str:
    cleaned_name = (name or "").strip()
    if cleaned_name == "":
        return "SIN_ESPECIE"
    return cleaned_name


def load_arbolado_dataset(url: str, max_rows: Optional[int] = None) -> List[Dict[str, str]]:
    dataset_rows: List[Dict[str, str]] = []

    with urllib.request.urlopen(url) as response:
        with io.TextIOWrapper(response, encoding="utf-8") as text_stream:
            reader = csv.DictReader(text_stream)
            for index, row in enumerate(reader):
                dataset_rows.append(row)
                if max_rows is not None and index + 1 >= max_rows:
                    break

    return dataset_rows


def build_species_trees(dataset_rows: List[Dict[str, str]]) -> Tuple[Dict[str, BinaryTree], Dict[str, Dict[int, Dict[str, str]]]]:
    grouped_rows: Dict[str, List[Tuple[int, Dict[str, str]]]] = defaultdict(list)

    for row in dataset_rows:
        nro_registro = parse_int(row.get("nro_registro", ""))
        if nro_registro is None:
            continue

        species = normalize_species(row.get("nombre_cientifico", ""))
        grouped_rows[species].append((nro_registro, row))

    species_trees: Dict[str, BinaryTree] = {}
    species_records: Dict[str, Dict[int, Dict[str, str]]] = {}
    for species, records in grouped_rows.items():
        records.sort(key=lambda item: item[0])
        nro_values = [nro_registro for nro_registro, _ in records]
        species_tree = build_balanced_tree(nro_values)
        if species_tree is not None:
            species_trees[species] = species_tree
            species_records[species] = {nro_registro: row for nro_registro, row in records}

    return species_trees, species_records


def build_master_species_tree(species_trees: Dict[str, BinaryTree]) -> Optional[BinaryTree]:
    species_values = sorted(species_trees.keys())
    return build_balanced_tree(species_values)


def search_in_raw_dataset(dataset_rows: List[Dict[str, str]], species: str, nro_registro: int) -> Optional[Dict[str, str]]:
    for row in dataset_rows:
        row_species = normalize_species(row.get("nombre_cientifico", ""))
        row_nro_registro = parse_int(row.get("nro_registro", ""))
        if row_species == species and row_nro_registro == nro_registro:
            return row
    return None


def search_in_species_tree(
    species_trees: Dict[str, BinaryTree],
    species_records: Dict[str, Dict[int, Dict[str, str]]],
    species: str,
    nro_registro: int,
) -> Optional[Dict[str, str]]:
    species_tree = species_trees.get(species)
    if species_tree is None:
        return None

    result_node = species_tree.search(nro_registro)
    if result_node is None:
        return None
    return species_records.get(species, {}).get(result_node.value)


def search_in_master_tree(
    master_tree: Optional[BinaryTree],
    species_trees: Dict[str, BinaryTree],
    species_records: Dict[str, Dict[int, Dict[str, str]]],
    species: str,
    nro_registro: int,
) -> Optional[Dict[str, str]]:
    if master_tree is None:
        return None

    species_node = master_tree.search(species)
    if species_node is None:
        return None
    return search_in_species_tree(species_trees, species_records, species, nro_registro)


def benchmark_lookup(lookup_fn: Callable[[], Any], repetitions: int) -> Tuple[Any, float]:
    safe_repetitions = max(1, repetitions)

    result = None
    start_time = time.perf_counter()
    for _ in range(safe_repetitions):
        result = lookup_fn()
    average_seconds = (time.perf_counter() - start_time) / safe_repetitions

    return result, average_seconds


def get_example_targets(dataset_rows: List[Dict[str, str]], amount: int = 2) -> List[Tuple[str, int]]:
    targets: List[Tuple[str, int]] = []
    seen_targets = set()

    if len(dataset_rows) == 0:
        return targets

    candidate_indexes = [
        len(dataset_rows) // 3,
        (2 * len(dataset_rows)) // 3,
        len(dataset_rows) - 1,
    ]

    for index in candidate_indexes:
        row = dataset_rows[index]
        species = normalize_species(row.get("nombre_cientifico", ""))
        nro_registro = parse_int(row.get("nro_registro", ""))

        if nro_registro is None:
            continue

        target = (species, nro_registro)
        if target in seen_targets:
            continue

        seen_targets.add(target)
        targets.append(target)

        if len(targets) >= amount:
            return targets

    for row in dataset_rows:
        species = normalize_species(row.get("nombre_cientifico", ""))
        nro_registro = parse_int(row.get("nro_registro", ""))

        if nro_registro is None:
            continue

        target = (species, nro_registro)
        if target in seen_targets:
            continue

        seen_targets.add(target)
        targets.append(target)

        if len(targets) >= amount:
            break

    return targets


def run_punto_6(max_rows: Optional[int] = None, repetitions: int = 20) -> None:
    print("Punto 6 - Arbolado publico lineal de CABA")
    print(f"Descargando dataset desde: {DATASET_URL}")

    load_start = time.perf_counter()
    dataset_rows = load_arbolado_dataset(DATASET_URL, max_rows=max_rows)
    load_time = time.perf_counter() - load_start

    trees_start = time.perf_counter()
    species_trees, species_records = build_species_trees(dataset_rows)
    species_trees_time = time.perf_counter() - trees_start

    master_start = time.perf_counter()
    master_tree = build_master_species_tree(species_trees)
    master_tree_time = time.perf_counter() - master_start

    print(f"Filas cargadas: {len(dataset_rows)}")
    print(f"Especies detectadas: {len(species_trees)}")
    print(f"Tiempo de carga del CSV: {load_time:.3f} s")
    print(f"Tiempo de creacion de arboles por especie: {species_trees_time:.3f} s")
    print(f"Tiempo de creacion del arbol maestro: {master_tree_time:.6f} s")
    print(f"Repeticiones para benchmark por busqueda: {max(1, repetitions)}")

    search_targets = get_example_targets(dataset_rows, amount=2)
    if len(search_targets) < 2:
        print("No hay suficientes registros validos para ejecutar las busquedas de ejemplo.")
        return

    for index, (species, nro_registro) in enumerate(search_targets, start=1):
        species_lookup = lambda: search_in_species_tree(species_trees, species_records, species, nro_registro)
        master_lookup = lambda: search_in_master_tree(master_tree, species_trees, species_records, species, nro_registro)
        raw_lookup = lambda: search_in_raw_dataset(dataset_rows, species, nro_registro)

        species_result, species_time = benchmark_lookup(species_lookup, repetitions)
        master_result, master_time = benchmark_lookup(master_lookup, repetitions)
        raw_result, raw_time = benchmark_lookup(raw_lookup, repetitions)

        print("\n" + "=" * 72)
        print(f"Busqueda {index}: especie='{species}', nro_registro={nro_registro}")
        print(f"Arbol por especie: {species_time * 1000:.6f} ms")
        print(f"Arbol maestro (especie -> arbol): {master_time * 1000:.6f} ms")
        print(f"Dataset original (busqueda lineal): {raw_time * 1000:.6f} ms")

        if species_result is not None:
            print(f"Encontrado en arbol por especie: SI | direccion={species_result.get('direccion_normalizada', 'N/D')}")
        else:
            print("Encontrado en arbol por especie: NO")

        if master_result is not None:
            print(f"Encontrado en arbol maestro: SI | direccion={master_result.get('direccion_normalizada', 'N/D')}")
        else:
            print("Encontrado en arbol maestro: NO")

        if raw_result is not None:
            print(f"Encontrado en dataset lineal: SI | direccion={raw_result.get('direccion_normalizada', 'N/D')}")
        else:
            print("Encontrado en dataset lineal: NO")


def main() -> None:
    # Punto 6
    # max_rows=None usa el dataset completo.
    # Para una corrida mas rapida se puede cambiar el valor del parametro max_rows, max_rows=50000.
    run_punto_6(max_rows=None, repetitions=20)

if __name__ == "__main__":
    main()
