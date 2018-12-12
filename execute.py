# -*- coding:utf-8 -*-

import random

import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

from get_cats import Cats


if __name__ == '__main__' :

    fig = plt.figure(figsize = (4, 3)) # 3:2

    gs_master = GridSpec(nrows = 3, ncols = 4, height_ratios = [1, 1, 1])

    gs = [0] * 4
    gs[0] = GridSpecFromSubplotSpec(nrows = 3, ncols = 3, subplot_spec = gs_master[0:3, 0:3])
    gs[1] = GridSpecFromSubplotSpec(nrows = 1, ncols = 1, subplot_spec = gs_master[0, 3])
    gs[2] = GridSpecFromSubplotSpec(nrows = 1, ncols = 1, subplot_spec = gs_master[1, 3])
    gs[3] = GridSpecFromSubplotSpec(nrows = 1, ncols = 1, subplot_spec = gs_master[2, 3])

    ax = [0] * 4
    for i in range(len(gs)) :
        ax[i] = fig.add_subplot(gs[i][:, :])

    cats = Cats()
    len_cats = len(cats)

    def update(i) :
        for i in range(len(ax)) :
            ax[i].clear()

        # img = cv2.imread(cats.get_cat_path(i))
        img = cv2.imread(cats.get_cat_path(random.randint(0, len_cats)))

        ### Split image
        b, g, r = cv2.split(img)

        ### Histogram
        x = np.arange(0, 256)
        hist_r, _ = np.histogram(r.ravel(), 256, [0, 255])
        hist_g, _ = np.histogram(g.ravel(), 256, [0, 255])
        hist_b, _ = np.histogram(b.ravel(), 256, [0, 255])

        ### Display histogram
        ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax[0].axis('off')
        ax[1].plot(x, hist_r, '-r')
        ax[2].set_xlim([0, 255])
        ax[2].plot(x, hist_g, '-g')
        ax[2].tick_params(length = 0)
        ax[3].set_xlim([0, 255])
        ax[3].plot(x, hist_b, '-b')
        ax[3].tick_params(length = 0)

        for i in range(1, 4) :
            ax[i].set_xlim([0, 255])
            ax[i].tick_params(axis = 'both', which = 'both', bottom = False, top = False, labelbottom = False, right = False, left = False, labelleft = False)


    ani = animation.FuncAnimation(fig, update, interval = 2000, frames = len_cats)
    plt.show()

