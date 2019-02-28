# encoding: utf-8

import numpy as np
import sys
import os
import fnmatch as fm
import netCDF4 as nc4
import calendar as cl
import datetime

sys.path.append('src/')
from claudio_createSo import createSo

def main(infile,outfile,vname):

    fnames = fm.filter(os.listdir(infile),'*.nc')

    if np.size(fnames) == 0:
        errmsg = "Nenhum arquivo NetCDF foi encontrado!"
        exit()

    Ro0 = createSo(infile, 0)
    Ro1 = createSo(infile, 1)

    coefa = 0.251
    coefb = 0.509

    for fname in fnames:

        filename = str(infile)+str(fname)
        infile = nc4.Dataset(filename, 'r')
        try:
            rad = infile.variables[vname][:]
            errmsg = "Sucesso!"
        except:
            errmsg = "Variável "+vname+" não encontrada no arquivo netCDF."
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

        ofname = outfile+"cld.daily."+str(date.year)+".nc"

        outfile = nc4.Dataset(ofname,'w',format='NETCDF4_CLASSIC')

        time_values = time

        latitude = outfile.createDimension("latitude", nlat)
        longituded = outfile.createDimension("longitude", nlon)
        time = outfile.createDimension("time", None)
        time.isunlimited()

        times = outfile.createVariable("time",np.float32,("time",))
        latitudes = outfile.createVariable("latitude",np.float32,("latitude",))
        longitudes = outfile.createVariable("longitude",np.float32,("longitude",))
        clds = outfile.createVariable(varname = "cld",
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

if __name__ == '__main__':
    main()
