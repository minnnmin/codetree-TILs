N = int(input())
jobs = [] # [시작 가능 일, 기간, 수익]
for i in range(N):
    jobs.append([i+1] + list(map(int, input().split())))

max_profit = 0
visited = [False] * (N+1)

# job_start_day: 새 작업 시작 가능일
# job_end_day: 이전 작업 종료일
def func(job_start_day, job_end_day, sum_profit):
    global max_profit

    if job_end_day > N:
        return
    else:
        max_profit = sum_profit if sum_profit > max_profit else max_profit

    for i, days, profit in jobs:
        if not visited[i] and i == job_start_day:
            visited[i] = True
            func(job_start_day + days, job_end_day + days, sum_profit + profit)
            visited[i] = False
        elif not visited[i] and i > job_start_day:
            visited[i] = True
            func(i + days, i + days - 1, sum_profit + profit)
            visited[i] = False

func(1, 0, 0)

print(max_profit)