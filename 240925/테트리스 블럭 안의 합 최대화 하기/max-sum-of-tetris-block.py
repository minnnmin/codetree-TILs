N, M = map(int, input().split())
matrix = []
for _ in range(N):
    matrix.append(list(map(int, input().split())))

answer = 0

#(i, j)를 시작점으로 해서 가능한 모든 도형 탐색

# ㅁㅁㅁㅁ
for i in range(N):
    for j in range(M):
        if j+3 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i][j+2] + matrix[i][j+3]
            answer = res if res > answer else answer
# ㅁ
# ㅁ
# ㅁ
# ㅁ
for j in range(M):
    for i in range(N):
        if i+3 < N:
            res = matrix[i][j] + matrix[i+1][j] + matrix[i+2][j] + matrix[i+3][j]
            answer = res if res > answer else answer
# ㅁㅁ
# ㅁㅁ
for i in range(N):
    for j in range(M):
        if i+1 < N and j+1 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i+1][j] + matrix[i+1][j+1]
            answer = res if res > answer else answer

# ㅁ
# ㅁ ㅁ
#   ㅁ
for i in range(N):
    for j in range(M):
        if i+2 < N and j+1 < M:
            res = matrix[i][j] + matrix[i+1][j] + matrix[i+1][j+1] + matrix[i+2][j+1]
            answer = res if res > answer else answer
#   ㅁ ㅁ
# ㅁ ㅁ
for i in range(N):
    for j in range(M):
        if 0 < i < N and j+2 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i-1][j+1] + matrix[i-1][j+2]
            answer = res if res > answer else answer
#   ㅁ
# ㅁ ㅁ
# ㅁ
for i in range(N):
    for j in range(M):
        if 1 < i < N and j+1 < M:
            res = matrix[i][j] + matrix[i-1][j] + matrix[i-1][j+1] + matrix[i-2][j+1]
            answer = res if res > answer else answer
# ㅁ ㅁ
#   ㅁ ㅁ
for i in range(N):
    for j in range(M):
        if i+1 < N and j+2 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i+1][j+1] + matrix[i+1][j+2]
            answer = res if res > answer else answer
# ㅁ
# ㅁ
# ㅁㅁ
for i in range(N):
    for j in range(M):
        if i+2 < N and j+1 < M:
            res = matrix[i][j] + matrix[i+1][j] + matrix[i+2][j] + matrix[i+2][j+1]
            answer = res if res > answer else answer
#    ㅁ
# ㅁㅁㅁ
for i in range(N):
    for j in range(M):
        if 0 < i < N and j+2 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i][j+2] + matrix[i-1][j+2]
            answer = res if res > answer else answer
# ㅁㅁ
#  ㅁ
#  ㅁ
for i in range(N):
    for j in range(M):
        if i+2 < N and j+1 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i+1][j+1] + matrix[i+2][j+1]
            answer = res if res > answer else answer
# ㅁㅁㅁ
# ㅁ
for i in range(N):
    for j in range(M):
        if 0 < i < N and j+2 < M:
            res = matrix[i][j] + matrix[i-1][j] + matrix[i-1][j+1] + matrix[i-1][j+2]
            answer = res if res > answer else answer
#  ㅁ
#  ㅁ
# ㅁㅁ
for i in range(N):
    for j in range(M):
        if 1 < i < N and j+1 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i-1][j+1] + matrix[i-2][j+1]
            answer = res if res > answer else answer
# ㅁ
# ㅁㅁㅁ
for i in range(N):
    for j in range(M):
        if i+1 < N and j+2 < M:
            res = matrix[i][j] + matrix[i+1][j] + matrix[i+1][j+1] + matrix[i+1][j+2]
            answer = res if res > answer else answer
# ㅁㅁ
# ㅁ
# ㅁ
for i in range(N):
    for j in range(M):
        if i+2 < N and j+1 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i+1][j] + matrix[i+2][j]
            answer = res if res > answer else answer
# ㅁㅁㅁ
#    ㅁ
for i in range(N):
    for j in range(M):
        if i+1 < N and j+2 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i][j+2] + matrix[i+1][j+2]
            answer = res if res > answer else answer
# ㅁ
# ㅁㅁ
# ㅁ
for i in range(N):
    for j in range(M):
        if i+2 < N and j+1 < M:
            res = matrix[i][j] + matrix[i+1][j] + matrix[i+1][j+1] + matrix[i+2][j]
            answer = res if res > answer else answer
# ㅁㅁㅁ
#  ㅁ
for i in range(N):
    for j in range(M):
        if i+1 < N and j+2 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i+1][j+1] + matrix[i][j+2]
            answer = res if res > answer else answer
#  ㅁ
# ㅁㅁ
#  ㅁ
for i in range(N):
    for j in range(M):
        if 0 < i < N-1 and j+1 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i-1][j+1] + matrix[i+1][j+1]
            answer = res if res > answer else answer

#  ㅁ
# ㅁㅁㅁ
for i in range(N):
    for j in range(M):
        if 0 < i < N and j+2 < M:
            res = matrix[i][j] + matrix[i][j+1] + matrix[i-1][j+1] + matrix[i][j+2]
            answer = res if res > answer else answer

print(answer)