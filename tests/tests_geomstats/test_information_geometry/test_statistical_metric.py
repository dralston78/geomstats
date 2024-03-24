

import geomstats.backend as gs
from geomstats.geometry.euclidean import Euclidean
from geomstats.information_geometry.statistical_metric import StatisticalMetric
from geomstats.information_geometry.statistical_metric import DivergenceConnection, DualDivergenceConnection
from geomstats.information_geometry.statistical_metric import AlphaConnection
from geomstats.test.test_case import autograd_only
from geomstats.test_cases.geometry.riemannian_metric import RiemannianMetricTestCase


@autograd_only
# @pytest.mark.slow
class TestStatisticalMetric(RiemannianMetricTestCase):
    """
    Test StatisticalMetric class by verifying expected induced metric, connection,
    and dual connection properties in the case of Bregman divergence.

    Using properties from Nielson's An Elementary Introduction to
    Information Geometry, Section 3.7 on page 14 (https://arxiv.org/abs/1808.08271)
    """

    def setup_method(self):
        def bregman_divergence(func):
            def _bregman_divergence(point, base_point):
                grad_func = gs.autodiff.value_and_grad(func)
                func_basepoint, grad_func_basepoint = grad_func(base_point)
                bregman_div = (
                    func(point)
                    - func_basepoint
                    - gs.dot(point - base_point, grad_func_basepoint)
                )
                return bregman_div

            return _bregman_divergence

        def potential_function(point):
            return gs.sum(point**4)

        self.potential_function = potential_function
        self.breg_divergence = bregman_divergence(self.potential_function)
        self.euclidean_space = Euclidean(dim=2, equip=False)
        self.primal_connection = DivergenceConnection(
            space=self.euclidean_space, divergence=self.breg_divergence
        )
        self.dual_connection = DualDivergenceConnection(
            space=self.euclidean_space, divergence=self.breg_divergence
        )
        self.alpha_connection = AlphaConnection(
            space=self.euclidean_space,
            alpha=0.0,
            primal_connection=self.primal_connection,
            dual_connection=self.dual_connection,
        )
        self.stat_metric = StatisticalMetric(
            space=self.euclidean_space,
            divergence=self.breg_divergence,
            primal_connection=self.primal_connection,
            dual_connection=self.dual_connection,
        )

        self.euclidean_space.metric = self.stat_metric

        self.base_point = gs.random.uniform(low=-10, high=10, size=(2,))

    def test_metric_matrix(
        self,
    ):
        """Test equation (58) on page 15"""
        potential_hessian = gs.autodiff.hessian(self.potential_function)
        potential_hessian_base_point = potential_hessian(self.base_point)
        metric_matrix_base_point = self.stat_metric.metric_matrix(self.base_point)
        self.assertAllClose(metric_matrix_base_point, potential_hessian_base_point)

    def test_divergence_christoffels(
        self,
    ):
        """Test equation (59) on page 15"""
        divergence_christoffels_base_point = self.primal_connection.christoffels(
            self.base_point
        )
        self.assertAllClose(
            divergence_christoffels_base_point,
            gs.zeros(divergence_christoffels_base_point.shape),
        )

    def test_dual_divergence_christoffels(
        self,
    ):
        pass

    def test_alpha_christoffels(
            self,
    ):
        """Test that LC connection is recovered"""
        alpha_christoffels_base_point = self.alpha_connection.christoffels(
            self.base_point
        )
        metric_base_point = self.euclidean_space.metric.metric_matrix(self.base_point)

        first_kind_alpha_christoffels_base_point = gs.einsum(
            '...kij,...km->...mij', alpha_christoffels_base_point, metric_base_point
        )

        levi_civita_christoffels_base_point = self.euclidean_space.metric.christoffels(
            self.base_point
        )

        firsk_kind_levi_civita_christoffels_base_point = gs.einsum(
            '...kij,...km->...mij', levi_civita_christoffels_base_point, metric_base_point
        )

        self.assertAllClose(
            first_kind_alpha_christoffels_base_point,
            firsk_kind_levi_civita_christoffels_base_point,
        )

    def test_amari_divergence_tensor(
        self,
    ):
        """Test equation (60) on page 15"""
        potential_func_first = gs.autodiff.jacobian(self.potential_function)
        potential_func_second = gs.autodiff.jacobian(potential_func_first)
        potential_func_third = gs.autodiff.jacobian(potential_func_second)
        potential_func_third_base_point = potential_func_third(self.base_point)
        amari_divergence_tensor_base_point = self.stat_metric.amari_divergence_tensor(
            self.base_point
        )

        self.assertAllClose(
            amari_divergence_tensor_base_point, potential_func_third_base_point
        )