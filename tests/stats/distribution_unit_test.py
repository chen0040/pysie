import unittest

from numpy.random import normal, random

from pysie.stats.distributions import MeanSamplingDistribution, DistributionFamily, ProportionSamplingDistribution
from pysie.stats.samples import Sample, SampleDistribution


class MeanSamplingDistributionUnitTest(unittest.TestCase):

    def test_confidence_interval_with_sample_stats_normal(self):
        sample_mean = 0
        sample_sd = 1
        sample_size = 31
        sampling_distribution = MeanSamplingDistribution(sample_mean=sample_mean, sample_sd=sample_sd, sample_size=sample_size)
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error=' + str(sampling_distribution.standard_error) + ')')
        print('confidence interval for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_normal(self):
        mu = 0.0
        sigma = 1.0
        sample_size = 31
        sample = Sample()

        for i in range(sample_size):
            sample.add_numeric(normal(mu, sigma))

        sampling_distribution = MeanSamplingDistribution(sample_distribution=SampleDistribution(sample))
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence interval for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_stats_student(self):
        sample_mean = 0
        sample_sd = 1
        sample_size = 29
        sampling_distribution = MeanSamplingDistribution(sample_mean=sample_mean, sample_sd=sample_sd, sample_size=sample_size)
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.student_t)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence interval for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_student(self):
        mu = 0.0
        sigma = 1.0
        sample_size = 29
        sample = Sample()

        for i in range(sample_size):
            sample.add_numeric(normal(mu, sigma))

        sampling_distribution = MeanSamplingDistribution(sample_distribution=SampleDistribution(sample))
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.student_t)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence interval for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))


class ProportionSamplingDistributionUnitTest(unittest.TestCase):

    def test_confidence_interval_with_sample_stats_normal(self):
        sample_proportion = 0.6
        sample_size = 31
        sampling_distribution = ProportionSamplingDistribution(sample_proportion=sample_proportion,
                                                               sample_size=sample_size)
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence level for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_normal(self):
        sample = Sample()

        for i in range(100):
            if random() <= 0.6:
                sample.add_category("OK")
            else:
                sample.add_category("CANCEL")

        sampling_distribution = ProportionSamplingDistribution(sample_distribution=SampleDistribution(sample,
                                                                                                      categorical_value="OK"))
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence level for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_stats_simulation(self):
        sample_proportion = 0.6
        sample_size = 10
        sampling_distribution = ProportionSamplingDistribution(sample_proportion=sample_proportion,
                                                               sample_size=sample_size)
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.simulation)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence level for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_simulation(self):
        sample = Sample()

        for i in range(10):
            if random() <= 0.6:
                sample.add_category("OK")
            else:
                sample.add_category("CANCEL")

        sampling_distribution = ProportionSamplingDistribution(sample_distribution=SampleDistribution(sample,
                                                                                                      categorical_value="OK"))
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.simulation)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence level for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))


if __name__ == '__main__':
    unittest.main()
