pysie
=====

Package pysie implements a statistical inference engine in Python

.. image:: https://travis-ci.org/chen0040/pysie.svg?branch=master
    :target: https://travis-ci.org/chen0040/pysie

.. image:: https://coveralls.io/repos/github/chen0040/pysie/badge.svg?branch=master
    :target: https://coveralls.io/github/chen0040/pysie?branch=master

.. image:: https://scrutinizer-ci.com/g/chen0040/pysie/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/chen0040/pysie/?branch=master


Install
=======

Run the following command to install pysie using pip

.. code-block:: bash

    $ pip install pysie


Features
========

* Automatically switch between Student's T, binomial simulation bootstrapping, or normal sampling distribution based on the sample size
* Computer the confidence interval for the sampling distribution given a confidence level
* Carry out hypothesis testing for both mean (for numerical sample data) and proportion (for categorical sample data)
* Carry out hypothesis testing between two different experiment setup (or two different distinct groups or populations)
* Anova: Carry out hypothesis testing on whether a numerical variable is independent of a categorical variable given a sample data table containing the two variables as columns
* Chi-Square Testing: Carry out hypothesis testing on whether two categorical variables are independent of each other given a sample data table containing the two variables as columns
* Anova for regression: Carry out hypothesis testing on whether two numerical variables are independent of each other given a sample data table containing the two variables as columns

Usage
=====

Numerical sample
----------------

The sample code below shows how to create numerical sample:

.. code-block:: python

    sample = Sample()
    sample.add_numeric(x=0.001)
    sample.add_numeric(x=0.02)
    ...

    print(sample.size()) # return the rows in the sample data table
    print(sample.is_numerical()) # return True
    print(sample.is_categorical()) # return False
    print(sample.get(0).x) # return 0.001
    print(sample.get(1).x) # return 0.02


In the above code, the numerical variable is 'x'

Categorical sample
------------------

The sample code below shows how to create categorical sample:

.. code-block:: python

    sample = Sample()
    sample.add_category(label="OK")
    sample.add_category(label="CANCEL")
    sample.add_category(label="OK")
    ...

    print(sample.size()) # return the rows int the sample data table
    print(sample.is_categorical()) # return True
    print(sample.is_numerical()) # return False
    print(sample.get(0).label) # return "OK"
    print(sample.get(1).label) # return "CANCEL"


In the above code, the categorical variable is 'label'

Sample containing one numerical variable and one categorical variables
-----------------------------------------------------------------------

The sample code below shows how to create a sample containing two columns (one numerical and the other categorical):

.. code-block:: python

    sample = Sample()
    sample.add_numeric(x=0.001, group_id='grp1')
    sample.add_numeric(x=0.02, group_id='grp1')
    sample.add_numeric(x=0.003, group_id='grp1')
    ...

    print(sample.size()) # return the rows in the sample data table
    print(sample.is_numerical()) # return True
    print(sample.is_categorical()) # return False
    print(sample.get(0).x) # return 0.001
    print(sample.get(0).group_id) # return 'grp1'
    print(sample.get(1).x) # return 0.02
    print(sample.get(1).group_id) # return 'grp1'


In the above code, the numerical variable is 'x' and the categorical variable is 'group_id'

Sample containing two categorical variables as its data columns
---------------------------------------------------------------

The sample code below shows how to create a sample containing two categorical columns

.. code-block:: python

    sample = Sample()
    sample.add_category(label='OK', group_id='grp1')
    sample.add_category(label='CANCEL', group_id='grp1')
    sample.add_category(label='OK', group_id='grp1')
    ...

    print(sample.size()) # return the rows int the sample data table
    print(sample.is_categorical()) # return True
    print(sample.is_numerical()) # return False
    print(sample.get(0).label) # return "OK"
    print(sample.get(0).group_id) # return 'grp1'
    print(sample.get(1).label) # return "CANCEL"
    print(sample.get(1).group_id) # return 'grp1'


In the above code, the first categorical variable is 'label', and the second categorical variable is 'group_id'

Sample containing two numerical variables as its data columns
-------------------------------------------------------------

The sample code below shows how to create a sample containing two numerical columns

.. code-block:: python

    sample = Sample()
    sample.add_xy(x=0.001, y=0.01)
    sample.add_xy(x=0.02, y=0.2)
    ...

    print(sample.size()) # return the rows in the sample data table
    print(sample.is_numerical()) # return True
    print(sample.is_categorical()) # return False
    print(sample.get(0).x) # return 0.001
    print(sample.get(0).y) # return 0.01
    print(sample.get(1).x) # return 0.02
    print(sample.get(1).y) # return 0.2


Sampling distribution for Sample Means
--------------------------------------

The sample code below show how to derive the sampling distribution for the sample means of a population given a numerical
sample from that population:

