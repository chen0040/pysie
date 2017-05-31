import unittest

from numpy.random import normal, random

from pysie.stats.distributions import MeanSamplingDistribution, DistributionFamily, ProportionSamplingDistribution, \
    MeanDiffSamplingDistribution, ProportionDiffSamplingDistribution
from pysie.stats.samples import Sample, SampleDistribution


class MeanSamplingDistributionUnitTest(unittest.TestCase):
    def test_confidence_interval_with_sample_stats_normal(self):
        sample_mean = 0
        sample_sd = 1
        sample_size = 31
        sampling_distribution = MeanSamplingDistribution(sample_mean=sample_mean, sample_sd=sample_sd,
                                                         sample_size=sample_size)
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
        sampling_distribution = MeanSamplingDistribution(sample_mean=sample_mean, sample_sd=sample_sd,
                                                         sample_size=sample_size)
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


class MeanDiffSamplingDistributionUnitTest(unittest.TestCase):
    def test_confidence_interval_with_sample_stats_normal(self):
        grp1_sample_mean = 0
        grp1_sample_sd = 1
        grp1_sample_size = 31
        grp2_sample_mean = 0.001
        grp2_sample_sd = 2.1
        grp2_sample_size = 36
        sampling_distribution = MeanDiffSamplingDistribution(grp1_sample_mean=grp1_sample_mean,
                                                             grp1_sample_sd=grp1_sample_sd,
                                                             grp1_sample_size=grp1_sample_size,
                                                             grp2_sample_mean=grp2_sample_mean,
                                                             grp2_sample_sd=grp2_sample_sd,
                                                             grp2_sample_size=grp2_sample_size)
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error=' + str(sampling_distribution.standard_error) + ')')
        print('confidence interval for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_normal(self):
        grp1_mu = 0.0
        grp1_sigma = 1.0
        grp1_sample_size = 31
        grp1_sample = Sample()

        grp2_mu = 0.09
        grp2_sigma = 2.0
        grp2_sample_size = 36
        grp2_sample = Sample()

        for i in range(grp1_sample_size):
            grp1_sample.add_numeric(normal(grp1_mu, grp1_sigma))

        for i in range(grp2_sample_size):
            grp2_sample.add_numeric(normal(grp2_mu, grp2_sigma))

        sampling_distribution = MeanDiffSamplingDistribution(grp1_sample_distribution=SampleDistribution(grp1_sample),
                                                             grp2_sample_distribution=SampleDistribution(grp2_sample))
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence interval for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_stats_student(self):
        grp1_sample_mean = 0
        grp1_sample_sd = 1
        grp1_sample_size = 29
        grp2_sample_mean = 0.001
        grp2_sample_sd = 1.3
        grp2_sample_size = 24
        sampling_distribution = MeanDiffSamplingDistribution(grp1_sample_mean=grp1_sample_mean,
                                                             grp1_sample_sd=grp1_sample_sd,
                                                             grp1_sample_size=grp1_sample_size,
                                                             grp2_sample_mean=grp2_sample_mean,
                                                             grp2_sample_sd=grp2_sample_sd,
                                                             grp2_sample_size=grp2_sample_size)
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.student_t)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence interval for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_student(self):
        grp1_mu = 0.0
        grp1_sigma = 1.0
        grp1_sample_size = 29
        grp1_sample = Sample()
        grp2_mu = 0.08
        grp2_sigma = 1.1
        grp2_sample_size = 27
        grp2_sample = Sample()

        for i in range(grp1_sample_size):
            grp1_sample.add_numeric(normal(grp1_mu, grp1_sigma))
        for i in range(grp2_sample_size):
            grp2_sample.add_numeric(normal(grp2_mu, grp2_sigma))

        sampling_distribution = MeanDiffSamplingDistribution(grp1_sample_distribution=SampleDistribution(grp1_sample),
                                                             grp2_sample_distribution=SampleDistribution(grp2_sample))
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


class ProportionDiffSamplingDistributionUnitTest(unittest.TestCase):
    def test_confidence_interval_with_sample_stats_normal(self):
        grp1_sample_proportion = 0.6
        grp1_sample_size = 31
        grp2_sample_proportion = 0.51
        grp2_sample_size = 32
        sampling_distribution = ProportionDiffSamplingDistribution(grp1_sample_proportion=grp1_sample_proportion,
                                                                   grp1_sample_size=grp1_sample_size,
                                                                   grp2_sample_proportion=grp2_sample_proportion,
                                                                   grp2_sample_size=grp2_sample_size)
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence level for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_normal(self):
        grp1_sample = Sample()
        grp2_sample = Sample()

        for i in range(100):
            if random() <= 0.6:
                grp1_sample.add_category("OK")
            else:
                grp1_sample.add_category("CANCEL")

        for i in range(100):
            if random() <= 0.61:
                grp2_sample.add_category("OK")
            else:
                grp2_sample.add_category("CANCEL")

        sampling_distribution = ProportionDiffSamplingDistribution(grp1_sample_distribution=SampleDistribution(
            grp1_sample, categorical_value="OK"),
            grp2_sample_distribution=SampleDistribution(
                grp2_sample, categorical_value="OK"))
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence level for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_stats_simulation(self):
        grp1_sample_proportion = 0.6
        grp1_sample_size = 10
        grp2_sample_proportion = 0.61
        grp2_sample_size = 9
        sampling_distribution = ProportionDiffSamplingDistribution(grp1_sample_proportion=grp1_sample_proportion,
                                                                   grp1_sample_size=grp1_sample_size,
                                                                   grp2_sample_proportion=grp2_sample_proportion,
                                                                   grp2_sample_size=grp2_sample_size
                                                                   )
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.simulation)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence level for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))

    def test_confidence_interval_with_sample_simulation(self):
        grp1_sample = Sample()
        grp2_sample = Sample()

        for i in range(10):
            if random() <= 0.6:
                grp1_sample.add_category("OK")
            else:
                grp1_sample.add_category("CANCEL")

        for i in range(9):
            if random() <= 0.61:
                grp2_sample.add_category("OK")
            else:
                grp2_sample.add_category("CANCEL")

        sampling_distribution = ProportionDiffSamplingDistribution(
            grp1_sample_distribution=SampleDistribution(grp1_sample,
                                                        categorical_value="OK"),
            grp2_sample_distribution=SampleDistribution(
                grp2_sample,
                categorical_value="OK")
            )
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.simulation)
        print('sampling distribution: (point_estimate = ' + str(sampling_distribution.point_estimate)
              + ', standard_error = ' + str(sampling_distribution.standard_error) + ')')
        print('confidence level for 95% confidence level: ' + str(sampling_distribution.confidence_interval(0.95)))


if __name__ == '__main__':
    unittest.main()
