# https://arxiv.org/pdf/2211.17192
# В этом задании вам предстоит реализовать функцию resample(sample_id: int) -> resampled_id: int
# Она принимает sample_id, распределенные как draft_dist (q) и возвращает resampled_id
# resampled_id должны быть распределены как target_dist (p)
# При этом максимально возможное число resampled_id должно совпадать с входными sampled_id
# 
# Для этого предлагается воспользоваться алгоритмом Speculative Sampling:
# Оставлять sampled_id с вероятностью p / q
# А если не оставили, то ресэмплировать из normalize(max(0, p - q))


import numpy as np


class SpeculativeSampler:
    def __init__(self, draft_dist: np.ndarray, target_dist: np.ndarray):
        """
        draft_dist : np.ndarray
            1D probability vector q over the vocabulary (sums to 1).
        target_dist : np.ndarray
            1D probability vector p over the vocabulary (sums to 1).
        """
        self.p = target_dist
        self.q = draft_dist

        self.residual = np.maximum(0, self.p - self.q)
        if self.residual.sum() > 0:
            self.residual /= self.residual.sum()
        else:
            self.residual = np.ones_like(self.p) / len(self.p)

    def resample(self, sample_id: int, rng: np.random.Generator) -> int:
        """
        Apply the speculative-sampling accept/reject step.
        """
        if self.q[sample_id] == 0:
            return sample_id
        
        accept_prob = min(1.0, self.p[sample_id] / self.q[sample_id])
        if rng.random() < accept_prob:
            return sample_id
        return rng.choice(len(self.p), p=self.residual)


def run_experiment(vocab_size: int = 10, num_samples: int = 200_000, seed: int = None):
    rng = np.random.default_rng(seed)

    draft_dist = rng.dirichlet(np.ones(vocab_size))
    target_dist = rng.dirichlet(np.ones(vocab_size))

    sampler = SpeculativeSampler(draft_dist, target_dist)

    draft_samples = rng.choice(vocab_size, size=num_samples, p=draft_dist)

    final_samples = np.empty(num_samples, dtype=np.int64)
    num_accepted = 0
    for i, x in enumerate(draft_samples):
        y = sampler.resample(x, rng)
        final_samples[i] = y
        num_accepted += y == x

    empirical_dist = np.bincount(final_samples, minlength=vocab_size) / num_samples

    theoretical_accept = np.minimum(draft_dist, target_dist).sum()
    empirical_accept = num_accepted / num_samples
    print(f"Theoretical acceptance rate: {theoretical_accept:.4f}")
    print(f"Empirical   acceptance rate: {empirical_accept:.4f}")
    if empirical_accept < theoretical_accept - 0.01:
        print('вќЊ Empirical acceptance too low')
    else:
        print('вњ… Empirical acceptance is ok')

    max_abs_err = np.max(np.abs(empirical_dist - target_dist))
    print(f"Max |empirical - target|: {max_abs_err:.4f}")

    if max_abs_err > 0.01:
        print("вќЊ Resulting distribution doesn't match with target")
    else:
        print("вњ… Resulting distribution is ok")


if __name__ == "__main__":
    run_experiment()
