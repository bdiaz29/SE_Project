import numpy as np
from random import randint

# a mapping to help operation handler
# first letter tells the type of operation
# first number tells if the first number is larger or not
# second number tells it what state it is in (positive, positive),(positive,negative) ect...
operation_dict = {
    'a10': ['a', '+'],
    'a00': ['a', '+'],
    'a11': ['s', '+'],
    'a01': ['s', '-'],
    'a12': ['s', '-'],
    'a02': ['s', '+'],
    'a13': ['a', '-'],
    'a03': ['a', '-'],
    's10': ['s', '+'],
    's00': ['s', '-'],
    's11': ['a', '+'],
    's01': ['a', '+'],
    's12': ['a', '-'],
    's02': ['a', '-'],
    's13': ['s', '-'],
    's03': ['s', '+']
}


# converts integer number into an array
def convert_to_array(num_int):
    dot_position = 0
    num_array = []
    # converts to sting
    str_int = str(num_int)
    for i, char_int in enumerate(str_int):
        char = ord(char_int)
        # checks if it is a digit or not
        if char == 46:
            dot_position = (len(str_int) - 1) - i
        elif char >= 48 and char <= 57:
            # cast character into int
            tmp = int(char_int)
            num_array += [tmp]
        else:
            num_array += [char_int]

    # if negative sign not present insert positive sign
    if num_array[0] != '-':
        num_array.insert(0, '+')
    return num_array, dot_position


# runs a test on a random operation
# and two random numbers
def test(upper_limit=10000000000):
    # selects random operation
    o = bool(randint(0, 1))
    if o:
        op_code = 'a'
    else:
        op_code = 's'
    # selects random number
    # diffrent upper limits created for each random number
    # in order to give numbers with changing number of digits
    U1 = randint(10, upper_limit)
    U2 = randint(10, upper_limit)

    S1 = 1 - (randint(0, 1) * 2)
    S2 = 1 - (randint(0, 1) * 2)

    number_1 = randint(1, U1) * S1
    number_2 = randint(1, U2) * S2
    # calculate the real values of the operation
    if op_code == 'a':
        answer = number_1 + number_2
    elif op_code == 's':
        answer = number_1 - number_2
    else:
        print("error:do not recognize operation")
        return False
    # convert number and real answer to arrays
    number_1_array, dot_1 = convert_to_array(number_1)
    number_2_array, dot_2 = convert_to_array(number_2)
    answer_array, dot_3 = convert_to_array(answer)
    # pass arrays to operation handler and get result
    result, instruct = operation_handler(number_1_array, number_2_array, dot_1, dot_2, op_code=op_code)
    # compare result with real answer
    for i, ret in enumerate(result):
        r_actual = answer_array[i]
        r_predicted = result[i]
        if r_actual != r_predicted:
            print('incorrect answer for:', str(number_1), str(number_2), op_code, str(instruct))
            return False
    return result


# takes an array and pads it with zeros until its in the desired length
def zero_pad(desired_length, arr, pad_direction=True):
    array = list(np.copy(arr))
    array_length = len(array)
    if array_length == desired_length:
        return array
    length_difference = abs(array_length - desired_length)
    zero_padding = list(np.zeros((length_difference), dtype=np.int))
    if pad_direction:
        zero_padding.extend(array)
        ans = zero_padding
    else:
        array.extend(zero_padding)
        ans = array
    return ans


# removes the trailing zeros in front of array
def de_zero_pad(array):
    # iterativly remove zeros until it reaches a non zero value
    # or the length of the number and sign is two
    while True:
        # if array has reach the .
        if array[1] == '.':
            break
        # if array plus its sign is as short as it can get
        # just return the zero
        if len(array) == 2:
            if array[1] == 0:
                # zeros always represented as positive
                array[0] = '+'
            break
        if array[1] == 0:
            array.pop(1)
        else:
            break
    return array


# handles the operations
# default operation is add
def operation_handler(a_in, b_in, dot_1, dot_2, op_code='a'):
    global operation_dict
    # create copy of original arrays since
    # operation may modify arrays
    A = list.copy(a_in)
    B = list.copy(b_in)
    forward_pad_a = max(dot_2 - dot_1, 0)
    forward_pad_b = max(dot_1 - dot_2, 0)
    new_dot = 0

    # pad to batch dots
    A = zero_pad(len(A) + forward_pad_a, A, pad_direction=False)
    B = zero_pad(len(B) + forward_pad_b, B, pad_direction=False)
    if forward_pad_a >= forward_pad_b:
        new_dot = dot_1 + forward_pad_a
    else:
        new_dot = dot_2 + forward_pad_b
    # call the arrange_and_pad function to properly format arrays
    # and get info of what state they are in
    A, B, first_larger, state = arrange_and_pad(A, B)
    # take in the info found into the operation dictionary to get instructions
    # of how to solve the problem
    search_string = op_code + str(int(first_larger)) + str(state)
    # instructions contain what function to call and what
    # the resulting sign will be after the operation
    instructions = operation_dict[search_string]
    # sub op code determine which specific operation to call
    sub_op_code = instructions[0]
    sign = instructions[1]
    # perform operation
    result = operation(A, B, sub_op_code)
    result.insert(0, sign)
    # result.insert((len(result)) - new_dot, '.')
    result = de_zero_pad(result)
    return result, new_dot


# runs the operation on the arrays according to the opcodes
def operation(a_in, b_in, op_code):
    if op_code == 'a':
        result = add_arrays(a_in, b_in)
    elif op_code == 's':
        result = subtract_arrays(a_in, b_in)
    else:
        print("invalid op code")
        result = None
    return result


