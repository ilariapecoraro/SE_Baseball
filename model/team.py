from dataclasses import dataclass

@dataclass
class Team:
    id : int
    team_code : str
    salario : float
    name : str



    def __str__(self):
        return f"{self.team_code}({self.name})"

    # Serve per poter usare l'oggetto come nodo del grafo
    def __hash__(self):
        return hash(self.id)