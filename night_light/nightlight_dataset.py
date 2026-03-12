import numpy as np
import rasterio
from rasterio.windows import from_bounds

# load center coordinates
center_lat = np.load("../../data_create/created_data/center_lat_test.npy")
center_lon = np.load("../../data_create/created_data/center_lon_test.npy")

eagrid = np.load('../../data_create/created_data/eagrid_dataset_test.npy')

print(len(center_lat), len(center_lon))

ntl_file = "F182010.v4/F182010.v4d_web.stable_lights.avg_vis.tif"

dataset = rasterio.open(ntl_file)

print(dataset.res)  # check resolution
print(dataset.bounds)

grid_size = 50
pixel_size = 0.01
half_extent = (grid_size * pixel_size) / 2   # 0.25 degrees

images = []

for lat, lon in zip(center_lat, center_lon):

    left   = lon - half_extent
    right  = lon + half_extent
    bottom = lat - half_extent
    top    = lat + half_extent

    window = from_bounds(
        left, bottom, right, top,
        transform=dataset.transform
    )
    print(window)
    data = dataset.read(
        1,
        window=window,
        out_shape=(grid_size, grid_size),
        resampling=rasterio.enums.Resampling.bilinear
    )

    images.append(data)

images = np.array(images)
print(images.shape)

np.save("ntl_grid_images.npy", images)


