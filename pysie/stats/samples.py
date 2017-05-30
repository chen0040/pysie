import math


class Observation(object):
    x = None
    y = None
    group_id = None
    label = None

    def __init__(self, x=None, label=None, group_id=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

        if label is not None:
            self.label = label

        if group_id is not None:
            self.group_id = group_id

    def is_categorical(self):
        return self.label is not None

    def is_numerical(self):
        return self.x is not None


class Sample(object):
    observations = None

    def __init__(self):
        self.observations = []

    def add(self, observation):
        self.observations.append(observation)

    def add_numeric(self, numeric, group_id=None):
        ob = Observation()
        ob.x = numeric
        ob.group_id = group_id
        self.add(ob)

    def add_category(self, category, group_id=None):
        ob = Observation()
        ob.label = category
        ob.group_id = group_id
        self.add(ob)

    def add_xy(self, x, y, group_id=None):
        ob = Observation()
        ob.x = x
        ob.y = y
        ob.group_id = group_id
        self.add(ob)

    def size(self):
        return len(self.observations)

    def get(self, index):
        return self.observations[index]

    def is_categorical(self):
        return self.observations[0].is_categorical()

    def is_numerical(self):
        return self.observations[0].is_numerical()

    def count_by_group_id(self, group_id):
        return sum(1 for x in self.observations if group_id is None or x.group_id == group_id)


class SampleDistribution(object):
    sample = None
    group_id = None

    categorical_value = None
    is_categorical = False
    is_numerical = False

    sd = None
    sample_size = None
    mean = None
    variance = None
    sum_of_squares= None

    proportion = None

    def __init__(self, sample=None, group_id=None, categorical_value=None, mean=None, sd=None, sample_size=None, proportion=None):
        if group_id is not None:
            self.group_id = group_id
        if categorical_value is not None:
            self.categorical_value = categorical_value

        if mean is not None:
            self.mean = mean
            self.is_numerical = True

        if proportion is not None:
            self.proportion = proportion
            self.is_categorical = True

        if sample_size is not None:
            self.sample_size = sample_size

        if sd is not None:
            self.sd = sd

        if self.sd is not None and self.sample_size is not None:
            self.variance = self.sd * self.sd
            self.sum_of_squares = self.variance * (self.sample_size-1)

        if sample is not None:
            self.build(sample)

    def build(self, sample):
        self.sample = sample
        if sample.is_numerical():
            self.mean = SampleDistribution.calculate_mean(sample, self.group_id)
            self.sum_of_squares = SampleDistribution.calculate_sum_of_squares(sample, self.mean, self.group_id)
            self.sample_size = sample.count_by_group_id(self.group_id)
            self.variance = self.sum_of_squares / (self.sample_size - 1)
            self.sd = math.sqrt(self.variance)
            self.is_numerical = True
        elif sample.is_categorical() and self.categorical_value is not None:
            self.proportion = SampleDistribution.calculate_proportion(sample, self.categorical_value, self.group_id)
            self.sample_size = sample.count_by_group_id(self.group_id)
            self.mean = self.proportion * self.sample_size
            self.variance = self.proportion * (1.0 - self.proportion) * self.sample_size
            self.is_categorical = True

    @staticmethod
    def calculate_mean(sample, group_id):
        count = 0
        the_sum = 0
        for i in range(sample.size()):
            observation = sample.get(i)
            if group_id is not None and observation.group_id != group_id:
                continue
            the_sum += observation.x
            count += 1
        return the_sum / count

    @staticmethod
    def calculate_sum_of_squares(sample, mean, group_id):
        the_sum = 0
        for i in range(sample.size()):
            observation = sample.get(i)
            if group_id is not None and observation.group_id != group_id:
                continue
            the_sum += (observation.x - mean) * (observation.x - mean)
        return the_sum

    @staticmethod
    def calculate_proportion(sample, categorical_value, group_id):
        counter1 = 0
        counter2 = 0
        for i in range(sample.size()):
            observation = sample.get(i)
            if group_id is not None and observation.group_id != group_id:
                continue
            counter2 += 1
            if observation.label == categorical_value:
                counter1 += 1
        if counter2 == 0:
            return 0
        return counter1 / counter2

