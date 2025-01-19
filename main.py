from collections import defaultdict, deque
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
            score += self.a[i] * dfs(i, memo, result)
        return score
def dfs(i, memo, result):
    if result[i] == -1:
        memo[i] = 1
        return 1
    if i in memo:
        return memo[i]
    memo[i] = 1 + dfs(result[i], memo, result)
    return memo[i]


class Solver:
    '''
    問題を解くためのクラス
    '''
    def __init__(self, n, m, h, a, edges):
        self.n = n
        self.m = m
        self.h = h
        self.a = a
        self.result = [-1] * n  # 初期値: 全てのノードを親（-1） に設定
        self.graph = self.build_graph(edges)
        self.score_calculator = ScoreCalculator(n, a)
    def build_graph(self, edges):
        """辺情報からグラフを構築"""
        graph = [[] for _ in range(self.n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        return graph
    def calculate_score(self):
        return self.score_calculator.calculate_score(self.result)


    def solve(self):
        """
        0から順に見ていき、-1ならば根と設定して伸ばしていく
        ->
        """
        visited = [-1] * self.n
        for i in range(self.n):
            if self.result[i] == -1:
                self.bfs(i, visited)
        return self.result

    def bfs(self, start, visited):
        """幅優先探索"""
        visited[start] = 0
        queue = deque([start])
        while queue:
            v = queue.popleft()
            if visited[v] >= self.h:
                break
            for nv in self.graph[v]:
                if visited[nv] != -1:
                    continue
                visited[nv] = visited[v] + 1
                self.result[nv] = v
                queue.append(nv)


# 入力の読み取り部分
n,m,h = map(int, input().split())
a = list(map(int, input().split()))
edges = [tuple(map(int, input().split())) for _ in range(m)]
_ = [tuple(map(int, input().split())) for _ in range(n)]

solver = Solver(n, m, h, a, edges)
result = solver.solve()

print(" ".join(map(str, result)))

score = solver.calculate_score()
print(f"Score: {score}", file=sys.stderr)
