import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmcrameri.cm as cm
from matplotlib.gridspec import GridSpec
import cartopy.io.img_tiles as cimgt



# city = 'tokyo'
# target_center_lon, target_center_lat = 139.76, 35.68

# city = 'miyazaki'
# target_center_lon, target_center_lat = 131.42, 31.91

# city = "osaka"
# target_center_lon, target_center_lat = 135.50, 34.69

# city = 'nagoya'
# target_center_lon, target_center_lat = 136.91, 35.18

city = 'sapporo'
target_center_lon, target_center_lat = 141.35, 43.06

# ----------------------------
# load data
# ----------------------------
center_lat = np.load("../../data_create/created_data/center_lat_test.npy")
center_lon = np.load("../../data_create/created_data/center_lon_test.npy")

eagrid = np.load("../../data_create/created_data/eagrid_dataset_test.npy")
nightlight = np.load("data/ntl_grid_images_2000.npy")

print("nightlight shape:", nightlight.shape)
print("eagrid shape:", eagrid.shape)

# ----------------------------
# parameters
# ----------------------------
grid_size = 50
pixel_size = 0.01
half_extent = (grid_size * pixel_size) / 2

# ----------------------------
# get the closest index
# ----------------------------
dist = (center_lat - target_center_lat)**2 + (center_lon - target_center_lon)**2


idx = np.argmin(dist)

lat = center_lat[idx]
lon = center_lon[idx]

ntl_img = nightlight[idx]
eagrid_img = eagrid[idx]

# ----------------------------
# create lat lon grid
# ----------------------------
left = lon - half_extent
right = lon + half_extent
bottom = lat - half_extent
top = lat + half_extent

lon_grid = np.linspace(left, right, grid_size + 1)
lat_grid = np.linspace(bottom, top, grid_size  + 1)

x, y = np.meshgrid(lon_grid, lat_grid)


# =========================
# figure
# =========================
fig = plt.figure(figsize=(12,4))

gs = GridSpec(1,3, figure=fig)

ax0 = fig.add_subplot(gs[0], projection=ccrs.PlateCarree())
ax1 = fig.add_subplot(gs[1], sharex=ax0, sharey=ax0)
ax2 = fig.add_subplot(gs[2], sharex=ax0, sharey=ax0)

axes = [ax0, ax1, ax2]

# =========================
# map
# =========================
tiler = cimgt.GoogleTiles(style="satellite")
gl = ax0.gridlines(
    draw_labels=True,
    linewidth=0.3,
    linestyle="--",
    color="gray"
)

gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {"size":8}
gl.ylabel_style = {"size":8}

ax0 = fig.add_subplot(gs[0], projection=ccrs.PlateCarree())

ax0.set_extent([left, right, bottom, top], crs=ccrs.PlateCarree())

ax0.add_image(tiler, 12)

# same grid
# dummy = np.zeros_like(ntl_img)

# ax0.pcolormesh(
#     x, y, dummy,
#     edgecolors="lightgray",
#     linewidth=0.1,
#     facecolor="none",
#     transform=ccrs.PlateCarree()
# )

# center point
ax0.scatter(
    lon, lat,
    color="red",
    s=40,
    transform=ccrs.PlateCarree(),
    zorder=5
)

ax0.set_title("Location (Satellite)")

# =========================
# nightlight
# =========================
norm=mcolors.Normalize(vmin=0,vmax=1.806)
im=ax1.pcolormesh(
    x,y,np.log10(ntl_img + 1),
    norm=norm,
    cmap="inferno",
    edgecolors="lightgray",
    linewidth=0.2
)

cb=plt.colorbar(im,ax=ax1,shrink=0.8)
cb.set_label("log10(Nightlight)")

ax1.set_title("Nightlight")

# =========================
# eagrid
# =========================
cmap=cm.roma_r
norm=mcolors.Normalize(vmin=2.5,vmax=6.5)

sc=ax2.pcolormesh(
    x,y,np.log10(eagrid_img),
    cmap=cmap,
    norm=norm,
    edgecolors="lightgray",
    linewidth=0.2
)

cb=plt.colorbar(sc,ax=ax2,shrink=0.8)
cb.set_label("log10(EAGrid)")

ax2.set_title("EAGrid")

# =========================
# same extent
# =========================
for ax in axes:
    ax.set_xlim(left,right)
    ax.set_ylim(bottom,top)

# =========================
# perfect square
# =========================
for ax in axes:
    ax.set_box_aspect(1)

plt.tight_layout()
plt.savefig(f'plots/{city}.png')
plt.show()