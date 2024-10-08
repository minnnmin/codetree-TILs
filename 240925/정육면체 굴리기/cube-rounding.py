N, M, X, Y, K = map(int, input().split())
matrix = []
for _ in range(N):
    matrix.append(list(map(int, input().split())))

move_order = list(map(int, input().split()))

# 정육면체 6면에 쓰인 숫자
down = 0
front = 0
right = 0
up = 0
left = 0
back = 0

def move_east():
    global Y, down, front, right, up, left, back
    # 주사위 숫자 갱신
    tmp = down
    down = right
    right = up
    up = left
    left = tmp
    
    Y += 1

    if matrix[X][Y] == 0:
        matrix[X][Y] = down
    elif matrix[X][Y] != 0:
        down = matrix[X][Y]
        matrix[X][Y] = 0

    print(up)
    
def move_west():
    global Y, down, front, right, up, left, back
    tmp = left
    left = up
    up = right
    right = down
    down = tmp

    Y -= 1

    if matrix[X][Y] == 0:
        matrix[X][Y] = down
    elif matrix[X][Y] != 0:
        down = matrix[X][Y]
        matrix[X][Y] = 0

    print(up)

def move_north():
    global X, down, front, right, up, left, back
    tmp = back
    back = up
    up = front
    front = down
    down = tmp

    X -= 1
    
    if matrix[X][Y] == 0:
        matrix[X][Y] = down
    elif matrix[X][Y] != 0:
        down = matrix[X][Y]
        matrix[X][Y] = 0
    print(up)

def move_south():
    global X, down, front, right, up, left, back
    tmp = down
    down = front
    front = up
    up = back
    back = tmp

    X += 1

    if matrix[X][Y] == 0:
        matrix[X][Y] = down
    elif matrix[X][Y] != 0:
        down = matrix[X][Y]
        matrix[X][Y] = 0
    
    # print(X, Y, 's')
    print(up)

for mo in move_order:
    if mo == 1: # east
        if Y+1 < M:
            move_east()
    elif mo == 2: # west
        if Y-1 > -1:
            move_west()
    elif mo == 3: # north
        if X-1 > -1:
            move_north()
    elif mo == 4: # south
        if X+1 < N:
            move_south()