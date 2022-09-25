from math import *
import numpy as np
from numpy import dot
from numpy.linalg import norm
from scipy.spatial import distance

# similarity metric은 클수록 유사 
def cos_sim(A, B):
  return dot(A, B)/(norm(A)*norm(B))

def imporved_sqrt_cos_sim(A, B):
  return dot(sqrt(A), sqrt(B))/(sqrt(norm(A, ord=1))*sqrt(norm(B, ord=1)))

def dot_sim(A, B):
    return dot(A,B)

# jaccard sim은 딱히 적절치 않은...?

# distance metric은 작을수록 유사
def euclidean_dis(A, B):
    return distance.euclidean(A,B)

# higer dimension에서는 L2 norm 보다 L1 norm이 더 효과적이라고 함
def manhattan_dis(A, B):
    return distance.cityblock(A,B)

# order을 파라매터로 지정 가능
def minkowski_dis(A, B, p=1792): # p is order parameter. 만약 지정해주지 않는다면 우리 feature output 크기 default
    distance.minkowski(A, B, p)

def fractional_distance(self, p_vec, q_vec, fraction=2.0):
    """
    This method implements the fractional distance metric. I have implemented memoization for this method to reduce
    the number of function calls required. The net effect is that the algorithm runs 400% faster. A similar approach
    can be used with any of the above distance metrics as well.
    :param p_vec: vector one
    :param q_vec: vector two
    :param fraction: the fractional distance value (power)
    :return: the fractional distance between vector one and two
    """
    memoization = {}

    # memoization is used to reduce unnecessary calculations ... makes a BIG difference
    memoize = True
    if memoize:
        key = self.get_key(p_vec, q_vec)
        x = memoization.get(key)
        if x is None:
            diff = p_vec - q_vec
            diff_fraction = diff**fraction
            return max(pow(np.sum(diff_fraction), 1/fraction), self.e)
        else:
            return x
    else:
        diff = p_vec - q_vec
        diff_fraction = diff**fraction
        return max(pow(np.sum(diff_fraction), 1/fraction), self.e)


def metric_result(j, idx, sim_list):
    list_argmax = []
    list_max = []

    for i in range(3):
        list_argmax.append(np.argmax(np.array(sim_list)))
        list_max.append(max(sim_list))
        if i == 2:
            break
        sim_list.remove(list_max[i])

    print(f"[object: {j}, target: {idx}] => max: [{list_argmax[0]}, {list_max[0]}], max-1: [{list_argmax[1]}, {list_max[1]}], max-2: [{list_argmax[2]}, {list_max[2]}], mean_dis_sim: {np.mean(sim_list)}, var_dis_sim: {np.var(sim_list)}")
