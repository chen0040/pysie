import unittest

from pysie.stats.distributions import MeanSamplingDistribution, DistributionFamily
from pysie.stats.samples import Sample


class MeanSamplingDistributionUnitTest(unittest.TestCase):

    def test_confidence_interval_with_sample_stats(self):
        sample_mean = 0
        sample_sd = 1
        sample_size = 31
        sampling_distribution = MeanSamplingDistribution(sample_mean=sample_mean, sample_sd=sample_sd, sample_size=sample_size)
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate) + ', standard_error=' + str(sampling_distribution.standard_error) + ')')
        print('confidence interval for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

if __name__ == '__main__':
    unittest.main()
