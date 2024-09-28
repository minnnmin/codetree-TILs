N = int(input())
dust = [list(map(int, input().split())) for _ in range(N)]

tmp = []
for i in range(1, N):
    tmp.append(i)
    tmp.append(i)
tmp.append(N-1)

# (이동방향, 이동크기)
order_list = [] # [(0, 1), (1, 1), (2, 2), (3, 2), (0, 3), (1, 3), (2, 4), (3, 4), (0, 4)]
for i in range(len(tmp)):
    order_list.append((i%4, tmp[i]))