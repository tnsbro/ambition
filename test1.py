import math

# 주어진 길이와 기준점에 따라 각도를 계산하고, 길이가 10인 선분의 끝 점을 구하는 함수
def find_endpoint(x1, y1, x2, y2, a, base_point_flag, line_length):
    # 빗변의 길이 계산
    c = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    base_angle = math.atan2(y2 - y1, x2 - x1)
    # 각도를 계산 (기준점에 따라 sin 또는 cos을 사용)
    if base_point_flag == 0:
        # 두 변이 이루는 각을 sin으로 계산
        angle = math.asin(a / c)
    elif base_point_flag == 1:
        # 두 변이 이루는 각을 cos으로 계산
        angle = math.acos(a / c)
    else:
        return "base_point_flag는 0 또는 1이어야 합니다."
    
    # 주어진 각도에 맞춰 길이가 10인 선분의 끝 점을 계산
    dx = c * math.cos(angle)
    dy = c * math.sin(angle)
    
    # 기준점에 따라 선분을 그릴 점을 계산
    if base_point_flag == 0:  # 기준점 0 (두 번째 좌표에서 그음)
        end_x = x2 + dx
        end_y = y2 + dy
    elif base_point_flag == 1:  # 기준점 1 (첫 번째 좌표에서 그음)
        end_x = x1 + dx
        end_y = y1 + dy
    
    return end_x, end_y

# 예시 사용
x1, y1 = 0, 0  # 첫 번째 빗변 끝점
x2, y2 = 4, 3  # 두 번째 빗변 끝점
a = 4          # 다른 변의 길이
base_point_flag = 0  # 기준점 선택 (0: 두 번째 좌표, 1: 첫 번째 좌표)
line_length = 10  # 선분의 길이

# 결과 계산
result = find_endpoint(x1, y1, x2, y2, a, base_point_flag, line_length)
print(result)
