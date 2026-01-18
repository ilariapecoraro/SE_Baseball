import flet as ft
import networkx

from UI.view import View
from model.model import Model
class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def get_years(self):
        return self._model.get_all_years()

    def handle_year_change(self, e):
        """Handler per gestire on_change del dropdown dd_anno"""
        year = int(self._view.dd_anno.value)
        teams =self._model.get_team(year)
        # ottengo quindi una lista di oggetti team

        # Inserisci il numero di squadre e le squadre nella listview
        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(
            ft.Text(f"Numero squadre: {len(teams)}"
        ))
        for t in teams:
            self._view.txt_out_squadre.controls.append(ft.Text(t))

        self._view.dd_squadra.clean()
        self._view.dd_squadra.options = [
        ft.dropdown.Option(key=str(t.id), text=t)for t in teams]

        self._view.update()

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO

        try:
            anno = int(self._view.dd_anno.value)
        except Exception:
            self._view.show_alert("Anno invalido")
            return

        self._model.build_graph(anno)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO
        self._view.txt_risultato.controls.clear()
        selected_id = int(self._view.dd_squadra.value)
        team_nodo = self._model.dict_teams[selected_id]
        vicini = self._model.get_vicino(team_nodo)
        if vicini:
            for n, w in vicini:
                self._view.txt_risultato.controls.append(
                ft.Text(f"{n}-peso: {w}")
            )
        else:
            self._view.txt_risultato.controls.append(ft.Text("Nessun vicino trovato"))
        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO
        K = 3
        selected_id = int(self._view.dd_squadra.value)
        team_nodo = self._model.dict_teams[selected_id]

        # ricerca cammino massimo
        self._model.ricerca_cammino(team_nodo, K)

        # pulizia dell'output
        self._view.txt_risultato.controls.clear()

        # stampa cammino trovato
        for nodo_1, nodo_2, attr in self._model.best_path:
            self._view.txt_risultato.controls.append(ft.Text(
                f"{nodo_1} --> {nodo_2}: {attr['weight']}"))

        # stampa il peso totale
        self._view.txt_risultato.controls.append(ft.Text(f"Peso Totale: {self._model.max_weight}"))

        self._view.update()

    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO