import unittest

import numpy
from numpy.random.mtrand import normal

from pysie.dsl.variable_independence_testing import Anova, ContingencyTable, ChiSquare
from pysie.stats.samples import Sample


class AnovaUnitTest(unittest.TestCase):
    def test_anova(self):
        sample = Sample()

        mu1 = 1.0
        sigma1 = 1.0

        mu2 = 1.1
        sigma2 = 1.0

        mu3 = 1.09
        sigma3 = 1.0

        for i in range(100):
            sample.add_numeric(normal(mu1, sigma1), 'group1')
            sample.add_numeric(normal(mu2, sigma2), 'group2')
            sample.add_numeric(normal(mu3, sigma3), 'group3')

        testing = Anova(sample=sample)

        print('p-value: ' + str(testing.p_value))
        reject = testing.will_reject(0.01)
        print('will reject [same mean for all groups] ? ' + str(reject))
        self.assertFalse(reject)


class ContingencyTableUnitTest(unittest.TestCase):
    def test_table(self):
        table = ContingencyTable()
        table.set_cell('eventA', 'eventB', 10)
        table.set_cell('eventC', 'eventB', 20)
        table.set_cell('eventA', 'eventD', 15)
        table.set_cell('eventC', 'eventD', 10)

        print(table.get_column_total('eventB'))
        self.assertEqual(table.get_column_total('eventB'), 30)
        print(table.get_column_total('eventD'))
        self.assertEqual(table.get_column_total('eventD'), 25)
        print(table.get_row_total('eventA'))
        self.assertEqual(table.get_row_total('eventA'), 25)
        print(table.get_row_total('eventC'))
        self.assertEqual(table.get_row_total('eventC'), 30)
        self.assertEqual(table.get_total(), 55)


class ChiSquareUnitTest(unittest.TestCase):
    def test_anova(self):
        sample = Sample()

        for i in range(1000):
            sample.add_category('itemA' if numpy.random.randn() > 0 else 'itemB', 'group1')
            sample.add_category('itemA' if numpy.random.randn() > 0 else 'itemB', 'group2')
            sample.add_category('itemA' if numpy.random.randn() > 0 else 'itemB', 'group3')

        testing = ChiSquare(sample=sample)

        print('p-value: ' + str(testing.p_value))
        reject = testing.will_reject(0.01)
        print('will reject [two categorical variables are independent of each other] ? ' + str(reject))

if __name__ == '__main__':
    unittest.main()
