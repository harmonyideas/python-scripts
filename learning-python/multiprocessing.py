import random
import itertools
import humanize
import logging
import time

from multiprocessing import Process

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


class RandomKeys(object):

    def __init__(self):
        self.keys = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@', ':', '/', '*',
                     '[SHIFT LOCK]', '[TAB]', '[BACKSPACE]', '[SHIFT1]', '[SHIFT2]', '[0.5]', '[0.25]')

    def pick_random_keys(self, counter):
        rsample = ""
        for x in xrange(abs(counter)):
            rsample = rsample + random.choice(RandomKeys().keys)
        return rsample
        # return ''.join(random.sample(RandomKeys().keys, abs(counter)))

    def gen_random_keys(self, search_string, keys_length, start_time, pid):
        logging.debug("[STARTING]: keyword is " + search_string)
        for x in itertools.count(1):
            sample = RandomKeys().pick_random_keys(keys_length)
            if search_string in sample:
                days, seconds = divmod(time.time() - start_time, 24 * 60 * 60)
                hours, seconds = divmod(time.time() - start_time, 3600)
                minutes, seconds = divmod(time.time() - start_time, 60)
                logging.debug(
                    "[MATCH FOUND!] " +
                    "[RUNTIME {:0>2}d:{:0>2}h:{:0>2}m:{:0.0f}s]"
                    .format(int(days), int(hours), int(minutes),seconds) +
                    "[PID: " + str(pid) + "]" +
                    "[Word Count: " + humanize.intword(x) + "]" +
                    "[Last Result: " + sample + "] [EXITING...]")
                break
            else:
                if x % 1000000 == 0:
                    days, seconds = divmod(time.time() - start_time, 24 * 60 * 60)
                    hours, seconds = divmod(time.time() - start_time, 3600)
                    minutes, seconds = divmod(time.time() - start_time, 60)
                    logging.debug(
                        "[RUNNING] " +
                        "[RUNTIME {:0>2}d:{:0>2}h:{:0>2}m:{:0.0f}s]"
                        .format(int(days), int(hours), int(minutes), seconds) +
                        "[PID: " + str(pid) + "]" +
                        "[Word Count: " + humanize.intword(x) + "]" +
                        "[Last Result: " + sample + "]")


processes = []
if __name__ == '__main__':
    for i in range(10):
        start_time = time.time()
        mySample = RandomKeys()
        p = Process(target=mySample.gen_random_keys, args=("ettubrute", 7, start_time, i))
        processes.append(p)
        p.start()
