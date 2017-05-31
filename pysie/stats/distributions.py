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
    sample_sd = None
    sample_size = None

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


class MeanDiffSamplingDistribution(object):
    grp1_sample_distribution = None
    grp2_sample_distribution = None
    grp1_point_estimate = None
    grp2_point_estimate = None
    grp1_sample_sd = None
    grp2_sample_sd = None
    grp1_sample_size = None
    grp2_sample_size = None
    distribution_family = None
    df = None
    point_estimate = None

    def __init__(self, grp1_sample_distribution=None, grp1_sample_mean=None, grp1_sample_sd=None, grp1_sample_size=None,
                 grp2_sample_distribution=None, grp2_sample_mean=None, grp2_sample_sd=None, grp2_sample_size=None):
        self.build_grp1(grp1_sample_distribution, grp1_sample_mean, grp1_sample_sd, grp1_sample_size)
        self.build_grp2(grp2_sample_distribution, grp2_sample_mean, grp2_sample_sd, grp2_sample_size)

        self.standard_error = self.calculate_standard_error()

        self.df = min(self.grp1_sample_size - 1.0, self.grp2_sample_size - 1.0)
        self.point_estimate = self.grp1_point_estimate - self.grp2_point_estimate

        if self.grp1_sample_size < 30 or self.grp2_sample_size < 30:
            self.distribution_family = DistributionFamily.student_t
        else:
            self.distribution_family = DistributionFamily.normal

    def build_grp1(self, grp1_sample_distribution=None, grp1_sample_mean=None, grp1_sample_sd=None, grp1_sample_size=None):
        if grp1_sample_mean is not None:
            self.grp1_point_estimate = grp1_sample_mean

        if grp1_sample_sd is not None:
            self.grp1_sample_sd = grp1_sample_sd

        if grp1_sample_size is not None:
            self.grp1_sample_size = grp1_sample_size

        if grp1_sample_distribution is not None:
            self.grp1_sample_distribution = grp1_sample_distribution
            self.grp1_point_estimate = grp1_sample_distribution.mean
            self.grp1_sample_sd = grp1_sample_distribution.sd
            self.grp1_sample_size = grp1_sample_distribution.sample_size
            
    def build_grp2(self, grp2_sample_distribution=None, grp2_sample_mean=None, grp2_sample_sd=None, grp2_sample_size=None):
        if grp2_sample_mean is not None:
            self.grp2_point_estimate = grp2_sample_mean

        if grp2_sample_sd is not None:
            self.grp2_sample_sd = grp2_sample_sd

        if grp2_sample_size is not None:
            self.grp2_sample_size = grp2_sample_size

        if grp2_sample_distribution is not None:
            self.grp2_sample_distribution = grp2_sample_distribution
            self.grp2_point_estimate = grp2_sample_distribution.mean
            self.grp2_sample_sd = grp2_sample_distribution.sd
            self.grp2_sample_size = grp2_sample_distribution.sample_size

    def calculate_standard_error(self):
        return math.sqrt(self.grp1_sample_sd * self.grp1_sample_sd / self.grp1_sample_size + 
                         self.grp2_sample_sd * self.grp2_sample_sd / self.grp2_sample_size)

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
        for i in range(1000):
            count = 0
            for trials in range(self.sample_size):
                if random.random() <= self.point_estimate:
                    count += 1
            self.simulated_proportions[i] = float(count) / self.sample_size
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
        
        
class ProportionDiffSamplingDistribution(object):
    grp1_sample_distribution = None
    grp2_sample_distribution = None
    grp1_point_estimate = None
    grp2_point_estimate = None
    distribution_family = None
    grp1_sample_size = None
    grp2_sample_size = None
    categorical_value = None
    standard_error = None
    grp1_simulated_proportions = None
    grp2_simulated_proportions = None
    diff_simulated_proportions = None
    point_estimate = None

    def __init__(self, categorical_value=None,
                 grp1_sample_distribution=None, grp1_sample_proportion=None, grp1_sample_size=None,
                 grp2_sample_distribution=None, grp2_sample_proportion=None, grp2_sample_size=None):
        if categorical_value is not None:
            self.categorical_value = categorical_value
            
        self.build_grp1(grp1_sample_distribution, grp1_sample_proportion, grp1_sample_size)
        self.build_grp2(grp2_sample_distribution, grp2_sample_proportion, grp2_sample_size)

        if not self.is_clt_held():
            self.distribution_family = DistributionFamily.simulation
            self.simulate()
        else:
            self.distribution_family = DistributionFamily.normal
            self.standard_error = self.calculate_standard_error()

        self.point_estimate = self.grp1_point_estimate - self.grp2_point_estimate
            
    def calculate_standard_error(self):
        return math.sqrt(self.grp1_point_estimate * (1 - self.grp1_point_estimate) / self.grp2_sample_size +
                         self.grp2_point_estimate * (1 - self.grp2_point_estimate) / self.grp2_sample_size)

    def is_clt_held(self):
        if self.grp1_sample_size * self.grp1_point_estimate < 10:
            return False
        if self.grp1_sample_size * (1 - self.grp1_point_estimate) < 10:
            return False
        if self.grp2_sample_size * self.grp2_point_estimate < 10:
            return False
        if self.grp2_sample_size * (1 - self.grp2_point_estimate) < 10:
            return False
        return True

    def build_grp1(self, grp1_sample_distribution=None, grp1_sample_proportion=None, grp1_sample_size=None):
        if grp1_sample_proportion is not None:
            self.grp1_point_estimate = grp1_sample_proportion

        if grp1_sample_size is not None:
            self.grp1_sample_size = grp1_sample_size

        if grp1_sample_distribution is not None:
            self.grp1_sample_distribution = grp1_sample_distribution
            self.grp1_point_estimate = grp1_sample_distribution.proportion
            self.categorical_value = grp1_sample_distribution.categorical_value
            self.grp1_sample_size = grp1_sample_distribution.sample_size

    def build_grp2(self, grp2_sample_distribution=None, grp2_sample_proportion=None, grp2_sample_size=None):
        if grp2_sample_proportion is not None:
            self.grp2_point_estimate = grp2_sample_proportion

        if grp2_sample_size is not None:
            self.grp2_sample_size = grp2_sample_size

        if grp2_sample_distribution is not None:
            self.grp2_sample_distribution = grp2_sample_distribution
            self.grp2_point_estimate = grp2_sample_distribution.proportion
            self.categorical_value = grp2_sample_distribution.categorical_value
            self.grp2_sample_size = grp2_sample_distribution.sample_size
            
    def simulate(self):
        self.grp1_simulated_proportions = ProportionDiffSamplingDistribution.simulate_grp(self.grp1_point_estimate,
                                                                                          self.grp1_sample_size)
        self.grp2_simulated_proportions = ProportionDiffSamplingDistribution.simulate_grp(self.grp2_point_estimate,
                                                                                          self.grp2_sample_size)

        self.diff_simulated_proportions = [0] * 1000;
        for i in range(1000):
            self.diff_simulated_proportions[i] = self.grp1_simulated_proportions[i] - self.grp2_simulated_proportions[i]
        
    @staticmethod
    def simulate_grp(proportion, sample_size):
        simulated_proportions = [0] * 1000
        for iter in range(1000):
            count = 0
            for trials in range(sample_size):
                if random.random() <= proportion:
                    count += 1
            simulated_proportions[iter] = float(count) / sample_size

        return sorted(simulated_proportions)
    
    def confidence_interval(self, confidence_level):
        q = 1 - (1 - confidence_level) / 2
        if self.distribution_family == DistributionFamily.normal:
            z = norm.ppf(q)
            pf = z * self.standard_error
            return self.point_estimate - pf, self.point_estimate + pf
        else:
            threshold1 = int(1000 * (1 - confidence_level) / 2)
            threshold2 = int(1000 * q)
            return self.diff_simulated_proportions[threshold1], self.diff_simulated_proportions[threshold2]



