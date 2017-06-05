import math

from pysie.dsl.set import TernarySearchSet, TernarySearchTrie
from pysie.stats.distributions import MeanSamplingDistribution
from pysie.stats.samples import SampleDistribution

from scipy.stats import f


class ContingencyTable(object):
    values = None
    rows = None
    columns = None

    def __init__(self):
        self.rows = TernarySearchSet()
        self.columns = TernarySearchSet()
        self.values = TernarySearchTrie()

    def set_cell(self, row_name, column_name, value):
        key = self.make_key(row_name, column_name)
        self.values.put(key, value)
        self.rows.add(row_name)
        self.columns.add(column_name)

    def get_cell(self, row_name, column_name):
        key = self.make_key(row_name, column_name)
        if not self.values.contains_key(key):
            return 0
        return self.values.get(key)

    def make_key(self, row_name, column_name):
        return row_name + '-' + column_name

    def get_row_total(self, row_name):
        column_names = self.columns.to_array()
        result = 0
        for x in column_names:
            result += self.get_cell(row_name, x)
        return result

    def get_column_total(self, column_name):
        row_names = self.rows.to_array()
        result = 0
        for x in row_names:
            result += self.get_cell(x, column_name)
        return result

    def get_total(self):
        values = self.values.values()
        result = 0
        for val in values:
            result += val
        return result


class Anova(object):
    sample = None
    individual_samples = None
    individual_sample_distributions = None
    individual_sampling_distributions = None
    overall_sample_distribution = None
    overall_sampling_distribution = None

    sum_of_squares_total = None
    sum_of_squares_group = None
    sum_of_squares_error = None

    df_group = None
    df_error = None
    df_total = None

    mean_square_group = None
    mean_square_error = None

    F = None
    p_value = None

    significance_level = None
    reject_mean_same = None

    def __init__(self, sample, significance_level=None):
        if significance_level is not None:
            self.significance_level = significance_level

        self.sample = sample
        self.individual_sampling_distributions = TernarySearchTrie()
        self.individual_sample_distributions = TernarySearchTrie()
        self.individual_samples = sample.split_by_group_id()
        for group_id in self.individual_samples.keys():
            sample_distribution = SampleDistribution(sample=self.individual_samples.get(group_id), group_id=group_id)
            sampling_distribution = MeanSamplingDistribution(sample_distribution=sample_distribution)
            self.individual_sample_distributions.put(group_id, sample_distribution)
            self.individual_sampling_distributions.put(group_id, sampling_distribution)

        self.overall_sample_distribution = SampleDistribution(sample=sample, group_id=None)
        self.overall_sampling_distribution = MeanSamplingDistribution(self.overall_sample_distribution)
        self.build()

    def build(self):
        self.sum_of_squares_total = self.overall_sample_distribution.sum_of_squares
        self.sum_of_squares_group = 0
        mean_overall = self.overall_sample_distribution.mean
        for sample_distribution_i in self.individual_sample_distributions.values():
            mean_i = sample_distribution_i.mean
            self.sum_of_squares_group += math.pow(mean_i - mean_overall, 2.0) * sample_distribution_i.sample_size
        self.sum_of_squares_error = self.sum_of_squares_total - self.sum_of_squares_group

        self.df_total = self.sample.size() - 1
        self.df_group = self.individual_samples.size() - 1
        self.df_error = self.df_total - self.df_group

        self.mean_square_error = self.sum_of_squares_error / self.df_error
        self.mean_square_group = self.sum_of_squares_group / self.df_group

        self.F = self.mean_square_group / self.mean_square_error
        self.p_value = 1 - f.cdf(self.F, self.df_group, self.df_error)

        if self.significance_level is not None:
            self.reject_mean_same = self.p_value >= self.significance_level

    def will_reject(self, significance_level):

        return self.p_value < significance_level
