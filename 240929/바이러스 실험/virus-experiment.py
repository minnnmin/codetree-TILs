# 배지의 크기 n, 바이러스의 개수 m, 총 사이클의 수 k
N, M, K = map(int, input().split())
NUTRIENT = [[5 for _ in range(N)] for _ in range(N)]
ADD_NUTRIENT = [list(map(int, input().split())) for _ in range(N)]
VIRUS = [[[] for _ in range(N)] for _ in range(N)]

for _ in range(M):
    x, y, age = map(int, input().split())
    VIRUS[x-1][y-1].append(age)

# 인접 8칸: 오른쪽부터 반시계 방향
dx = [0, -1, -1, -1, 0, 1, 1, 1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]

def in_range(x, y):
    return -1 < x < N and -1 < y < N


# 바이러스가 양분 섭취, 죽은 바이러스 양분으로 변함
def virus_eat_nutrient():
    global NUTRIENT, VIRUS

    dead_virus = [] #(x, y, age)
    for x in range(N):
        for y in range(N):
            survive_virus = [] #(x, y, age)
            if len(VIRUS[x][y]) > 0: # 바이러스가 있다는 뜻. 그리고 이때는 크기순으로 정렬되어 있음
                for age in VIRUS[x][y]:
                    if NUTRIENT[x][y] >= age: # 영양분 먹을 수 있다면
                        survive_virus.append((x, y, age+1))
                        NUTRIENT[x][y] -= age
                    else:
                        dead_virus.append((x, y, age))
            VIRUS[x][y] = []
            for x, y, age in survive_virus:
                VIRUS[x][y].append(age) 

    # 죽은 바이러스 양분으로 변함
    if dead_virus:
        for x, y, age in dead_virus:
            NUTRIENT[x][y] += age//2


# 바이러스 번식 - 나이가 5의 배수인 경우에만
def make_virus():
    for x in range(N):
        for y in range(N):
            if len(VIRUS[x][y]) > 0:
                for age in VIRUS[x][y]:
                    if age % 5 == 0:
                        for i in range(8):
                            nx, ny = x + dx[i], y + dy[i]
                            if in_range(nx, ny):
                                VIRUS[nx][ny].append(1)
                                VIRUS[nx][ny].sort()

# 양분 증가
def add_nutrient():
    global NUTRIENT

    for i in range(N):
        for j in range(N):
            NUTRIENT[i][j] += ADD_NUTRIENT[i][j]


for _ in range(K):
    virus_eat_nutrient()
    # for _ in NUTRIENT:
    #     print(_)
    # print()
    make_virus()
    # for _ in VIRUS:
    #     print(_)
    # print()
    add_nutrient()
    # for _ in NUTRIENT:
    #     print(_)
    # print()


viruses = 0
for i in range(N):
    for j in range(N):
        viruses += len(VIRUS[i][j])

print(viruses)