import numpy as np

rng = np.random.default_rng()
a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
m = a.shape[0]
k = 4
idx = int(rng.integers(m))
selected = [idx]
diff = a - a[idx]
min_dist2 = np.abs(diff)

print(a[idx])
print(a)
print(min_dist2)

for _ in range(1, k):
    idx = int(np.argmax(min_dist2))
    selected.append(idx)
    diff = a - a[idx]
    dist2 = np.abs(diff)
    min_dist2 = np.minimum(min_dist2, dist2)
    print(a[idx])
    print(a)
    print(min_dist2)

print("Selected indices:", selected) 
print("Selected values:", a[selected])   