from typing import List, Tuple


class Hotel(object):

    """
    Stellt ein Hotel aus der Datei da
    """

    def __init__(self, name: str, time: int, rating: float):
        self.time = time
        self.rating = rating
        self.name = name

    def __repr__(self) -> str:
        return "Hotel(name=%r, time=%s, rating=%s)" % (self.name, self.time, self.rating)
    

def read_file(filename: str) -> Tuple[int, List[Hotel]]:
    """Konvertiert Dateiinhalt in Datenformen für das Programm

    Args:
        filename (str): der Dateiname

    Returns:
        Tuple[int, List[Hotel]]: Die Gesamtfahrzeit und Hotels im Datenformat des Programms
    """
    with open(filename, 'r') as f:
        d = f.read()

    d = d.splitlines()[1:]  # in python number of hotels can be ignored
    total_time = int(d.pop(0))  # d.pop(0) removing time (2nd line) from lines

    hotel_tuples = [(int(line.split(" ")[0]), float(line.split(" ")[1])) for line in d]

    hotels = [Hotel("Hotel %i" % i, *attr) for i, attr in enumerate(hotel_tuples, start=3)]

    return total_time, hotels


def get_ratings(hotels: List[Hotel]) -> List[float]:
    """Gibt eine Liste der verschiedene Bewertungen und sortiert diese von
       gut zu schlecht.

    Args:
        hotels (List[Hotel]): die Liste der Hotels auf der Strecke

    Returns:
        List[float]: die bewertungen sortiert von gut zu schlecht
    """
    ratings = []
    
    for h in hotels:
        if h.rating not in ratings:
            ratings.append(h.rating)
    
    ratings.sort(reverse=True)  # good to bad
    return ratings
    
    
def get_next_hotels(hotels: List[Hotel], position: int, interval: int = 6 * 60) -> List[Hotel]:
    """Gibt die Hotels die erreichbar sind zurück und sortiert diese nach 1. deren Bewertung
       und 2. deren Zeit/Entfernung vom Startpunkt

    Args:
        hotels (List[Hotel]): Die Hotels auf der Strecke oder die in der "Zukunft" kommenden
        position (int): wie lange/weit bereits gefahren wurde
        interval (int): die maximale Länge (Zeit oder Weg) einer Fahrt

    Returns:
        List[Hotel]: die Liste der erreichbaren Hotels
    """
    return list(
        sorted(
            filter(lambda h: h.time > position and h.time <= position + interval, hotels),
            key=lambda h: (h.rating, h.time),
            reverse=True
        )
    )


def solve(hotels: List[Hotel], total_time: int, days: int = 5, interval: int = 6 * 60) -> List[Hotel]:
    """Die Implementierung der Lösung

    Args:
        hotels (List[Hotel]): die Hotels auf dem Weg
        days (int): Wie viele Fahrten gemacht werden. Z. B. 5 Tage = 5 Fahrten = 4 Nächte
        interval (int): Die Fahrzeit pro Fahrt

    Returns:
        List[Hotel]: die Lösung (4 Hotels)
    """
    ratings = get_ratings(hotels)
    
    for i in range(len(ratings)):
        min_requirement = ratings[:i + 1]
        position = 0
        history: List[Hotel] = [] # Bsp: nur 4 Übernachtungen bei 5 Tagen
        
        while len(history) < days - 1:  # Abbruchfall 2
            next_hotels = get_next_hotels(hotels, position, interval)
            next_hotels = [h for h in next_hotels if h.rating in min_requirement]
            next_hotels.sort(key=lambda h: h.time, reverse=True)  # Entfernung (weit -> klein) von position
            
            # Abbruchfall 1
            if not next_hotels:
                # keine Lösung gefunden, da es kein Hotel mehr gibt zu dem sie fahren können und sie können von 
                # ihrem momentanem Standpunkt nicht das Ziel erreichen
                break  
            
            history.append(next_hotels[0])
            position = history[-1].time

            # Abbruchfall 3
            if position + interval >= total_time:
                return history  # Lösung gefunden
    
    return []  # No solution



def main():
    total_time, hotels  = read_file("a2input.txt")
    res = solve(hotels, total_time)
    
    
    if res:
        prev = None
        for h in res:
            
            if prev is not None:
                print("diff:", h.time - prev.time)
                
            print(h)
            prev = h
        
        print("left: ", total_time - prev.time)  # type: ignore
    else:
        print("No solution")
        
    print("Total time:", total_time)
        

if __name__ == "__main__":
    main()