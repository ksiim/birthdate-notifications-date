import openpyxl
from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
    Base class for table parsers.
    """

    def __init__(self, file_path: str):
        """Initializes the parser with the file path.

        Args:
            file_path (str): The path to the file.
        """
        self.file_path = file_path
        self.workbook = openpyxl.load_workbook(file_path)
        self.sheet = self.workbook.active

    @abstractmethod
    async def parse(self):
        """Parses the table and returns the data."""
        pass

    async def close(self):
        """Closes the workbook."""
        self.workbook.close()


class Parser(BaseParser):
    """
    Parser for full table.
    """

    async def parse(self):
        """Parses the full table and returns the data."""
        data = []
        for row in self.sheet.iter_rows(values_only=True, min_row=2):
            if row[0]:
                data.append(row)
        return data
