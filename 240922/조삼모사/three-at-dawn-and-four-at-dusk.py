N = int(input())
intensity = []
for _ in range(N):
    intensity.append(list(map(int, input().split())))


min_intensity = 300 - 3
visited = [False] * (N+1)
work_pairs = []


# n은 1부터 시작. n은 현재까지 선택된 일의 개수
def pick_works(n, work_list):
    if n == N//2:
        work_pairs.append(work_list)
        return
    
    # 얘는 근데 2로 시작해서 1을 볼 필요는 없는데 어케 조정하지
    for w in range(1, N+1):
        if not visited[w]:
            if len(work_list) == 0 or w > max(work_list):
                visited[w] = True
                pick_works(n+1, work_list + [w])
                visited[w] = False


# 작업 쌍을 구하는 함수. 예를 들어 1, 2, 3을 넣으면 4, 5, 6을 반환해 줌
# works는 list
def pick_others(works):
    tmp = [i for i in range(1, N+1)]
    for i in works:
        tmp.remove(i)
    return tmp

# work_pairs 세팅
pick_works(0, [])

for works in work_pairs:
    # print('--- 시작 ---')
    day_intensity = 0
    night_intensity = 0
    others = pick_others(works)
    # print(works)
    # print(others)
    for x in works:
        for y in works:
            if x != y:
                day_intensity += intensity[x-1][y-1]
    # print('낮', day_intensity)
    for a in others:
        for b in others:
            if a != b:
                night_intensity += intensity[a-1][b-1]
    # print('밤', night_intensity)
    if min_intensity > abs(day_intensity - night_intensity):
        min_intensity = abs(day_intensity - night_intensity)
    # print('--- 끝 ---')

print(min_intensity)