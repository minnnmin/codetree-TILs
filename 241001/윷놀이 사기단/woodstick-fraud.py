from copy import deepcopy

ORDER = list(map(int, input().split()))
MAX_SCORE = 0

# 현재위치 now, 현재 그룹 group, 이동횟수 cnt를 주면 최종 위치와 그룹을 반환
def get_next_pos(now, group, cnt):
    next_pos = -1
    next_group = group

    # 시작 위치가 교차로인 경우 먼저 처리 # 교차로일 경우 그룹 '' 이거여야 함. 혹은 40을 초과할 때도.
    if now == 10:
        if cnt <= 3:
            next_pos = 10 + cnt*3
            next_group = 'E'
        elif cnt == 4:
            next_pos = 25
            next_group = ''
        elif cnt == 5:
            next_pos = 30
            next_group = 'H'

    elif now == 20:
        if cnt <= 2:
           next_pos = 20 + cnt*2
           next_group = 'F'
        elif cnt == 3:
            next_pos = 25
            next_group = ''
        elif cnt >= 4:
            next_pos = 25 + (cnt-3)*5
            next_group = 'H'

    elif now == 30 and group == '':
        if cnt == 1:
            next_pos = 28
            next_group = 'G'
        elif cnt <= 2:
            next_pos = 28 - (cnt-1)*1
            next_group = 'G'
        elif cnt == 4:
            next_pos = 25
            next_group = ''
        elif cnt == 5:
            next_pos = 30
            next_group = 'H'

    elif now == 25:
        next_pos = 25 + cnt*5
        if next_pos >= 40:
            next_group = ''
        else:
            next_group = 'H'
        
    elif now == 40:
        next_pos = 40 + cnt*1
        next_group = ''

    else:
        if group == 'A':
            next_pos = now + cnt*2
            if next_pos > 10:
                next_group = 'B'
            elif next_pos == 10:
                next_group = ''
        elif group == 'B':
            next_pos = now + cnt*2
            if next_pos > 20:
                next_group = 'C'
            elif next_pos == 20:
                next_group = ''
        elif group == 'C':
            next_pos = now + cnt*2
            if next_pos > 30:
                next_group = 'D'
            elif next_pos == 30:
                next_group = ''
        elif group == 'D':
            next_pos = now + cnt*2
            if next_pos >= 40:
                next_group = ''
        elif group == 'E':
            if now == 13:
                if cnt <= 2:
                    next_pos = 13 + cnt*3
                elif cnt == 3:
                    next_pos = 25
                    next_group = ''
                elif cnt >= 4:
                    next_pos = 25 + (cnt-3)*5
                    next_group = 'H'
            elif now == 16:
                if cnt == 1:
                    next_pos = 19
                elif cnt == 2:
                    next_pos = 25
                    next_group = ''
                elif cnt >= 3:
                    next_pos = 25 + (cnt-2)*5
                    next_group = 'H'
                    if next_pos >= 40:
                        next_group = ''
            elif now == 19:
                if cnt == 1:
                    next_pos = 25
                    next_group = ''
                elif cnt >= 2:
                    next_pos = 25 + (cnt-1)*5
                    next_group = 'H'
                    if next_pos >= 40:
                        next_group = ''
        elif group == 'F':
            if now == 22:
                if cnt == 1:
                    next_pos = 24
                elif cnt == 2:
                    next_pos = 25
                    next_group = ''
                elif cnt >= 3:
                    next_pos = 25 + (cnt-2)*5
                    next_group = 'H'
                    if next_pos >= 40:
                        next_group = ''
            elif now == 24:
                if cnt == 1:
                    next_pos = 25
                    next_group = ''
                elif cnt >= 2:
                    next_pos = 25 + (cnt-1)*5
                    next_group = 'H'
                    if next_pos >= 40:
                        next_group = ''
        elif group == 'G':
            if now == 28:
                if cnt <= 3:
                    next_pos = 28 - cnt*1
                    if next_pos == 25:
                        next_group = ''
                elif cnt >= 4:
                    next_pos = 25 + (cnt-3)*5
                    next_group = 'H'
                    if next_pos >= 40:
                        next_group = ''
            elif now == 27:
                if cnt <= 2:
                    next_pos = 27 - cnt*1
                    if next_pos == 25:
                        next_group = ''
                elif cnt >= 3:
                    next_pos = 25 + (cnt-2)*5
                    next_group = 'H'
                    if next_pos >= 40:
                        next_group = ''
            elif now == 26:
                if cnt == 1:
                    next_pos = 25
                    next_group = ''
                elif cnt >= 2:
                    next_pos = 25 + (cnt-1)*5
                    next_group = 'H'
                    if next_pos >= 40:
                        next_group = ''
        elif group == 'H':
            next_pos = now + cnt*5
            if next_pos >= 40:
                next_group = ''


    return next_pos, next_group


# players_pos = [[위치, 그룹], [], ..]
def dfs(t, players_pos, history):
    global MAX_SCORE
    # if len(history) == 6:
    #     print(players_pos)
    #     print('turn', t)
    #     print(history)
    #     print()

    done = True
    for pos, group in players_pos:
        if pos <= 40:
            done = False
            break
    if done:
        for his in history:
            if his[3] <= 40:
                score += his[3]
        MAX_SCORE = score if score > MAX_SCORE else MAX_SCORE
        # print(history)
        # print(players_pos)
        # print()
        return

    if t == 10:
        # score 계산
        score = 0
        for his in history:
            if his[3] <= 40:
                score += his[3]
        MAX_SCORE = score if score > MAX_SCORE else MAX_SCORE
        # print(history)
        # print(players_pos)
        # print()
        return

    # 진행
    for i in range(len(players_pos)):
        pos, group = players_pos[i]
        if pos > 40:
            continue
        next_pos, next_group = get_next_pos(pos, group, ORDER[t])
        if next_pos > 40 or (next_pos, next_group) not in players_pos:
            players_pos[i] = (next_pos, next_group)
            history.append((t, pos, group, next_pos, next_group))
            dfs(t+1, players_pos, history)
            players_pos[i] = (pos, group)
            history.pop()

    
dfs(0, [(0, 'A'), (0, 'A'), (0, 'A'), (0, 'A')], [])
print(MAX_SCORE)