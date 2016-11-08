from __future__ import print_function


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m' + '\033[22m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BACKGROUND_RED = '\033[41m'
YELLOW = '\033[33m'


def compareTime(function_list):
    from time import time
    number = len(function_list)
    times = list()
    for function in function_list:
        function()
        now = time()
        function()
        duration = time() - now
        times.append(duration)

    small_counts = max(10, int(.1 / min(times)))
    times = [0] * number

    big_counts = 10
    for _ in range(big_counts):
        for i, function in enumerate(function_list):
            now = time()
            for _ in range(small_counts):
                function()
            duration = time() - now
            times[i] += duration
    speed = [0] * number
    for i in range(number):
        times[i] = times[i] / (big_counts * small_counts)
        speed[i] = 1. / times[i]
    slowest = min(speed)
    for i in range(number):
        percentage = 100 * (speed[i] - slowest) / slowest
        if percentage == 0:
            print("#%i:" % (i + 1), function_list[i].__name__)
        else:
            print("#%i:" % (i + 1), function_list[i].__name__, "is %%%.1f faster" % percentage)
        print("%.2e s | %.1e Hz" % (times[i], speed[i]))
        print()


def bigAlert(text):
    from pyfiglet import Figlet
    f = Figlet(font='big')
    print(BOLD + BACKGROUND_RED + YELLOW + f.renderText(text) + ENDC)


def stringFormat(code, text):
    return code + text + ENDC


def fail(text):
    return stringFormat(FAIL, text)


def warn(text):
    return stringFormat(WARNING, text)


def green(text):
    return stringFormat(OKGREEN, text)


def blue(text):
    return stringFormat(OKBLUE, text)


def bold(text):
    return stringFormat(BOLD, text)


def pertentageBar(fraction, depth=10):
    perten = int(fraction * depth)
    return "[" + "=" * perten + " " * (depth - perten) + "]"


def countDown(seconds):
    from time import sleep
    from sys import stdout, exit

    for i in range(seconds):
        print("Counting Down: " + str(seconds - i) + " seconds")
        sleep(1)
        stdout.write("\033[F\033[K")


def setupLogger(name, stream_level='DEBUG', file_level=None):
    import logging
    import sys
    from time import strftime

    def getLevel(log_level):
        if log_level is 'DEBUG':
            return logging.DEBUG
        elif log_level is 'INFO':
            return logging.INFO
        elif log_level is 'WARNING':
            return logging.WARNING
        elif log_level is 'ERROR':
            return logging.ERROR
        elif log_level is 'CRITICAL':
            return logging.CRITICAL
        else:
            return None

    stream_level = getLevel(stream_level)
    file_level = getLevel(file_level)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('-----\n%(asctime)s | %(levelname)s\n%(message)s')
    levels = []
    if file_level is not None:
        levels.append(file_level)
        log_file_name = name + '_' + strftime("%d%b%Y_%X") + '.log'
        print('Logging to:', log_file_name)
        debug_file = logging.FileHandler(log_file_name)
        debug_file.setLevel(file_level)
        debug_file.setFormatter(formatter)
        logger.addHandler(debug_file)
    if stream_level is not None:
        levels.append(stream_level)
        debug_stream = logging.StreamHandler(sys.stdout)
        debug_stream.setLevel(stream_level)
        debug_stream.setFormatter(formatter)
        logger.addHandler(debug_stream)
    elif file_level is None:
        raise ValueError('At least one of log levels should not be `None`.')
    return logger

if __name__ == "__main__":
    for i in range(5):
        print(pertentageBar(i / 4., 29))
    countDown(40)
    # l = setupLogger('sss','CRITICAL','DEBUG')

    # l.critical('somethign')
    # l.info('info here')
    # l.debug('this is the freaking msg')
    # l.critical('critical one')

    # justPlotIt([1, 2, 3, 4, 5, 2, 3])
    pass
