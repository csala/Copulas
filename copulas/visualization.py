import matplotlib
import pandas as pd
from mpl_toolkits import mplot3d  # noqa: importing this fixes import error in py35

matplotlib.use('PS')   # Avoid crash on macos
import matplotlib.pyplot as plt   # noqa isort:skip


def scatter_3d(data, columns=None, fig=None, title=None, position=None):
    """Plot 3 dimensional data in a scatter plot."""
    fig = fig or plt.figure()
    position = position or 111

    ax = fig.add_subplot(position, projection='3d')
    ax.scatter(*(
        data[column]
        for column in columns or data.columns
    ))
    if title:
        ax.set_title(title)
        ax.title.set_position([.5, 1.05])

    return ax


def scatter_2d(data, columns=None, fig=None, title=None, position=None):
    """Plot 2 dimensional data in a scatter plot."""
    fig = fig or plt.figure()
    position = position or 111

    ax = fig.add_subplot(position)
    columns = columns or data.columns
    if len(columns) != 2:
        raise ValueError('Only 2 columns can be plotted')

    x, y = columns

    ax.scatter(data[x], data[y])
    plt.xlabel(x)
    plt.ylabel(y)

    if title:
        ax.set_title(title)
        ax.title.set_position([.5, 1.05])

    return ax


def hist_1d(data, fig=None, title=None, position=None, bins=20, label=None):
    """Plot 1 dimensional data in a histogram."""
    fig = fig or plt.figure()
    position = position or 111

    ax = fig.add_subplot(position)
    ax.hist(data, density=True, bins=bins, alpha=0.8, label=label)

    if label:
        ax.legend()

    if title:
        ax.set_title(title)
        ax.title.set_position([.5, 1.05])

    return ax


def side_by_side(plotting_func, arrays):
    fig = plt.figure(figsize=(10, 4))

    position_base = '1{}'.format(len(arrays))
    for index, (title, array) in enumerate(arrays.items()):
        position = int(position_base + str(index + 1))
        plotting_func(array, fig=fig, title=title, position=position)

    plt.tight_layout()


def compare_3d(real, synth, columns=None, figsize=(10, 4)):
    columns = columns or real.columns
    fig = plt.figure(figsize=figsize)

    scatter_3d(real[columns], fig=fig, title='Real Data', position=121)
    scatter_3d(synth[columns], fig=fig, title='Synthetic Data', position=122)

    plt.tight_layout()


def compare_2d(real, synth, columns=None, figsize=None):
    x, y = columns or real.columns
    ax = real.plot.scatter(x, y, color='blue', alpha=0.5, figsize=figsize)
    ax = synth.plot.scatter(x, y, ax=ax, color='orange', alpha=0.5, figsize=figsize)
    ax.legend(['Real', 'Synthetic'])


def compare_1d(real, synth, columns=None, figsize=None):
    if len(real.shape) == 1:
        real = pd.DataFrame({'': real})
        synth = pd.DataFrame({'': synth})

    columns = columns or real.columns

    num_cols = len(columns)
    fig_cols = min(2, num_cols)
    fig_rows = (num_cols // fig_cols) + 1
    prefix = '{}{}'.format(fig_rows, fig_cols)

    figsize = figsize or (5 * fig_cols, 3 * fig_rows)
    fig = plt.figure(figsize=figsize)

    for idx, column in enumerate(columns):
        position = prefix + str(idx + 1)
        hist_1d(real[column], fig=fig, position=position, title=column, label='Real')
        hist_1d(synth[column], fig=fig, position=position, title=column, label='Synthetic')

    plt.tight_layout()
