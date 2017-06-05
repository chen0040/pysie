import random

from pysie.stats.distributions import DistributionFamily
from scipy.stats import norm, t
import math


class MeanDiffTesting(object):
    sampling_distribution = None
    p_value_one_tail = None
    p_value_two_tail = None
    test_statistic = None
    significance_level = None
    reject_mean_same = None

    def __init__(self, sampling_distribution, significance_level=None):
        self.sampling_distribution = sampling_distribution
        if significance_level is not None:
            self.significance_level = significance_level

        if self.sampling_distribution.distribution_family == DistributionFamily.normal:
            Z = sampling_distribution.point_estimate / sampling_distribution.standard_error
            self.test_statistic = Z
            pf = norm.cdf(Z)
            if Z < 0:
                pf = 1 - pf
            self.p_value_one_tail = 1 - pf
            self.p_value_two_tail = self.p_value_one_tail * 2
        else:
            td_df = sampling_distribution.point_estimate / sampling_distribution.standard_error
            self.test_statistic = td_df
            pf = t.cdf(td_df, sampling_distribution.df)
            if td_df < 0:
                pf = 1 - pf
            self.p_value_one_tail = 1 - pf
            self.p_value_two_tail = self.p_value_one_tail * 2

        if significance_level is not None:
            self.reject_mean_same = (self.p_value_one_tail < significance_level,
                                     self.p_value_two_tail < significance_level)

    def will_reject(self, significance_level):

        return self.p_value_one_tail < significance_level, self.p_value_two_tail < significance_level


class ProportionDiffTesting(object):
    sampling_distribution = None
    p_value_one_tail = None
    p_value_two_tail = None
    p_null = None
    test_statistic = None
    significance_level = None
    reject_proportion_same = None

    def __init__(self, sampling_distribution, significance_level=None):
        self.sampling_distribution = sampling_distribution
        p_null = (sampling_distribution.grp1_point_estimate + sampling_distribution.grp2_point_estimate) / 2
        self.p_null = p_null
        if significance_level is not None:
            self.significance_level = significance_level

        if self.sampling_distribution.distribution_family == DistributionFamily.normal:
            standard_error_null = math.sqrt(p_null * (1 - p_null) / sampling_distribution.grp1_sample_size + p_null * (1-p_null) / sampling_distribution.grp2_sample_size)
            Z = sampling_distribution.point_estimate / standard_error_null
            self.test_statistic = Z
            pf = norm.cdf(Z)
            if Z < 0:
                pf = 1 - pf
            self.p_value_one_tail = 1 - pf
            self.p_value_two_tail = self.p_value_one_tail * 2
        else:
            simulated_proportions = self.simulate()
            diff = sampling_distribution.grp1_point_estimate - sampling_distribution.grp2_point_estimate
            pf = sum(1.0 for x in simulated_proportions if x > diff) / 1000.0
            self.p_value_one_tail = pf
            self.p_value_two_tail = sum(1.0 for x in simulated_proportions if x > diff or x < -diff) / 1000.0

        if significance_level is not None:
            self.reject_proportion_same = (self.p_value_one_tail < significance_level,
                                           self.p_value_two_tail < significance_level)

    def simulate(self):
        simulated_proportions = [0] * 1000
        for i in range(1000):
            count1 = 0
            for trials in range(self.sampling_distribution.grp1_sample_size):
                if random.random() <= self.p_null:
                    count1 += 1
            count2 = 0
            for trials in range(self.sampling_distribution.grp2_sample_size):
                if random.random() <= self.p_null:
                    count2 += 1

            simulated_proportions[i] = float(count1) / self.sampling_distribution.grp1_sample_size - float(count2) / self.sampling_distribution.grp2_sample_size
        return sorted(simulated_proportions)

    def will_reject(self, significance_level):

        return self.p_value_one_tail < significance_level, self.p_value_two_tail < significance_level