def justPlotIt(array, array_x=None):
    import matplotlib.pyplot as plt
    if array_x is None:
        array_x = range(len(array))

    plt.ion()
    plt.figure()
    plt.plot(array_x, array)
    plt.show()
    plt.waitforbuttonpress()
    plt.close()
