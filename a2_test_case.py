import inspect
import unittest
from society_hierarchy import *
import ast


class A2TestUtil(unittest.TestCase):
    def assertRecursion(self, fun):
        fun_name = fun.__name__
        ast_ = ast.parse('class T:\n' + inspect.getsource(fun))
        q = [ast_]
        acc = []
        while q:
            node = q.pop()
            acc.append(node)
            if isinstance(node, ast.Module):
                for x in node.body:
                    q.append(x)
            elif isinstance(node, ast.ClassDef):
                for x in node.body:
                    q.append(x)
            elif isinstance(node, ast.FunctionDef):
                for x in node.body:
                    q.append(x)
            elif isinstance(node, ast.If):
                q.append(node.test)
                for x in node.body:
                    q.append(x)
                for x in node.orelse:
                    q.append(x)
            elif isinstance(node, ast.Return):
                q.append(node.value)
            elif isinstance(node, ast.For):
                if isinstance(node.target, ast.Name):
                    q.append(node.target)
                elif isinstance(node.target, tuple) or isinstance(node.target,
                                                                  list):
                    for x in node.target:
                        q.append(x)
                for x in node.body:
                    q.append(x)
                for x in node.orelse:
                    q.append(x)
            elif isinstance(node, ast.Assign):
                for x in node.targets:
                    q.append(x)
                q.append(node.value)
            elif isinstance(node, ast.Expr):
                q.append(node.value)
            elif isinstance(node, ast.Call):
                q.append(node.func)
                for x in node.args:
                    q.append(x)
        calls = list(filter(lambda x: isinstance(x, ast.Call), acc))
        valid_calls = list(filter(lambda x: isinstance(x.func,
                                                       ast.Name) and x.func.id == fun.__name__ or isinstance(
            x.func, ast.Attribute) and x.func.attr == fun.__name__, calls))
        self.assertTrue(valid_calls != [],
                        f'The function {fun_name} must be recursive')

    def assertCitizen(self, obj: Citizen, exp):
        err_msg = lambda exp, act, attr: f'Exp {attr}: {exp} Act {attr}: {attr}'
        for k, v in exp.items():
            act = getattr(obj, k)
            if not (isinstance(act, int) or isinstance(act, str)):
                act = act()
            self.assertEqual(v, act, err_msg(v, act, k))

    def assertNoPublicMethod(self, obj, method):
        methods = obj.__class__.__dict__.keys()
        public_method = list(filter(lambda x: x[0] != '_', methods))
        self.assertListEqual(sorted(public_method),
                             sorted(method),
                             f'You should not add new public methods for {str(obj.__class__)}')

    def assertNoPublicAttr(self, obj, attr):
        attrs = obj.__dict__.keys()
        public_attr = list(filter(lambda x: x[0] != '_', attrs))
        self.assertListEqual(sorted(public_attr),
                             sorted(attr),
                             f'You should not add new public attribute for {str(obj.__class__)}')


class TestNoPublic(A2TestUtil):
    def setUp(self) -> None:
        self.c1 = Citizen(1, "A", 2020, "PositionA", 10)
        self.society = Society()
        self.leader = DistrictLeader(1, "A", 2020, "PositionA", 10, 'sample')

    def test_no_public_attr_citizen(self):
        self.assertNoPublicAttr(self.c1, ['cid', 'job', 'manufacturer', 'model_year', 'rating'])

    def test_no_public_method_citizen(self):
        self.assertNoPublicMethod(self.c1, ['add_subordinate',
                                            'become_subordinate_to',
                                            'get_all_subordinates',
                                            'get_citizen',
                                            'get_closest_common_superior',
                                            'get_direct_subordinates',
                                            'get_district_name',
                                            'get_highest_rated_subordinate',
                                            'get_society_head',
                                            'get_superior',
                                            'remove_subordinate',
                                            'rename_district',
                                            'set_superior'])

    def test_no_public_attr_leader(self):
        self.assertNoPublicAttr(self.leader, ['cid', 'job', 'manufacturer', 'model_year', 'rating'])

    def test_no_public_method_leader(self):
        self.assertNoPublicMethod(self.leader, ['get_district_citizens', 'get_district_name', 'rename_district'])

    def test_no_public_attr_society(self):
        self.assertNoPublicAttr(self.society, [])

    def test_no_public_method_society(self):
        self.assertNoPublicMethod(self.society, ['add_citizen',
                                                 'change_citizen_type',
                                                 'delete_citizen',
                                                 'get_all_citizens',
                                                 'get_citizen',
                                                 'get_citizens_with_job',
                                                 'get_head',
                                                 'promote_citizen',
                                                 'set_head'])
class TestTask1(A2TestUtil):
    def setUp(self) -> None:
        self.c1 = Citizen(1, "A", 2020, "PositionA", 10)
        self.c2 = Citizen(2, "B", 2020, "PositionB", 20)
        self.c3 = Citizen(3, "C", 2020, "PositionC", 30)
        self.c4 = Citizen(4, "D", 2020, "PositionD", 40)
        self.c5 = Citizen(5, "E", 2020, "PositionE", 50)
        self.nodes = [self.c1, self.c2, self.c3, self.c4, self.c5]
        self.society = Society()

    def tearDown(self) -> None:
        self.c1 = Citizen(1, "A", 2020, "PositionA", 10)
        self.c2 = Citizen(2, "B", 2020, "PositionB", 20)
        self.c3 = Citizen(3, "C", 2020, "PositionC", 30)
        self.c4 = Citizen(4, "D", 2020, "PositionD", 40)
        self.c5 = Citizen(5, "E", 2020, "PositionE", 50)
        self.nodes = [self.c1, self.c2, self.c3, self.c4, self.c5]
        self.society = Society()

    def formLine(self):
        for i in range(len(self.nodes) - 1):
            self.nodes[i].add_subordinate(self.nodes[i + 1])

    def formTree(self):
        self.c4.add_subordinate(self.c5)
        self.c4.add_subordinate(self.c2)
        self.c2.add_subordinate(self.c3)
        self.c2.add_subordinate(self.c1)


