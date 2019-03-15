from un_uniform_flow_class import UnUniformFlowSquare
from un_uniform_flow_class import DataPlot
import tkinter as tk
import tkinter.filedialog as fd
import un_uniform_flow_def
import un_uniform_flow_Excel
import itertools

# 定数の整理--------------------
g = 9.8
n = 0.015
calv = [0.7, 0.6, 0.5, 0.4]
cost = [7000, 6000, 5000, 4000]   # m単価

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
plt_bool = True
# 組み合わせの格納
calv_num = [i for i in range(len(calv))]
calv_num_all = list(itertools.combinations_with_replacement(calv_num, len(flow_data)))
# Main Calculate ******************************************
req = []
for cnt in range(len(calv_num_all)):
    flow = UnUniformFlowSquare(g, n, calv, flow_data, calv_num_all[cnt], sl, h1)
    # グラフ描画開始---------------------------------------------------
    xh, yh, xu, yu = un_uniform_flow_def.flow_plot(flow.flow_data, flow.h1, sl)
    if plt_bool:
        flow_plot = DataPlot(xu, yu, xh, yh, af)
        plt_bool = False
    else:
        flow_plot.update_plot(xu, yu, xh, yh)
    # グラフ描画終了---------------------------------------------------
    if flow.flow_data[len(flow_data)-1][4] < -1*af:
        req.append(calv_num_all[cnt])
    print(flow.flow_data)
# 最適化検討***********************************************************
if len(req) == 0:
    print("条件を満たすサイズがありません")
else:
    # コストの算出
    req_cost = [0 for i in range(len(req))]
    for i in range(len(req)):
        for j in range(len(req[i])):
            req_cost[i] += cost[req[i][j]] * float(flow_data[j][2])
    # 検討ケースの抽出　※リストに格納するべき！！！！！！！！
    if cases < len(req):
        cases = len(req)
    print("最適条件より{0}ケース抽出".format(cases))
    for case in range(cases):
        flow = UnUniformFlowSquare(g, n, calv, flow_data, req[req_cost.index(min(req_cost))], sl, h1)
        # グラフ描画
        xh, yh, xu, yu = un_uniform_flow_def.flow_plot(flow.flow_data, flow.h1, sl)
        flow_plot.update_plot_save(xu, yu, xh, yh)
        print(flow.flow_data)
        #un_uniform_flow_Excel.out_sheet(flow.flow_data, case)
        req_cost.pop(req_cost.index(min(req_cost)))
    print("<{0}>の組み合わせの内、余裕{1}mを満たす組み合わせは<{2}>.".format(
        len(calv_num_all), af, len(req)
    ))
