import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Grid size
W, H = 120, 80

# Build palette (black → red → orange → yellow → white)
palette = []
for i in range(256):
    r = min(255, int(i * 1.1))
    g = min(255, int(max(0, (i - 64) * 1.3)))
    b = min(255, int(max(0, (i - 160) * 0.8)))
    palette.append((r, g, b))
palette = np.array(palette, dtype=np.uint8)

# Fire grid
fire = np.zeros((H, W), dtype=np.uint8)

# Update function
def update(frame):
    global fire
    # Heat source at bottom
    fire[-1, :] = np.random.randint(180, 255, size=W, dtype=np.uint8)

    # Propagate upwards
    below = fire[1:, :]
    left = np.pad(below[:, :-1], ((0,0),(1,0)), mode='edge')
    right = np.pad(below[:, 1:], ((0,0),(0,1)), mode='edge')
    avg = (below + left + right) // 3
    cooled = np.clip(avg - np.random.randint(0, 6, size=avg.shape), 0, 255)
    fire[:-1, :] = cooled

    # Map to RGB
    rgb = palette[fire]
    im.set_array(rgb)
    return [im]

# Plot setup
fig, ax = plt.subplots(figsize=(6,4))
im = ax.imshow(palette[fire], interpolation="nearest")
ax.axis("off")

# Animate
ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
HTML(ani.to_jshtml())
