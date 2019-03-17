import un_uniform_flow_def
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines


class UnUniformFlowSquare:
    def __init__(self):
        self.h1 = 0
        self.calv_num_opt = []

    def wl_cal(self, g, n, calv, flow_data, calv_num, sl, h1, af):
        for i in range(len(flow_data)):
            q = float(flow_data[i][1])
            tl = float(flow_data[i][2])
            b = calv[calv_num[i]]

            # 区間の算出
            span_n = int(tl / sl)
            span_end = float(tl % sl)
            if span_n == 0:
                span_st = span_end
            else:
                span_st = sl

            # 下流スパンの不等流計算
            if i == 0:
                h1 = un_uniform_flow_def.lim_depth(g, q, b, h1)
                flow_data[i][3] = h1 - b
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, span_st, h1)
                self.h1 = h2 - b
            else:
                h1 = flow_data[i-1][4] + b
                h1 = un_uniform_flow_def.lim_depth(g, q, b, h1)
                flow_data[i][3] = h1 - b
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, sl, h1)
            # 中間スパンの不等流計算
            if span_n <= 1:
                pass
            else:
                for j in range(span_n-2):
                    h2 = un_uniform_flow_def.wl_cal(g, n, q, b, sl, h2)
                # 上流スパンの不等流計算
                if span_end == 0:
                    span_end = sl
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, span_end, h2)
            flow_data[i][4] = h2 - b
            flow_data[i][5] = -1 * b
        if flow_data[-1][4] < -1*af:
            self.calv_num_opt.append(calv_num)
        return flow_data

    def wl_cal_detail(self, g, n, calv, flow_data, calv_num, sl, h1, af):
        for i in range(len(flow_data)):
            q = float(flow_data[i][1])
            tl = float(flow_data[i][2])
            b = calv[calv_num[i]]

            # 区間の算出
            span_n = int(tl / sl)
            span_end = float(tl % sl)
            if span_n == 0:
                span_st = span_end
            else:
                span_st = sl

            # 下流スパンの不等流計算
            if i == 0:
                h1 = un_uniform_flow_def.lim_depth(g, q, b, h1)
                flow_data[i][3] = h1 - b
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, span_st, h1)
                flow_detail = [[sl], [h1-b], [h2-b]]
                self.h1 = h2 - b
            else:
                h1 = flow_data[i-1][4] + b
                h1 = un_uniform_flow_def.lim_depth(g, q, b, h1)
                flow_data[i][3] = h1 - b
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, sl, h1)
                flow_detail[0].append(sl + flow_detail[0][-1])
                flow_detail[1].append(h1 - b)
                flow_detail[2].append(h2 - b)
            # 中間スパンの不等流計算
            if span_n <= 1:
                pass
            else:
                for j in range(span_n-2):
                    flow_detail[0].append(sl + flow_detail[0][-1])
                    flow_detail[1].append(h2 - b)
                    h2 = un_uniform_flow_def.wl_cal(g, n, q, b, sl, h2)
                    flow_detail[2].append(h2 - b)
                # 上流スパンの不等流計算
                if span_end == 0:
                    span_end = sl
                flow_detail[0].append(sl + flow_detail[0][-1])
                flow_detail[1].append(h2 - b)
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, span_end, h2)
                flow_detail[2].append(h2 - b)
            flow_data[i][4] = h2 - b
            flow_data[i][5] = -1 * b
            if flow_data[-1][4] < -1 * af:
                self.calv_num_opt.append(calv_num)
        return flow_data, flow_detail


class DataPlot:
    def __init__(self):
        self.fig = plt.figure(num=None, figsize=(15, 4), dpi=80, facecolor='w', edgecolor='k')
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_title('Water Level')
        self.ax.set_xlabel('Length (m)')
        self.ax.set_ylabel('Level (m)')
        self.rects = []
        self.plines = []

    def update_plot(self, xu, yu, xh, yh, cnt, calv_num_all):
        self.ax.set_title("{0:d} %".format(int(100*cnt/len(calv_num_all))))
        self.ax.set_xlim(0, xu[-1][1])
        self.ax.set_ylim(yu[0] - 0.1, -1 * yu[0] + 0.1)
        if cnt == 0:
            for x, y in zip(xu, yu):
                rect = patches.Rectangle((x[0], 0), x[1] - x[0], y, label='Calvert', color='grey', linewidth='0')
                self.rects.append(rect)
                self.ax.add_patch(rect)
            for x, y in zip(xh, yh):
                pline = lines.Line2D(x, y, color='blue', label='Water Level')
                self.plines.append(pline)
                self.ax.add_line(pline)
            plt.pause(0.01)
        else:
            for rect, h in zip(self.rects, yu):
                rect.set_height(h)
            for pline, x, y in zip(self.plines, xh, yh):
                pline.set_data(x, y)
            plt.pause(0.01)

    def plot_save(self, xu, yu, xh, yh, af, case):
        self.ax.set_title('Water Level')
        self.ax.axhline(y=-1 * af, color='k', linestyle='-.')
        for x in xu:
            self.ax.axvline(x=x[1], color='k', linewidth='0.5')
        self.ax.set_xlim(0, xu[-1][1])
        self.ax.set_ylim(yu[0]-0.1, -1*yu[0]+0.1)
        ann_list = []
        for rect, h, x in zip(self.rects, yu, xu):
            rect.set_height(h)
            ann = self.ax.annotate(
                "U-{0:d}".format(int(-1000*h)), (x[0]+(x[1]-x[0])/2, h+0.01), horizontalalignment='center'
            )
            ann_list.append(ann)
        for pline, x, y in zip(self.plines, xh, yh):
            pline.set_data(x, y)
            ann1 = self.ax.annotate('{0:.3f}'.format(y[0]), (x[0], y[0]))
            ann2 = self.ax.annotate('{0:.3f}'.format(y[1]), (x[1], y[1]))
            ann_list.append(ann1)
            ann_list.append(ann2)
        plt.savefig("Calvert{0}".format(case+1))
        for a in ann_list:
            a.remove()
