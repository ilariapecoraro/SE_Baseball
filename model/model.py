import copy
from encodings import search_function
from operator import itemgetter

import networkx as nx
from datetime import datetime
from database.dao import DAO

class Model:


        def __init__(self):
            self.G = nx.Graph()
            self.dict_teams = {}  # dizionario dei teams {id: team}
            self.lista_team = [] # lista degli oggetti team
            self.connessioni = [] # lista di tuple (id1, id1, weight)
            self.all_years = []

            # Per la ricorsione
            self._max_weight = 0
            self._best_path = []

        def get_all_years(self):
            return DAO.get_all_years()

        def get_team(self, year):
            lista_team = DAO.get_teams(year)
            return lista_team


        def build_graph(self, year):
            """
            Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
            con campo `anno` <= year passato come argomento.
            Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
            :param durata: durata minima degli album
            """
            # TODO

            # Pulisco il grafo e lo ricreo
            self.G.clear()
            self.dict_teams = {}
            self.lista_team = []
            self.connessioni = []

            self.lista_team = self.get_team(year)
            # creo un dizionario
            for team in self.lista_team:
                if team.id not in self.dict_teams:
                    self.dict_teams[team.id] = team

            # aggiungo i nodi
            self.G.add_nodes_from(self.lista_team)

            # prendo le connessioni
            self.connessioni = DAO.get_connections(self.dict_teams, year)

            # seleziono gli oggetti e il salario
            for t1_id, t2_id, salary in self.connessioni:
                if t1_id in self.dict_teams and t2_id in self.dict_teams:
                    t1 = self.dict_teams[t1_id]
                    t2 = self.dict_teams[t2_id]

                # aggiungi l'arco con l'attributo
                    self.G.add_edge(t1, t2, weight=salary)

            print(self.G)

        def ricerca_cammino(self, team, K):

            self.best_path = []
            self.max_weight = 0

            partial = [team]
            partial_edges = []
            self.ricorsione(partial, partial_edges, K)

            return self.max_weight, self.best_path

        def ricorsione(self, partial_nodes, partial_edges, K):

            n_last = partial_nodes[-1]
            neigh = self._get_admissible_neighbors(n_last, partial_nodes)

            if not neigh:
                return

            # stop
            if len(partial_edges) == K:
                weight_path = self.compute_weight_path(partial_edges)
                if weight_path > self.max_weight:
                    self.best_path = partial_edges[:]
                    self.max_weight = weight_path
                return

            for n in neigh:
                print("...")
                partial_nodes.append(n)
                partial_edges.append((n_last, n, self.G.get_edge_data(n_last, n)))
                self.ricorsione(partial_nodes, partial_edges, K)
                partial_nodes.pop()
                partial_edges.pop()

        def _get_admissible_neighbors(self, node, partial):
            result = []
            for v, peso in self.get_vicino(node):
                if v in partial:
                    continue
                result.append(v)
            return result

        def compute_weight_path(self, mylist):
            weight = 0
            for e in mylist:
                weight += e[2]['weight']
            return weight

        def get_vicino(self, team):
            neigh = []
            if team in self.G.nodes():
                for neighbor in self.G.neighbors(team):
                    attr = self.G.get_edge_data(team, neighbor)
                    if attr:
                        salario = attr.get("weight")
                        neigh.append((neighbor, salario))
            neigh_ordinati = sorted(neigh, key=lambda x: x[1], reverse=True)
            return neigh_ordinati
