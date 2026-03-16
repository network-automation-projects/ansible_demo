import numpy as np
import matplotlib.pyplot as plt

# Define some points: circle, square, and a line
theta = np.linspace(0, 2*np.pi, 100)
circle = np.array([np.cos(theta), np.sin(theta)])          # unit circle
square = np.array([[0,0], [1,0], [1,1], [0,1], [0,0]]).T   # square
line = np.array([[0, 0], [1, 0]]).T                        # horizontal line from origin

# Combine into one set of points (columns = points)
points = np.hstack([circle, square + np.array([[0.5],[0.5]]), line])

# Define your transformation matrix here (change these numbers!)
A = np.array([[1.5, 0.5],   # example: scale x by 1.5 + shear
              [0.3, 0.8]])  # try rotation: [[0, -1], [1, 0]] or scaling [[2,0],[0,0.5]]

# Apply transformation: new_points = A @ points
transformed = A @ points

# Plot
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

# Original
ax[0].plot(points[0], points[1], 'b-', linewidth=2)
ax[0].set_title("Original")
ax[0].axis('equal')
ax[0].grid(True)
ax[0].axhline(0, color='gray', lw=0.5)
ax[0].axvline(0, color='gray', lw=0.5)

# Transformed
ax[1].plot(transformed[0], transformed[1], 'r-', linewidth=2)
ax[1].set_title("After Transformation")
ax[1].axis('equal')
ax[1].grid(True)
ax[1].axhline(0, color='gray', lw=0.5)
ax[1].axvline(0, color='gray', lw=0.5)

plt.suptitle(f"Matrix:\n{A}")
plt.tight_layout()
plt.show()