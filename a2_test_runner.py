import unittest
import sys
from a2_test_case import *
import time


def load_suite(case):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for t in case:
        tests = loader.loadTestsFromTestCase(t)
        suite.addTest(tests)
    return suite


def main(verbosity=1):
    text = '''
   _____  _____  _____ __ _  _   ___             ___    _______ ______  _____ _______ ______ _____  
  / ____|/ ____|/ ____/_ | || | / _ \      /\   |__ \  |__   __|  ____|/ ____|__   __|  ____|  __ \ 
 | |    | (___ | |     | | || || (_) |    /  \     ) |    | |  | |__  | (___    | |  | |__  | |__) |
 | |     \___ \| |     | |__   _> _ <    / /\ \   / /     | |  |  __|  \___ \   | |  |  __| |  _  / 
 | |____ ____) | |____ | |  | || (_) |  / ____ \ / /_     | |  | |____ ____) |  | |  | |____| | \ \ 
  \_____|_____/ \_____||_|  |_| \___/  /_/    \_\____|    |_|  |______|_____/   |_|  |______|_|  \_\
    '''
    runner = unittest.TextTestRunner(verbosity=verbosity)
    err = lambda x: sys.stderr.write(x)
    clear = lambda: sys.stderr.flush()
    task_to_case = {"Task 1": (TestTask11, TestTask12, TestTask13),
                    "Task 2": (TestTask21, TestTask22, TestTask23),
                    "Task 3": (TestTask31, TestTask32),
                    "No Public": (TestNoPublic, )}
    fail = {}
    errs = {}
    acc = 0
    total = 0
    err(text + '\n')
    err('*' * 100 + '\n')
    for k in sorted(task_to_case.keys()):
        suite = load_suite(task_to_case[k])
        err(f'Start to test {k}\n')
        results = runner.run(suite)
        fails = len(results.failures)
        errors = len(results.errors)
        fail[k] = results.failures
        errs[k] = results.errors
        acc += fails + errors
        total += results.testsRun
        err('*' * 100 + '\n')
    err(f'\nTotal:{total} Cases\n')
    err(f'\nResult:{sum(map(lambda x: len(x), fail.values()))} failure(s) & {sum(map(lambda y: len(y), errs.values()))}error(s)\n')
    if acc == 0:
        err("\nAll test passed\n")
        pass_ = '''

       _____  ____   ____  _____         _  ____  ____    _ 
      / ____|/ __ \ / __ \|  __ \       | |/ __ \|  _ \  | |
     | |  __| |  | | |  | | |  | |      | | |  | | |_) | | |
     | | |_ | |  | | |  | | |  | |  _   | | |  | |  _ <  | |
     | |__| | |__| | |__| | |__| | | |__| | |__| | |_) | |_|
      \_____|\____/ \____/|_____/   \____/ \____/|____/  (_)

                    '''
        for char in pass_:
            clear()
            err(char)
            time.sleep(0.009)
    else:
        for k in sorted(fail.keys()):
            cases = lambda x: '\n'.join(
                list(map(lambda y: '\t' + y[0]._testMethodName, x)))
            err(f'\nNumber of failure in {k}:{len(fail[k])}\n{"" if verbosity == 1 else cases(fail[k])}\nNumber of error in {k}:{len(errs[k])}\n{"" if verbosity == 1 else cases(errs[k])}\n')



if __name__ == '__main__':
    main(verbosity=1)
