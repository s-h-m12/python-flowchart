import ast
import logging
import networkx as nx

logger = logging.getLogger(__name__)

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
    def _process_statement(self, node: ast.stmt, previous_node: int) -> int:
        text = ast.get_source_segment(self.source_code, node)
        if text is None:
            raise TypeError("Вместо кода получен None")
        if isinstance(node, ast.Assign):
            if (
                    isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and node.value.func.id == "input"
            ):
                new_node = self._add_node(kind="input", text=text, lineno=node.lineno)
                self._add_edge(previous_node, new_node)
                return new_node
            else:
                new_node = self._add_node(kind="process", text=text, lineno=node.lineno)
                self._add_edge(previous_node, new_node)
                return new_node
        elif isinstance(node, ast.Expr):
            if (
                    isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and node.value.func.id == "print"
            ):
                new_node = self._add_node(kind="output", text=text, lineno=node.lineno)
                self._add_edge(previous_node, new_node)
                return new_node
        elif isinstance(node, ast.If):
            new_node = self._add_node(
                kind="decision",
                text=ast.get_source_segment(self.source_code, node.test),
                lineno=node.lineno
            )
            self._add_edge(previous_node, new_node)
            true_exit_node = self._build_sequence(node.body, new_node)
            if node.orelse:
                false_exit_node = self._build_sequence(node.orelse, new_node)
            else:
                false_exit_node = new_node
            newer_node = self._add_node(kind="connector", text="", lineno=None)
            self._add_edge(false_exit_node, newer_node)
            self._add_edge(true_exit_node, newer_node)
            return newer_node

    def _build_sequence(self, statements: list[ast.stmt], start_node: int) -> int:
        current_node = start_node
        for statement in statements:
            current_node = self._process_statement(statement, current_node)
        return current_node