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
        self.rows.add(row_name)
        self.columns.add(column_name)

    def get_cell(self, row_name, column_name):
        key = self.make_key(row_name, column_name)
        if not self.values.contains_key(key):
            return 0
        return self.values.get(key)

    def make_key(self, row_name, column_name):
        return row_name + '-' + column_name

    def get_row_total(self, row_name):
        column_names = self.columns.to_array()
        result = 0
        for x in column_names:
            result += self.get_cell(row_name, x)
        return result

    def get_column_total(self, column_name):
        row_names = self.rows.to_array()
        result = 0
        for x in row_names:
            result += self.get_cell(x, column_name)
        return result

    def get_total(self):
        values = self.values.values()
        result = 0
        for val in values:
            result += val
        return result