class TestTask11(TestTask1):
    def test_add_subordinate_1(self):
        """
        Test add a single subordinate
        """
        self.c2.add_subordinate(self.c1)
        self.assertTrue(self.c1.get_superior() is self.c2)
        self.assertTrue(len(self.c2.get_direct_subordinates()) == 1 and
                        self.c2.get_direct_subordinates()[0] is self.c1)

    def test_add_subordinate_2(self):
        """
        Test add two subordinates.  The order should still be ascending
        """
        self.c2.add_subordinate(self.c3)
        self.c2.add_subordinate(self.c1)
        self.assertTrue(self.c1.get_superior() is self.c2)
        self.assertTrue(self.c3.get_superior() is self.c2)
        self.assertTrue(len(self.c2.get_direct_subordinates()) == 2 and
                        self.c2.get_direct_subordinates()[0] is self.c1 and
                        self.c2.get_direct_subordinates()[1] is self.c3)

    def test_add_subordinate_3(self):
        """
        Test add different levels.  Check proper superior and order
            4
         2   5
        1 3
        """
        self.formTree()
        self.assertTrue(self.c1.get_superior() is self.c2)
        self.assertTrue(self.c3.get_superior() is self.c2)
        self.assertTrue(self.c2.get_superior() is self.c4)
        self.assertTrue(self.c5.get_superior() is self.c4)
        self.assertTrue(len(self.c4.get_direct_subordinates()) == 2)
        self.assertListEqual([2, 5],
                             [i.cid for i in self.c4.get_direct_subordinates()])
        self.assertListEqual([1, 3],
                             [i.cid for i in self.c2.get_direct_subordinates()])

    def test_remove_subordinate_1(self):
        """Remove direct subordinate from node"""
        self.c2.add_subordinate(self.c5)
        self.c2.add_subordinate(self.c1)
        self.c2.add_subordinate(self.c3)
        self.c2.add_subordinate(self.c4)
        self.c2.remove_subordinate(self.c1.cid)
        self.assertTrue(len(self.c2.get_direct_subordinates()) == 3)
        self.assertTrue(self.c1 not in self.c2.get_direct_subordinates())
        self.assertTrue(self.c1.get_superior() is None)

    def test_become_subordinate_1(self):
        """Superior is None"""
        self.c1.become_subordinate_to(None)
        self.assertIsNone(self.c1.get_superior())

    def test_become_subordinate_2(self):
        """
        Superior is not None.  No previous superior
        """
        self.c2.become_subordinate_to(self.c1)
        self.assertIsNotNone(self.c2.get_superior())
        self.assertEqual(self.c1, self.c2.get_superior())
        self.assertListEqual([self.c2], self.c1.get_direct_subordinates())

    def test_become_subordinate_3(self):
        """
        Remove from previous superior
        """
        self.c3.become_subordinate_to(self.c2)
        self.c2.become_subordinate_to(self.c1)
        self.c3.become_subordinate_to(self.c1)
        self.assertEqual(self.c1, self.c3.get_superior())
        self.assertListEqual([self.c2, self.c3],
                             self.c1.get_direct_subordinates())
        self.assertEqual([], self.c2.get_direct_subordinates())

    def test_get_citizen_0(self):
        self.assertRecursion(Citizen.get_citizen)

    def test_get_citizen_1(self):
        """
        Find node itself
        """
        nodes = self.nodes[:]
        acc = [node.get_citizen(node.cid) for node in nodes]
        self.assertListEqual(nodes, acc)

    def test_get_citizen_2(self):
        """
        Direct child
        """
        self.formLine()
        nodes = self.nodes[:]
        acc = [node.get_citizen(node.cid + 1) for node in nodes]
        self.assertListEqual(nodes[1:] + [None], acc)

    def test_get_citizen_3(self):
        """
        Indirect child
        """
        self.formTree()
        acc = [self.c4.get_citizen(i) for i in range(1, 6)]
        self.assertListEqual([self.c1, self.c2, self.c3, self.c4, self.c5], acc)


class TestTask12(TestTask1):
    def test_get_all_subordinates_0(self):
        self.assertRecursion(Citizen.get_all_subordinates)

    def test_get_all_subordinate_1(self):
        """
        Leaf
        """
        nodes = self.nodes[:]
        self.assertTrue(all([x.get_all_subordinates() == [] for x in nodes]))

    def test_get_all_subordinate_2(self):
        """
        Straight line
        """
        self.formLine()
        nodes = self.nodes[:]
        for i in range(len(nodes)):
            node = nodes[i]
            self.assertEqual(nodes[i + 1:], node.get_all_subordinates())

    def test_get_all_subordinate_3(self):
        """
        Left Tree
         c4
         c2
        c1 c3
        """
        self.c4.add_subordinate(self.c2)
        self.c2.add_subordinate(self.c3)
        self.c2.add_subordinate(self.c1)
        self.assertEqual([self.c1, self.c3], self.c2.get_all_subordinates())
        self.assertEqual([self.c1, self.c2, self.c3],
                         self.c4.get_all_subordinates())

    def test_get_all_subordinate_4(self):
        """
        Two side tree
             c4
          c2   c5
        c1 c3
        """
        self.formTree()
        self.assertEqual([self.c1, self.c2, self.c3, self.c5],
                         self.c4.get_all_subordinates())

    def test_get_society_head_0(self):
        self.assertRecursion(Citizen.get_society_head)

    def test_get_society_head_1(self):
        """
        Single node always return itself
        """
        nodes = self.nodes[:]
        acc = [nodes[i].get_society_head() for i in range(len(nodes))]
        self.assertEqual(nodes, acc)

    def test_get_society_head_2(self):
        """
        Straight line
        """
        nodes = self.nodes[:]
        self.formLine()
        for node in nodes:
            self.assertEqual(self.c1, node.get_society_head())

    def test_get_society_head_3(self):
        """
        Tree
        """
        nodes = self.nodes[:]
        self.formTree()
        self.assertTrue(
            all([node.get_society_head() == self.c4 for node in nodes]))

    def test_get_closest_common_superior_0(self):
        self.assertRecursion(Citizen.get_closest_common_superior)

    def test_get_closest_common_superior_1(self):
        nodes = self.nodes[:]
        self.assertTrue(
            all([node.get_closest_common_superior(node.cid) == node for node in
                 nodes]))

    def test_get_closest_common_superior_2(self):
        nodes = self.nodes[:]
        self.formLine()
        for source in nodes:
            for sink in nodes:
                self.assertTrue(source.get_closest_common_superior(
                    sink.cid) == source if source.cid <= sink.cid else sink)

    def test_get_closest_common_superior_3(self):
        self.formTree()
        # bottom level
        bottom = [self.c1, self.c3]
        for source in bottom:
            for sink in bottom:
                self.assertTrue(
                    source.get_closest_common_superior(
                        sink.cid) == self.c2 if source != sink else source)
        # Internal level
        middle = [self.c2, self.c5]
        for source in middle:
            for sink in middle:
                self.assertTrue(
                    source.get_closest_common_superior(
                        sink.cid) == self.c4 if source != sink else source)
        # Cross branch
        for node in bottom:
            self.assertTrue(
                node.get_closest_common_superior(self.c5.cid) == self.c4)


