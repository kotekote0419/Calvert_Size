from un_uniform_flow_class import UnUniformFlowSquare
from un_uniform_flow_class import DataPlot
import un_uniform_flow_Excel
import tkinter as tk
import tkinter.filedialog as fd
import un_uniform_flow_def
import itertools
import datetime

# 時間の取得
d = datetime.datetime.now()
d_t = "{0}{1:0=2}{2:0=2}{3:0=2}{4:0=2}".format(
    d.year, d.month, d.day, d.hour, d.minute
)

# 定数の整理--------------------
g = 9.8
n = 0.015
calv = [0.6, 0.45, 0.36, 0.3, 0.24]
cost = [7850, 4790, 3560, 3280, 1980]   # m単価

# Inputファイルの選択--------------------
root = tk.Tk()
root.withdraw()

file_flow = fd.askopenfilename(
    title="Input data指定.(.txt)",
    filetypes=[("TEXT", ".txt")]
)
flow_data = un_uniform_flow_def.flow_data(file_flow)

length_min = float(min([i[2] for i in flow_data]))
while True:
    sl = float(input("step length(m) ?: "))
    if sl > length_min:
        print("各区間の延長より小さい値を指定.")
    else:
        break
h1 = float(input("Start Water Level(m) ?: "))
af = float(input("Afford Level(m) ?: "))
cases = int(input("抽出するケース数を指定: "))
# 組み合わせの格納
calv_num = [i for i in range(len(calv))]
calv_num_all = list(itertools.combinations_with_replacement(calv_num, len(flow_data)))
# Main Calculate ******************************************
flow = UnUniformFlowSquare()
flow_plot = DataPlot()
for cnt in range(len(calv_num_all)):
    flow_cal = flow.wl_cal(
        g, n, calv, flow_data, calv_num_all[cnt], sl, h1, af
    )
    # グラフ描画開始---------------------------------------------------
    xh, yh, xu, yu = un_uniform_flow_def.flow_plot(flow_cal, flow.h1, sl)
    flow_plot.update_plot(xu, yu, xh, yh, cnt, calv_num_all)
# 最適化検討***********************************************************
if len(flow.calv_num_opt) == 0:
    print("条件を満たすサイズがありません")
else:
    # コストの算出
    condition_cost = [0 for i in range(len(flow.calv_num_opt))]
    for i in range(len(flow.calv_num_opt)):
        for j in range(len(flow.calv_num_opt[i])):
            condition_cost[i] += cost[flow.calv_num_opt[i][j]] * float(flow_data[j][2])
    # 検討ケースの抽出
    if cases > len(flow.calv_num_opt):
        cases = len(flow.calv_num_opt)
    # 最適ケースの再計算
    print("Results-------------------------------------------")
    print("<{0}>の組み合わせの内、余裕{1}mを満たす組み合わせは<{2}>.".format(
        len(calv_num_all), af, len(flow.calv_num_opt)
    ))
    print("最適条件より{0}ケース抽出".format(cases))
    for case in range(cases):
        flow_cal, flow_detail = flow.wl_cal_detail(
            g, n, calv, flow_data,
            flow.calv_num_opt[condition_cost.index(min(condition_cost))], sl, h1, af
        )
        xh, yh, xu, yu = un_uniform_flow_def.flow_plot(flow_cal, flow.h1, sl)
        condition_cost.pop(condition_cost.index(min(condition_cost)))
        # グラフ描画
        flow_plot.plot_save(xu, yu, xh, yh, af, case)
        # Excel - Output
        if case == 0:
            xl = un_uniform_flow_Excel.xl_sheet(flow_cal, flow_detail, case, d_t)
        else:
            xl = un_uniform_flow_Excel.xl_update(xl, flow_cal, case, d_t)
cl = input("any key...")
