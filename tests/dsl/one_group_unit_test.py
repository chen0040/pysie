import unittest
from random import random

from numpy.random.mtrand import normal

from pysie.dsl.one_group import MeanTesting, ProportionTesting
from pysie.stats.distributions import MeanSamplingDistribution, ProportionSamplingDistribution
from pysie.stats.samples import Sample, SampleDistribution


class MeanTestingUnitTest(unittest.TestCase):
    def test_mean_normal(self):
        mu = 0.0
        sigma = 1.0
        sample_size = 31
        sample = Sample()

        for i in range(sample_size):
            sample.add_numeric(normal(mu, sigma))

        sampling_distribution = MeanSamplingDistribution(sample_distribution=SampleDistribution(sample))
        testing = MeanTesting(sampling_distribution=sampling_distribution, mean_null=0.0)

        print('one tail p-value: ' + str(testing.p_value_one_tail))
        print('two tail p-value: ' + str(testing.p_value_two_tail))
        reject_one_tail, reject_two_tail = testing.will_reject(0.01)
        print('will reject mean = 0 (one-tail) ? ' + str(reject_one_tail))
        print('will reject mean = 0 (two-tail) ? ' + str(reject_two_tail))
        self.assertFalse(reject_one_tail)
        self.assertFalse(reject_two_tail)

    def test_mean_student(self):
        mu = 0.0
        sigma = 1.0
        sample_size = 29
        sample = Sample()

        for i in range(sample_size):
            sample.add_numeric(normal(mu, sigma))

        sampling_distribution = MeanSamplingDistribution(sample_distribution=SampleDistribution(sample))
        testing = MeanTesting(sampling_distribution=sampling_distribution, mean_null=0.0)

        print('one tail p-value: ' + str(testing.p_value_one_tail))
        print('two tail p-value: ' + str(testing.p_value_two_tail))
        reject_one_tail, reject_two_tail = testing.will_reject(0.01)
        print('will reject mean = 0 (one-tail) ? ' + str(reject_one_tail))
        print('will reject mean = 0 (two-tail) ? ' + str(reject_two_tail))
        self.assertFalse(reject_one_tail)
        self.assertFalse(reject_two_tail)


class ProportionTestingUnitTest(unittest.TestCase):
    def test_proportion_normal(self):
        sample = Sample()

        for i in range(100):
            if random() <= 0.6:
                sample.add_category("OK")
            else:
                sample.add_category("CANCEL")

        sampling_distribution = ProportionSamplingDistribution(
            sample_distribution=SampleDistribution(sample, categorical_value="OK"))

        testing = ProportionTesting(sampling_distribution=sampling_distribution, p_null=0.6)

        print('one tail p-value: ' + str(testing.p_value_one_tail))
        print('two tail p-value: ' + str(testing.p_value_two_tail))
        reject_one_tail, reject_two_tail = testing.will_reject(0.01)
        print('will reject p = 0.6 (one-tail) ? ' + str(reject_one_tail))
        print('will reject p = 0.6 (two-tail) ? ' + str(reject_two_tail))
        self.assertFalse(reject_one_tail)
        self.assertFalse(reject_two_tail)

    def test_proportion_simulation(self):
        sample = Sample()

        for i in range(10):
            if random() <= 0.6:
                sample.add_category("OK")
            else:
                sample.add_category("CANCEL")

        sampling_distribution = ProportionSamplingDistribution(
            sample_distribution=SampleDistribution(sample, categorical_value="OK"))

        testing = ProportionTesting(sampling_distribution=sampling_distribution, p_null=0.6)

        print('one tail p-value: ' + str(testing.p_value_one_tail))
        print('two tail p-value: ' + str(testing.p_value_two_tail))
        reject_one_tail, reject_two_tail = testing.will_reject(0.01)
        print('will reject p = 0.6 (one-tail) ? ' + str(reject_one_tail))
        print('will reject p = 0.6 (two-tail) ? ' + str(reject_two_tail))
        self.assertFalse(reject_one_tail)
        self.assertFalse(reject_two_tail)

if __name__ == '__main__':
    unittest.main()
