import unittest

from numpy.random.mtrand import normal

from pysie.dsl.one_group import MeanTesting
from pysie.stats.distributions import MeanSamplingDistribution
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

if __name__ == '__main__':
    unittest.main()
