import ast
import logging

logger = logging.getLogger(__name__)

class PythonASTParser:
    def __init__(self, source_code: str, filename: str):
        self.source_code = source_code
        self.filename = filename
        self.tree: ast.Module | None = None

    # Построение ast древа через метод ast.parse
    def parse(self) -> ast.Module | None:
        self.tree = None
        try:
            self.tree = ast.parse(self.source_code, self.filename)
        except SyntaxError as error:
            logger.error(
                "Ошибка в файле %s, строка %s столбец %s: %s",
                error.filename,
                error.lineno,
                error.offset,
                error.msg
            )
        return self.tree

    # Получение списка нодов из self.tree
    def get_statements(self) -> list[ast.stmt]:
        if self.tree is None:
            raise RuntimeError("Сначала необходимо выполнить parse()")

        return self.tree.body

    def get_source_segment(self, node: ast.AST) -> str:
        segment = ast.get_source_segment(self.source_code, node)

        if segment is None:
            raise ValueError("Возникла ошибка сопоставления кода с указанным нодом")

        return segment

    # Возвращает форматированную строку кода из древа
    def format_ast(self) -> str:
        if self.tree is None:
            raise RuntimeError("Сначала необходимо выполнить parse()")

        return ast.dump(node=self.tree, indent=4, include_attributes=False)
