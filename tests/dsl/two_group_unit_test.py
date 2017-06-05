import unittest
from random import random

from numpy.random.mtrand import normal

from pysie.dsl.two_groups import MeanDiffTesting, ProportionDiffTesting
from pysie.stats.distributions import MeanDiffSamplingDistribution, DistributionFamily, \
    ProportionDiffSamplingDistribution
from pysie.stats.samples import Sample, SampleDistribution


class MeanDiffTestingUnitTest(unittest.TestCase):

    def test_normal(self):
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
        testing = MeanDiffTesting(sampling_distribution=sampling_distribution)
        print('one tail p-value: ' + str(testing.p_value_one_tail))
        print('two tail p-value: ' + str(testing.p_value_two_tail))
        reject_one_tail, reject_two_tail = testing.will_reject(0.01)
        print('will reject mean_1 == mean_2 (one-tail) ? ' + str(reject_one_tail))
        print('will reject mean_1 == mean_2 (two-tail) ? ' + str(reject_two_tail))
        self.assertFalse(reject_one_tail)
        self.assertFalse(reject_two_tail)

    def test_student(self):
        grp1_mu = 0.0
        grp1_sigma = 1.0
        grp1_sample_size = 29
        grp1_sample = Sample()

        grp2_mu = 0.09
        grp2_sigma = 2.0
        grp2_sample_size = 28
        grp2_sample = Sample()

        for i in range(grp1_sample_size):
            grp1_sample.add_numeric(normal(grp1_mu, grp1_sigma))

        for i in range(grp2_sample_size):
            grp2_sample.add_numeric(normal(grp2_mu, grp2_sigma))

        sampling_distribution = MeanDiffSamplingDistribution(grp1_sample_distribution=SampleDistribution(grp1_sample),
                                                             grp2_sample_distribution=SampleDistribution(grp2_sample))
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.student_t)
        testing = MeanDiffTesting(sampling_distribution=sampling_distribution)
        print('one tail p-value: ' + str(testing.p_value_one_tail))
        print('two tail p-value: ' + str(testing.p_value_two_tail))
        reject_one_tail, reject_two_tail = testing.will_reject(0.01)
        print('will reject mean_1 == mean_2 (one-tail) ? ' + str(reject_one_tail))
        print('will reject mean_1 == mean_2 (two-tail) ? ' + str(reject_two_tail))
        self.assertFalse(reject_one_tail)
        self.assertFalse(reject_two_tail)


class ProportionDiffTestingUnitTest(unittest.TestCase):

    def test_normal(self):
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

        testing = ProportionDiffTesting(sampling_distribution=sampling_distribution)
        print('one tail p-value: ' + str(testing.p_value_one_tail))
        print('two tail p-value: ' + str(testing.p_value_two_tail))
        reject_one_tail, reject_two_tail = testing.will_reject(0.01)
        print('will reject p_1 == p_2 (one-tail) ? ' + str(reject_one_tail))
        print('will reject p_1 == p_2 (two-tail) ? ' + str(reject_two_tail))
        self.assertFalse(reject_one_tail)
        self.assertFalse(reject_two_tail)

    def test_student(self):
        grp1_sample = Sample()
        grp2_sample = Sample()

        for i in range(20):
            if random() <= 0.6:
                grp1_sample.add_category("OK")
            else:
                grp1_sample.add_category("CANCEL")

        for i in range(20):
            if random() <= 0.61:
                grp2_sample.add_category("OK")
            else:
                grp2_sample.add_category("CANCEL")

        sampling_distribution = ProportionDiffSamplingDistribution(grp1_sample_distribution=SampleDistribution(
            grp1_sample, categorical_value="OK"),
            grp2_sample_distribution=SampleDistribution(
                grp2_sample, categorical_value="OK"))
        self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.simulation)

        testing = ProportionDiffTesting(sampling_distribution=sampling_distribution)
        print('one tail p-value: ' + str(testing.p_value_one_tail))
        print('two tail p-value: ' + str(testing.p_value_two_tail))
        reject_one_tail, reject_two_tail = testing.will_reject(0.01)
        print('will reject p_1 == p_2 (one-tail) ? ' + str(reject_one_tail))
        print('will reject p_1 == p_2 (two-tail) ? ' + str(reject_two_tail))
        self.assertFalse(reject_one_tail)
        self.assertFalse(reject_two_tail)

if __name__ == '__main__':
    unittest.main()