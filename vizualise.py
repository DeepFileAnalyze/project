import igraph as ig
import json
import plotly.plotly as py
from plotly.graph_objs import *
import plotly

def vizualise():
    plotly.tools.set_credentials_file(username='liskior', api_key='kzd46P6dYy85bxhKUbnG')

    data = []
    f = open("g.json")
    data = json.loads(f.read())

    N=len(data['nodes'])
    print(N)
    L=len(data['links'])
    Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

    G=ig.Graph(Edges, directed=False)
    data['nodes'][0]
    labels=[]
    group=[]
    desc=[]
    for node in data['nodes']:
        labels.append(node['name'])
        group.append(node['group'])
        desc.append(node['desc'])

    layt=G.layout('kk', dim=3)

    Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
    Yn=[layt[k][1] for k in range(N)]# y-coordinates
    Zn=[layt[k][2] for k in range(N)]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for e in Edges:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]

    trace1=Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=Line(color='rgb(125,125,125)', width=1),
                   hoverinfo='none'
                   )
    trace2=Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode='markers',
                   name=desc,
                   marker=Marker(symbol='dot',
                                 size=6,
                                 color=group,
                                 colorscale='Viridis',
                                 line=Line(color='rgb(50,50,50)', width=0.5)
                                 ),
                   text=desc,

                   hoverinfo='text'
                   )

    axis=dict(showbackground=False,
              showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )
    layout = Layout(
             title="Lecture (3D visualization)",
             width=1000,
             height=1000,
             showlegend=False,
             scene=Scene(
             xaxis=XAxis(axis),
             yaxis=YAxis(axis),
             zaxis=ZAxis(axis),
            ),
         margin=Margin(
            t=100
        ),
        hovermode='closest',
        annotations=Annotations([
               Annotation(
               showarrow=False,
                text="Data source: Lecture",
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=Font(
                size=14
                )
                )
            ]),    )

    data=Data([trace1, trace2])
    fig=Figure(data=data, layout=layout)

    py.iplot(fig, filename='Lecture')