from collections import defaultdict, deque
import numpy as np
import sys
sys.setrecursionlimit(1000000)


class ScoreCalculator:
    '''
    score計算用のクラス
    '''
    def __init__(self, n, a):
        self.n = n
        self.a = a
    def calculate_score(self, result):
        """現在の解 `result` を元にスコアを計算する"""
        # メモ化再帰でやるしかない
        memo = {}
        score = 1
        for i in range(self.n):
            score += self.a[i] * dfs_for_score(i, memo, result)
        return score
def dfs_for_score(i, memo, result):
    if result[i] == -1:
        memo[i] = 1
        return 1
    if i in memo:
        return memo[i]
    memo[i] = 1 + dfs_for_score(result[i], memo, result)
    return memo[i]


class Solver:
    '''
    問題を解くためのクラス
    '''
    def __init__(self, n, m, h, a, edges):
        self.n = n
        self.m = m
        self.h = h
        self.a = np.array(a)
        self.result = [-1] * n  # 初期値: 全てのノードを親（-1） に設定
        self.final_result = None
        self.graph = self.build_graph(edges)
        self.score_calculator = ScoreCalculator(n, a)
    def build_graph(self, edges):
        """辺情報からグラフを構築"""
        graph = [[] for _ in range(self.n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        # graphについて、aの値が小さくなるようにソート
        for i in range(self.n):
            graph[i].sort(key=lambda x: self.a[x])
        return graph
    def calculate_score(self, res):
        return self.score_calculator.calculate_score(res)


    def solve(self):
        """
        a[i]が小さい順に並べて、a[i]が小さい順に頂点を見ていく
        """
        sorted_indices = np.argsort(self.a)
        visited = [-1] * self.n
        for i in sorted_indices:
            if self.result[i] == -1:
                visited[i] = 0
                self.dfs(i, visited)
        now_score = self.calculate_score(self.result)
        self.final_result = [i for i in self.result]
        self.random_solve(sorted_indices, now_score)
        return self.final_result

    def random_solve(self, sorted_indices, now_score):
        """
        a[i]が小さい順に並べて、a[i]が小さい順に頂点を見ていく
        """
        # sorted_indicesの最初の10個をランダムに入れ替える
        for _ in range(1000000):
            np.random.shuffle(sorted_indices[:100])
            self.result = [-1] * self.n
            visited = [-1] * self.n
            for i in sorted_indices:
                if self.result[i] == -1:
                    visited[i] = 0
                    self.dfs(i, visited)
            score = self.calculate_score(self.result)
            if score > now_score:
                self.final_result = [i for i in self.result]
                now_score = score
            return self.final_result

    def dfs(self, now, visited):
        """深さ優先探索"""
        if visited[now] >= self.h:
            return
        for nv in self.graph[now]:
            if visited[nv] != -1:
                continue
            visited[nv] = visited[now] + 1
            self.result[nv] = now
            self.dfs(nv, visited)


# 入力の読み取り部分
n,m,h = map(int, input().split())
a = list(map(int, input().split()))
edges = [tuple(map(int, input().split())) for _ in range(m)]
_ = [tuple(map(int, input().split())) for _ in range(n)]

solver = Solver(n, m, h, a, edges)
result = solver.solve()

print(" ".join(map(str, result)))

score = solver.calculate_score(result)
print(score, file=sys.stderr)