class TestTask13(TestTask1):
    def setUp(self) -> None:
        super().setUp()
        self.society = Society()

    def tearDown(self) -> None:
        super().tearDown()
        self.society = Society()

    def test_get_citizen_1(self):
        nodes = self.nodes[:]
        for node in nodes:
            self.assertIsNone(self.society.get_citizen(node.cid))
        for i in range(len(nodes)):
            self.society.set_head(nodes[i])
            for j in range(len(nodes)):
                if i != j:
                    self.assertIsNone(self.society.get_citizen(nodes[j].cid))
                else:
                    self.assertEqual(self.society.get_head(),
                                     self.society.get_citizen(
                                         self.society.get_head().cid))

    def test_get_citizen_2(self):
        self.formLine()
        self.society.set_head(self.c1)
        nodes = self.nodes[:]
        for i in range(len(nodes)):
            self.assertEqual(nodes[i], self.society.get_citizen(nodes[i].cid))

    def test_get_citizen_3(self):
        self.formTree()
        self.society.set_head(self.c4)
        nodes = self.nodes[:]
        for i in range(len(nodes)):
            self.assertEqual(nodes[i], self.society.get_citizen(nodes[i].cid))

    def test_get_all_citizens_1(self):
        nodes = self.nodes[:]
        for _ in nodes:
            self.assertListEqual([], self.society.get_all_citizens())

    def test_get_all_citizens_2(self):
        self.formLine()
        self.society.set_head(self.c1)
        self.assertListEqual(self.nodes[:], self.society.get_all_citizens())

    def test_get_all_citizens_3(self):
        self.formTree()
        self.society.set_head(self.c4)
        self.assertListEqual(self.nodes[:], self.society.get_all_citizens())

    def test_add_citizen_1(self):
        self.society.add_citizen(self.c1)
        self.assertEqual(self.c1,
                         self.society.get_head())
        self.assertEqual(self.society.get_head(),
                         self.society.get_citizen(self.c1.cid))

    def test_add_citizen_2(self):
        self.society.add_citizen(self.c1)
        self.society.add_citizen(self.c2)
        self.assertEqual(self.c2,
                         self.society.get_head())
        self.assertEqual(self.c1,
                         self.society.get_citizen(self.c1.cid))
        self.assertEqual(self.c1,
                         self.society.get_citizen(self.c1.cid))

    def test_add_citizen_3(self):
        self.society.add_citizen(self.c1)
        self.society.add_citizen(self.c2, self.c1.cid)
        self.assertEqual(self.c1, self.society.get_head())
        self.assertTrue(self.c2 in self.c1.get_direct_subordinates())

    def test_get_citizens_with_job_0(self):
        job = ''
        nodes = self.nodes[:]
        for node in nodes:
            self.society.set_head(node)
            self.assertListEqual([], self.society.get_citizens_with_job(job))
            self.assertEqual([node],
                             self.society.get_citizens_with_job(node.job))

    def test_get_citizen_with_job_1(self):
        job = 'job'
        for i in range(1, len(self.nodes)):
            self.nodes[i].job = job
        self.formLine()
        self.society.set_head(self.c1)
        self.assertListEqual(self.nodes[1:],
                             self.society.get_citizens_with_job(job))
        self.society.get_head().job = job
        self.assertListEqual(self.nodes[:],
                             self.society.get_citizens_with_job(job))

    def test_get_citizen_with_job_2(self):
        j1, j2 = 'Even', 'Odd'
        for i in range(len(self.nodes)):
            self.nodes[i].job = j1 if i % 2 == 0 else j2
        self.formTree()
        self.society.set_head(self.c4)
        self.assertListEqual(
            [self.nodes[i] for i in range(0, len(self.nodes), 2)],
            self.society.get_citizens_with_job(j1))
        self.assertListEqual(
            [self.nodes[i] for i in range(1, len(self.nodes), 2)],
            self.society.get_citizens_with_job(j2))


class TestTask2(A2TestUtil):
    def setUp(self) -> None:
        self.c1 = Citizen(1, "A", 2020, "PositionA", 10)
        self.c2 = Citizen(2, "B", 2020, "PositionB", 20)
        self.c3 = Citizen(3, "C", 2020, "PositionC", 30)
        self.c4 = Citizen(4, "D", 2020, "PositionD", 40)
        self.c5 = Citizen(5, "E", 2020, "PositionE", 50)
        self.district = DistrictLeader(0, 'x', 2020, 'sample', 100, 'sample')
        self.nodes = [self.c1, self.c2, self.c3, self.c4, self.c5]
        self.society = Society()

    def tearDown(self) -> None:
        self.c1 = Citizen(1, "A", 2020, "PositionA", 10)
        self.c2 = Citizen(2, "B", 2020, "PositionB", 20)
        self.c3 = Citizen(3, "C", 2020, "PositionC", 30)
        self.c4 = Citizen(4, "D", 2020, "PositionD", 40)
        self.c5 = Citizen(5, "E", 2020, "PositionE", 50)
        self.district = DistrictLeader(0, 'x', 2020, 'sample', 100, 'sample')
        self.nodes = [self.c1, self.c2, self.c3, self.c4, self.c5]
        self.society = Society()

    def formLine(self):
        for i in range(len(self.nodes) - 1):
            self.nodes[i].add_subordinate(self.nodes[i + 1])

    def formTree(self):
        self.c4.add_subordinate(self.c5)
        self.c4.add_subordinate(self.c2)
        self.c2.add_subordinate(self.c3)
        self.c2.add_subordinate(self.c1)


