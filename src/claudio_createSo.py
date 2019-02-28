# encoding: utf-8

import numpy as np
import argparse
import netCDF4 as nc4
import fnmatch as fm
import os
import calendar as cl


def createSo(infile,isleap):

    if (isleap != 0 and isleap != 1):
        print("Option --isleap needs to be 0 (non-leap year) or 1 (leap year).")
        exit()

    fname = fm.filter(os.listdir(infile),'*.nc')

    if (np.size(fname) == 0):
        print("Nenhum arquivo NetCDF foi encontrado!")
        exit()

    filename = infile+fname[0]
    infile = nc4.Dataset(filename,'r')

    try:
        lat = infile.variables['lat'][:]
    except:
        lat = infile.variables['latitude'][:]

    nlat = np.size(lat)

    if (isleap == 0):
        ndays = 365
    else:
        ndays = 366

    H = np.zeros(shape = (ndays,nlat))
    Ro = np.zeros(shape = (ndays,nlat))

    delta = [23.45 * np.sin(np.deg2rad(360 * (284 + i) / 365)) for i in range(0, ndays)]

    x = [np.deg2rad(2 * np.pi * (i - 1) / ndays) for i in range(0, ndays)]

    for i in range(0, ndays):
        for j in range(0, nlat):
            H[i,j] = np.arccos(min(1.0,(max((-np.tan(np.deg2rad(lat[j]))*np.tan(np.deg2rad(delta[i]))),-1.0))))

    esd = [1.000110+(0.034221*np.cos(x[i]))+(0.001280*np.sin(x[i]))+(0.000719*np.cos(2*x[i]))+(0.000077*np.sin(2*x[i])) for i in range(0, ndays)]

    for i in range(0, ndays):
        for j in range(0, nlat):
            Ro[i,j] = 11.574074074 * (37.60 * esd[i] * ((H[i,j] * np.sin(np.deg2rad(lat[j])) * np.sin(np.deg2rad(delta[i]))) +
                     (np.cos(np.deg2rad(lat[j])) * np.cos(np.deg2rad(delta[j])) * np.sin(H[i,j]))))

    return np.matrix(Ro)

if __name__ == '__main__':
    createSo()
