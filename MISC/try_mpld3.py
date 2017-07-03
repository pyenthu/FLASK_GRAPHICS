import matplotlib.pyplot as plt
import mpld3
import webbrowser, pprint
import numpy as np
from mpl_toolkits.basemap import Basemap
from osgeo import gdal


def write_file(html_txt, file_name):
    f = open(file_name, 'w')
    f.write(html_txt)
    f.close()

def try_mpld3_html():
    fig, ax = plt.subplots()
    np.random.seed(0)
    x, y = np.random.normal(size=(2, 100))
    color, size = np.random.random((2, 100))

    ax.scatter(x, y, c=color, s=200* size, alpha=0.3)
    ax.grid(color='lightgray', alpha=0.7)
    mpld3_html = mpld3.fig_to_html(fig)
    write_file(mpld3_html, 'new.html')
    webbrowser.open_new('new.html')
    plt.show()

    print(mpld3_html)

    print(mpld3.fig_to_dict(fig))

    return mpld3_html

def draw_map_1():

    # set up orthographic map projection with
    # perspective of satellite looking down at 50N, 100W.
    # use low resolution coastlines.
    map = Basemap(projection='ortho', lat_0=45, lon_0=-100, resolution='l')
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    map.fillcontinents(color='coral', lake_color='aqua')
    # draw the edge of the map projection region (the projection limb)
    map.drawmapboundary(fill_color='aqua')
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 30))
    # make up some data on a regular lat/lon grid.
    nlats = 73;
    nlons = 145;
    delta = 2. * np.pi / (nlons - 1)
    lats = (0.5 * np.pi - delta * np.indices((nlats, nlons))[0, :, :])
    lons = (delta * np.indices((nlats, nlons))[1, :, :])
    wave = 0.75 * (np.sin(2. * lats) ** 8 * np.cos(4. * lons))
    mean = 0.5 * np.cos(2. * lats) * ((np.sin(2. * lats)) ** 2 + 2.)
    # compute native map projection coordinates of lat/lon grid.
    x, y = map(lons * 180. / np.pi, lats * 180. / np.pi)
    # contour data over the map.
    cs = map.contour(x, y, wave + mean, 15, linewidths=1.5)
    plt.title('contour lines over filled continent background')
    plt.show()

def draw_map_2():

    map = Basemap(projection='cyl')

    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='coral',lake_color='aqua')
    map.drawcoastlines()

    plt.show()

def draw_map_3():

    map = Basemap(llcrnrlon=-20.5, llcrnrlat=35, urcrnrlon=50., urcrnrlat=72.,
                  resolution='i', projection='tmerc', lon_0=10, lat_0=50)

    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='coral', lake_color='aqua')
    map.drawcoastlines()

    plt.show()


def bak_map():

    #map = Basemap(llcrnrlon=22.9572, llcrnrlat=72.7189, urcrnrlon=23.0156, urcrnrlat=72.77722,
    #              resolution='i', projection='tmerc', lat_0=25, lon_0=72.75)


    map = Basemap(llcrnrlon=22.9572, llcrnrlat=72.7189, urcrnrlon=45, urcrnrlat=72.77722,
                  resolution='i', projection='tmerc', lat_0=30.5, lon_0=72.75)

    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='coral', lake_color='aqua')
    map.drawcoastlines()

    plt.show()

if __name__ == '__main__':

    # try_mpld3_html()
    #draw_map_1()
    draw_map_3()
    #bak_map()
