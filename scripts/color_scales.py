import ast

def get_color(colorscale, min_weight, max_weight, current_weight):
    if colorscale == 'RdBu':
        colorscale = [[0, 'rgb(5,10,172)'], [0.35, 'rgb(106,137,247)'],
                      [0.5, 'rgb(190,190,190)'], [0.6, 'rgb(220,170,132)'],
                      [0.7, 'rgb(230,145,90)'], [1, 'rgb(178,10,28)']]
    elif colorscale == 'Greys':
        colorscale = [[0, 'rgb(0,0,0)'], [1, 'rgb(255,255,255)']]
    elif colorscale == 'YlOrRd':
        colorscale = [
            [0, 'rgb(128,0,38)'], [0.125, 'rgb(189,0,38)'],
            [0.25, 'rgb(227,26,28)'], [0.375, 'rgb(252,78,42)'],
            [0.5, 'rgb(253,141,60)'], [0.625, 'rgb(254,178,76)'],
            [0.75, 'rgb(254,217,118)'], [0.875, 'rgb(255,237,160)'],
            [1, 'rgb(255,255,204)']
        ]
    return interpolate((current_weight - min_weight) / current_weight, colorscale)


def interpolate(frac, colorscale):
    for i in range(len(colorscale)):
        if i == len(colorscale):
            end = ast.literal_eval(colorscale[i][1].replace("rgb", "").replace("(", "[").replace(")", "]"))
            start = ast.literal_eval(colorscale[i - 1][1].replace("rgb", "").replace("(", "[").replace(")", "]"))
            end_ind = colorscale[i][0]
            start_ind = colorscale[i - 1][0]
            return 'rgb' + str(
                [s + (e - s) * ((frac - start_ind) / (end_ind - start_ind)) for s, e in zip(start, end)]).replace("[",
                                                                                                                  "(").replace(
                "]", ")")
        if colorscale[i][0] < frac and colorscale[i + 1][0] > frac:
            start = ast.literal_eval(colorscale[i][1].replace("rgb", "").replace("(", "[").replace(")", "]"))
            end = ast.literal_eval(colorscale[i + 1][1].replace("rgb", "").replace("(", "[").replace(")", "]"))
            end_ind = colorscale[i + 1][0]
            start_ind = colorscale[i][0]
            return 'rgb' + str(
                [int(s + (e - s) * ((frac - start_ind) / (end_ind - start_ind))) for s, e in zip(start, end)]).replace(
                "[", "(").replace("]", ")")

        if colorscale[i][0] == frac:
            return colorscale[i][1]
