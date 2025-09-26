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
	budget = st.number_input("Total Budget ($)", min_value=1000, step=1000)
	budget_flex = st.slider("Budget Flexibility (%)", 0, 50, 10)
	kpis = st.multiselect(
		"Success KPIs",
		["ROAS", "Reach", "Lift", "Impressions", "Clicks", "Conversions", "Other"]
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
	must_use_channels = st.multiselect(
		"Must-Use Channels",
		[
			"Google Search", "Meta (Facebook/Instagram)", "Amazon Ads", "Walmart Connect",
			"Roundel (Target)", "Best Buy Ads", "YouTube", "TikTok"
		]
	)
	avoid_channels = st.multiselect(
		"Channels to Avoid",
		[
			"Google Search", "Meta (Facebook/Instagram)", "Amazon Ads", "Walmart Connect",
			"Roundel (Target)", "Best Buy Ads", "YouTube", "TikTok"
		]
	)
	geos = st.text_input("Geos (regions, markets, etc.)")
	legal_notes = st.text_area("Legal/Compliance Notes")
	submitted = st.form_submit_button("Generate Media Plan")


# Measurement Framework Builder
st.header("Measurement Framework Builder")
st.markdown("""
Map your business objective to a measurement framework, from big KPIs to tactical optimization metrics.
""")

measurement_map = {
	"Awareness": ["Reach", "Impressions", "CPM", "Video Views", "Brand Lift"],
	"Engagement": ["Clicks", "CTR", "Video Completion Rate", "Social Actions"],
	"Sales": ["Conversions", "ROAS", "CPA", "Revenue"],
	"Leads": ["Leads", "CPL", "Form Fills", "Signups"],
	"Other": ["Custom"]
}

selected_objective = business_objective if 'business_objective' in locals() else "Awareness"
st.subheader(f"Measurement Framework for: {selected_objective}")
metrics = measurement_map.get(selected_objective, ["Custom"])
selected_metrics = st.multiselect(
	"Select/Customize Metrics to Track",
	options=metrics + ["Clicks", "CTR", "CPM", "CPC", "Conversions", "ROAS", "Other"],
	default=metrics
)

if submitted:
	st.success("Inputs received! (Next: connect to engine and narrative modules.)")
	st.info(f"**Measurement Framework:** {selected_metrics}")
