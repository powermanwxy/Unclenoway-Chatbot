# -*- coding: UTF-8 -*-
from Uncle import Uncle
from multiprocessing import Pool


"""
Please take a look at <Uncle.py>. Make sure that config variables are correct.
"""

# In order to protect the website, processes should not more then four.
processes = 1


def create_instance(i):
    uncle = Uncle(i)
    print 'Uncle instance: ', i
    uncle.start()
    return

if __name__ == "__main__":

    pool = Pool(processes=processes)
    index = 0

    for i in xrange(processes):

        pool.apply_async(create_instance, args=(index,))
        index += 1

    pool.close()
    pool.join()
