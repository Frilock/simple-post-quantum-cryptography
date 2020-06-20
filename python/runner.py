from python.linearCode import LinearCode
import matplotlib.pyplot as plot
import numpy as np
# реализации методов декодера , подумать о входящих параметрах и прочих ограничениях


def get_graphics():
    plot.figure()
    plot.xlabel('weight')
    plot.ylabel('count')

    for i in range(2, 8):
        if i == 6:
            continue
        lc = LinearCode(15, 7, i)
        spectrum = lc.get_spectrum()
        weights, count = zip(*sorted(spectrum.most_common()))
        print(count)
        plot.plot(np.array(weights, dtype=int), np.array(count, dtype=int), label='spectrum(15, 7, {})'.format(i))
    plot.legend()
    plot.show()


get_graphics()
