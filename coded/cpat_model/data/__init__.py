"""Database access: the tidy tables of data/<edition>/tidy (or the full database), read once, as Excel-AI's data.

Only this package reads data files (NORMS 2, 5). Tables are read as the CSV text and converted to numbers here,
exactly (float parsing round-trips the CSV text). The list of tables is the tidy manifest (data/<edition>/tidy/_manifest.csv,
data/README.md); reading a table it does not list is an error.
"""
from cpat_model.data.database import Database, open_database  # noqa: F401
