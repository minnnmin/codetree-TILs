N, M, T = map(int, input().split())
dust = [] # 먼지 정보 저장
add_dust = [[0 for _ in range(M)] for _ in range(N)]

wind = [] # tc1 [[2, 0], [3, 0]]

for _ in range(N):
    dust.append(list(map(int, input().split())))

for i in range(N):
    for j in range(M):
        if dust[i][j] == -1:
            wind.append([i, j])

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# (r, c)에서 먼지 확산 -> add_dust만 갱신
def spread_dust(r, c):
    # 나눠줄 먼지
    small_dust = dust[r][c] // 5
    # 나눠준 개수
    cnt = 0
    for i in range(4):
        nr = r + dx[i]
        nc = c + dy[i]
        if -1 < nr < N and -1 < nc < M and dust[nr][nc] != -1:
            cnt += 1
            add_dust[nr][nc] += dust[r][c] // 5
    add_dust[r][c] += - (dust[r][c] // 5) * cnt

# dust 갱신 및 add_dust 초기화
def update_dust():
    global dust, add_dust
    for i in range(N):
        for j in range(M):
            dust[i][j] += add_dust[i][j]
    add_dust = [[0 for _ in range(M)] for _ in range(N)]

# 돌풍 위치 기준 위에는 반시계, 아래는 시계 방향으로 회전시켜
def wind_blows():
    global dust
    # 반시계
    # 왼쪽
    for i in range(wind[0][0]-1, 0, -1):
        dust[i][0] = dust[i-1][0]
    # 위쪽
    for i in range(M-1):
        dust[0][i] = dust[0][i+1]
    # 오른쪽
    for i in range(wind[0][0]):
        dust[i][M-1] = dust[i+1][M-1]
    # 아래쪽
    for i in range(M-1, 0, -1):
        dust[wind[0][0]][i] = dust[wind[0][0]][i-1]
        if i == 1:
            dust[wind[0][0]][i] = 0
    # 시계
    # 왼쪽
    for i in range(N-wind[1][0]-2):
        dust[wind[1][0]+1+i][0] = dust[wind[1][0]+1+i+1][0]
    # 아래쪽
    for i in range(M-1):
        dust[N-1][i] = dust[N-1][i+1]
    # 오른쪽
    for i in range(N-1, wind[1][0], -1):
        dust[i][M-1] = dust[i-1][M-1]        
    # 위쪽
    for i in range(M-1, 0, -1):
        dust[wind[1][0]][i] = dust[wind[1][0]][i-1]
        if i == 1:
            dust[wind[1][0]][i] = 0

for t in range(T):
    for i in range(N):
        for j in range(M):
            if [i, j] not in wind:
                spread_dust(i, j)

    update_dust()
    wind_blows()

s = 2 # 초기값이 0이 아닌 2인 이유: 돌풍 있는 두곳이 -1이니까
for d in dust:
    s += sum(d)

print(s)