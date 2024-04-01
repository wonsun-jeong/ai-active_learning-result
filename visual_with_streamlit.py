import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

color_chart = px.colors.qualitative.Light24
slicing_color_chart = color_chart[:14]
all_strategy_list = ["RS", "LCDO", "MSDO", "ESDO"]

data = pd.read_csv('./data/AL_all_result.csv')

def each_strategy_fig(base_fig, data, each_strategy, each_color):
    base_fig.add_trace(
        go.Scatter(
            x=data['round'],
            y=data[each_strategy],
            mode='lines',
            line=dict(color=f'{each_color}'),
            name=each_strategy,))

    max_score_round = data.loc[data[each_strategy].idxmax()]

    base_fig.add_trace(go.Scatter(
        x=[max_score_round['round']],
        y=[max_score_round[each_strategy]],
        mode='markers',
        marker=dict(
            size=10,
            color=f'{each_color}',
            symbol='star'),
        name='Max score')
    )

    base_fig.add_annotation(
        x=max_score_round['round'],
        y=max_score_round[each_strategy],
        text=f"{max_score_round[each_strategy]:.3f}",
        showarrow=False,
        xshift=5,
        yshift=12
    )

def each_class_fig(each_class, each_full_train_value, each_range, each_tick_value,
                   strategy_list=all_strategy_list, color_list=slicing_color_chart):
    fig = go.Figure()

    baseline_value = each_full_train_value

    fig.add_shape(type='line',
                  x0=0, y0=baseline_value,
                  x1=250, y1=baseline_value,
                  line=dict(color='grey', dash='dashdot', width=1))

    fig.add_annotation(
        x=data['round'].max(),
        y=baseline_value,
        text=f"<b style='font-size: 11pt;'>Full train: {baseline_value:.3f}</b>",
        showarrow=False,
        xshift=67,
        yshift=0
    )

    for i in range(len(strategy_list)):
        this_strategy = strategy_list[i]
        this_color = color_list[i]
        target = this_strategy + f'_{each_class}'

        each_strategy_fig(base_fig=fig, data=data, each_strategy=target, each_color=this_color)

    fig.update_layout(
        title=f'Active learning-{each_class} beat',
        xaxis_title='Round (Each round query 100 data.)',
        yaxis_title='f1 score',
        showlegend=True,
        xaxis=dict(range=[1, data['round'].max()],
                   dtick=10),
        yaxis=dict(range=each_range,
                   dtick=each_tick_value,
                   zeroline=True,
                   zerolinecolor='lightgrey'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis_gridcolor='lightgrey',
        margin=dict(
            l=70,
            r=150,
            b=50,
            t=50),
        legend=dict(x=1.06, y=0,
                    xanchor='right', yanchor='bottom'))

    fig.update_xaxes(ticks="outside", showline=True, linecolor='lightgrey')
    fig.update_yaxes(showline=True, linecolor='lightgrey')

    return fig

# Display the Streamlit app
st.title("Active Learning Beats")

class_list = ['N', 'S', 'V']
full_train_value = [0.95719087, 0.80864413, 0.92291774]
minmax_range = [[0.78, 0.98], [0.0, 0.9], [0.0, 0.99]]
tick_value_list = [0.02, 0.1, 0.1]

for beat_class, beat_baseline, y_range, class_tick in zip(class_list, full_train_value, minmax_range, tick_value_list):
    fig = each_class_fig(beat_class, beat_baseline, y_range, class_tick)

    for trace in fig.data:
        if 'Max score' in trace.name:
            trace.showlegend = False
            trace.legendgroup = 'Max score'

    st.plotly_chart(fig)
