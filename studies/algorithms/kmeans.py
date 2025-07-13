import math
import numpy as np


def run_kmeans(data, centers):
    _centers = centers

    print(f'First centers are = {centers}')

    k = 0
    while k < 10:
        for xy in data:
            # print(f'Finding nearest center for {xy}')
            nearest_center = find_nearest_center(xy, _centers)
            xy[2] = nearest_center[2]

        a, b, c = [], [], []
        for xy in data:
            if xy[2] == 'a':
                a.append(xy)
            elif xy[2] == 'b':
                b.append(xy)
            elif xy[2] == 'c':
                c.append(xy)
            else:
                raise Exception(f'No cluster associated to ${xy}')

        # print(f'This is a={a}')
        # print(f'This is b={b}')
        # print(f'This is c={c}')

        a_xy_mean = calculate_means(a)
        b_xy_mean = calculate_means(b)
        c_xy_mean = calculate_means(c)
        _centers = [a_xy_mean + ['a'], b_xy_mean + ['b'], c_xy_mean + ['c']]

        k += 1

    return data, _centers

def find_nearest_center(datapoint, cc):
    # Returns x, y of nearest center
    x, y = datapoint[0], datapoint[1]
    # print(f'This is cc={cc}')
    
    distances = list()
    for item in cc:
        x_, y_ = item[0], item[1]
        distances.append(math.sqrt((x_ - x)**2 + (y_ - y)**2))
    return cc[np.argmin(distances)]

def calculate_means(data):
    mean_0 = sum(row[0] for row in data) / len(data)
    mean_1 = sum(row[1] for row in data) / len(data)
    return [mean_0, mean_1]

def get_centroid():
    pass

# x, y
centers = [
    [6, 6, 'a'],
    [4, 6, 'b'],
    [5, 10, 'c']
]

data = [
    [1, 2, ''],
    [2, 1, ''],
    [1, 1, ''],
    [2, 2, ''],
    [8, 9, ''],
    [9, 8, ''],
    [9, 9, ''],
    [8, 8, ''],
    [1, 15, ''],
    [2, 15, ''],
    [1, 14, ''],
    [2, 14, '']
]

new_data, new_centers = run_kmeans(data, centers)

print(f'Centers = {new_centers}')
print(f'Data = {new_data}')