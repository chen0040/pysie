import math

from pysie.stats.distributions import DistributionFamily
from scipy.stats import norm, t


class MeanTesting(object):
    sampling_distribution = None
    p_value_one_tail = None
    p_value_two_tail = None
    mean_null = None
    test_statistic = None
    significance_level = None
    reject_mean_null = None

    def __init__(self, sampling_distribution, mean_null, significance_level=None):
        self.sampling_distribution = sampling_distribution
        self.mean_null = mean_null
        if significance_level is not None:
            self.significance_level = significance_level

        if self.sampling_distribution.distribution_family == DistributionFamily.normal:
            standard_error_null = sampling_distribution.standard_error
            Z = (sampling_distribution.point_estimate - mean_null) / standard_error_null
            self.test_statistic = Z
            pf = norm.cdf(Z)
            self.p_value_one_tail = 1 - pf
            self.p_value_two_tail = self.p_value_one_tail * 2
        else:
            standard_error_null = sampling_distribution.standard_error
            td_df = (sampling_distribution.point_estimate - mean_null) / standard_error_null
            self.test_statistic = td_df
            pf = t.cdf(td_df, sampling_distribution.df)
            self.p_value_one_tail = 1 - pf
            self.p_value_two_tail = self.p_value_one_tail * 2

        if significance_level is not None:
            self.reject_mean_null = (self.p_value_one_tail < significance_level,
                                     self.p_value_two_tail < significance_level)


class ProportionTesting(object):
    sampling_distribution = None
    p_value_one_tail = None
    p_value_two_tail = None
    mean_null = None
    test_statistic = None
    significance_level = None
    reject_mean_null = None

    def __init__(self, sampling_distribution, p_null, significance_level=None):
        self.sampling_distribution = sampling_distribution
        self.p_null = p_null
        if significance_level is not None:
            self.significance_level = significance_level

        if self.sampling_distribution.distribution_family == DistributionFamily.normal:
            standard_error_null = math.sqrt(p_null * (1 - p_null) / sampling_distribution.sample_size)
            Z = (sampling_distribution.point_estimate - p_null) / standard_error_null
            self.test_statistic = Z
            pf = norm.cdf(Z)
            self.p_value_one_tail = 1 - pf
            self.p_value_two_tail = self.p_value_one_tail * 2
        else:
            standard_error_null = math.sqrt(p_null * (1 - p_null) / sampling_distribution.sample_size)
            td_df = (sampling_distribution.point_estimate - p_null) / standard_error_null
            self.test_statistic = td_df
            pf = t.cdf(td_df, sampling_distribution.df)
            self.p_value_one_tail = 1 - pf
            self.p_value_two_tail = self.p_value_one_tail * 2

        if significance_level is not None:
            self.reject_mean_null = (self.p_value_one_tail < significance_level,
                                     self.p_value_two_tail < significance_level)

