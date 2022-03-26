import matplotlib.pylab as plt


# Draw and save chart in file "rainy_hours.jpg"
def draw_chart(colours, labels, date, *dicts):
    overlapping = [1, 0.5, 0.5]
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    line_widths = [2, 3, 4]
    i = 0
    for d in dicts:
        lists = sorted(d.items())  # Sorted by key, return a list of tuples.
        x, y = zip(*lists)  # Unpack a list of pairs into two tuples
        plt.plot(x, y, color='tab:' + colours[i], label=labels[i], alpha=overlapping[i], lw=line_widths[i])
        plt.gcf().autofmt_xdate()  # Beautify the x-labels.
        i += 1
    plt.title(f"Chance of rain in the next 12 hours in Weidach\n{date}")
    plt.xlabel('Time hour')
    plt.ylabel('%')
    plt.legend()
    # plt.show()

    plt.savefig("chance_of_rain.jpg")
    return

