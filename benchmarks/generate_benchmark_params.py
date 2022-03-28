import argparse
from itertools import chain, product

import pandas as pd

parser = argparse.ArgumentParser(
    description="Generate parameters for which benchmark is run"
)

parser.add_argument(
    "-m",
    "--manifold",
    type=str,
    default="all",
    help="Manifold for which benchmark is run. 'all' denotes all manifolds present.",
)
parser.add_argument(
    "-n",
    "--n_samples",
    type=int,
    default=10,
    help="Number of samples for which benchmark is run",
)
args = parser.parse_args()


def spd_manifold_params(n_samples):
    manifold = "SPDMatrices"
    manifold_args = [(2,), (5,), (10,)]
    module = "geomstats.geometry.spd_matrices"

    def affine_metric_params(kwargs={}):
        params = []
        metric = "SPDMetricAffine"
        power_args = [-0.5, 1, 0.5]
        metric_args = list(product([item for item, in manifold_args], power_args))
        manifold_args_re = [
            item for item in manifold_args for i in range(len(power_args))
        ]
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args_re[i], metric_args[i])]
        return params

    def bures_wasserstein_metric_params(kwargs={}):
        params = []
        metric = "SPDMetricBuresWasserstein"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    def euclidean_metric_params(kwargs={}):
        params = []
        metric = "SPDMetricEuclidean"
        power_args = [-0.5, 1, 0.5]
        metric_args = list(product([item for item, in manifold_args], power_args))
        manifold_args_re = [
            item for item in manifold_args for i in range(len(power_args))
        ]
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args_re[i], metric_args[i])]
        return params

    def log_euclidean_metric_params(kwargs={}):
        params = []
        metric = "SPDMetricLogEuclidean"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return list(
        chain(
            *[
                bures_wasserstein_metric_params(),
                affine_metric_params(),
                euclidean_metric_params(),
                log_euclidean_metric_params(),
            ]
        )
    )


def stiefel_params(n_samples):
    manifold = "Stiefel"
    manifold_args = [(3, 2), (4, 3)]
    module = "geomstats.geometry.stiefel"

    def stiefel_canonical_metric_params(kwargs={}):
        params = []
        metric = "StiefelCanonicalMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return stiefel_canonical_metric_params()


def pre_shape_params(n_samples):
    manifold = "PreShapeSpace"
    manifold_args = [(3, 3), (5, 5)]
    module = "geomstats.geometry.pre_shape"

    def pre_shape_metric_params(kwargs={}):
        params = []
        metric = "PreShapeMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return pre_shape_metric_params()


def positive_lower_triangular_matrices_params(n_samples):
    manifold = "PositiveLowerTriangularMatrices"
    manifold_args = [(3,), (5,)]
    module = "geomstats.geometry.positive_lower_triangular_matrices"

    def cholesky_metric_params(kwargs={}):
        params = []
        metric = "CholeskyMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return cholesky_metric_params()


def minkowski_params(n_samples):
    manifold = "Minkowski"
    manifold_args = [(3,), (5,)]
    module = "geomstats.geometry.minkowski"

    def minkowski_metric_params(kwargs={}):
        params = []
        metric = "MinkowskiMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return minkowski_metric_params()


def matrices_params(n_samples):
    manifold = "Matrices"
    manifold_args = [(3, 3), (5, 5)]
    module = "geomstats.geometry.matrices"

    def matrices_metric_params(kwargs={}):
        params = []
        metric = "MatricesMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return matrices_metric_params()


def hypersphere_params(n_samples):
    manifold = "Hypersphere"
    manifold_args = [(3,), (5,)]
    module = "geomstats.geometry.hypersphere"

    def hypersphere_metric_params(kwargs={}):
        params = []
        metric = "HypersphereMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return hypersphere_metric_params()


def grassmanian_params(n_samples):
    manifold = "Grassmannian"
    manifold_args = [(4, 3), (5, 4)]
    module = "geomstats.geometry.grassmannian"

    def grassmannian_canonical_metric_params(kwargs={}):
        params = []
        metric = "GrassmannianCanonicalMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return grassmannian_canonical_metric_params()


def full_rank_correlation_matrices_params(n_samples):
    manifold = "FullRankCorrelationMatrices"
    manifold_args = [(3,), (5,)]
    module = "geomstats.geometry.full_rank_correlation_matrices"

    def full_rank_correlation_matrices_metric_params(kwargs={}):
        params = []
        metric = "FullRankCorrelationAffineQuotientMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return full_rank_correlation_matrices_metric_params()


def hyperboloid_params(n_samples):
    manifold = "Hyperboloid"
    manifold_args = [(3,), (5,)]
    module = "geomstats.geometry.hyperboloid"

    def hyperboloid_metric_params(kwargs={}):
        params = []
        metric = "HyperboloidMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return hyperboloid_metric_params()


def poincare_ball_params(n_samples):
    manifold = "PoincareBall"
    manifold_args = [(3,), (5,)]
    module = "geomstats.geometry.poincare_ball"

    def poincare_ball_metric_params(kwargs={}):
        params = []
        metric = "PoincareBallMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return poincare_ball_metric_params()


def poincare_half_space_params(n_samples):
    manifold = "PoincareHalfSpace"
    manifold_args = [(3,), (5,)]
    module = "geomstats.geometry.poincare_half_space"

    def poincare_half_space_metric_params(kwargs={}):
        params = []
        metric = "PoincareHalfSpaceMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return poincare_half_space_metric_params()


def poincare_polydisk_params(n_samples):
    manifold = "PoincarePolydisk"
    manifold_args = [(3,), (5,)]
    kwargs = {}
    module = "geomstats.geometry.poincare_polydisk"

    def poincare_poly_disk_metric_params(kwargs={}):
        params = []
        metric = "PoincarePolydiskMetric"
        metric_args = manifold_args
        common = (manifold, module, metric, n_samples, kwargs)
        for i in range(len(manifold_args)):
            params += [common + (manifold_args[i], metric_args[i])]
        return params

    return poincare_poly_disk_metric_params()


manifolds = [
    "spd_manifold",
    "stiefel",
    "pre_shape",
    "positive_lower_triangular_matrices",
    "minkowski",
    "matrices",
    "hypersphere",
    "grassmanian",
    "hyperboloid",
    "poincare_ball",
    "poincare_half_space",
]


def generate_benchmark_exp_params(manifold="all", n_samples=10):
    params_list = []
    manifolds_list = manifolds if manifold == "all" else [manifold]
    params_list = [
        globals()[manifold + "_params"](n_samples) for manifold in manifolds_list
    ]
    params_list = list(chain(*params_list))
    df = pd.DataFrame(
        params_list,
        columns=[
            "manifold",
            "module",
            "metric",
            "n_samples",
            "exp_kwargs",
            "manifold_args",
            "metric_args",
        ],
    )
    df.to_pickle("benchmark_params.pkl")
    print("Generated params at benchmark_params.pkl.")


def main():
    generate_benchmark_exp_params(args.manifold, args.n_samples)


if __name__ == "__main__":
    main()