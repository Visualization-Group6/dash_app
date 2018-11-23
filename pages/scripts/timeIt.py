import time


""""
Run this .py to test it's functionality, observe and use in your own script through importing.
>from pages.scripts import timeIt
>timeIt.get_average_runtime(yourFunctionWithoutParentheses, listOfArgumentsForFunction, nTestRuns)
"""


def get_average_runtime(function, function_args: list, n=10):
    cum_time = 0
    for i in range(n):
        start_time = time.time()
        function(*tuple(function_args))
        delta_time = time.time()-start_time
        cum_time += delta_time
    return cum_time/n


# Only here for showing off functionality of get_average_runtime, no further purpose.
def test_function(n, p, t):
    for i in range(n):
        for i in range(p):
            time.sleep(t)


if __name__ == '__main__':
    print(get_average_runtime(test_function, [10, 5, 0.001], 20))
