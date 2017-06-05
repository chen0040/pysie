import unittest

from numpy.random.mtrand import normal

from pysie.dsl.variable_independence_testing import Anova
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

if __name__ == '__main__':
    unittest.main()
