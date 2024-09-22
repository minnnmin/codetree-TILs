N = int(input())
jobs = [] # [id, 기간, 수익]
for i in range(N):
    jobs.append([i] + list(map(int, input().split())))

max_profit = 0
visited = [False] * N

def func(n, sum_profit):
    global max_profit

    if n > N:
        return
    else:
        max_profit = sum_profit if sum_profit > max_profit else max_profit

    for i, days, profit in jobs:
        if not visited[i]:
            visited[i] = True
            func(n + days, sum_profit + profit)
            visited[i] = False

func(0, 0)

print(max_profit)