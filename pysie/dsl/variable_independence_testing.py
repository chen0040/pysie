from pysie.dsl.set import TernarySearchSet, TernarySearchTrie


class ContingencyTable(object):
    values = None
    rows = None
    columns = None

    def __init__(self):
        self.rows = TernarySearchSet()
        self.columns = TernarySearchSet()
        self.values = TernarySearchTrie()

    def set_cell(self, row_name, column_name, value):
        key = self.make_key(row_name, column_name)
        self.values.put(key, value)

    def get_cell(self, row_name, column_name):
        key = self.make_key(row_name, column_name)
        return self.values.get(key)

    def make_key(self, row_name, column_name):
        return row_name + '-' + column_name


