import streamlit as st
import pandas as pd
from collect_data import *
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

ct = time.time()

st.set_page_config(layout="wide", page_title="Stock Analysis")


try:
    col1, col2, col3 = st.columns(3)
    st.markdown(
        "<h1 style='text-align: center;'>Indian Stock Analysis Tool</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h4 style='text-align: center;'>Analyze any Indian listed stock with 65+ interactive plots covering financials, trends, and key metrics.</h4><br>",
        unsafe_allow_html=True,
    )

    comp = st.selectbox("Select company", allComp)

    col1, col2, col3 = st.columns([3, 1, 3])

    with col2:
        btn = st.button("Show Analysis")

    if btn:
        placeholder = st.empty()

        # loading gif
        with placeholder.container():
            col1, col2, col3 = st.columns([3, 1, 3])
            with col2:
                st.write("Loading... Please wait")
                st.image("https://i.gifer.com/ZZ5H.gif", width=100)

        table = [
            "🔑 Key Metrics",
            "✅ Pros & Cons",
            "🚀 CAGR",
            "🤝 Peers",
            "🕒 Quarter-wise",
            "📉 P&L",
            "🏦 Balance Sheet",
            "💰 Cash Flows",
            "📊 Ratios YoY",
            "📈 Share Holding",
            "📌 Similar Companies",
        ]

        st.header("Table of Contents")
        # Build navbar HTML list items
        ht = ""
        for i, title in enumerate(table):
            ht += f'<li><a href="#{i}">{title}</a></li>'

        st.markdown(
            f"""
        <style>
        .toc-container {{
            position: -webkit-sticky;
            position: sticky;
            top: 0;
            display: flex;
            flex-wrap: wrap;
            list-style-type: none;
            padding: 8px;
            margin: 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            z-index: 9999;
        }}
        .toc-container li {{
            margin: 4px 12px;
            padding: 6px 10px;
            color: #333;
            background: #e0e0e0;
            border-radius: 6px;
            transition: all 0.2s ease-in-out;
        }}
        .toc-container a {{
            color: #0073e6;        /* link color */
            text-decoration: none; /* removes underline */
            font-weight: 600;
        }}
        .toc-container a:hover {{
            text-decoration: underline; /* underline on hover */
        }}
        .toc-container li:hover {{
            background: #4CAF50;
            color: white;
            transform: scale(1.05);
            cursor: pointer;
        }}
        
        </style>
        <div style="overflow: scroll"> 
        <ul class="toc-container">
            {ht}
        </ul><div/>
        """,
            unsafe_allow_html=True,
        )

        # Add content sections with matching IDs

        key_met = getKeymetrics(comp)
        st.header("Key metrics")
        st.markdown('<br id="0">', unsafe_allow_html=True)
        col = st.columns(3)
        colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
            "#FF5733",
            "#33FFCE",
        ]

        for i in range(len(key_met[0])):
            with col[i % 3]:
                st.markdown(
                    f"""
                    <div style="border:1px solid #444;padding:10px;border-radius:10px;background-color:#111;">
                        <div style="font-weight:bold;color:#ccc;font-size:14px;">{key_met[0][i]}</div>
                        <div style="font-size:20px;color:{colors[i % len(colors)]};">{key_met[1][i]}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        st.divider()

        # Pros and Cons
        st.header("Pros and Cons")
        st.markdown('<br id="1">', unsafe_allow_html=True)
        pros, cons = getpts(comp)

        # Create columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Pros")
            htmlp = ""
            for pro in pros:
                htmlp += f"<li>{pro}</li>"
            if len(htmlp) == 0:
                htmlp += f"<li>No pros</li>"
            st.markdown(
                f'<div style="border:2px solid white;text-align:left;color:green;border-radius:8px;padding:10px;min-height:150px;display: flex;align-items:center"><ul>{htmlp}</ul></div>',
                unsafe_allow_html=True,
            )

        with col2:
            st.subheader("Cons")
            htmlp = ""
            for pro in cons:
                htmlp += f"<li>{pro}</li>"
            if len(htmlp) == 0:
                htmlp += f"<li>No Cons</li>"
            st.markdown(
                f'<div style="border:2px solid white;text-align:left;color:red;border-radius:8px;padding:10px;min-height:150px;display: flex;align-items: center;"><ul>{htmlp}</ul></div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # CAGR graphs
        st.header("CAGR values")
        st.markdown('<br id="2">', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        df = getCAGR(comp)
        st.dataframe(df)

        st.subheader("CAGR visualisation")
        for col in df.columns.to_list():
            fig = px.bar(
                df,
                y=col,
                x=df.index,
                title=f"{col} (%) ",
                color=df.index,
                text_auto=True,
            )
            st.plotly_chart(fig, theme=None)

        st.divider()

        # peers data
        peers = peers_table(comp)
        st.header("Peers Comparision")
        st.markdown('<br id="3">', unsafe_allow_html=True)
        st.dataframe(peers)

        companyName = getCompName()
        pull = [0 if companyName != i else 0.2 for i in peers["Name"]]
        fig = make_subplots(
            rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
        )

        st.subheader("Peers visualisation")
        # Add Market Cap pie
        fig.add_trace(
            go.Pie(
                labels=peers["Name"],
                values=peers["Mar Cap Rs.Cr."],
                name="Market cap share among peers",
                pull=pull,
                hole=0.4,  # Optional: donut style
            ),
            1,
            1,
        )

        # Add Sales pie
        fig.add_trace(
            go.Pie(
                labels=peers["Name"],
                values=peers["Sales Qtr Rs.Cr."],
                pull=pull,
                name="Sales share among peers",
                hole=0.4,  # Optional: donut style
            ),
            1,
            2,
        )

        # Update hover info and colors
        fig.update_traces(
            hoverinfo="label+percent+name",
            textinfo="percent",
            textfont_size=12,
            marker=dict(
                line=dict(color="#000000", width=2)  # Black border around slices
            ),
        )

        # Layout
        fig.update_layout(
            title_text="Peer Comparison: Market Cap and Sales Share comparision among peers",
            annotations=[
                dict(text="Market Cap", x=0.20, y=0.5, font_size=14, showarrow=False),
                dict(text="Sales", x=0.80, y=0.5, font_size=14, showarrow=False),
            ],
        )

        st.plotly_chart(fig, use_container_width=True)
        for col in peers.columns.to_list()[1:]:
            fig = px.bar(
                peers,
                y=col,
                x="Name",
                title=f"Peers comparision of {col}",
                text_auto=True,
                color="Name",
            )
            st.plotly_chart(fig, theme=None)

        st.divider()
        dfs = collectDataStandalone(comp)
        (
            quarterly_results_Standalone,
            Profit_Loss_Standalone,
            Balance_sheet_Standalone,
            Cash_flows_Standalone,
            ratios_Standalone,
            share_holding_pattern_Standalone,
        ) = dfs

        dfs = collectDataConsolidated(comp)
        (
            quarterly_results_Consolidated,
            Profit_Loss_Consolidated,
            Balance_sheet_Consolidated,
            Cash_flows_Consolidated,
            ratios_Consolidated,
            share_holding_pattern_Consolidated,
        ) = dfs

        quarterly_results_Consolidated.drop(["Raw PDF"], axis=1, inplace=True)
        quarterly_results_Standalone.drop(["Raw PDF"], axis=1, inplace=True)

        st.header("Quater wise Analysis")
        st.markdown('<br id="4">', unsafe_allow_html=True)
        for col in quarterly_results_Consolidated.columns.to_list():
            trace1 = go.Scatter(
                x=quarterly_results_Standalone.index,
                y=quarterly_results_Standalone[col],
                mode="lines+markers",
                name="standalone",
                marker=dict(size=8, symbol="circle"),
                line=dict(width=2),
            )
            trace2 = go.Scatter(
                x=quarterly_results_Consolidated.index,
                y=quarterly_results_Consolidated[col],
                mode="lines+markers",
                name="consolidated",
                marker=dict(size=8, symbol="square"),
                line=dict(width=2, dash="dot"),
            )

            data = [trace1, trace2]

            title = "amount in crores"
            if col in ["Tax ", "OPM "]:
                title = "Percentage %"

            layout = go.Layout(
                title=f"Quaterly analsis of {col}",
                xaxis={"title": "time"},
                yaxis={"title": title},
            )
            fig = go.Figure(data, layout)
            st.plotly_chart(fig, theme=None)

        st.divider()

        # profit loss analysis
        st.header("Profit Loss Analysis YoY")
        st.markdown('<br id="5">', unsafe_allow_html=True)
        for col in Profit_Loss_Consolidated.columns.to_list():
            trace1 = go.Scatter(
                x=Profit_Loss_Standalone.index,
                y=Profit_Loss_Standalone[col],
                mode="lines+markers",
                name="standalone",
            )
            trace2 = go.Scatter(
                x=Profit_Loss_Consolidated.index,
                y=Profit_Loss_Consolidated[col],
                mode="lines+markers",
                name="consolidated",
                marker=dict(size=8, symbol="square"),
                line=dict(width=2, dash="dot"),
            )

            data = [trace1, trace2]
            title = "amount in crores"

            if col in ["Tax ", "OPM "]:
                title = "Percentage %"

            layout = go.Layout(
                title=f"Profit loss analsis of {col}",
                xaxis={"title": "time"},
                yaxis={"title": title},
            )
            fig = go.Figure(data, layout)
            st.plotly_chart(fig, theme=None)

        st.divider()

        # balance sheet analysis
        st.markdown('<br id="6">', unsafe_allow_html=True)
        st.header("Balance sheet analysis YOY")
        for col in Balance_sheet_Standalone.columns.to_list():
            trace1 = go.Scatter(
                x=Balance_sheet_Standalone.index,
                y=Balance_sheet_Standalone[col],
                mode="lines+markers",
                name="standalone",
            )
            trace2 = go.Scatter(
                x=Balance_sheet_Consolidated.index,
                y=Balance_sheet_Consolidated[col],
                mode="lines+markers",
                name="consolidated",
                marker=dict(size=8, symbol="square"),
                line=dict(width=2, dash="dot"),
            )
            data = [trace1, trace2]
            layout = go.Layout(
                title=f"Balance sheet analsis of {col}",
                xaxis={"title": "time"},
                yaxis={"title": "amount in crores"},
            )
            fig = go.Figure(data, layout)
            st.plotly_chart(fig, theme=None)

        st.divider()

        # cash flow analysis
        st.markdown('<br id="7">', unsafe_allow_html=True)
        st.header("Cash Flows Analysis YoY")
        for col in Cash_flows_Standalone.columns.to_list():
            trace1 = go.Scatter(
                x=Cash_flows_Standalone.index,
                y=Cash_flows_Standalone[col],
                mode="lines+markers",
                name="standalone",
            )
            trace2 = go.Scatter(
                x=Cash_flows_Consolidated.index,
                y=Cash_flows_Consolidated[col],
                mode="lines+markers",
                name="consolidated",
                marker=dict(size=8, symbol="square"),
                line=dict(width=2, dash="dot"),
            )
            data = [trace1, trace2]
            layout = go.Layout(
                title=f"Cash_flows analysis of {col}",
                xaxis={"title": "time"},
                yaxis={"title": "amount in crores"},
            )
            fig = go.Figure(data, layout)
            st.plotly_chart(fig, theme=None)

        st.divider()

        # ratio analysis
        st.markdown('<br id="8">', unsafe_allow_html=True)
        st.header("Analysis of Ratio's YoY")
        for col in ratios_Standalone.columns.to_list():
            trace1 = go.Bar(
                x=ratios_Standalone.index,
                y=ratios_Standalone[col],
                name="standalone",
                text=ratios_Standalone[col],
                textposition="auto",
            )
            trace2 = go.Bar(
                x=ratios_Consolidated.index,
                y=ratios_Consolidated[col],
                name="consolidated",
                text=ratios_Consolidated[col],
                textposition="auto",
            )
            data = [trace1, trace2]
            layout = go.Layout(
                title=f"ratios analsis of {col}",
                xaxis={"title": "time"},
                yaxis={"title": "ratio"},
            )
            fig = go.Figure(data, layout)
            st.plotly_chart(fig, theme=None)

        st.divider()

        # Share Holding Pattern Analysis

        st.header("Share Holding Pattern Analysis YoY")
        st.markdown('<br id="9">', unsafe_allow_html=True)
        col = st.columns(2)
        i = 0
        for ind in share_holding_pattern_Consolidated.index:

            with col[i % 2]:
                fig = px.pie(
                    values=[
                        share_holding_pattern_Consolidated.loc[ind, col]
                        for col in share_holding_pattern_Consolidated.columns.to_list()[
                            :-1
                        ]
                    ],
                    names=[
                        col
                        for col in share_holding_pattern_Consolidated.columns.to_list()[
                            :-1
                        ]
                    ],
                    title=ind,
                )
                st.plotly_chart(fig, theme=None)
            i += 1

        if (
            "No. of Shareholders"
            in share_holding_pattern_Consolidated.columns.to_list()
        ):
            trace2 = go.Scatter(
                x=share_holding_pattern_Consolidated.index,
                y=share_holding_pattern_Consolidated["No. of Shareholders"],
                marker=dict(symbol="square", color="red", size=8),
                line=dict(color="blue"),
            )
            data = [trace2]
            title = "No of Shareholders "
            layout = go.Layout(
                title=f"No of shareholders over the year",
                xaxis={"title": "year"},
                yaxis={"title": title},
            )
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig)

        # similar companies
        st.divider()
        st.header("Similar Companies")
        st.markdown('<br id="10">', unsafe_allow_html=True)
        col = st.columns(4)
        for i in range(len(peers)):
            with col[i % 4]:
                st.write(peers["Name"][i])

        placeholder.success(f"Done loading in {(time.time()-ct)} seconds")

except Exception as E:
    placeholder.empty()
    print(E)
    st.error(
        "⚠️ An error occurred. Please reload the page or try again after some time. We are working on it!"
    )
    # placeholder.fa("Done loaded Succesfully!")
