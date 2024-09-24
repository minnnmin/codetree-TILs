# 격자 N^2, 원자 M개, K초
N, M, K = map(int, input().split())
atom = [[[] for _ in range(N)] for _ in range(N)]
# x, y, m, s, d
for _ in range(M):
    x, y, m, s, d = map(int, input().split())
    atom[x-1][y-1].append([m, s, d])


# 0부터 7까지 순서대로 ↑, ↗, →, ↘, ↓, ↙, ←, ↖
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]


# 원자의 위치 x, y와 방향 d, 속력 s를 주면 새 위치를 반환하는 함수
# 주의: 범위 넘어가도 이동 가능
def new_pos(x, y, s, d):
    nx = x + dx[d]*s
    ny = y + dy[d]*s
    if nx < 0:
        if -nx % N == 0:
            nx += N*(-nx//N)
        else: 
            nx += N*(-nx//N+1) #아 미친 딱 떨어지는 걸 간과했어
    elif nx > N-1:
        nx = nx - N*(nx//N)
    if ny < 0:
        if -ny % N == 0:
            ny += N*(-ny//N)
        else:
            ny += N*(-ny//N+1)
    elif ny > N-1:
        ny = ny - N*(ny//N)
    return nx, ny

# 원자 이동
def move():
    global atom
    add_atoms = [] #[x, y, m, s, d]
    for i in range(N):
        for j in range(N):
            # atom[i][j] 에는 (i, j)에 있는 원자들이 리스트 형태로 담겨있어
            l = len(atom[i][j])
            for _  in range(l):
                m, s, d = atom[i][j].pop()
                nx, ny = new_pos(i, j, s, d)
                add_atoms.append([nx, ny, m, s, d])
    for x, y, m, s, d in add_atoms:
        atom[x][y].append([m, s, d])


# 원자 합성 (질량 0인 경우 아예 소멸)
def mix_atom():
    global atom
    # atom 순회하면서, 한 자리에 원자가 2개 이상이면 합성 진행
    for i in range(N):
        for j in range(N):
            l = len(atom[i][j])
            if l >= 2:
                s_mass = 0
                s_speed = 0
                s_dir = [] # 모두 상하좌우 혹은 모두 대각선이면: 상하좌우, 아니면: 대각선
                for _  in range(l):
                    m, s, d = atom[i][j].pop()
                    s_mass += m
                    s_speed += s
                    s_dir.append(d)
                
                new_mass = s_mass // 5
                if new_mass == 0:
                    continue
                new_speed = s_speed // l
                new_dir = True
                tmp_s = s_dir[0]
                if tmp_s % 2 == 0:  # 다 짝수면 True
                    for sd in s_dir[1:]:
                        if sd % 2 != 0:
                            new_dir = False
                else:               # 다 홀수면 True
                    for sd in s_dir[1:]:
                        if sd % 2 == 0:
                            new_dir = False
                # 방향 설정
                for k in range(4): # 다시 제자리에 합성된 원자 추가
                    atom[i][j].append([new_mass, new_speed, k*2 if new_dir else k*2+1])

for k in range(K):
    # 원자 이동
    move()
    # 원자 합성
    mix_atom()

# 원자 개수 출력
sum_of_mass = 0
for i in atom:
    for j in i:
        for at in j:
            sum_of_mass += at[0]
print(sum_of_mass)