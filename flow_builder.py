import ast
import networkx as nx

class FlowBuilder:
    def __init__(self, statements: list[ast.stmt], source_code: str):
        self.statements = statements
        self.source_code = source_code
        self.graph = nx.DiGraph()
        self.node_counter = 0

    # Создание узла графа
    def _add_node(self, kind: str, text: str, lineno: int | None = None) -> int:
        self.graph.add_node(
            self.node_counter,
            kind=kind,
            text=text,
            lineno=lineno
        )
        self.node_counter += 1
        return self.node_counter - 1

    # Создание ребра между узлами
    def _add_edge(self, source: int, target: int, label: str | None = None) -> None:
        self.graph.add_edge(source, target, label=label)

    # Создание структурированного блока
    def _process_statement(self, node: ast.stmt) -> int:
        if isinstance(node, ast.Assign):
            text = ast.get_source_segment(self.source_code, node)
            return self._add_node(kind="process", text=text, lineno=node.lineno)
        else:
            raise TypeError("Передан неподдерживаемый тип конструкции")