class TestTask21(TestTask2):
    def test_init(self):
        sample = DistrictLeader(0, 'x', 2020, 'PositionF', 60, 'sample')
        self.assertEqual(0, sample.cid)
        self.assertEqual('x', sample.manufacturer)
        self.assertEqual(2020, sample.model_year)
        self.assertEqual('PositionF', sample.job)
        self.assertEqual(60, sample.rating)

    def test_get_district_citizens_0(self):
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            self.nodes[i] = DistrictLeader(node.cid, node.manufacturer,
                                           node.model_year, node.job,
                                           node.rating, str(i))
            self.assertEqual([self.nodes[i]],
                             self.nodes[i].get_district_citizens())

    def test_get_district_citizens_1(self):
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            self.nodes[i] = DistrictLeader(node.cid, node.manufacturer,
                                           node.model_year, node.job,
                                           node.rating, str(i))
        self.formLine()
        for i in range(len(self.nodes)):
            self.assertListEqual(self.nodes[i:],
                                 self.nodes[i].get_district_citizens())
        self.nodes[0].become_subordinate_to(self.district)
        self.assertEqual([self.district] + self.nodes[:],
                         self.district.get_district_citizens())

    def test_get_district_citizens_2(self):
        self.formTree()
        for node in self.nodes:
            if node.get_superior() is None:
                node.become_subordinate_to(self.district)
        self.assertEqual([self.district] + self.nodes,
                         self.district.get_district_citizens())


class TestTask22(TestTask2):
    def test_get_district_name_0(self):
        self.assertRecursion(Citizen.get_district_name)

    def test_get_district_name_1(self):
        self.assertEqual('sample', self.district.get_district_name())

    def test_get_district_name_2(self):
        self.formLine()
        for node in self.nodes:
            self.assertEqual('', node.get_district_name())

    def test_get_district_name_3(self):
        self.formLine()
        self.nodes[0].become_subordinate_to(self.district)
        for node in self.nodes:
            self.assertEqual('sample', node.get_district_name())

    def test_get_district_name_4(self):
        self.formTree()
        for node in self.nodes:
            if node.get_superior() is None:
                node.become_subordinate_to(self.district)
        for node in self.nodes:
            self.assertEqual('sample', node.get_district_name())

    def test_get_district_name_5(self):
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            if i % 2 == 0:
                self.nodes[i] = DistrictLeader(node.cid, node.manufacturer,
                                               node.model_year, node.job,
                                               node.rating, str(i))
        self.formLine()
        self.assertEqual('0', self.nodes[0].get_district_name())
        for i in range(1, len(self.nodes)):
            if i % 2 == 0:
                self.assertEqual(str(i), self.nodes[i].get_district_name())
            else:
                self.assertEqual(str(i - 1), self.nodes[i].get_district_name())

    def test_rename_district_0(self):
        self.assertRecursion(Citizen.rename_district)

    def test_rename_district_1(self):
        self.district.rename_district('rename')
        self.assertEqual('rename', self.district.get_district_name())

    def test_rename_district_2(self):
        self.formLine()
        for node in self.nodes:
            node.rename_district('rename')
        for node in self.nodes:
            self.assertEqual('', node.get_district_name())

    def test_rename_district_3(self):
        self.formLine()
        self.nodes[0].become_subordinate_to(self.district)
        for node in self.nodes:
            node.rename_district(node.job)
            for n1 in self.nodes:
                self.assertEqual(node.job, n1.get_district_name())
        self.assertEqual(self.nodes[-1].job, self.district.get_district_name())

    def test_rename_district_4(self):
        self.formTree()
        for node in self.nodes:
            if node.get_superior() is None:
                node.become_subordinate_to(self.district)
        self.district.rename_district('rename')
        for node in self.nodes:
            self.assertTrue('rename', node.get_district_name())

    def test_rename_district_5(self):
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            if i % 2 == 0:
                self.nodes[i] = DistrictLeader(node.cid, node.manufacturer,
                                               node.model_year, node.job,
                                               node.rating, str(i))
        self.formLine()
        for i in range(len(self.nodes)):
            if i % 2 == 0:
                self.nodes[i].rename_district(str(i + 1))
        for i in range(len(self.nodes)):
            if i % 2 == 0:
                self.assertEqual(str(i + 1), self.nodes[i].get_district_name())
            else:
                self.assertEqual(str(i), self.nodes[i].get_district_name())

    def test_rename_district_6(self):
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            if i % 2 == 0:
                self.nodes[i] = DistrictLeader(node.cid, node.manufacturer,
                                               node.model_year, node.job,
                                               node.rating, str(i))
        self.formLine()
        for i in range(len(self.nodes)):
            if i % 2 == 1:
                self.nodes[i].rename_district(str(i))
        for i in range(len(self.nodes)):
            if i % 2 == 0 and self.nodes[i].get_direct_subordinates() != []:
                self.assertEqual(str(i + 1), self.nodes[i].get_district_name())
            elif i % 2 == 0 and not self.nodes[i].get_direct_subordinates():
                self.assertEqual(str(i), self.nodes[i].get_district_name())
            else:
                self.assertEqual(str(i), self.nodes[i].get_district_name())


