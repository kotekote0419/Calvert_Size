def flow_data(file):
    input_data = []
    if file:
        with open(file, "r", encoding="utf-8-sig") as fileobj:
            while True:
                line = fileobj.readline()
                if line:
                    line = line.rstrip()
                    line = line.replace(" ", "")
                    list_data = line.split(",")
                    input_data.append(list_data)
                else:
                    break
    for i in range(len(input_data)):
        input_data[i].append(0.0)   # 上流水深
        input_data[i].append(0.0)   # 下流水深
        input_data[i].append(0.0)   # 側溝サイズ
    return input_data


def flow_plot(pflow_data, pflow_data0, sl):
    pdata = []
    xh = []
    yh = []
    xu = []
    yu = []
    for k in range(len(pflow_data)+1):
        if k == 0:
            xh.append([0, sl])
            yh.append([pflow_data[k][3], pflow_data0])
        elif k == 1:
            xh.append([sl, float(pflow_data[k-1][2])])
            yh.append([pflow_data0, pflow_data[k-1][4]])
        else:
            xh.append([xh[k-1][1], xh[k-1][1]+float(pflow_data[k-1][2])])
            yh.append([pflow_data[k-1][3], pflow_data[k-1][4]])
    for k in range(len(pflow_data)):
        if k == 0:
            xu.append([float(xh[k][0]), xh[k+1][1]])
            yu.append(pflow_data[k][5])
        else:
            xu.append([xh[k+1][0], xh[k+1][1]])
            yu.append(pflow_data[k][5])
    pdata.append(xh)
    pdata.append(yh)
    pdata.append(xu)
    pdata.append(yu)
    return pdata


def lim_depth(g, q, b, h1):
    lim_h = pow(pow(q / 60, 2) / (g * pow(b, 2)), 1 / 3)
    if h1 > lim_h:
        return h1
    else:
        return lim_h


def wl_cal(g, n, q, b, sl, h1):
    # 下流側の流積と径深
    a1 = h1 * b
    r1 = a1 / (2 * h1 + b)

    h2 = h1
    # ループ---------------------------
    while True:
        # 上流側の流積と径深
        a2 = h2 * b
        r2 = a2 / (2 * h2 + b)

        # 第2項
        hh1 = pow(q / 60, 2) * ((1 / pow(a1, 2)) - (1 / pow(a2, 2))) / (2 * g)

        # 第3項
        hhh1 = 0.5 * pow(q / 60, 2) * sl * (
                (pow(n, 2) / (pow(a1, 2) * pow(r1, 4 / 3))) + (pow(n, 2) / (pow(a2, 2) * pow(r2, 4 / 3))))

        h3 = h1 + hh1 + hhh1
        if abs(h3-h2) < 0.0001:
            break
        else:
            h2 = h3
    return h3