.. code-block:: python

    sample = Sample()
    sample.add_numeric(x=0.001)
    sample.add_numeric(x=0.02)
    ...

    sampling_distribution = MeanSamplingDistribution(sample_distribution=SampleDistribution(sample))
    print('sampling distribution: (mu = ' + str(sampling_distribution.point_estimate)
              + ', SE = ' + str(sampling_distribution.standard_error) + ')')
    print('The sampling distribution belong to family: ' + sampling_distribution.distribution_family)
    print('We are 95% confident that the true mean for the underlying population is between : '
              + str(sampling_distribution.confidence_interval(0.95)))


Sampling distribution for Sample Proportions
--------------------------------------------

The sample code below show how to derive the sampling distribution for the proportion of class 'A' of a population
given a categorical sample from that population:

.. code-block:: python

    sample = Sample()
    sample.add_category(label='A')
    sample.add_category(label='C')
    sample.add_category(label='A')
    sample.add_category(label='B')
    ...

    sampling_distribution = ProportionSamplingDistribution(sample_distribution=SampleDistribution(sample,
        categorical_value="A"))
    print('sampling distribution: (p = ' + str(sampling_distribution.point_estimate)
              + ', SE = ' + str(sampling_distribution.standard_error) + ')')
    print('The sampling distribution belong to family: ' + sampling_distribution.distribution_family)
    print('We are 95% confident that the true proportion of "A" in the underlying population is between : '
              + str(sampling_distribution.confidence_interval(0.95)))


Compare Sample Means between Two Different Groups
-------------------------------------------------

The sample code below shows how to derive the sampling distribution for the difference between sample means of two
different groups (e.g., two different experiment setups or two different populations):

.. code-block:: python

    grp1_sample = Sample()
    grp1_sample.add_numeric(x=0.001)
    grp1_sample.add_numeric(x=0.02)
    ...
    grp2_sample = Sample()
    grp2_sample.add_numeric(x=0.02)
    grp2_sample.add_numeric(x=0.03)
    ...
    sampling_distribution = MeanDiffSamplingDistribution(grp1_sample_distribution=SampleDistribution(grp1_sample),
                                                             grp2_sample_distribution=SampleDistribution(grp2_sample))
    self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
    print('sampling distribution: (mean_diff = ' + str(sampling_distribution.point_estimate)
          + ', SE = ' + str(sampling_distribution.standard_error) + ')')
    print('We are 95% confident that the difference between them is : '
          + str(sampling_distribution.confidence_interval(0.95)))


Compare Sample Proportions between Two Different Groups
-------------------------------------------------------

The sample code below shows how to derive the sampling distribution for the difference between sample means of two
different groups (e.g., two different experiment setups or two different populations):

.. code-block:: python

    grp1_sample = Sample()
    grp1_sample.add_category(label='A')
    grp1_sample.add_category(label='C')
    ...
    grp2_sample = Sample()
    grp2_sample.add_category(label='A')
    grp2_sample.add_category(label='B')
    ...
    sampling_distribution = ProportionDiffSamplingDistribution(
        grp1_sample_distribution=SampleDistribution(grp1_sample, categorical_value="A"),
        grp2_sample_distribution=SampleDistribution(grp2_sample, categorical_value="A"))
    self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)
    print('sampling distribution: (proportion_diff = ' + str(sampling_distribution.point_estimate)
          + ', SE = ' + str(sampling_distribution.standard_error) + ')')
    print('We are 95% confident that the difference in proportion of "A" between them is : '
          + str(sampling_distribution.confidence_interval(0.95)))


Hypothesis Testing on Mean
--------------------------

The sample code below shows how to test whether the true mean of a population (from which the numerical sample is taken)
is equal to a particular value 0.99:

.. code-block:: python

    sample = Sample()
    sample.add_numeric(0.01)
    sample.add_numeric(0.02)
    ...

    sampling_distribution = MeanSamplingDistribution(sample_distribution=SampleDistribution(sample))
    testing = MeanTesting(sampling_distribution=sampling_distribution, mean_null=0.99)

    print('one tail p-value: ' + str(testing.p_value_one_tail))
    print('two tail p-value: ' + str(testing.p_value_two_tail))
    reject_one_tail, reject_two_tail = testing.will_reject(0.01) # 0.01 is the significance level
    print('will reject mean = 0.99 (one-tail) ? ' + str(reject_one_tail))
    print('will reject mean = 0.99 (two-tail) ? ' + str(reject_two_tail))


Hypothesis Testing on Proportion
--------------------------------

The sample code below shows how to test whether the true proportion of class "A" in a population (from which the
categorical sample is taken) is equal to a particular value 0.51:

.. code-block:: python

    sample = Sample()
    sample.add_category("A")
    sample.add_category("B")
    sample.add_category("A")
    ...

    sampling_distribution = ProportionSamplingDistribution(
        sample_distribution=SampleDistribution(sample, categorical_value="A"))

    testing = ProportionTesting(sampling_distribution=sampling_distribution, p_null=0.51)

    print('one tail p-value: ' + str(testing.p_value_one_tail))
    print('two tail p-value: ' + str(testing.p_value_two_tail))
    reject_one_tail, reject_two_tail = testing.will_reject(0.01) # 0.01 is the significance level
    print('will reject proportion(A) = 0.51 (one-tail) ? ' + str(reject_one_tail))
    print('will reject proportion(A) = 0.51 (two-tail) ? ' + str(reject_two_tail))


Hypothesis Testing on Mean Comparison (Two Groups)
--------------------------------------------------

The sample code below shows how to test whether to reject the hypothesis that the means of two different groups (e.g.
two different experiments or populations from which the numerical samples are take) are the same:

.. code-block:: python

    grp1_sample = Sample()
    grp1_sample.add_numeric(0.01)
    grp1_sample.add_numeric(0.02)
    ...
    grp2_sample = Sample()
    grp2_sample.add_numeric(0.03)
    grp2_sample.add_numeric(0.02)
    ...

    sampling_distribution = MeanDiffSamplingDistribution(grp1_sample_distribution=SampleDistribution(grp1_sample),
                                                             grp2_sample_distribution=SampleDistribution(grp2_sample))

    testing = MeanDiffTesting(sampling_distribution=sampling_distribution)

    print('one tail p-value: ' + str(testing.p_value_one_tail))
    print('two tail p-value: ' + str(testing.p_value_two_tail))
    reject_one_tail, reject_two_tail = testing.will_reject(0.01) # 0.01 is the significance level
    print('will reject hypothesis that two groups have same means (one-tail) ? ' + str(reject_one_tail))
    print('will reject hypothesis that two groups have same means (two-tail) ? ' + str(reject_two_tail))


Hypothesis Testing on Proportion Comparison (Two Groups)
--------------------------------------------------------

The sample code below shows how to test whether reject the hypothesis that the true proportion of class "A" in two
groups (from which the categorical samples are taken) are equal to each other:

.. code-block:: python

    grp1_sample = Sample()
    grp1_sample.add_category("A")
    grp1_sample.add_category("B")
    grp1_sample.add_category("A")
    ...
    grp2_sample = Sample()
    grp2_sample.add_category("A")
    grp2_sample.add_category("B")
    grp2_sample.add_category("C")
    ...

    sampling_distribution = ProportionDiffSamplingDistribution(
        grp1_sample_distribution=SampleDistribution(grp1_sample, categorical_value="A"),
        grp2_sample_distribution=SampleDistribution(grp2_sample, categorical_value="A"))
    self.assertEqual(sampling_distribution.distribution_family, DistributionFamily.normal)

    testing = ProportionDiffTesting(sampling_distribution=sampling_distribution)

    print('one tail p-value: ' + str(testing.p_value_one_tail))
    print('two tail p-value: ' + str(testing.p_value_two_tail))
    reject_one_tail, reject_two_tail = testing.will_reject(0.01) # 0.01 is the significance level
    print('will reject proportion(A, grp1) = proportion(A, grp2) (one-tail) ? ' + str(reject_one_tail))
    print('will reject proportion(A, grp1) = proportion(A, grp2) (two-tail) ? ' + str(reject_two_tail))


Independence Testing between One Numerical and One Categorical Variable (ANOVA)
-------------------------------------------------------------------------------

The sample code below show how to test whether to reject the hypothesis that a numerical and categorical variable are
independent of each other for a population (from which the numerical sample is taken):

.. code-block:: python

    sample = Sample()
    sample.add_numeric(x=0.001, group_id='grp1')
    sample.add_numeric(x=0.02, group_id='grp1')
    sample.add_numeric(x=0.003, group_id='grp1')
    ...

    testing = Anova(sample=sample)

    print('p-value: ' + str(testing.p_value))
    reject = testing.will_reject(0.01)
    print('will reject [same mean for all groups] ? ' + str(reject))


Independence Testing between Two Categorical Variables (Chi-Square Testing):

The sample code below show how to test whether to reject that hypothesis that two categorical variables are independent
of each other for a population (from which the categorical sampleis taken):


.. code-block:: python

    sample = Sample()

    for i in range(1000):
        sample.add_category('itemA' if numpy.random.randn() > 0 else 'itemB', 'group1')
        sample.add_category('itemA' if numpy.random.randn() > 0 else 'itemB', 'group2')
        sample.add_category('itemA' if numpy.random.randn() > 0 else 'itemB', 'group3')

    testing = ChiSquare(sample=sample)

    print('p-value: ' + str(testing.p_value))
    reject = testing.will_reject(0.01)
    print('will reject [two categorical variables are independent of each other] ? ' + str(reject))