class TestTask23(TestTask2):
    def test_change_type_1(self):
        self.society.add_citizen(self.district)
        x = self.society.change_citizen_type(self.district.cid)
        self.assertTrue(isinstance(x, Citizen))
        self.assertTrue(len(self.society.get_all_citizens()) == 1)
        self.assertTrue(x in self.society.get_all_citizens())
        self.assertCitizen(x, {'cid': self.district.cid,
                               'job': self.district.job,
                               'rating': self.district.rating,
                               'model_year': self.district.model_year,
                               'get_superior': self.district.get_superior(),
                               'get_all_subordinates': self.district.get_all_subordinates()})

    def test_change_type_2(self):
        district = 'sample'
        self.society.add_citizen(self.c1)
        x = self.society.change_citizen_type(self.nodes[0].cid, district)
        self.assertIsInstance(x, DistrictLeader)
        self.assertTrue(len(self.society.get_all_citizens()) == 1)
        self.assertTrue(x in self.society.get_all_citizens())
        self.assertCitizen(x, {'cid': self.nodes[0].cid,
                               'job': self.nodes[0].job,
                               'rating': self.nodes[0].rating,
                               'model_year': self.nodes[0].model_year,
                               'get_superior': self.nodes[0].get_superior(),
                               'get_all_subordinates': self.nodes[
                                   0].get_all_subordinates(),
                               'get_district_name': district})

    def test_change_type_3(self):
        self.formLine()
        self.society.add_citizen(self.nodes[0])
        prev = None
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            x = self.society.change_citizen_type(node.cid, str(i))
            self.assertIsInstance(x, DistrictLeader)
            self.assertTrue(x in self.society.get_all_citizens())
            self.assertTrue(all([self.society.get_all_citizens()[
                                     j].get_district_name() == str(i) for j in
                                 range(i, len(self.nodes))]))
            self.assertTrue(all([isinstance(temp, DistrictLeader) for temp in
                                 self.society.get_all_citizens()[:i + 1]]))
            self.assertCitizen(x, {'cid': node.cid,
                                   'job': node.job,
                                   'rating': node.rating,
                                   'model_year': node.model_year,
                                   'get_superior': prev,
                                   'get_all_subordinates': self.nodes[i + 1:],
                                   'get_district_name': str(i)})
            if i > 0:
                self.assertTrue(x in prev.get_direct_subordinates())
            if i + 1 < len(self.nodes):
                self.assertEqual(x, self.nodes[i + 1].get_superior())
            prev = x

    def test_change_type_4(self):
        district = 'sample'
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            self.nodes[i] = DistrictLeader(node.cid, node.manufacturer,
                                           node.model_year, node.job,
                                           node.rating, str(i))
        self.formLine()
        self.society.add_citizen(self.nodes[0])
        prev = None
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            # The district should not be used in the call
            x = self.society.change_citizen_type(node.cid, district)
            self.assertIsInstance(x, Citizen)
            self.assertTrue(x in self.society.get_all_citizens())
            self.assertTrue(all([temp.get_district_name() == '' for temp in
                                 self.society.get_all_citizens()[:i + 1]]))
            self.assertTrue(all([isinstance(temp, Citizen) for temp in
                                 self.society.get_all_citizens()[:i + 1]]))
            self.assertCitizen(x, {'cid': node.cid,
                                   'job': node.job,
                                   'rating': node.rating,
                                   'model_year': node.model_year,
                                   'get_superior': prev,
                                   'get_all_subordinates': self.nodes[i + 1:],
                                   'get_district_name': ''})
            if i > 0:
                self.assertTrue(x in prev.get_direct_subordinates())
            if i + 1 < len(self.nodes):
                self.assertEqual(x, self.nodes[i + 1].get_superior())
            prev = x

    def test_change_type_5(self):
        self.c2.become_subordinate_to(self.c1)
        self.c3.become_subordinate_to(self.c1)
        self.c4.become_subordinate_to(self.c2)
        self.c5.become_subordinate_to(self.c2)
        self.society.set_head(self.c1)
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            node_i = self.society.change_citizen_type(node.cid, str(i))
            self.assertIsInstance(node_i, DistrictLeader)
            self.assertTrue(node_i in self.society.get_all_citizens())
            self.assertTrue(all([isinstance(temp, DistrictLeader) for temp in self.society.get_all_citizens()[:i]]))
            self.assertTrue(all([temp.get_district_name() == str(i) for temp in
                                 self.society.get_all_citizens()[2*i+1:2*i + 3]]))


class TestTask3(A2TestUtil):
    ...


