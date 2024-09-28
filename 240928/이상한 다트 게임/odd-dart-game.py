# 원판의 개수 N, 원판 내의 숫자의 개수 M, 회전 횟수 Q
N, M, Q = map(int, input().split())

# 다트판 정보
DARTS = [list(map(int, input().split())) for _ in range(N)]


# 회전 명령
ROTATE_ORDER = []
for q in range(Q):
    x, d, k = map(int, input().split())
    ROTATE_ORDER.append((x-1, d, k))
    # 회전하는 원판의 종류 x, 방향 d, 회전하는 칸 수 k


def rotate(dart_num, rotate_cnt, rotate_dir):
    # 만약 회전 방향이 숫자 개수의 배수면 돌리지마
    if rotate_cnt % M == 0:
        return
    
    # 다 돌리면 됨
    if dart_num == 0:
        if rotate_dir == 0: # 시계 방향
            for i in range(0, len(DARTS)):
                DARTS[i] = DARTS[i][M-1:] + DARTS[i][:M-rotate_cnt]
        else: # 반시계 방향
            for i in range(len(DARTS)):
                DARTS[i] = DARTS[i][rotate_cnt:] + DARTS[i][:rotate_cnt]

    # 돌려야 되는 얘의 배수만 돌려야 됨
    ㄷif rotate_dir == 0: # 시계 방향
        for i in range(0, len(DARTS)):
            DARTS[i] = DARTS[i][M-1:] + DARTS[i][:M-rotate_cnt]
    else: # 반시계 방향
        for i in range(len(DARTS)):
            DARTS[i] = DARTS[i][rotate_cnt:] + DARTS[i][:rotate_cnt]

# print('전')
# for _ in DARTS:
#     print(_)

# print()
# print('반시계방향 회전')
# rotate(0, 4, 1)
# for _ in DARTS:
#     print(_)