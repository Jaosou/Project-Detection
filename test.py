import numpy as np
from numpy.linalg import norm

# Hu moments จากรูปที่ 1
m1 = np.array([ 2.74301701e-03,  3.02146222e-08,  9.31428399e-11,  4.69034559e-11,
  1.37082872e-23, -7.41672798e-15, -3.10011466e-21])

# Hu moments จากรูปที่ 2
m2 = np.array([2.13620021e-03, 4.90558728e-08, 5.31007617e-12, 3.74187546e-11,
               4.92446176e-22, 6.18573439e-15, 1.88955558e-22])

# 1) Euclidean Distance
euclidean = norm(m1 - m2)

# 2) Cosine Similarity
cosine = np.dot(m1, m2) / (norm(m1) * norm(m2))

print("Euclidean distance =", euclidean)
print("Cosine similarity =", cosine)