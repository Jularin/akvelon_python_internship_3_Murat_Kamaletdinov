import sys


def fibo(number: int) -> int:
    """
    Function to calculate n'th number of fibonacci sequence
    Function works very fast because it save cached numbers
    """

    if number < 0:
        print("Invalid number please enter positive int number")
        sys.exit(-1)

    nums = [0] * number
    nums[0], nums[1] = 0, 1

    for i in range(2, number):
        nums[i] = nums[i - 1] + nums[i - 2]
    return nums[number - 1]


fibo(3)  # return 1
fibo(10)  # return 34
fibo(100)  # return 218922995834555169026

