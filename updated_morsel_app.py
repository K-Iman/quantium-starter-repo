from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ── 1. Load & prep data ──────────────────────────────────────────────────────
df = pd.read_csv('formatted_morsel_data.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

PRICE_INCREASE_DATE = pd.Timestamp('2021-01-15').timestamp() * 1000

REGION_COLORS = {
    'all':   '#FF6B9D',
    'north': '#00D4FF',
    'south': '#FFB347',
    'east':  '#7CFC8A',
    'west':  '#BF9FFF',
}

# ── 2. App init ───────────────────────────────────────────────────────────────
app = Dash(__name__)

# ── 3. External font (Google Fonts via CDN) ───────────────────────────────────
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Soul Foods — Pink Morsel Sales</title>
        {%favicon%}
        {%css%}
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
        <style>
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                background-color: #0A0A12;
                background-image:
                    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(255,107,157,0.18) 0%, transparent 70%),
                    repeating-linear-gradient(
                        0deg,
                        transparent,
                        transparent 39px,
                        rgba(255,255,255,0.02) 39px,
                        rgba(255,255,255,0.02) 40px
                    ),
                    repeating-linear-gradient(
                        90deg,
                        transparent,
                        transparent 39px,
                        rgba(255,255,255,0.02) 39px,
                        rgba(255,255,255,0.02) 40px
                    );
                min-height: 100vh;
                font-family: 'DM Sans', sans-serif;
                color: #E8E8F0;
                overflow-x: hidden;
            }

            /* Animated top bar */
            .top-bar {
                height: 3px;
                background: linear-gradient(90deg, #FF6B9D, #FF9F6B, #FFD96B, #6BFFD9, #6BB3FF, #C46BFF, #FF6B9D);
                background-size: 300% 100%;
                animation: shimmer 4s linear infinite;
            }
            @keyframes shimmer {
                0%   { background-position: 0% 0%; }
                100% { background-position: 300% 0%; }
            }

            /* Header */
            .header {
                text-align: center;
                padding: 48px 24px 24px;
                position: relative;
            }
            .header-eyebrow {
                font-family: 'DM Sans', sans-serif;
                font-size: 11px;
                font-weight: 500;
                letter-spacing: 0.3em;
                text-transform: uppercase;
                color: #FF6B9D;
                margin-bottom: 12px;
                opacity: 0;
                animation: fadeUp 0.6s ease forwards 0.2s;
            }
            .header-title {
                font-family: 'Bebas Neue', sans-serif;
                font-size: clamp(42px, 6vw, 80px);
                letter-spacing: 0.06em;
                line-height: 1;
                background: linear-gradient(135deg, #FFFFFF 0%, #FF6B9D 60%, #FFB347 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                opacity: 0;
                animation: fadeUp 0.6s ease forwards 0.4s;
            }
            .header-subtitle {
                font-size: 14px;
                font-weight: 300;
                color: rgba(232,232,240,0.5);
                margin-top: 10px;
                letter-spacing: 0.05em;
                opacity: 0;
                animation: fadeUp 0.6s ease forwards 0.6s;
            }
            @keyframes fadeUp {
                from { opacity: 0; transform: translateY(16px); }
                to   { opacity: 1; transform: translateY(0); }
            }

            /* Stats bar */
            .stats-bar {
                display: flex;
                justify-content: center;
                gap: 40px;
                padding: 20px 24px;
                opacity: 0;
                animation: fadeUp 0.6s ease forwards 0.8s;
            }
            .stat {
                text-align: center;
            }
            .stat-value {
                font-family: 'Bebas Neue', sans-serif;
                font-size: 28px;
                letter-spacing: 0.05em;
                color: #FF6B9D;
            }
            .stat-label {
                font-size: 10px;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                color: rgba(232,232,240,0.4);
                margin-top: 2px;
            }
            .stat-divider {
                width: 1px;
                background: rgba(255,255,255,0.08);
                align-self: stretch;
            }

            /* Controls panel */
            .controls-wrapper {
                display: flex;
                justify-content: center;
                padding: 16px 24px 28px;
                opacity: 0;
                animation: fadeUp 0.6s ease forwards 1s;
            }
            .controls-panel {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 16px;
                padding: 20px 32px;
                display: flex;
                align-items: center;
                gap: 24px;
                backdrop-filter: blur(8px);
            }
            .controls-label {
                font-size: 10px;
                font-weight: 500;
                letter-spacing: 0.25em;
                text-transform: uppercase;
                color: rgba(232,232,240,0.45);
                white-space: nowrap;
            }

            /* Radio buttons — override Dash defaults */
            .region-radio .form-check {
                display: inline-flex !important;
                align-items: center !important;
                gap: 6px !important;
                margin-right: 4px !important;
            }
            .region-radio label {
                cursor: pointer !important;
                padding: 8px 20px !important;
                border-radius: 30px !important;
                border: 1px solid rgba(255,255,255,0.12) !important;
                font-size: 13px !important;
                font-weight: 500 !important;
                letter-spacing: 0.05em !important;
                color: rgba(232,232,240,0.6) !important;
                transition: all 0.2s ease !important;
                background: transparent !important;
                user-select: none !important;
            }
            .region-radio label:hover {
                border-color: rgba(255,107,157,0.5) !important;
                color: #FF6B9D !important;
                background: rgba(255,107,157,0.06) !important;
            }
            .region-radio input[type="radio"] { display: none !important; }
            .region-radio input[type="radio"]:checked + label {
                background: rgba(255,107,157,0.15) !important;
                border-color: #FF6B9D !important;
                color: #FF6B9D !important;
                box-shadow: 0 0 16px rgba(255,107,157,0.2) !important;
            }

            /* Chart wrapper */
            .chart-wrapper {
                padding: 0 32px 48px;
                opacity: 0;
                animation: fadeUp 0.6s ease forwards 1.2s;
            }
            .chart-container {
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 20px;
                overflow: hidden;
                box-shadow:
                    0 0 0 1px rgba(255,107,157,0.05),
                    0 32px 80px rgba(0,0,0,0.6),
                    inset 0 1px 0 rgba(255,255,255,0.06);
                background: rgba(255,255,255,0.02);
            }

            /* Footer */
            .footer {
                text-align: center;
                padding: 24px;
                font-size: 11px;
                letter-spacing: 0.15em;
                color: rgba(232,232,240,0.2);
                text-transform: uppercase;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ── 4. Layout ─────────────────────────────────────────────────────────────────
app.layout = html.Div([

    html.Div(className='top-bar'),

    html.Div([
        html.Div('Soul Foods Analytics', className='header-eyebrow'),
        html.H1('Pink Morsel Sales Visualiser', className='header-title'),
        html.P('2018 – 2022  ·  Regional Performance Dashboard', className='header-subtitle'),
    ], className='header'),

    html.Div([
        html.Div([
            html.Div('$6,604', className='stat-value'),
            html.Div('Avg Daily Sales Before', className='stat-label'),
        ], className='stat'),
        html.Div(className='stat-divider'),
        html.Div([
            html.Div('+35.8%', className='stat-value', style={'color': '#7CFC8A'}),
            html.Div('Revenue Uplift Post-Increase', className='stat-label'),
        ], className='stat'),
        html.Div(className='stat-divider'),
        html.Div([
            html.Div('$8,972', className='stat-value', style={'color': '#7CFC8A'}),
            html.Div('Avg Daily Sales After', className='stat-label'),
        ], className='stat'),
    ], className='stats-bar'),

    html.Div([
        html.Div([
            html.Span('Filter by Region', className='controls-label'),
            dcc.RadioItems(
                id='region-radio',
                options=[
                    {'label': 'All Regions', 'value': 'all'},
                    {'label': 'North',       'value': 'north'},
                    {'label': 'South',       'value': 'south'},
                    {'label': 'East',        'value': 'east'},
                    {'label': 'West',        'value': 'west'},
                ],
                value='all',
                inline=True,
                className='region-radio',
                labelStyle={'display': 'inline-block'},
            ),
        ], className='controls-panel'),
    ], className='controls-wrapper'),

    html.Div([
        html.Div([
            dcc.Graph(id='sales-line-chart', config={'displayModeBar': False}),
        ], className='chart-container'),
    ], className='chart-wrapper'),

    html.Div('Soul Foods Confidential · Internal Use Only', className='footer'),

], style={'maxWidth': '1400px', 'margin': '0 auto'})


# ── 5. Callback ───────────────────────────────────────────────────────────────
@callback(Output('sales-line-chart', 'figure'), Input('region-radio', 'value'))
def update_chart(region):
    if region == 'all':
        plot_df = df.groupby('date', as_index=False)['sales-$'].sum()
        label = 'All Regions'
    else:
        plot_df = df[df['region'] == region].copy()
        label = region.capitalize()

    line_color = REGION_COLORS.get(region, '#FF6B9D')

    fig = go.Figure()

    # Shaded zones
    split = pd.Timestamp('2021-01-15')
    fig.add_vrect(
        x0=plot_df['date'].min(), x1=split,
        fillcolor='rgba(255,107,157,0.04)', line_width=0,
        annotation_text='PRE-INCREASE', annotation_position='top left',
        annotation_font=dict(size=9, color='rgba(255,107,157,0.35)', family='DM Sans'),
    )
    fig.add_vrect(
        x0=split, x1=plot_df['date'].max(),
        fillcolor='rgba(124,252,138,0.03)', line_width=0,
        annotation_text='POST-INCREASE', annotation_position='top right',
        annotation_font=dict(size=9, color='rgba(124,252,138,0.35)', family='DM Sans'),
    )

    # Main line
    fig.add_trace(go.Scatter(
        x=plot_df['date'],
        y=plot_df['sales-$'],
        mode='lines',
        name=label,
        line=dict(color=line_color, width=1.5),
        fill='tozeroy',
        fillcolor='rgba(255,255,255,0.05)',  # ✅ Fixed
        hovertemplate='<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>',
    ))

    # Price increase vline
    fig.add_vline(
        x=PRICE_INCREASE_DATE,
        line_dash='dot',
        line_color='rgba(255,200,100,0.7)',
        line_width=1.5,
        annotation_text='Price Increase · Jan 15, 2021',
        annotation_position='top',
        annotation_font=dict(size=10, color='rgba(255,200,100,0.8)', family='DM Sans'),
        annotation_bgcolor='rgba(255,200,100,0.08)',
        annotation_bordercolor='rgba(255,200,100,0.25)',
        annotation_borderwidth=1,
        annotation_borderpad=6,
    )

    fig.update_layout(
        title=dict(
            text=f'Sales Trend — <span style="color:{line_color}">{label}</span>',
            font=dict(family='Bebas Neue', size=22, color='rgba(232,232,240,0.85)'),
            x=0.02, xanchor='left', y=0.97,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='rgba(232,232,240,0.7)'),
        xaxis=dict(
            title='Date',
            title_font=dict(size=11, color='rgba(232,232,240,0.4)'),
            tickfont=dict(size=11),
            gridcolor='rgba(255,255,255,0.04)',
            linecolor='rgba(255,255,255,0.1)',
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title='Total Sales ($)',
            title_font=dict(size=11, color='rgba(232,232,240,0.4)'),
            tickfont=dict(size=11),
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.1)',
            showgrid=True,
            zeroline=False,
            tickprefix='$',
            tickformat=',',
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='rgba(10,10,18,0.95)',
            bordercolor=line_color,
            font=dict(family='DM Sans', size=12, color='#E8E8F0'),
        ),
        margin=dict(l=60, r=40, t=60, b=60),
        height=480,
        showlegend=False,
    )

    return fig


# ── 6. Run ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)