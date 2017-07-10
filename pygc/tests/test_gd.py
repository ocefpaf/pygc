import os
import unittest
import numpy as np
from pygc import great_distance


class GreatDistanceTest(unittest.TestCase):

    def test_great_distance_scalars(self):
        # One decimal degree at the equator is about 111.32km
        latitude_start  = 0.
        latitude_end    = 0.
        longitude_start = 50.
        longitude_end   = 52.
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert np.round(gd['distance'] / 1000, 2) == 111.32 * 2

        # One decimal degree is 111000m
        latitude_start  = 0.
        latitude_end    = 0.
        longitude_start = [49., 75.]
        longitude_end   = [50., 76.]
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert np.allclose(gd["distance"] / 1000, 111.32)

        latitude_start  = np.nan
        latitude_end    = np.nan
        longitude_start = np.nan
        longitude_end   = np.nan
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert np.isnan(gd['distance'])

    def test_great_distance_numpy(self):
        latitude_start  = np.asarray([0.])
        latitude_end    = np.asarray([0.])
        longitude_start = np.asarray([50.])
        longitude_end   = np.asarray([52.])
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert np.round(gd['distance'] / 1000, 2) == 111.32 * 2

        latitude_start  = np.asarray([0.])
        latitude_end    = np.asarray([0.])
        longitude_start = 50.
        longitude_end   = 52.
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert np.round(gd['distance'] / 1000, 2) == 111.32 * 2

    def test_great_distance_masked_numpy(self):
        with self.assertRaises(ValueError):
            latitude_start  = np.ma.asarray([0.])
            latitude_end    = 0.
            longitude_start = 50.
            longitude_end   = 52.
            great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)

        latitude_start  = np.ma.asarray([0.])
        latitude_end    = np.ma.asarray([0.])
        longitude_start = np.ma.asarray([50.])
        longitude_end   = np.ma.asarray([52.])
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert np.round(gd['distance'] / 1000, 2) == 111.32 * 2

        xmask = np.load(os.path.join(os.path.dirname(__file__), 'xmask.npy'))
        ymask = np.load(os.path.join(os.path.dirname(__file__), 'ymask.npy'))
        xdata = np.load(os.path.join(os.path.dirname(__file__), 'x.npy'))
        x = np.ma.fix_invalid(xdata, mask=xmask)
        ydata = np.load(os.path.join(os.path.dirname(__file__), 'y.npy'))
        y = np.ma.fix_invalid(ydata, mask=ymask)
        gd = great_distance(start_latitude=y[0:-1], start_longitude=x[0:-1], end_latitude=y[1:], end_longitude=x[1:])

        latitude_start  = np.ma.MaskedArray(np.ma.asarray([0.]), mask=[1])
        latitude_end    = np.ma.MaskedArray(np.ma.asarray([0.]), mask=[1])
        longitude_start = np.ma.MaskedArray(np.ma.asarray([50.]), mask=[1])
        longitude_end   = np.ma.MaskedArray(np.ma.asarray([52.]), mask=[1])
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert np.all(gd['distance'].mask == True)  # noqa
        assert np.all(gd['azimuth'].mask == True)  # noqa
        assert np.all(gd['reverse_azimuth'].mask == True)  # noqa

        latitude_start  = np.ma.MaskedArray(np.ma.asarray([0., 1.]), mask=[1, 0])
        latitude_end    = np.ma.MaskedArray(np.ma.asarray([0., 1.]), mask=[1, 0])
        longitude_start = np.ma.MaskedArray(np.ma.asarray([49., 75.]), mask=[1, 0])
        longitude_end   = np.ma.MaskedArray(np.ma.asarray([50., 76.]), mask=[1, 0])
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert gd['distance'].mask.tolist() == [True, False]
        assert gd['azimuth'].mask.tolist() == [True, False]
        assert gd['reverse_azimuth'].mask.tolist() == [True, False]

        latitude_start  = np.ma.MaskedArray(np.ma.asarray([0., 1.]), mask=[1, 1])
        latitude_end    = np.ma.MaskedArray(np.ma.asarray([0., 1.]), mask=[1, 1])
        longitude_start = np.ma.MaskedArray(np.ma.asarray([49., 75.]), mask=[1, 1])
        longitude_end   = np.ma.MaskedArray(np.ma.asarray([50., 76.]), mask=[1, 1])
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert gd['distance'].mask.tolist() == [True, True]
        assert gd['azimuth'].mask.tolist() == [True, True]
        assert gd['reverse_azimuth'].mask.tolist() == [True, True]

    def test_great_distance_empty_numpy(self):
        latitude_start  = np.ma.asarray([])
        latitude_end    = np.ma.asarray([])
        longitude_start = np.ma.asarray([])
        longitude_end   = np.ma.asarray([])
        gd = great_distance(start_latitude=latitude_start, start_longitude=longitude_start, end_latitude=latitude_end, end_longitude=longitude_end)
        assert np.all(gd['distance'].mask == True)  # noqa
        assert np.all(gd['azimuth'].mask == True)  # noqa
        assert np.all(gd['reverse_azimuth'].mask == True)  # noqa
