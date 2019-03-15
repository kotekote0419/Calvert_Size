import un_uniform_flow_def
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines


class UnUniformFlowSquare:
    def __init__(self, g, n, calv, flow_data, calv_num, sl, h1):
        for i in range(len(flow_data)):
            self.flow_data = flow_data
            q = float(self.flow_data[i][1])
            tl = float(self.flow_data[i][2])
            b = calv[calv_num[i]]

            # 区間の算出
            span_n = int(tl / sl)
            span_end = float(tl % sl)

            # 下流スパンの不等流計算
            if i == 0:
                h1 = un_uniform_flow_def.lim_depth(g, q, b, h1)
                self.flow_data[i][3] = h1 - b
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, sl, h1)
                self.h1 = h2 - b
            else:
                h1 = self.flow_data[i-1][4] + b
                h1 = un_uniform_flow_def.lim_depth(g, q, b, h1)
                self.flow_data[i][3] = h1 - b
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, sl, h1)
            # 中間スパンの不等流計算
            for j in range(span_n-1):
                h2 = un_uniform_flow_def.wl_cal(g, n, q, b, sl, h2)
            # 上流スパンの不等流計算
            h2 = un_uniform_flow_def.wl_cal(g, n, q, b, span_end, h2)
            self.flow_data[i][4] = h2 - b
            self.flow_data[i][5] = -1 * b


class DataPlot:
    def __init__(self, xu, yu, xh, yh, af):
        plt.ion()
        self.fig = plt.figure(num=None, figsize=(15, 4), dpi=80, facecolor='w', edgecolor='k')
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_title('Water Level')
        self.ax.set_xlabel('Length (m)')
        self.ax.set_ylabel('Level (m)')
        self.ax.set_xlim(0, xu[-1][1])
        self.ax.set_ylim(yu[0]-0.1, -1*yu[0]+0.1)
        self.ax.axhline(y=-1 * af, color='k', linestyle='-.')
        for x_line in xh:
            self.ax.axvline(x=x_line[1], color='k', linewidth='0.5')
        self.rects = []
        for x, y in zip(xu, yu):
            rect = patches.Rectangle((x[0], 0), x[1]-x[0], y, label='Calvert', color='grey', linewidth='0')
            self.rects.append(rect)
            self.ax.add_patch(rect)
        self.plines = []
        for x, y in zip(xh, yh):
            pline = lines.Line2D(x, y, color='blue', label='Water Level')
            self.plines.append(pline)
            self.ax.add_line(pline)
        plt.pause(0.01)

    def update_plot(self, xu, yu, xh, yh):
        self.ax.set_xlim(0, xu[-1][1])
        self.ax.set_ylim(yu[0]-0.1, -1*yu[0]+0.1)
        for rect, h in zip(self.rects, yu):
            rect.set_height(h)
        for pline, x, y in zip(self.plines, xh, yh):
            pline.set_data(x, y)
        plt.pause(0.01)

    def update_plot_save(self, xu, yu, xh, yh):
        self.ax.set_xlim(0, xu[-1][1])
        self.ax.set_ylim(yu[0]-0.1, -1*yu[0]+0.1)
        for rect, h, x in zip(self.rects, yu, xu):
            rect.set_height(h)
            self.ax.annotate(
                "U-{0:d}".format(int(-1000*h)), (x[0]+(x[1]-x[0])/2, h+0.01), horizontalalignment='center'
            )
        for pline, x, y in zip(self.plines, xh, yh):
            pline.set_data(x, y)
            self.ax.annotate('{0:.3f}'.format(y[0]), (x[0], y[0]))
            self.ax.annotate('{0:.3f}'.format(y[1]), (x[1], y[1]))
        plt.savefig("Calvert")
