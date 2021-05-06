import unittest
import operations


class TestOperations(unittest.TestCase):
    def test_convert_to_array(self):
        self.assertEqual(operations.convert_to_array(5), (['+', 5], 0))
        self.assertEqual(operations.convert_to_array(5.01), (['+', 5, 0, 1], 2))
        self.assertEqual(operations.convert_to_array(-5.01), (['-', 5, 0, 1], 2))
        self.assertEqual(operations.convert_to_array(-5000.001), (['-', 5, 0, 0, 0, 0, 0, 1], 3))

    def test_zero_pad(self):
        self.assertEqual(operations.zero_pad(7, [0, 0, 0, 1], pad_direction=True), [0, 0, 0, 0, 0, 0, 1])
        self.assertEqual(operations.zero_pad(7, [0, 0, 0, 1], pad_direction=False), [0, 0, 0, 1, 0, 0, 0])
        self.assertEqual(operations.zero_pad(7, [0, 0, 0, 1, 0, 0, 0], pad_direction=False), [0, 0, 0, 1, 0, 0, 0])

    def test_de_zero_pad(self):
        self.assertEqual(operations.de_zero_pad([0, 0, 0, 1, 0, 0, 0]), [0, 1, 0, 0, 0])
        self.assertEqual(operations.de_zero_pad([0, 0, '.', 0, 0, 0, 1, 0, 0, 0]), [0, '.', 0, 0, 0, 1, 0, 0, 0])

    def test_operation_handler(self):
        # operation_handler(a_in, b_in, dot_1, dot_2, op_code='a'):
        # return result, new_dot
        self.assertEqual(operations.operation_handler(['+', 1, 2, 5, 1, 4], ['+', 4, 7, 2, 6, 3], 2, 3, 'a'),
                         (['+', 1, 7, 2, 4, 0, 3], 3))
        self.assertEqual(operations.operation_handler(['+', 1, 2, 5, 1, 4], ['-', 4, 7, 2, 6, 3], 2, 3, 'a'),
                         (['+', 7, 7, 8, 7, 7], 3))
        self.assertEqual(operations.operation_handler(['-', 1, 2, 5, 1, 4], ['-', 4, 7, 2, 6, 3], 2, 3, 'a'),
                         (['-', 1, 7, 2, 4, 0, 3], 3))
        self.assertEqual(operations.operation_handler(['+', 1, 2, 5, 1, 4], ['+', 4, 7, 2, 6, 3], 2, 3, 's'),
                         (['+', 7, 7, 8, 7, 7], 3))
        self.assertEqual(operations.operation_handler(['+', 1, 2, 5, 1, 4], ['-', 4, 7, 2, 6, 3], 2, 3, 's'),
                         (['+', 1, 7, 2, 4, 0, 3], 3))
        self.assertEqual(operations.operation_handler(['-', 1, 2, 5, 1, 4], ['-', 4, 7, 2, 6, 3], 2, 3, 's'),
                         (['-', 7, 7, 8, 7, 7], 3))

    def test_add_arrays(self):
        self.assertEqual(operations.add_arrays([1, 2, 5, 1, 4, 0],[0, 4, 7, 2, 6, 3]),[1, 7, 2, 4, 0, 3])
        self.assertEqual(operations.add_arrays([1, 1, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3]), [1, 6, 2, 4, 0, 3])
        self.assertEqual(operations.add_arrays([1, 2, 5, 1, 4, 5], [0, 4, 7, 2, 6, 3]), [1, 7, 2, 4, 0, 8])

    def test_subtract_arrays(self):
        self.assertEqual(operations.subtract_arrays([1, 2, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3]), [0, 7, 7, 8, 7, 7])
        self.assertEqual(operations.subtract_arrays([0, 4, 7, 2, 6, 3],[0, 1, 4, 0, 3, 0]), [0, 3, 3, 2, 3, 3])

    def test_arrange_and_pad(self):
        # return A, B, first_larger, state
        self.assertEqual(operations.arrange_and_pad(['1', '2', '5', '1', '4', 0],['4', '7', '2', '6', '3']),
                         ([2, 5, 1, 4, 0], [0, 7, 2, 6, 3], True, 4))

        self.assertEqual(operations.arrange_and_pad(['+', '1', '2', '5', '1', '4', 0], ['+', '4', '7', '2', '6', '3']),
                         ([1, 2, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3], True, 0))

    def test_format(self):
        self.assertEqual(operations.format(['+', 1, 2, 5, 1, 4],2),'+125.14')
        self.assertEqual(operations.format(['+', 4, 7, 2, 6, 3], 3), '+47.263')
        self.assertEqual(operations.format(['+', 1, 7, 2, 4, 0, 3], 3),'+172.403')


    def test_convert_float_rep(self):
        self.assertEqual(operations.convert_float_rep('+125.14'),'125.14')
        self.assertEqual(operations.convert_float_rep('+47.263'), '47.263')

    def test_operation(self):
        # operation_handler(a_in, b_in, dot_1, dot_2, op_code='a'):
        # return result, new_dot
        self.assertEqual(operations.operation([1, 2, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3], 'a'), [1, 7, 2, 4, 0, 3])
        self.assertEqual(operations.operation([1, 2, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3], 's'), [0, 7, 7, 8, 7, 7])
        self.assertEqual(operations.operation([1, 2, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3], 'a'), [1, 7, 2, 4, 0, 3])
        self.assertEqual(operations.operation([1, 2, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3], 's'),[0, 7, 7, 8, 7, 7])
        self.assertEqual(operations.operation([1, 2, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3], 'a'), [1, 7, 2, 4, 0, 3])
        self.assertEqual(operations.operation([1, 2, 5, 1, 4, 0], [0, 4, 7, 2, 6, 3], 's'), [0, 7, 7, 8, 7, 7])


if __name__ == '__main__':
    unittest.main()
