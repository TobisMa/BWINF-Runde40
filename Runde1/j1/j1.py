# -*- coding: utf-8 -*-
import math
from typing import List, Tuple
import os


Coordinate = Tuple[int, int]


def to_int_tuple(arg1, arg2) -> Tuple[int, int]:
    """Konvertiert die gegebenen Argumente in ein Tuple aus 2 Ganzzahlen

    Args:
        arg1 (SupportingIntConvert): erstes Argument, welches in eine Ganzzahle konvertiert werden soll
        arg2 (SupportingIntConvert): zweites Argument, welches in eine Ganzzahle konvertiert werden soll

    Returns:
        Tuple[int, int]: das Ganzzahlentuple
    """
    return int(arg1), int(arg2)


def read_file(filename: str) -> Tuple[List[Coordinate], List[Coordinate]]:
    """Liest die Datei ein und verarbeitet den Inhalt in eine für das
       Programm verwendbare Darstellung

    Args:
        filename (str): der Dateiname oder relative Pfad zur Datei

    Returns:
        Tuple[List[Coordinate], List[Coordinate]]: Ein Tuple aus zwei Listen. An erster Stelle die Windräder
                                                   und an zweiter die Wohnorte
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()
    lines = data.splitlines()

    # Variablen für Dateikontext
    first_part_ends = int(lines[0].split(" ")[0])
    wohnorte_now = True

    windraeder: List[Coordinate] = []
    wohnorte: List[Coordinate] = list()

    for i, line in enumerate(lines[1:], start=0):
        if i == first_part_ends:  # Anpassung des Dateikontextes
            wohnorte_now = False
        
        if wohnorte_now:
            wohnorte.append(to_int_tuple(*line.split(" ")))
        else:
            windraeder.append(to_int_tuple(*line.split(" ")))
    
    return windraeder, wohnorte


def get_distance(coord1: Coordinate, coord2: Coordinate) -> float:
    """Berechnet die Distanz zwischen zwei Koordinaten (mit dem Satz des Pythagoras)

    Args:
        coord1 (Coordinate): erste Koordinate
        coord2 (Coordinate): zweite Koordinate

    Returns:
        float: die Distanz
    """
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


def solve(windraeder: List[Coordinate], wohnorte: List[Coordinate]) -> List[Tuple[Coordinate, float]]:
    """Löst die Problemstellung "Was ist die maximale Bauhöhe der Windräder bei Anwendung der 10H-Regel
       mit den gegebenen Wohnorten"

    Args:
        windraeder (List[Coordinate]): die Windradkoordinaten aus der Datei
        wohnorte (List[Coordinate]): die Wohnortkoordinaten aus der Datei

    Returns:
        List[Tuple[Coordinate, float]]: Eine Liste aus Tuplen, in welchen die Koordinate des Windrads und 
                                        dessen maximale Bauhöhe vermerkt sind
    """
    results = []

    for windrad in windraeder:
        # Sucht den nächstgelegenen Ort
        smallest_distance = float("inf")  # default value (auch wegen Speicherplatz, aber nur für j1 irrelevant)

        for wohnort in wohnorte:
            d = get_distance(windrad, wohnort)

            if d < smallest_distance:
                smallest_distance = d  # aktualisieren von der kleinsten Distanz
        
        # Kleinste Distanz auswerten, verrechnen und im Speicher (=results) vermerken
        if smallest_distance != float("inf"):
            results.append((windrad, smallest_distance / 10))
        else:
            # in case no wohnort was given. So `NaN` for no result
            results.append((windrad, float("NaN")))

    return results


def main():
    windraeder, wohnorte = read_file(input("path to file (relative to '" + os.getcwd() + "'): "))
    results = solve(windraeder, wohnorte)

    # Ausgabe
    for res in results:
        if res[1] <= 0:
            # 0-Fall
            print("Windrad", res[0], "darf kann nicht gebaut werden.")
        else:
            print("Windrad", res[0], "mit maximaler Bauhöhe von", str(res[1]) + "m.")
    


if __name__ == "__main__":
    main()
