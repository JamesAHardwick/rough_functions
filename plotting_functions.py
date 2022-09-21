import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import itertools as it
import math as math
from scipy.special import comb


def basic_plotter(nrows, ncols, figsize,
                  plottable_list,
                  cmap_list,
                  vmax_list, vmin_list,
                  points_list,
                  colorbar_flag=True,
                  extents_flag=True):
                  
                  
    """
    
    Basic plotting function to plot images using matplotlib's imshow call.
    
    args:
        nrows, ncols:
        figsize:
        plottable_list:
        cmap_list:
        vmax_list, vmin_list:
        points_list:
        colorbar_flag:
        extents_flag:
    
    returns:
        fig, ax:
        
    """
    
    from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

    fig, ax = plt.subplots(nrows, ncols, figsize=figsize)
    
    if nrows == ncols == 1:
        
        if extents_flag:
            
            extents = extents_finder(points_list[0])
            
            im = ax.imshow(plottable_list[0], cmap=cmap_list[0],
                           vmax=vmax_list[0], vmin=vmin_list[0],
                           extent=extents)
    
        else:
                
            im = ax.imshow(abs(plottable_list[0]), cmap=cmap_list[0],
                           vmax=vmax_list[0], vmin=vmin_list[0])

            plot_edger(ax, edge_line_width=2)
        
        if colorbar_flag:

                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size='5%', pad=.1)
                plt.colorbar(im, cax=cax)
                
    else:
    
        for i, plottable in enumerate(plottable_list):
            
            if extents_flag:
                
                extents = extents_finder(points_list[i])
            
                im = ax.flat[i].imshow(plottable, cmap=cmap_list[i],
                               vmax=vmax_list[i], vmin=vmin_list[i],
                               extent=extents)
                
            else:

                im = ax.flat[i].imshow(plottable, cmap=cmap_list[i],
                                       vmax=vmax_list[i], vmin=vmin_list[i])

                plot_edger(ax.flat[i], edge_line_width=2)

            if colorbar_flag:

                divider = make_axes_locatable(ax.flat[i])
                cax = divider.append_axes("right", size='5%', pad=.1)
                plt.colorbar(im, cax=cax)
    
    return fig, ax


def extents_finder(points):


    """
    
    Finds the extents of the plane being plotted
    
    args:
        points: list of [x, y, z] coordinates for the plane being plotted.
    
    returns:
        extents: the extents in the yz, xz or xy plane for the plane to be passed to the plt.imshow call.
        
    """
    
    
    full_extents = [(1000*np.amin(points[0]), 1000*np.amax(points[0])),
                    (1000*np.amin(points[1]), 1000*np.amax(points[1])), 
                    (1000*np.amin(points[2]), 1000*np.amax(points[2]))]
    
    # ----> yz plane <----
    if full_extents[0][0] == full_extents[0][1]:
    
        extents = [full_extents[1][0], full_extents[1][1], full_extents[2][0], full_extents[2][1]]
    
    # ----> xz plane <----
    elif full_extents[1][0] == full_extents[1][1]:
    
        extents = [full_extents[0][0], full_extents[0][1], full_extents[2][0], full_extents[2][1]]
        
    # ----> xy plane <----
    elif full_extents[2][0] == full_extents[2][1]:
    
        extents = [full_extents[0][0], full_extents[0][1], full_extents[1][0], full_extents[1][1]]
    
    return extents


def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    
    """
    
    https://stackoverflow.com/questions/14720331/how-to-generate-random-colors-in-matplotlib
    
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    
    args:
        nlabels: Number of labels (size of colormap)
        type: 'bright' for strong colors, 'soft' for pastel colors
        first_color_black: Option to use first color as black, True or False
        last_color_black: Option to use last color as black, True or False
        verbose: Prints the number of labels and shows the colormap. True or False
    
    returns:
        colormap for matplotlib
        
    """
    
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np

    if type not in ('bright', 'soft'):
        print('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')
    return random_colormap
  
  
def contour_rect(im):
    
    """
    
    Creates a set of vectors which can be plotted to draw lines around the edges of coalitions
    
    args:
        im: image
    
    returns:
        lines: list of line vectors to be drawn onto a plot
    
    """
    
    lines = []
    pad = np.pad(im, [(2, 2), (2, 2)])  # zero padding
    
    im0 = np.abs(np.diff(pad, n=1, axis=0))[:, 1:]
    im1 = np.abs(np.diff(pad, n=1, axis=1))[1:, :]

    im0 = np.diff(im0, n=1, axis=1)
    starts = np.argwhere(im0 == 1) - 1
    ends = np.argwhere(im0 == -1) - 1
    lines += [([s[0]-.5, s[0]-.5], [s[1]+.5, e[1]+.5]) for s, e in zip(starts, ends)]

    im1 = np.diff(im1, n=1, axis=0).T
    starts = np.argwhere(im1 == 1) - 1
    ends = np.argwhere(im1 == -1) - 1
    lines += [([s[1]+.5, e[1]+.5], [s[0]-.5, s[0]-.5]) for s, e in zip(starts, ends)]
    
    return lines
    
    
