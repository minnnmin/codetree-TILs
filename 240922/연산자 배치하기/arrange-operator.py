N = int(input())
numbers = list(map(int, input().split()))
plus, minus, mul = map(int, input().split())
operators = ['+']*plus + ['-']*minus + ['*']*mul


# opers는 최종 선택된 연산자들
def evaluate(opers):
    answer = numbers[0]
    i = 1
    for op in opers:
        if op == '+':
            answer += numbers[i]
        elif op == '-':
            answer -= numbers[i]
        elif op == '*':
            answer *= numbers[i]
        i += 1
    return answer


max_val = int(-1e9)
min_val = int(1e9//1)
visited = [False] * len(operators)

def func(n, result):
    global max_val, min_val
    if n == N-1:
        answer = evaluate(result)
        max_val = answer if answer > max_val else max_val
        min_val = answer if answer < min_val else min_val
        return

    for i in range(len(operators)):
        if not visited[i]:
            visited[i] = True
            func(n+1, result + [operators[i]])
            visited[i] = False

func(0, [])
print(min_val, max_val)