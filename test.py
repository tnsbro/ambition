def calculate_circumcenter(x1, y1, x2, y2, x3, y3):
    # 삼각형 변의 중점 계산
    mid1_x, mid1_y = (x1 + x2) / 2, (y1 + y2) / 2
    mid2_x, mid2_y = (x2 + x3) / 2, (y2 + y3) / 2

    # 삼각형 변의 기울기 계산
    slope1 = (y2 - y1) / (x2 - x1) if x2 != x1 else None
    slope2 = (y3 - y2) / (x3 - x2) if x3 != x2 else None

    # 수직이등분선의 기울기 계산
    perp_slope1 = -1 / slope1 if slope1 not in [None, 0] else None
    perp_slope2 = -1 / slope2 if slope2 not in [None, 0] else None

    # 수직이등분선의 방정식 정의
    def line_equation(slope, mid_x, mid_y):
        if slope is None:  # 수직선 (x = 상수)
            return None, mid_x
        elif slope == 0:  # 수평선 (y = 상수)
            return 0, mid_y
        else:  # 일반적인 직선
            intercept = mid_y - slope * mid_x
            return slope, intercept

    line1 = line_equation(perp_slope1, mid1_x, mid1_y)
    line2 = line_equation(perp_slope2, mid2_x, mid2_y)

    # 두 수직이등분선의 교점 계산
    if line1[0] is None:  # 첫 번째 선이 수직 (x = 상수)
        cx = line1[1]
        cy = line2[0] * cx + line2[1] if line2[0] is not None else line2[1]
    elif line2[0] is None:  # 두 번째 선이 수직 (x = 상수)
        cx = line2[1]
        cy = line1[0] * cx + line1[1] if line1[0] is not None else line1[1]
    elif line1[0] == line2[0]:  # 두 선이 평행한 경우
        raise ValueError("외심을 계산할 수 없습니다. 세 점이 한 직선에 가까이 있습니다.")
    else:  # 일반적인 교점 계산
        cx = (line2[1] - line1[1]) / (line1[0] - line2[0])
        cy = line1[0] * cx + line1[1]

    return cx, cy

# 테스트 데이터
x1, y1 = 1, 1
x2, y2 = 1, 4  # 수직선
x3, y3 = 5, 1

# 외심 계산
try:
    circumcenter = calculate_circumcenter(x1, y1, x2, y2, x3, y3)
    print(f"블루투스 기기의 대략적인 위치 (외심): {circumcenter}")
except ValueError as e:
    print(f"오류: {e}")
