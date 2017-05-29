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

    def __init__(self, sample=None, group_id=None):
        if group_id is not None:
            self.group_id = group_id
        if sample is not None:
            self.sample = sample
            self.mean = SampleDistribution.calculate_mean(sample, group_id)

    @staticmethod
    def calculate_mean(sample, group_id):
        count = 0
        sum = 0
        for i in range(sample.size()):
            observation = sample.get(i)
            if observation.group_id != group_id:
                continue
            sum += observation.x
            count += 1
        return sum / count
