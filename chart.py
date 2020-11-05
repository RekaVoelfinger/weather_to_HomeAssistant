import matplotlib.pylab as plt
from matplotlib.collections import EventCollection

# Draw and save chart in file "rainy_hours.jpg"
def draw_chart(colours, labels, *dicts):
    i = 0
    for dict in dicts:
        lists = sorted(dict.items()) # sorted by key, return a list of tuples
        x, y = zip(*lists) # unpack a list of pairs into two tuples
        plt.plot(x, y, color='tab:' + colours[i], label=labels[i])
        xevents = EventCollection(x, color='tab:' + colours[i], linelength=0.05)
        yevents = EventCollection(y, color='tab:' + colours[i], linelength=0.05, orientation='vertical')
        i +=1
    plt.title("Chance of rain in the next 12 hours in Weidach")
    plt.xlabel('Time hour')
    plt.ylabel('%')
    plt.legend()
    #plt.show()

    plt.savefig("rainy_hours.jpg")
    return


