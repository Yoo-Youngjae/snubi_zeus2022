from math import *
import numpy as np
from numpy import dot
from numpy.linalg import norm
from scipy.spatial import distance
import hashlib
from sklearn.metrics import top_k_accuracy_score
import torch


# similarity metric은 클수록 유사
def cos_sim(A, B):
    return [dot(i, B)/(norm(i)*norm(B)) for i in A]


def improved_sqrt_cos_sim(A, B):
    return [dot(np.sqrt(i+0.0001), np.sqrt(B+0.0001))/(np.sqrt(norm(i, ord=1))*np.sqrt(norm(B, ord=1))) for i in A]


def dot_sim(A, B):
    return [dot(i,B) for i in A]

# jaccard sim은 딱히 적절치 않은...?


# distance metric은 작을수록 유사
def euclidean_dis(A, B):
    return [distance.euclidean(i,B) for i in A]


# higer dimension에서는 L2 norm 보다 L1 norm이 더 효과적이라고 함
def manhattan_dis(A, B):
    return [distance.cityblock(i,B) for i in A]


# order을 파라매터로 지정 가능
def minkowski_dis(A, B, p=1792): # p is order parameter. 만약 지정해주지 않는다면 우리 feature output 크기 default
    return [distance.minkowski(i, B, p) for i in A]


def get_key(p_vec, q_vec):
    """
    This method returns a unique hash value for two vectors. The hash value is equal to the concatenated string of
    the hash value for vector one and vector two. E.g. is hash(p_vec) = 1234 and hash(q_vec) = 5678 then get_key(
    p_vec, q_vec) = 12345678. Memoization improved the speed of this algorithm 400%.
    :param p_vec: vector one
    :param q_vec: vector two
    :return: a unique hash
    """
    # return str(hash(tuple(p_vec))) + str(hash(tuple(q_vec)))
    return str(hashlib.sha1(p_vec)) + str(hashlib.sha1(q_vec))


def fractional_dis(p_vec, q_vec, fraction=2):
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
    e = 0.001
    # memoization is used to reduce unnecessary calculations ... makes a BIG difference
    memoize = True

    if torch.is_tensor(p_vec):
        p_vec = p_vec.numpy()

    if torch.is_tensor(q_vec):
        q_vec = q_vec.numpy()

    sim_np = []
    for i in p_vec:
        if memoize:
            key = get_key(i, q_vec)
            x = memoization.get(key)
            if x is None:
                diff = i - q_vec
                diff_fraction = diff**fraction
                sim_np.append(max(pow(np.sum(diff_fraction), 1/fraction), e))
            else:
                sim_np.append(x)
        else:
            diff = i - q_vec
            diff_fraction = diff**fraction
            sim_np.append(max(pow(np.sum(diff_fraction), 1/fraction), e))

    return sim_np


def similarity_calculation(metric, full_database_features, object):
    if metric == "all":
        return [cos_sim(full_database_features, object),
                improved_sqrt_cos_sim(full_database_features, object),
                dot_sim(full_database_features, object),
                euclidean_dis(full_database_features, object),
                manhattan_dis(full_database_features, object),
                minkowski_dis(full_database_features, object, 10),
                fractional_dis(full_database_features, object)]
    elif metric == "cos_sim":
        return cos_sim(full_database_features, object)
    elif metric == "improved_sqrt_cos_sim":
        return improved_sqrt_cos_sim(full_database_features, object)
    elif metric == "dot_sim":
        return dot_sim(full_database_features, object)
    elif metric == "euclidean_dis":
        return euclidean_dis(full_database_features, object)
    elif metric == "manhattan_dis":
        return manhattan_dis(full_database_features, object)
    elif metric == "minkowski_dis":
        return minkowski_dis(full_database_features, object)
    elif metric == "fractional_dis":
        return fractional_dis(full_database_features, object)


def poll(sim_np, m='max', top_k=3):
    k = top_k
    sim_list = list(sim_np)
    if m == 'max':
        temp = sorted(sim_list, reverse=True)[:k]
    else:
        temp = sorted(sim_list, reverse=False)[:k]

    return [sim_list.index(temp[i]) for i in range(top_k)]


def is_top_k(database_df, test_product_id, sim_np, m='max', top_k=3):
    k = top_k
    sim_list = list(sim_np)
    if m == 'max':
        temp = sorted(sim_list, reverse=True)[:k]
        temp = [database_df['product_id'][sim_list.index(temp[i])] for i in range(top_k)]

        if test_product_id in temp:
            return 1
        else:
            return 0

    if m == 'min':
        temp = sorted(sim_list, reverse=False)[:k]
        temp = [database_df['product_id'][sim_list.index(temp[i])] for i in range(top_k)]

        if test_product_id in temp:
            return 1
        else:
            return 0


def print_top_k_values(database_df, test_product_id, sim_np, m='max', top_k=3):
    sim_list = list(sim_np)
    if m == 'max':
        temp = sorted(sim_list, reverse=True)[:top_k]
        list_max = []
        for m in temp:
            list_max.append([sim_list.index(m), m])

        print(f"[{test_product_id == database_df['product_id'][list_max[0][0]]}][test_product_id: {test_product_id}] and pred[product_id, sim] => "
              f"max=[{database_df['product_id'][list_max[0][0]]}, {list_max[0][1]}], "
              f"max-1=[{database_df['product_id'][list_max[1][0]]}, {list_max[1][1]}], "
              f"max-2=[{database_df['product_id'][list_max[2][0]]}, {list_max[2][1]}], "
              f"mean_dis_sim: {np.mean(sim_list)}, var_dis_sim: {np.var(sim_list)}")

    if m == 'min':
        temp = sorted(sim_list, reverse=False)[:top_k]
        list_min = []
        for m in temp:
            list_min.append([sim_list.index(m), m])

        print(
            f"{test_product_id == database_df['product_id'][list_min[0][0]]}][test_product_id: {test_product_id}] and pred[product_id, sim] => "
            f"min=[{database_df['product_id'][list_min[0][0]]}, {list_min[0][1]}], "
            f"min-1=[{database_df['product_id'][list_min[1][0]]}, {list_min[1][1]}], "
            f"min-2=[{database_df['product_id'][list_min[2][0]]}, {list_min[2][1]}], "
            f"mean_dis_sim: {np.mean(sim_list)}, var_dis_sim: {np.var(sim_list)}")


def print_top_k_metric_result(top_k_accuracy):
    print('<Top 1 Accuracy | Top 3 Accuracy>')
    print(f'{np.average(top_k_accuracy[0])} | {np.average(top_k_accuracy[1])}')


def print_all_top_k_metric_result(all_top_k_accuracy):
    similarity_name_list = ['cos_sim',
     'improved_sqrt_cos_sim',
     'dot_sim',
     'euclidean_dis',
     'manhattan_dis',
     'minkowski_dis',
     'fractional_dis']

    print('<Top 1 Accuracy | Top 3 Accuracy>')
    for idx, top_k_accuracy in enumerate(all_top_k_accuracy):
        print(f"{similarity_name_list[idx]}: {np.average(top_k_accuracy[0])} | {np.average(top_k_accuracy[1])}")

