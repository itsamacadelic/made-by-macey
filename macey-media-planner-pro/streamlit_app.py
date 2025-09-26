# Streamlit app entry point for Macey Media Planner Pro

import streamlit as st


st.title("Macey Media Planner Pro")
st.markdown("""
An interactive tool for strategists to build data-driven media plans with AI-powered rationale.
""")


with st.form("media_plan_form"):
	st.header("Enter Media Plan Inputs")
	business_objective = st.selectbox(
		"Business Objective",
		["Awareness", "Sales", "Leads", "Engagement", "Other"]
	)
	funnel_phase = st.selectbox(
		"Funnel Phase",
		["Full Funnel", "Awareness", "Consideration", "Conversion"]
	)
	budget = st.number_input("Total Budget ($)", min_value=1000, step=1000)
	budget_flex = st.slider("Budget Flexibility (%)", 0, 50, 10)
	kpis = st.multiselect(
		"Success KPIs",
		[
			"ROAS", "Reach", "Lift", "Impressions", "Clicks", "Conversions", "CTR", "CPM", "CPC", "VCR (Video Completion Rate)",
			"Video Views", "Brand Lift", "Audio Completes", "Audio Listens", "Viewable Impressions", "Engagement Rate", "Cost per Completed View (CPCV)",
			"Cost per Action (CPA)", "Cost per Lead (CPL)", "Revenue", "Signups", "Form Fills", "Social Actions", "Other"
		]
	)
	audience_demo = st.text_input("Audience Demographics (age, gender, etc.)")
	audience_psych = st.text_input("Audience Psychographics (interests, values, etc.)")
	commerce_bias = st.selectbox(
		"Commerce Bias",
		["Retail", "DTC", "Social Commerce", "Omnichannel", "Other"]
	)
	brand_vibe = st.multiselect(
		"Brand Vibe",
		["Urgency", "Authority", "Belonging", "Discovery", "Aspiration", "Value", "Other"]
	)
	competitor_activity = st.text_area(
		"Competitor Activity (where are they heavy/light, known spend, etc.)"
	)
	market_factors = st.text_area(
		"Market Factors (CPM inflation, audience channel affinity, etc.)"
	)

	# Holistic channel categories
	holistic_channels = [
		"Search", "Paid Social", "Retail Media", "Display", "Video", "Audio", "Influencer", "Affiliate", "CTV/OTT", "OOH", "Other"
	]

	must_have_channels = st.multiselect(
		"Must-Have Channel Types",
		holistic_channels
	)

	avoid_channels = st.multiselect(
		"Channel Types to Avoid",
		holistic_channels
	)
	geos = st.text_input("Geos (regions, markets, etc.)")
	legal_notes = st.text_area("Legal/Compliance Notes")
	submitted = st.form_submit_button("Generate Media Plan")


# Measurement Framework Builder
st.header("Measurement Framework Builder")
st.markdown("""
Map your business objective to a measurement framework, from big KPIs to tactical optimization metrics.
""")


# Expanded measurement map with more media KPIs and funnel phases
measurement_map = {
	"Awareness": ["Reach", "Impressions", "CPM", "Video Views", "Brand Lift", "Viewable Impressions", "Audio Listens"],
	"Consideration": ["Video Completion Rate", "VCR (Video Completion Rate)", "Audio Completes", "Engagement Rate", "Clicks", "CTR", "Social Actions"],
	"Conversion": ["Conversions", "ROAS", "CPA", "CPC", "CPL", "Revenue", "Signups", "Form Fills", "Cost per Completed View (CPCV)", "Cost per Action (CPA)", "Cost per Lead (CPL)", "Other"],
	"Full Funnel": [
		"Reach", "Impressions", "CPM", "Video Views", "Brand Lift", "Viewable Impressions", "Audio Listens",
		"Video Completion Rate", "VCR (Video Completion Rate)", "Audio Completes", "Engagement Rate", "Clicks", "CTR", "Social Actions",
		"Conversions", "ROAS", "CPA", "CPC", "CPL", "Revenue", "Signups", "Form Fills", "Cost per Completed View (CPCV)", "Cost per Action (CPA)", "Cost per Lead (CPL)", "Other"
	],
	"Other": ["Custom"]
}

selected_phase = funnel_phase if 'funnel_phase' in locals() else "Full Funnel"
st.subheader(f"Measurement Framework for: {selected_phase}")
metrics = measurement_map.get(selected_phase, ["Custom"])
selected_metrics = st.multiselect(
	"Select/Customize Metrics to Track",
	options=metrics,
	default=metrics
)



import pandas as pd
from utils import engine, narrative

if submitted:
	st.success("Inputs received! Generating media plan...")
	st.info(f"**Measurement Framework:** {selected_metrics}")

	# Example: Show budget reserved for must-have channels and available for others
	must_have_budget = budget * 0.5 if must_have_channels else 0
	other_budget = budget - must_have_budget
	if must_have_channels:
		st.markdown(f"**Budget reserved for must-have channels:** ${must_have_budget:,.0f}")
		st.markdown(f"**Budget available for other channels:** ${other_budget:,.0f}")

	# --- ENGINE LOGIC (simple demo) ---
	# Assign base weights to holistic channels (for demo, equal weights)
	weights = {ch: 1 for ch in holistic_channels if ch not in avoid_channels}
	# Must-have channels get double weight
	for ch in must_have_channels:
		if ch in weights:
			weights[ch] *= 2
		else:
			weights[ch] = 2
	# Prepare channel list
	selected_channels = [ch for ch in holistic_channels if ch not in avoid_channels]

	# Dummy cost benchmarks for holistic channels
	cost_benchmarks = pd.DataFrame({
		"channel": holistic_channels,
		"CPC": [2, 1.5, 1.8, 1.2, 1.3, 1.1, 2.5, 2.2, 2.8, 3.0, 2.0],
		"CPM": [30, 12, 18, 10, 20, 8, 25, 22, 28, 35, 15]
	})

	# Run allocation
	allocation = engine.allocate_budget(
		selected_channels,
		weights,
		budget,
		cost_benchmarks=cost_benchmarks,
		kpi_focus=selected_metrics[0] if selected_metrics else None
	)

	# Show channel mix table
	mix_df = pd.DataFrame({
		"Channel": list(allocation.keys()),
		"% Allocation": [v / budget * 100 for v in allocation.values()],
		"Budget ($)": [v for v in allocation.values()]
	})
	st.subheader("Recommended Channel Mix")
	st.dataframe(mix_df.style.format({"% Allocation": "{:.1f}%", "Budget ($)": "${:,.0f}"}))

	# --- NARRATIVE LOGIC ---
	rationale = narrative.generate_narrative(allocation)
	st.subheader("Strategy Narrative")
	st.markdown(rationale)
