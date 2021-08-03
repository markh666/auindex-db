import numpy as np

__all__ = ["t_test_statistic"]
def t_test_statistic(sample, example):
    sample_std = np.std(sample)
    sample_mean = np.mean(sample)
    return (example-sample_mean)/(sample_std+1e-7)