# adds the two arrays together
# sign is ignored since that is handles by the operation handler
def add_arrays(a_in, b_in):
    array_length = len(a_in)
    answer = []
    # the carry value originally a 0
    c = 0
    # arrays iterated backwards to perform arithmetic
    # in correct format
    for i in range(array_length - 1, -1, -1):
        a = a_in[i]
        b = b_in[i]
        ans = a + b + c
        # if addition cases a carry
        if ans > 9:
            c = 1
            ans = ans - 10
        else:
            c = 0
        answer += [ans]
    # if the final carry is not a zero add it to the end
    if c != 0:
        answer += [c]
    # reverse the array to give correct answer
    return [ele for ele in reversed(answer)]


# subtracts two arrays together
# sign is ignored since that is handles by the operation handler
def subtract_arrays(a_in, b_in):
    array_length = len(a_in)
    answer = []
    # arrays iterated backwards to perform arithmetic
    # in correct format
    for i in range(array_length - 1, -1, -1):
        a = a_in[i]
        b = b_in[i]
        # if the digit is negative due to borrow
        # or if digit a is smaller than digit b initiate borrow operation
        if a < 0 or a < b:
            # subtract 1 due to borrow
            a_in[i - 1] -= 1
            # add ten due to borrow
            a += 10
        ans = a - b
        answer += [ans]
    # reverse the array to give correct answer
    answer_reversed = [ele for ele in reversed(answer)]
    return answer_reversed


# zero pads both numbers so that they the arrays are of equal length
# arranges it so that A output has the higher absolute value
# outputs if the first number is larger and what state it is n
# state meaning if its a
# positive number and another positive number , negative and a positive number and so on
def arrange_and_pad(num1, num2):
    first_larger = True
    state = 0
    num1_sign = num1.pop(0)
    num2_sign = num2.pop(0)
    # concatenate signs for easy assigning of state
    sign_concat = num1_sign + num2_sign
    if sign_concat == '++':
        state = 0
    elif sign_concat == '+-':
        state = 1
    elif sign_concat == '-+':
        state = 2
    elif sign_concat == '--':
        state = 3
    else:
        state = 4
    # determine both lengths to compare
    len1 = len(num1)
    len2 = len(num2)
    max_len = max(len1, len2)
    # if lengths are diffrent than the larger absolute value is the longer length
    if len1 > len2:
        A = zero_pad(max_len, num1)
        B = zero_pad(max_len, num2)
        first_larger = True
    elif len1 < len2:
        A = zero_pad(max_len, num2)
        B = zero_pad(max_len, num1)
        first_larger = False
    # if the lengths are the same then an algorithm has to be called
    # to determine which is longer
    else:
        # algorithm to determine which number is larger
        # first set default
        A = zero_pad(max_len, num1)
        B = zero_pad(max_len, num2)
        first_larger = True
        # then run iterator
        for i in range(max_len):
            if num1[i] > num2[i]:
                A = zero_pad(max_len, num1)
                B = zero_pad(max_len, num2)
                first_larger = True
                break
            elif num1[i] < num2[i]:
                A = zero_pad(max_len, num2)
                B = zero_pad(max_len, num1)
                first_larger = False
                break
    A = list(np.array(A, dtype=int))
    B = list(np.array(B, dtype=int))
    return A, B, first_larger, state


# 1101.001
def format(pre_array, dot):
    num_arr = []
    if dot != 0:
        array_part_a = pre_array[0:-dot]
        array_part_b = pre_array[-dot:len(pre_array)]
    else:
        array_part_a = pre_array
        array_part_b = []

    array_length = len(array_part_a)
    for i in range(array_length - 1, 0, -1):
        tmp = array_length - i + -1
        if tmp % 3 == 0 and tmp != 0:
            num_arr += [',']
        num_arr += [str(array_part_a[i])]
    num_arr += [str(array_part_a[0])]
    num_arr_reversed = [ele for ele in reversed(num_arr)]
    num_str = ''
    for num in num_arr_reversed:
        num_str += num
    num_str += '.'

    for num in array_part_b:
        num_str += str(num)

    return num_str


def convert_float_rep(num):
    spl = num.split('.')
    if len(spl) < 2:
        return int(num)
    int_part = str(int(spl[0]))
    # just to test its a number
    dec_part = str(spl[1])

    whole = int_part + '.' + dec_part
    return whole


txt = open('inputs.txt', 'r')
lines = txt.readlines()
for line in lines:
    arguments = line.replace('\n', '').split(' ')
    if len(arguments) != 3:
        print(str('invalid amount of arguments'), str(len(arguments)), 'were given')
        continue
    if arguments[0] != 'a' and arguments[0] != 's':
        print('did not use valid operation code')
        continue
    try:
        numA = convert_float_rep(arguments[1])
        numB = convert_float_rep(arguments[2])
    except ValueError:
        print("inputs not numbers")
        continue
    number_A_array, dot_A = convert_to_array(numA)
    number_B_array, dot_B = convert_to_array(numB)
    op_code = arguments[0]
    result, dot_C = operation_handler(number_A_array, number_B_array, dot_A, dot_B, op_code=op_code)

    formattedA = format(number_A_array, dot_A)
    formattedB = format(number_B_array, dot_B)
    formattedResult = format(result, dot_C)
    print(formattedA)
    if op_code == 'a':
        print('plus')
    elif op_code == 's':
        print('mius')
    else:
        print("?")
    print(formattedB)
    print("equals")
    print(formattedResult)
    print("")
