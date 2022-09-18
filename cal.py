def board_num(action):
    """
    棋盘坐标转化为数字坐标
    :param action:棋盘坐标，比如A1
    :return:数字坐标，比如 A1 --->(0,0)
    """

    row, col = str(action[1]).upper(), str(action[0]).upper()
    if row in '12345678' and col in 'ABCDEFGH':
        # 坐标正确
        x, y = '12345678'.index(row), 'ABCDEFGH'.index(col)  # 转化为对应的索引
        return [y,x]

roxanne_table = [
            ['A1', 'H1', 'A8', 'H8'],
            ['C3', 'F3', 'C6', 'F6'],
            ['C4', 'F4', 'C5', 'F5', 'D3', 'E3', 'D6', 'E6'],
            ['A3', 'H3', 'A6', 'H6', 'C1', 'F1', 'C8', 'F8'],
            ['A4', 'H4', 'A5', 'H5', 'D1', 'E1', 'D8', 'E8'],
            ['B3', 'G3', 'B6', 'G6', 'C2', 'F2', 'C7', 'F7'],
            ['B4', 'G4', 'B5', 'G5', 'D2', 'E2', 'D7', 'E7'],
            ['B2', 'G2', 'B7', 'G7'],
            ['A2', 'H2', 'A7', 'H7', 'B1', 'G1', 'B8', 'G8']
        ]
ans=[]
for s in roxanne_table:
    tmp=[]
    for i in s:
        tmp.append(board_num(i))
    ans.append(tmp)
print(ans)
