"""
Unit tests for tensorflow backend.
"""

import importlib
import os
import tensorflow as tf

import geomstats.backend as gs


class TestHypersphereOnTensorFlow(tf.test.TestCase):
    _multiprocess_can_split_ = True

    @classmethod
    def setUpClass(cls):
        tf.enable_eager_execution()
        os.environ['GEOMSTATS_BACKEND'] = 'tensorflow'
        importlib.reload(gs)

    @classmethod
    def tearDownClass(cls):
        os.environ['GEOMSTATS_BACKEND'] = 'numpy'
        importlib.reload(gs)

    def test_vstack(self):
        with self.test_session():
            tensor_1 = gs.array([[1., 2., 3.], [4., 5., 6.]])
            tensor_2 = gs.array([[7., 8., 9.]])

            result = gs.vstack([tensor_1, tensor_2])
            expected = gs.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
            self.assertAllClose(gs.eval(result), gs.eval(expected))


if __name__ == '__main__':
    tf.test.main()
