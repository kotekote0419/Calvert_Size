import openpyxl as px


def out_sheet(flow_data, case):
    wb = px.Workbook()

    for i in range(case):
        if case == 0:
            ws = wb.active
            ws.title = 'CASE-1'
        else:
            ws = wb.create_sheet('CASE-{0}'.format(case+1))

        ws.cell(1, 2).value = 'Q(m3/min)'
        ws.cell(1, 3).value = 'L(m)'
        ws.cell(1, 4).value = 'Down WL(m)'
        ws.cell(1, 5).value = 'Up WL(m)'
        for i in range(len(flow_data)):
            for j in range(5):
                ws.cell(i+2, j+1).value = flow_data[i][j]
        img = px.drawing.image.Image('Calvert.png')
        ws.add_image(img, 'A{0}'.format(len(flow_data)+1))

    wb.save('xlSheet.xls')
