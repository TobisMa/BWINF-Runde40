import os
from typing import Dict, Tuple, List


def read_file(path: str) -> List[List[int]]:
    """Liest Datei ein und gibt die Tabelle zurück

    Args:
        path (str): Der Pfad zur Datei

    Returns:
        List[List[int]]: Die Präferenztabelle
    """
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    table: List[List[int]] = []
    for line in lines[1:]:  # ignoriere erste Zeile, da nur Breite und Höhe (nicht wichtig in python)
        table.append([])

        for d in line.split(" "):   
            table[-1].append(int(d))

    return table


def get_best_type_of_date(table: List[List[int]]) -> Dict[int, int]:
    """Bestimmt die angenehmste Art von Termin jeder Person und gibt
       das dabei entsehende Dictionary zurück.

    Args:
        table (List[List[int]]): die Präferenztabelle

    Returns:
        Dict[int, int]: das Dictionary, welches die angenehmste Art von Termin jeder Person beinhaltet
    """
    return {i: min(person_dates) for i, person_dates in enumerate(table)}


def solve(table: List[List[int]]) -> Tuple[List[int], int]:
    """Berechnet den/die besten Termin(e) und dessen/deren notwenidgen Änderungen

    Args:
        table (List[List[int]]): die Pröferenztabelle

    Returns:
        Tuple[List[int], int]: An erster Stelle alle Spalten
    """
    persons_best_type_of_date = get_best_type_of_date(table)

    columns_in_row = len(table[0])  # Annahme: Jede Zeile hat dieselbe Anzahl von Werten,
                                    # was der Fall in einer Tabelle ist
    res_columns = []
    res_changes: int = len(table)  # mindestens die Änderungen in einer anderen Spalte
                                   # sind größer

    for column in range(columns_in_row):
        # berechnen der Änderungen
        changes = 0
        for row in range(len(table)):
            if table[row][column] > persons_best_type_of_date[row]:
                changes += 1
        
        # speichervariable nach den 3 Optionen anpassen
        if changes < res_changes:
            res_changes = changes
            res_columns = [column]  # aktuelle Spalte ist die erste mit den neuen wenigsten Änderungen
        
        elif changes == res_changes:
            res_columns.append(column)

    return res_columns, res_changes
    

def main():
    table = read_file(input("Path (relative to %s): " % os.getcwd()))
    columns, changes = solve(table)

    # Ausgabe: in mathematischer Zählweise (Start bei 1)
    print("Spalte(n):", ", ".join(str(e + 1) for e in columns))
    print("Anzahl der Änderungen:", changes)


if __name__ == "__main__":
    main()