import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()

        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for airport in self._airports:
            self._idMapAirports[airport.ID] = airport

    # I NODI SONO AEROPORTI CON UNA CERTA CONDIZIONE (NON POSSO PRENDERLI TUTTI)
    # DEVO LEGGERE DUE TABELLE

    def buildGraph(self, nMin):

        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes) # I nodi sono quelli gia filtrati, ora devo collegarli tramite gli edge
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        self.addEdges()
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        self._graph.clear_edges()
        self.addEdgesV2()
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")

    def addEdges(self):

        allTratte = DAO.getAllEdgesV1(self._idMapAirports)

        # Queste tratte hanno due problemi:
        # 1) Archi diretti e inversi
        # 2) ho archi fra aeroporti che avevo filtrato

        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                # Allora posso aggiungerlo
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    self._graph[t.aeroportoP][t.aeroportoA]['weight'] += t.peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)


    def addEdgesV2(self):
        allTratte = DAO.getAllEdgesV2(self._idMapAirports)
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                # Allora posso aggiungerlo
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)



    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key = lambda x:x.IATA_CODE)
        return nodes