class TestTask31(TestTask3):
    def setUp(self) -> None:
        self.district = DistrictLeader(1, "A", 2020, "PositionA", 10, "Company")
        self.c2 = Citizen(2, "B", 2020, "PositionB", 20)
        self.c3 = Citizen(3, "C", 2020, "PositionC", 30)
        self.c4 = Citizen(4, "D", 2020, "PositionD", 40)
        self.c5 = Citizen(5, "E", 2020, "PositionE", 50)
        self.society = Society()

    def tearDown(self) -> None:
        self.district = DistrictLeader(1, "A", 2020, "PositionA", 10, "Company")
        self.c2 = Citizen(2, "B", 2020, "PositionB", 20)
        self.c3 = Citizen(3, "C", 2020, "PositionC", 30)
        self.c4 = Citizen(4, "D", 2020, "PositionD", 40)
        self.c5 = Citizen(5, "E", 2020, "PositionE", 50)
        self.society = Society()

    def test_promote_1(self):
        """
        Before:
            c2(2, B, PositionB, 20, Company)
            |
            c1(1, A, PositionA, 10)
        After:
            c2(2, B, PositionB, 20, Company)
            |
            c1(1, A, PositionA, 10)
        """
        self.c2 = DistrictLeader(2, "B", 2020, "PositionB", 20, "Company")
        self.c1 = Citizen(1, "A", 2020, "PositionA", 10)
        self.c1.become_subordinate_to(self.c2)
        self.society.set_head(self.c2)
        self.society.promote_citizen(self.c1.cid)
        res = self.society.get_citizen(self.c1.cid)
        self.assertIsInstance(res, Citizen)
        node = self.c1
        self.assertCitizen(res, {'cid': node.cid,
                                 'job': node.job,
                                 'rating': node.rating,
                                 'model_year': node.model_year,
                                 'get_superior': self.c2,
                                 'get_all_subordinates': [],
                                 'get_district_name': 'Company'})
        self.assertTrue(self.society.get_head() is self.c2)

    def test_promote_2(self):
        """
        Before:
            c1(1, A, PositionA, 10)
            |
            c2(2, B, PositionB, 20)
        After:
            c2(2, B, PositionA, 20)
            |
            c1(1, A, PositionB, 10)
        """
        temp = Citizen(1, 'A', 2020, 'PositionA', 10)
        self.c2.become_subordinate_to(temp)
        self.society.set_head(temp)
        self.society.promote_citizen(self.c2.cid)
        head = self.society.get_head()
        self.assertIsInstance(head, Citizen)
        self.assertCitizen(head, {'cid': 2,
                                  'job': "PositionA",
                                  'rating': 20,
                                  'model_year': 2020,
                                  'get_superior': None,
                                  'get_district_name': ''})
        self.assertTrue(len(head.get_all_subordinates()) == 1)
        res = self.society.get_head().get_all_subordinates()[0]
        self.assertIsInstance(res, Citizen)
        self.assertCitizen(res, {'cid': 1,
                                 'job': "PositionB",
                                 'rating': 10,
                                 'model_year': 2020,
                                 'get_superior': self.society.get_head(),
                                 'get_district_name': ''})

    def test_promote_3(self):
        """
        Before:
            c1(1, A, PositionA, 10, "Company")
            |
            c2(2, B, PositionB, 20)
            |
            c3(3, C, PositionC, 30)
        After:
            c3(3, C, PositionA, 30, "Company")
            |
            c1(1, A, PositionB, 10)
            |
            c2(2, B, PositionC, 20)
        """
        self.c3.become_subordinate_to(self.c2)
        self.c2.become_subordinate_to(self.district)
        self.society.set_head(self.district)
        self.society.promote_citizen(self.c3.cid)
        head = self.society.get_head()
        self.assertIsInstance(head, DistrictLeader)
        self.assertCitizen(head, {'cid': 3,
                                  'job': "PositionA",
                                  'rating': 30,
                                  'model_year': 2020,
                                  'get_superior': None,
                                  'get_district_name': 'Company'})
        self.assertTrue(len(head.get_direct_subordinates()) == 1)
        first_child = head.get_direct_subordinates()[0]
        self.assertIsInstance(first_child, Citizen)
        self.assertCitizen(first_child, {'cid': 1,
                                         'job': "PositionB",
                                         'rating': 10,
                                         'model_year': 2020,
                                         'get_superior': head,
                                         'get_district_name': 'Company'})
        self.assertTrue(len(first_child.get_direct_subordinates()) == 1)
        second_child = first_child.get_direct_subordinates()[0]
        self.assertIsInstance(second_child, Citizen)
        self.assertCitizen(second_child, {'cid': 2,
                                          'job': "PositionC",
                                          'rating': 20,
                                          'model_year': 2020,
                                          'get_superior': first_child,
                                          'get_district_name': 'Company'})

    def test_promote_4(self):
        """
        Before:
            c1(1, A, PositionA, 40, "Company")
            |
            c2(2, B, PositionB, 20)
            |
            c3(3, C, PositionC, 30)
        After:
            c1(1, A, PositionA, 40, "Company")
            |
            c3(3, C, PositionB, 30)
            |
            c2(2, B, PositionC, 20)
        """
        self.district.rating = 40
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.c2)
        self.society.set_head(self.district)
        self.society.promote_citizen(self.c3.cid)
        head = self.society.get_head()
        self.assertIsInstance(head, DistrictLeader)
        self.assertCitizen(head, {'cid': 1,
                                  'job': "PositionA",
                                  'rating': 40,
                                  'model_year': 2020,
                                  'get_superior': None,
                                  'get_district_name': 'Company'})
        self.assertTrue(len(head.get_direct_subordinates()) == 1)
        first_child = head.get_direct_subordinates()[0]
        self.assertIsInstance(first_child, Citizen)
        self.assertCitizen(first_child, {'cid': 3,
                                         'job': "PositionB",
                                         'rating': 30,
                                         'model_year': 2020,
                                         'get_superior': head,
                                         'get_district_name': 'Company'})
        self.assertTrue(len(first_child.get_direct_subordinates()) == 1)
        second_child = first_child.get_direct_subordinates()[0]
        self.assertCitizen(second_child, {'cid': 2,
                                          'job': "PositionC",
                                          'rating': 20,
                                          'model_year': 2020,
                                          'get_superior': first_child,
                                          'get_district_name': 'Company'})

    def test_promote_5(self):
        """
        Before:
            c1(1, A, PositionA, 10, "Company")
            |
            c2(2, B, PositionB, 20, "Sub")
            |
            c3(3, C, PositionC, 30)
        After:
            c1(1, A, PositionA, 10, "Company")
            |
            c3(3, C, PositionB, 30, "Sub")
            |
            c2(2, B, PositionC, 20)
        """
        self.c2 = DistrictLeader(self.c2.cid, self.c2.manufacturer,
                                 self.c2.model_year, self.c2.job,
                                 self.c2.rating, "Sub")
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.c2)
        self.society.set_head(self.district)
        self.society.promote_citizen(self.c3.cid)
        head = self.society.get_head()
        self.assertIsInstance(head, DistrictLeader)
        self.assertCitizen(head, {'cid': 1,
                                  'job': "PositionA",
                                  'rating': 10,
                                  'model_year': 2020,
                                  'get_superior': None,
                                  'get_district_name': 'Company'})
        self.assertTrue(len(head.get_direct_subordinates()) == 1)
        first_child = head.get_direct_subordinates()[0]
        self.assertIsInstance(first_child, DistrictLeader)
        self.assertCitizen(first_child, {'cid': 3,
                                         'job': "PositionB",
                                         'rating': 30,
                                         'model_year': 2020,
                                         'get_superior': head,
                                         'get_district_name': 'Sub'})
        self.assertTrue(len(first_child.get_direct_subordinates()) == 1)
        second_child = first_child.get_direct_subordinates()[0]
        self.assertIsInstance(second_child, Citizen)
        self.assertCitizen(second_child, {'cid': 2,
                                          'job': "PositionC",
                                          'rating': 20,
                                          'model_year': 2020,
                                          'get_superior': first_child,
                                          'get_district_name': 'Sub'})

    def test_promote_6(self):
        """
        Before:
            e1(1, A, PositionA, 10, "Company")
            /   |
        e2(2, B, PositionB, 20)  e3(3, C, PositionC, 30)

        After:
        e2(2, B, PositionA, 20, "Company")
            /                   \
        e1(1, A, PositionB, 10)  e3(3, C, PositionC, 30)
        """
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.district)
        self.society.set_head(self.district)
        self.society.promote_citizen(2)
        head = self.society.get_head()
        self.assertIsInstance(head, DistrictLeader)
        self.assertCitizen(head, {'cid': 2,
                                  'job': "PositionA",
                                  'rating': 20,
                                  'model_year': 2020,
                                  'get_superior': None,
                                  'get_district_name': 'Company'})
        self.assertTrue(len(head.get_direct_subordinates()) == 2)
        first, second = head.get_direct_subordinates()
        self.assertTrue(all([isinstance(x, Citizen) for x in [first, second]]))
        self.assertCitizen(first, {'cid': 1,
                                   'job': "PositionB",
                                   'rating': 10,
                                   'model_year': 2020,
                                   'get_superior': head,
                                   'get_district_name': 'Company'})
        self.assertCitizen(second, {'cid': 3,
                                    'job': "PositionC",
                                    'rating': 30,
                                    'model_year': 2020,
                                    'get_superior': head,
                                    'get_district_name': 'Company'})

    def test_promote_7(self):
        """
        Before:
                c1(1, A, PositionA, 10, Company)
        /                               |
        c2(2, B, PositionB, 20)  c3(3, C, PositionC, 30, Department)
                                        |
                                        c4(4, D, PositionD, 40)
                                        /                           \
                                c5(5, E, PositionE, 50)  c6(6, F, PositionF, 60)

        After:
        c1(1, A, PositionA, 10, Company)
        /                               |
        c2(2, B, PositionB, 20)  c5(5, E, PositionC, 50, Department)
                                        |
                                        c3(3, C, PositionD, 30)
                                        /                           \
                                c4(4, D, PositionE, 40)  c6(6, F, PositionF, 60)
        """
        self.c3 = DistrictLeader(self.c3.cid, self.c3.manufacturer,
                                 self.c3.model_year, self.c3.job,
                                 self.c3.rating, 'Department')
        c6 = Citizen(6, 'F', 2020, 'PositionF', 60)
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.district)
        self.c4.become_subordinate_to(self.c3)
        self.c5.become_subordinate_to(self.c4)
        c6.become_subordinate_to(self.c4)
        self.society.set_head(self.district)
        self.society.promote_citizen(self.c5.cid)
        head = self.society.get_head()
        self.assertIsInstance(head, DistrictLeader)
        self.assertCitizen(head, {'cid': 1,
                                  'job': "PositionA",
                                  'rating': 10,
                                  'model_year': 2020,
                                  'get_superior': None,
                                  'get_district_name': 'Company'})
        self.assertTrue(len(head.get_direct_subordinates()) == 2)
        first, second = head.get_direct_subordinates()
        self.assertIsInstance(first, Citizen)
        self.assertCitizen(first, {'cid': 2,
                                   'job': "PositionB",
                                   'rating': 20,
                                   'model_year': 2020,
                                   'get_superior': head,
                                   'get_district_name': 'Company'})
        self.assertIsInstance(second, DistrictLeader)
        self.assertCitizen(second, {'cid': 5,
                                    'job': "PositionC",
                                    'rating': 50,
                                    'model_year': 2020,
                                    'get_superior': head,
                                    'get_district_name': 'Department'})
        self.assertTrue(len(second.get_direct_subordinates()) == 1)
        temp = second.get_direct_subordinates()[0]
        self.assertIsInstance(temp, Citizen)
        self.assertCitizen(temp, {'cid': 3,
                                  'job': "PositionD",
                                  'rating': 30,
                                  'model_year': 2020,
                                  'get_superior': second,
                                  'get_district_name': 'Department'})
        self.assertTrue(len(temp.get_direct_subordinates()) == 2)
        l, r = temp.get_direct_subordinates()
        self.assertTrue(all([isinstance(x, Citizen) for x in [l, r]]))
        self.assertCitizen(l, {'cid': 4,
                               'job': "PositionE",
                               'rating': 40,
                               'model_year': 2020,
                               'get_superior': temp,
                               'get_district_name': 'Department'})
        self.assertCitizen(r, {'cid': 6,
                               'job': "PositionF",
                               'rating': 60,
                               'model_year': 2020,
                               'get_superior': temp,
                               'get_district_name': 'Department'})


