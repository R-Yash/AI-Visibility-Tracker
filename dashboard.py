from narwhals.typing import Backend
import streamlit as st
import pandas as pd
import plotly.express as px
from main import calculate_ai_visibility, calculate_ai_citation_score, generate_prompts

# Page Config
st.set_page_config(page_title="AI Brand Visibility Tracker", layout="wide")

st.title("🤖 AI Brand Share of Voice Tracker")
st.markdown("Analyze how generative AI perceives your brand vs. competitors.")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("Configuration")
category_input = st.sidebar.text_input("Category", value="CRM Software")
brands_input = st.sidebar.text_area("Brands (comma separated)", value="Salesforce, HubSpot, Pipedrive")

if st.sidebar.button("Run Analysis"):
    with st.spinner('Running AI Analysis... (This may take a minute)'):
        # 1. Parse Inputs
        brands_list = [b.strip() for b in brands_input.split(",")]
        prompts = generate_prompts(category_input)['prompts']
        vis_data = calculate_ai_visibility(brands=brands_list, prompts=prompts)
        cit_data = calculate_ai_citation_score(brands=brands_list, prompts=prompts)
        
        # --- DASHBOARD ROW 1: KEY METRICS ---
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        
        # Helper to find top brand
        vis_metrics = vis_data['metrics']
        top_vis_brand = max(vis_metrics, key=lambda x: vis_metrics[x]['visibility_score'])
        
        col1.metric("Total Prompts Analyzed", vis_data['total_prompts'])
        col2.metric("Most Visible Brand", top_vis_brand, f"{vis_metrics[top_vis_brand]['visibility_score']:.1f}% Visibility")
        col3.metric("Total Citations Scanned", sum([m['raw_citations'] for m in cit_data['metrics'].values()]))
        
        st.divider()

        # --- DASHBOARD ROW 2: LEADERBOARD ---
        st.subheader("🏆 Competitive Leaderboard")
        
        # Prepare Data for Plotting
        chart_data = []
        for brand in brands_list:
            chart_data.append({
                "Brand": brand,
                "AI Visibility %": vis_metrics[brand]['visibility_score'],
                "Citation Share %": cit_data['metrics'][brand]['share_of_voice']
            })
        
        df_chart = pd.DataFrame(chart_data)
        
        # Double Bar Chart
        fig = px.bar(
            df_chart, 
            x="Brand", 
            y=["AI Visibility %", "Citation Share %"],
            barmode='group',
            title="Brand Visibility vs. Search Citation Share",
            color_discrete_sequence=["#4C7BF4", "#00C896"]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- DASHBOARD ROW 3: DETAILED ANALYSIS ---
        tab1, tab2, tab3 = st.tabs(["📄 Prompt Analysis", "🔗 Top Cited Pages", "💬 Context Clouds"])

        # TAB 1: Prompts Table
        with tab1:
            st.markdown("### Which prompts triggered your brand?")
            
            # Convert breakdown list to DataFrame
            breakdown_data = []
            for item in vis_data['breakdown']:
                breakdown_data.append({
                    "User Query (Generated)": item['prompt'],
                    "Brands Mentioned": ", ".join(item['brands_mentioned']) if item['brands_mentioned'] else "❌ None",
                    "Response Preview": item['response_preview']
                })
            
            st.dataframe(
                pd.DataFrame(breakdown_data), 
                use_container_width=True,
                column_config={
                    "User Query (Generated)": st.column_config.TextColumn(width="medium"),
                    "Brands Mentioned": st.column_config.TextColumn(width="small"),
                }
            )

        # TAB 2: Cited Pages
        with tab2:
            st.markdown("### Where is the AI getting its info?")
            if cit_data['top_pages']:
                df_pages = pd.DataFrame(cit_data['top_pages'])
                # Count frequency of each URL to see top sources
                url_counts = df_pages['url'].value_counts().reset_index()
                url_counts.columns = ['URL', 'Citations Count']
                st.dataframe(url_counts, use_container_width=True)
            else:
                st.info("No web citations found for this category.")

        # TAB 3: Contexts
        with tab3:
            st.markdown("### How was the brand described?")
            selected_brand = st.selectbox("Select Brand", brands_list)
            contexts = vis_metrics[selected_brand]['contexts']
            
            if contexts:
                for ctx in contexts:
                    st.success(f"🗣️ \"{ctx}\"")
            else:
                st.warning("No specific context sentences found for this brand.")

else:
    st.info("Enter a category and brands in the sidebar, then click 'Run Analysis' to start.")

