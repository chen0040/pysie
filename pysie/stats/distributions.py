import math
import random

from enum import Enum

from scipy.stats import norm, t


class DistributionFamily(Enum):
    normal = 1
    student_t = 2
    fisher = 3
    chi_square = 4
    simulation = 5


class MeanSamplingDistribution(object):
    sample_distribution = None
    point_estimate = None
    distribution_family = None
    df = None

    def __init__(self, sample_distribution=None, sample_mean=None, sample_sd=None, sample_size=None):
        if sample_mean is not None:
            self.point_estimate = sample_mean

        if sample_sd is not None:
            self.sample_sd = sample_sd

        if sample_size is not None:
            self.sample_size = sample_size

        if sample_distribution is not None:
            self.sample_distribution = sample_distribution
            self.point_estimate = sample_distribution.mean
            self.sample_sd = sample_distribution.sd
            self.sample_size = sample_distribution.sample_size

        self.standard_error = MeanSamplingDistribution.calculate_standard_error(self.sample_sd, self.sample_size)

        self.df = self.sample_size - 1.0
        if self.sample_size < 30:
            self.distribution_family = DistributionFamily.student_t
        else:
            self.distribution_family = DistributionFamily.normal

    @staticmethod
    def calculate_standard_error(sample_sd, sample_size):
        return sample_sd / math.sqrt(sample_size)

    def confidence_interval(self, confidence_level):
        q = 1 - (1 - confidence_level) / 2
        if self.distribution_family == DistributionFamily.normal:
            z = norm.ppf(q)
            pf = z * self.standard_error
            return self.point_estimate - pf, self.point_estimate + pf
        else:
            t_df = t.ppf(q, self.df)
            pf = t_df * self.standard_error + self.point_estimate
            return self.point_estimate - pf, self.point_estimate + pf


class ProportionSamplingDistribution(object):
    sample_distribution = None
    point_estimate = None
    distribution_family = None
    sample_size = None
    categorical_value = None
    standard_error = None
    simulated_proportions = None

    def __init__(self, sample_distribution=None, categorical_value=None, sample_proportion=None, sample_size=None):
        if sample_proportion is not None:
            self.point_estimate = sample_proportion

        if sample_size is not None:
            self.sample_size = sample_size

        if categorical_value is not None:
            self.categorical_value = categorical_value

        if sample_distribution is not None:
            self.build(sample_distribution)

        if self.sample_size * self.point_estimate < 10 or self.sample_size * (1 - self.point_estimate) < 10:
            self.distribution_family = DistributionFamily.simulation
            self.simulate()
        else:
            self.distribution_family = DistributionFamily.normal
            self.standard_error = math.sqrt(self.point_estimate * (1 - self.point_estimate) / self.sample_size)

    def build(self, sample_distribution):
        self.sample_distribution = sample_distribution
        self.point_estimate = sample_distribution.proportion
        self.categorical_value = sample_distribution.categorical_value
        self.sample_size = sample_distribution.sample_size

    def simulate(self):
        self.simulated_proportions = [0] * 1000
        for iter in range(1000):
            count = 0
            for trials in range(self.sample_size):
                if random.random() <= self.point_estimate:
                    count += 1
            self.simulated_proportions[iter] = float(count) / self.sample_size
        self.simulated_proportions = sorted(self.simulated_proportions)

    def confidence_interval(self, confidence_level):
        q = 1 - (1 - confidence_level) / 2
        if self.distribution_family == DistributionFamily.normal:
            z = norm.ppf(q)
            pf = z * self.standard_error
            return self.point_estimate - pf, self.point_estimate + pf
        else:
            threshold1 = int(1000 * (1 - confidence_level) / 2)
            threshold2 = int(1000 * q)
            return self.simulated_proportions[threshold1], self.simulated_proportions[threshold2]

