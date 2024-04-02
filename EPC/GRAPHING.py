import numpy as np
from qiskit.visualization import plot_bloch_vector
 
# You can use spherical coordinates instead of cartesian.
 
plot_bloch_vector([1, np.pi/2, np.pi/3], coord_type='spherical')