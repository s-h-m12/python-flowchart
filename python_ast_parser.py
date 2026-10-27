import ast
import logging

logger = logging.getLogger(__name__)

class PythonASTParser:
    def __init__(self, source_code: str, filename: str):
        self.source_code = source_code
        self.filename = filename
        self.tree: ast.Module | None = None

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

    def get_statements(self) -> list[ast.stmt]:
        if self.tree is None:
            raise RuntimeError("Сначала необходимо выполнить parse()")

        return self.tree.body