def coalition_line_drawer(ax, segmented_CS, m, n, edge_line_width):
    
    """
    
    Creates a set of vectors which can be plotted to draw lines around the edges of coalitions
    
    args:
        ax:
        segmented_CS:
        m, n:
        num_pixels:
        edge_line_width:
    
    returns:
        None
        
    """
    
    CS_map_array = np.zeros(m*n) # segment array = positions of the various coalitions   
    for i, coalition in enumerate(segmented_CS):
        for pixel in coalition:
            CS_map_array[pixel] = i
    CS_map_array = np.reshape(CS_map_array, (m, n))
    
    contour_lines = []
    for ID in range(len(segmented_CS)):
        coalition = np.zeros(CS_map_array.size)
        coalition[list(segmented_CS[ID])] = 1
        coalition = coalition.reshape(CS_map_array.shape)
        contour_lines.append(contour_rect(coalition))
    for lines in contour_lines:
        for line in lines:
            ax.plot(line[1], line[0], color='k', lw=edge_line_width)
    return None
        
        
def plot_edger(ax, edge_line_width):

    """
    
    Creates a set of vectors which can be plotted to draw lines around the edges of coalitions
    
    args:
        ax:
        edge_line_width:
    
    returns:
        None
    
    """

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(edge_line_width)    
    ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False,
                   right=False, labelbottom=False, labelleft=False)
    return None    
    
    
def CS_structure_plotter(ax, segmented_CS, m, n, target_CS_length, font_size, edge_line_width, CS_labels=True, coalition_lines=True):

    """
    
    Creates a set of vectors which can be plotted to draw lines around the edges of coalitions
    
    args:
        ax:
        segmented_CS:
        m, n:
        font_size:
        edge_line_width:
        CS_labels:
        coalition_lines:
    
    returns:
        None
    
    """

    from matplotlib.colors import ListedColormap, LinearSegmentedColormap
    
        
    def PixIDToPos(apsize, ID):
        row = np.mod(ID, apsize[1])
        col = (ID - np.mod(ID, apsize[1])) / apsize[1]
        return int(col), int(row)

    CS_map_array = np.zeros(m*n) # segment array = positions of the various coalitions  
    
    for i, coalition in enumerate(segmented_CS):
        for pixel in coalition:
            CS_map_array[pixel] = i
    CS_map_array = np.reshape(CS_map_array, (m, n))

    cmap_list = [[1., 1., 1., 1.] for i in range(target_CS_length)]
    CS_cmap = ListedColormap(cmap_list)
    
    ax.imshow(CS_map_array, cmap=plt.get_cmap(CS_cmap))

    plot_edger(ax, edge_line_width)

    if CS_labels:
        for i, value in enumerate(np.reshape(CS_map_array, CS_map_array.size)):
            coord = PixIDToPos((m, n), i)
            ax.text(coord[1], coord[0], str(int(value+1)), ha="center", va="center", fontsize=font_size)
    
    if coalition_lines:
        coalition_line_drawer(ax, segmented_CS, m, n, edge_line_width)
    
    return None
    
    
def pareto_plotter(seg_CS_list, seg_mean_qualities_list, CS_ID, save_folder_path,
                   selected_data_label="selected data", data_label="data", save_flag=False):
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 14))
#     ax.set_title(dataset[10:].replace('_', " "), fontsize=20, pad=10)
    
    num_pixels = len(seg_mean_qualities_list)
    marker_size = 250
    color_range = plt.get_cmap("rainbow", 6)
    
    # ************* plot data for constant-diffs segmentation ****************
    ax.scatter(seg_CS_list, seg_mean_qualities_list, lw=2, color=color_range(1), label=data_label)
    ax.scatter(seg_CS_list[CS_ID], seg_mean_qualities_list[CS_ID], lw=2, color="r", label=selected_data_label)

    # x-axis formatting
    ax.set_xlabel("Number of Actuations $n_A$", fontsize=24)
    ax.set_xticks(list(np.arange(0, num_pixels+1, 4*np.sqrt(num_pixels))))
    ax.set_xticklabels([int(ix) for ix in np.arange(0, num_pixels+1, 4*np.sqrt(num_pixels))], rotation = 70, fontsize=24)

    # y-axis formatting
    ax.set_ylabel(r"Mean Acoustic Image Quality $\overline{Q}$", fontsize=28, labelpad=10)
    ax.set_yticks(list(np.arange(0, 1.01, 0.1)))
    ax.set_yticklabels(list(np.round(np.arange(0, 1.01, 0.1), 2)), fontsize=24)

    # general formatting
    ax.grid(True, axis='both', which='major', alpha=0.5, zorder=0)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    ax.tick_params('both', length=10, width=3, which='major')
    ax.tick_params('both', length=10, width=1.5, which='minor')
    ax.legend(loc="lower right", fontsize=25)
        
    # ************* saving *************
    if save_flag:    
        plt.savefig(save_folder_path+"/pareto_front_plot.png", bbox_inches='tight', transparent=True, dpi=500)
        print("saved to...", save_folder_path)