class TestTask32(TestTask3):
    def setUp(self) -> None:
        self.district = DistrictLeader(1, "A", 2020, "PositionA", 10, "Company")
        self.c2 = Citizen(2, "B", 2020, "PositionB", 20)
        self.c3 = Citizen(3, "C", 2020, "PositionC", 30)
        self.c4 = Citizen(4, "D", 2020, "PositionD", 40)
        self.c5 = Citizen(5, "E", 2020, "PositionE", 50)
        self.society = Society()

    def tearDown(self) -> None:
        self.district = DistrictLeader(1, "A", 2020, "PositionA", 10, "Company")
        self.c2 = Citizen(2, "B", 2020, "PositionB", 20)
        self.c3 = Citizen(3, "C", 2020, "PositionC", 30)
        self.c4 = Citizen(4, "D", 2020, "PositionD", 40)
        self.c5 = Citizen(5, "E", 2020, "PositionE", 50)
        self.society = Society()

    def test_highest_1(self):
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.district)
        highest = self.district.get_highest_rated_subordinate()
        self.assertTrue(highest, {'cid': 3,
                                  'job': "PositionC",
                                  'rating': 30,
                                  'model_year': 2020,
                                  'get_superior': self.district,
                                  'get_district_name': 'Company'})

    def test_highest_2(self):
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.c2)
        highest = self.district.get_highest_rated_subordinate()
        self.assertTrue(highest, {'cid': 2,
                                  'job': "PositionB",
                                  'rating': 20,
                                  'model_year': 2020,
                                  'get_superior': self.district,
                                  'get_district_name': 'Company'})
        self.district.add_subordinate(self.c4)
        highest = self.district.get_highest_rated_subordinate()
        self.assertTrue(highest, {'cid': 4,
                                  'job': "PositionD",
                                  'rating': 40,
                                  'model_year': 2020,
                                  'get_superior': self.district,
                                  'get_district_name': 'Company'})

    def test_delete_1(self):
        self.society.set_head(self.district)
        self.society.delete_citizen(self.district.cid)
        self.assertIsNone(self.society.get_head())

    def test_delete_2(self):
        """
        Before:
             c1
            / \
           c2  c3
               /\
            c4  c5

        After:
            c1
            / \ \
           c2 c4 c5
        """
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.district)
        self.c4.become_subordinate_to(self.c3)
        self.c5.become_subordinate_to(self.c3)
        self.society.set_head(self.district)
        self.society.delete_citizen(self.c3.cid)
        self.assertIsNone(self.society.get_citizen(self.c3.cid))
        self.assertTrue(
            len(self.society.get_head().get_direct_subordinates()) == 3)
        self.assertListEqual([temp.cid for temp in
                              self.society.get_head().get_direct_subordinates()],
                             [2, 4, 5])

    def test_delete_3(self):
        """
        Before:
             c1
            / \
           c2  c3
               /\
            c4  c5

        After:
              c1
             / \
            c2  c3
                |
                c5
        """
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.district)
        self.c4.become_subordinate_to(self.c3)
        self.c5.become_subordinate_to(self.c3)
        self.society.set_head(self.district)
        self.society.delete_citizen(self.c4.cid)
        self.assertIsNone(self.society.get_citizen(self.c4.cid),
                          "You should not have c4 in the society")
        self.assertTrue(
            len(self.society.get_head().get_direct_subordinates()) == 2,
            "You should obtain c4 and c5 as c1's direct children")
        self.assertListEqual(
            [temp.cid for temp in
             self.society.get_head().get_direct_subordinates()],
            [2, 3])
        new_e3 = self.society.get_head().get_direct_subordinates()[1]
        self.assertTrue(len(new_e3.get_direct_subordinates()) == 1)
        self.assertCitizen(new_e3.get_direct_subordinates()[0], {'cid': 5,
                                                                 'job': "PositionE",
                                                                 'rating': 50,
                                                                 'model_year': 2020,
                                                                 'get_superior': new_e3,
                                                                 'get_district_name': 'Company'})

    def test_delete_4(self):
        """
        Before:
            c1
            |
            c2
            |
            c3
            |
            c4
            |
            c5
        After:
            c1
            |
            c2
            |
            c4
            |
            c5
        """
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.c2)
        self.c4.become_subordinate_to(self.c3)
        self.c5.become_subordinate_to(self.c4)
        self.society.set_head(self.district)
        self.society.delete_citizen(self.c3.cid)
        self.assertIsNone(self.society.get_citizen(self.c3.cid),
                          "You should move the c3 from the organization")
        child = self.society.get_head().get_direct_subordinates()
        self.assertTrue(len(self.society.get_all_citizens()) == 4,
                        "You should only have 4 citizens")
        self.assertTrue(len(child) == 1,
                        "You are not moving any direct child under c1")
        self.assertListEqual(
            [temp.cid for temp in child[0].get_direct_subordinates()], [4],
            "The first child of c2 has to be c4")

    def test_delete_5(self):
        """
        Before:
             c1
             |
            c2
            /|
           c3 c4
             / |
            c5 c6
            |
            c7
        After:
            c1
             |
            c2
            /| \
           c3 c5 c6
              |
              c7
                """
        c1 = Citizen(1, "A", 2020, "PositionA", 10)
        c2 = Citizen(2, "B", 2020, "PositionB", 20)
        c3 = Citizen(3, "C", 2020, "PositionC", 30)
        c4 = Citizen(4, "D", 2020, "PositionD", 40)
        c5 = Citizen(5, "E", 2020, "PositionE", 50)
        c6 = Citizen(6, "F", 2020, "PositionF", 60)
        c7 = Citizen(7, "G", 2020, "PositionG", 70)
        c2.become_subordinate_to(c1)
        c3.become_subordinate_to(c2)
        c4.become_subordinate_to(c2)
        c5.become_subordinate_to(c4)
        c6.become_subordinate_to(c4)
        c7.become_subordinate_to(c5)
        self.society.set_head(c1)
        self.society.delete_citizen(c4.cid)
        self.assertIsNone(self.society.get_citizen(c4.cid))
        act = self.society.get_head()
        self.assertTrue(act.cid == 1, "c1 should remain as the head")
        self.assertTrue(len(act.get_direct_subordinates()) == 1,
                        "c2 should still under c1")
        new_c2 = act.get_direct_subordinates()[0]
        self.assertTrue(len(new_c2.get_direct_subordinates()) == 3,
                        "You should move c5 and c6 under c2")
        self.assertListEqual(
            [temp.cid for temp in new_c2.get_direct_subordinates()], [3, 5, 6],
            "Now c5 and c6 should be the children under c2")

    def test_delete_6(self):
        """
        Before:
             e1
            / \
           e2  e3
               /\
            e4  e5
        After:
              e3
             / | \
          e2 e4 e5
        """
        self.c2.become_subordinate_to(self.district)
        self.c3.become_subordinate_to(self.district)
        self.c4.become_subordinate_to(self.c3)
        self.c5.become_subordinate_to(self.c3)
        self.society.set_head(self.district)
        self.society.delete_citizen(self.district.cid)
        self.assertIsNone(self.society.get_citizen(self.district.cid))
        act = self.society.get_head()
        self.assertTrue(act.cid == 3, "c3 should be the new head")
        self.assertTrue(len(act.get_direct_subordinates()) == 3)
        self.assertListEqual(
            [temp.cid for temp in act.get_direct_subordinates()], [2, 4, 5],
            "This is the correct order of the children under c3")


if __name__ == '__main__':
    unittest.main(verbosity=3)
