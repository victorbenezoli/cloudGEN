import netCDF4 as nc4
import numpy as np

def main(infname):

    infile = nc4.Dataset(infname, "r")

    try:
        lat = infile.variables['lat'][:]
        lon = infile.variables['lon'][:]
    except:
        lat = infile.variables['latitude'][:]
        lon = infile.variables['longitude'][:]

    time = infile.variables['time'][:]
    t_units = getattr(infile.variables['time'],'units',False)
    date = nc4.num2date(time[0], units = t_units)
    year = date.year

    slat = np.min(lat)
    nlat = np.max(lat)
    wlon = np.min(lon)
    elon = np.max(lon)

    xlen = np.abs(lon[1] - lon[0])
    ylen = np.abs(lat[1] - lat[0])

    return year, slat, nlat, wlon, elon, ylen, xlen

if __name__ == '__main__':
    main()
