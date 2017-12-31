from __future__ import print_function, absolute_import

import pytest
from scipy.cluster import hierarchy

from idpflex import cnextend as cnx


class TestClusterNodeX(object):

    def test_property(self):
        n = cnx.ClusterNodeX(0)
        n._properties['prop'] = True
        assert n['prop'] is True

    def test_leafs(self, benchmark):
        t = benchmark['tree']
        cluster = t[benchmark['nleafs']]  # fist cluster that is not a leaf
        assert [n.id for n in cluster.leafs] == [19167, 19168]
        cluster = t.root
        assert cluster.leafs == t.leafs


class TestTree(object):

    def test_from_linkage_matrix(self, benchmark):
        t = cnx.Tree()
        t.from_linkage_matrix(benchmark['z'], node_class=hierarchy.ClusterNode)
        r = t.root
        assert hasattr(r, 'parent') is False
        t.from_linkage_matrix(benchmark['z'], node_class=cnx.ClusterNodeX)
        r = t.root
        assert r.parent is None
        assert len(t) == benchmark['nnodes']

    def test_leafs(self, benchmark):
        t = benchmark['tree']
        assert len(t.leafs) == benchmark['nleafs']

    def test_iter(self, benchmark):
        t = benchmark['tree']
        ids = sorted(range(benchmark['nnodes']), reverse=True)
        assert ids == list(node.id for node in t)

    def test_getitem(self, benchmark):
        t = benchmark['tree']
        assert t[-1] is t.root
        assert list(n.id for n in t[:3]) == list(range(3))

    def test_clusters_above_depth(self, benchmark):
        t = benchmark['tree']
        ids = [n.id for n in t.nodes_above_depth(depth=3)]
        assert ids == [44732, 44748, 44752, 44753, 44754, 44755, 44756]

    def test_clusters_at_depth(self, benchmark):
        t = benchmark['tree']
        ids = [n.id for n in t.nodes_at_depth(depth=3)]
        assert ids == [44732, 44748, 44752, 44753]


if __name__ == '__main__':
    pytest.main()
