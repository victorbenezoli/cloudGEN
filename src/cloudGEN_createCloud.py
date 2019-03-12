# encoding: utf-8

import numpy as np
import sys
import os
import fnmatch as fm
import netCDF4 as nc4
import calendar as cl
import cftime

sys.path.append('src/')
from cloudGEN_createSo import createSo

def main(infolder,outfolder,outpattern,invname,outvname,coefa,coefb):

    fnames = fm.filter(os.listdir(infolder),'*.nc')

    if np.size(fnames) == 0:
        errmsg = 1000
        return errmsg
        exit()

    Ro0 = createSo(infolder, 0)
    Ro1 = createSo(infolder, 1)

    for fname in fnames:

        filename = infolder+str(fname)
        infile = nc4.Dataset(filename, 'r')
        try:
            rad = infile.variables[invname][:]
            errmsg = "Success!"
        except:
            errmsg = 2000
            return errmsg
            exit()

        time = infile.variables['time'][:]
        t_units = getattr(infile.variables['time'],'units',False)
        date = nc4.num2date(time[0], units = t_units)
        isleap = cl.isleap(date.year)

        try:
            lat = infile.variables['lat'][:]
            lon = infile.variables['lon'][:]
        except:
            lat = infile.variables['latitude'][:]
            lon = infile.variables['longitude'][:]

        if (isleap):
            Ro = Ro1
        else:
            Ro = Ro0

        ntim = np.size(time)
        nlat = np.size(lat)
        nlon = np.size(lon)

        cld = np.zeros(shape = (ntim,nlat,nlon))

        for i in range(0, ntim):
            for j in range(0, nlon):
                cld[i,:,j] = (1 - (((rad[i,:,j] / Ro[i,:]) - coefa) / (coefb))) * 100

        cld = np.where(np.isneginf(cld),-999.99,cld)
        cld = np.where(np.isinf(cld),-999.99,cld)
        cld = np.where(np.isnan(cld),-999.99,cld)

        cld = np.where(cld > 100, 100, np.where(cld < 0, 0, cld))

        ofname = outfolder+outpattern+str(date.year)+".nc"

        outncfile = nc4.Dataset(ofname,'w',format='NETCDF4_CLASSIC')

        time_values = time

        latitude = outncfile.createDimension("latitude", nlat)
        longituded = outncfile.createDimension("longitude", nlon)
        time = outncfile.createDimension("time", None)
        time.isunlimited()

        times = outncfile.createVariable("time",np.float32,("time",))
        latitudes = outncfile.createVariable("latitude",np.float32,("latitude",))
        longitudes = outncfile.createVariable("longitude",np.float32,("longitude",))
        clds = outncfile.createVariable(varname = outvname,
                                      datatype = np.float32,
                                      dimensions = ("time","latitude","longitude",),
                                      fill_value = -999.99)

        latitudes.units = "degrees_north"
        latitudes.long_name = "latitude"

        longitudes.units = "degrees_east"
        longitudes.long_name = "longitude"

        times.units = t_units
        times.long_name = "time"

        clds.units = "%"
        clds.long_name = "cloud cover"

        latitudes[:] = lat
        longitudes[:] = lon
        times[:] = np.array(time_values)

        clds[:] = cld

        outncfile.close()

    return 0

if __name__ == '__main__':
    main()
