from typing import List
import time
import numpy as np


def test_function(function: callable, test_cases: List[tuple], verbose: bool=False) -> None:
    for test_idx, test_case in enumerate(test_cases):
        inp, out = test_case
        function_out = function(*inp)
        if out == function_out:
            print(f'Test {test_idx} passed')
        else:
            print(f'Test {test_idx} failed')
            if verbose:
                print(f'Error on input=\n{inp}\ncorrect output=\n{out}\nyour output=\n{function_out}')
                

def timeit(function: callable, inp: list, repeats: int = 1) -> float:
    start = time.time()
    for i in range(repeats):
        function(*inp)
    return (time.time() - start) / repeats

                
def time_inp_data(function: callable, inp_data: List[list], repeats: int = 1) -> np.ndarray:
    time_arr = []
    for inp in inp_data:
        time_arr.append(timeit(function, inp, repeats))
    return np.array(time_arr[1:]) / np.array(time_arr[:-1])