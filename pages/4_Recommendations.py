import streamlit as st

from database import SessionLocal
from crud import save_recommendation, get_recommendations_dataframe, get_recommendation_impact, mark_recommendation_followed
from ai_query import get_recommendation

st.set_page_config(page_title="Recommendations", page_icon="💡")
st.title("💡 Cost-Saving Recommendations")

if "active_business_id" not in st.session_state:
    st.warning("No business selected. Please go to the home page first.")
    st.stop()

business_id = st.session_state.active_business_id

st.write("Get an AI-generated recommendation on how to shift your energy usage to reduce costs.")

if st.button("Generate Recommendation"):
    with st.spinner("Analyzing your energy data..."):
        session = SessionLocal()
        recommendation = get_recommendation(session, business_id)
        save_recommendation(session, business_id, recommendation)
        session.close()

    st.text(recommendation)

st.subheader("Past Recommendations")

session = SessionLocal()
recs_df = get_recommendations_dataframe(session, business_id)

if recs_df.empty:
    st.info("No recommendations generated yet.")
else:
    for _, row in recs_df.iterrows():
        with st.expander(f"{row['created_at'].strftime('%B %d, %Y')}"):
            st.text(row["recommendation_text"])

            followed_status = row.get("followed")
            if followed_status is None:
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("I followed this", key=f"followed_yes_{row['id']}"):
                        mark_recommendation_followed(session, row["id"], True)
                        st.rerun()
                with col_no:
                    if st.button("I didn't follow this", key=f"followed_no_{row['id']}"):
                        mark_recommendation_followed(session, row["id"], False)
                        st.rerun()
            elif followed_status:
                st.caption("✅ You followed this recommendation")
            else:
                st.caption("⏭️ You didn't follow this recommendation")

            impact = get_recommendation_impact(session, business_id, row["id"])
            if not impact["possible"]:
                st.caption(impact.get("reason", "Not enough data to measure impact yet."))
            else:
                if impact["improved"]:
                    st.success(
                        f"Spending dropped from \\${impact['before_cost']:,.2f} to "
                        f"\\${impact['after_cost']:,.2f} the following month "
                        f"(saved \\${abs(impact['change']):,.2f})"
                    )
                else:
                    st.warning(
                        f"Spending went from \\${impact['before_cost']:,.2f} to "
                        f"\\${impact['after_cost']:,.2f} the following month "
                        f"(increased \\${impact['change']:,.2f})"
                    )

session.close()