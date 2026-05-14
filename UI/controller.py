import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._coicePartenza = None
        self._coiceArrivo = None

    def handleAnalizzaAeroporti(self, e):
        cMinTxt = self._view._txtInCiMin.value
        if cMinTxt == "":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore numetico per numero minimo compagnie",color = "red"))
            self._view.update_page()
            return

        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore intero per numero minimo compagnie",color = "red"))
            self._view.update_page()
            return

        if cMin <= 0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Il filtro deve essere intero positivo", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(cMin)
        numNodes, numEdges = self._model.getGraphDetails()

        allNodes = self._model.getAllNodes()
        self.fillDropdown(allNodes)

        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view._txtResults.controls.append(ft.Text(f"Il grafo contiene {numNodes} nodi e {numEdges} archi", color="green"))
        self._view.update_page()




    def handleConnessi(self, e):
        pass

    def handleCerca(self, e):
        pass

    def fillDropdown(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(
                    data = n,
                    key = n.IATA_CODE,
                    on_click = self._choiceDdPartenza
                )
            )

            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(
                    data=n,
                    key=n.IATA_CODE,
                    on_click=self._choiceDdArrivo
                )
            )

    def _choiceDdPartenza(self, e):
        self._coicePartenza = e.control.data
        print(f"Hai selezionato come aeroporto di partenza {self._coicePartenza}")

    def _choiceDdArrivo(self, e):
        self._coiceArrivo = e.control.data
        print(f"Hai selezionato come aeroporto di partenza {self._coiceArrivo}")