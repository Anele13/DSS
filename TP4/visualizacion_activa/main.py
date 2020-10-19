import pandas as pd

from bokeh.layouts import column, row
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.autompg import autompg_clean as df
import os


here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'datos.csv')

df = pd.read_csv(filename)
df = df.copy()

SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)


columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]


def create_figure():
  
    if provincia.value != 'Todas':
        df2 = df.loc[df.provincia == provincia.value]
        xs = df2[x.value].values
        ys = df2[y.value].values
        x_title = x.value.title()
        y_title = y.value.title()
    else:
        xs = df[x.value].values
        ys = df[y.value].values
        x_title = x.value.title()
        y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    p = figure(plot_height=1000, plot_width=1200, tools='pan,box_zoom,hover,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9

    c = "#31AADE"
    """
    if color.value != 'None':
        if len(set(df[color.value])) > N_COLORS:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[xx] for xx in groups.codes]
    """

    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='fecha', options=['fecha'])
x.on_change('value', update)

y = Select(title='Y-Axis', value='tot_casosconf', options=['tot_casosconf','penetracion_casos'])
y.on_change('value', update)

provincia = Select(title='Provincia', value='Todas', options=df.provincia.unique().tolist()+['Todas'])
provincia.on_change('value', update)

controls = column(x, y, provincia, width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Crossfilter"
