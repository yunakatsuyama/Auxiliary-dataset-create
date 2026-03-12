import rasterio
import numpy as np
import matplotlib.cm as cm


#ntl_file = "F182010.v4/F182010.v4d_web.stable_lights.avg_vis.tif"
src_file = 'F152000.v4/F152000.v4b_web.stable_lights.avg_vis.tif'

dst_file = "F1520000.v4/nightlight_log_color.tif"

with rasterio.open(src_file) as src:
    data = src.read(1)
    profile = src.profile

# log transform
log_data = np.log10(data + 1)

# normalize
norm = (log_data - log_data.min()) / (log_data.max() - log_data.min())

# apply colormap
cmap = cm.inferno
rgb = cmap(norm)

rgb = (rgb[:, :, :3] * 255).astype(np.uint8)

profile.update(count=3, dtype=rasterio.uint8)

with rasterio.open(dst_file, "w", **profile) as dst:
    dst.write(rgb[:,:,0], 1)
    dst.write(rgb[:,:,1], 2)
    dst.write(rgb[:,:,2], 3)