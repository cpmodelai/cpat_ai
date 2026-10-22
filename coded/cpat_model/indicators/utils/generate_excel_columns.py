def excel_column_to_index(
        column: str
        ) -> int:
    """
    Converts an Excel column label to a numeric index (1-based).

    Parameters:
        column (str):

    Returns:
        None
    """
    index = 0
    for char in column:
        index = index * 26 + (ord(char.upper()) - ord('A') + 1)
    return index

def index_to_excel_column(
        index: int
        ) -> str:
    """
    Converts a numeric index (1-based) to an Excel column label.

    Parameters:
        index (int):

    Returns:
        None
    """
    column = ''
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        column = chr(remainder + ord('A')) + column
    return column

def generate_excel_columns(
        starting_column: str,
        offset: int,
        length: int
        ) -> list:
    """
    Generates a list of Excel column labels given a starting column, an offset, and length.

    Parameters:
        starting_column (str):
        offset (int):
        length (int):

    Returns:
        None
    """
    start_index = excel_column_to_index(starting_column)
    result = []
    for i in range(length):
        column_index = start_index + i * offset
        result.append(index_to_excel_column(column_index))
    return result
