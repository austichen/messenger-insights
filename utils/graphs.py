import matplotlib.pyplot as plt

def simple_bar_graph(x, y, x_label, y_label, title, show_labels=True):
    x_ind = [i for i in range(len(y))]
    bars = plt.bar(x_ind, y)
    plt.xticks(x_ind, x, rotation=30)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if show_labels:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + .005, yval)
    plt.grid(axis='y')
    plt.show()

def partitioned_bar_graph(x, y1, y2, y1_legend, y2_legend, x_label, y_label, title, show_labels=True):
    def autolabel(rects, xpos='center'):
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(offset[xpos]*3, 3),  # use 3 points offset
                        textcoords="offset points",  # in both directions
                        ha=ha[xpos], va='bottom')

    x_ind = [i for i in range(len(x))]
    WIDTH = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar([pos - WIDTH/2 for pos in x_ind], y1, WIDTH, label=y1_legend)
    rects2 = ax.bar([pos + WIDTH/2 for pos in x_ind], y2, WIDTH, label=y2_legend)

    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x_ind)
    ax.set_xticklabels(x, rotation=30)
    ax.legend()

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    plt.grid(axis='y')
    plt.show()

def simple_time_graph(time_series, x_label, y_label, title):
    plt.plot(time_series)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(axis='y')
    plt.show()

def multiple_time_graphs(lines, x_label, y_label, title):
    fig, ax = plt.subplots()
    for sender, series in lines:
        # print(count.head())
        series.sort_index(inplace=True)
        ax.plot(series, label=sender)
    ax.legend()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(axis='y')
    plt.show()