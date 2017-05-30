import math
from enum import Enum

from scipy.stats import norm, t

class DistributionFamily(Enum):
    normal = 1
    student_t = 2
    fisher = 3
    chi_square = 4


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
            pf = z * self.standard_error + self.point_estimate
            return -pf, pf
        else:
            t_df = t.ppf(q, self.df)
            pf = t_df * self.standard_error + self.point_estimate
            return -pf, pf
