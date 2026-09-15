import streamlit as st

from database import SessionLocal
from crud import save_recommendation, get_recommendations_dataframe, get_recommendation_impact, mark_recommendation_followed, get_business_language
from ai_query import get_recommendation
from translations import t

if "active_business_id" not in st.session_state:
    st.warning(t("no_business_warning", "en"))
    st.stop()

business_id = st.session_state.active_business_id

lang_session = SessionLocal()
language = get_business_language(lang_session, business_id)
lang_session.close()

st.title(t("recommendations_title", language))

st.write(t("recommendations_intro", language))

if st.button(t("generate_recommendation_button", language)):
    with st.spinner(t("analyzing_spinner", language)):
        session = SessionLocal()
        recommendation = get_recommendation(session, business_id)
        save_recommendation(session, business_id, recommendation)
        session.close()

    st.text(recommendation)

st.subheader(t("past_recommendations_header", language))

session = SessionLocal()
recs_df = get_recommendations_dataframe(session, business_id)

if recs_df.empty:
    st.info(t("no_recommendations_info", language))
else:
    for _, row in recs_df.iterrows():
        with st.expander(f"{row['created_at'].strftime('%B %d, %Y')}"):
            st.text(row["recommendation_text"])

            followed_status = row.get("followed")
            if followed_status is None:
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button(t("followed_yes_button", language), key=f"followed_yes_{row['id']}"):
                        mark_recommendation_followed(session, row["id"], True)
                        st.rerun()
                with col_no:
                    if st.button(t("followed_no_button", language), key=f"followed_no_{row['id']}"):
                        mark_recommendation_followed(session, row["id"], False)
                        st.rerun()
            elif followed_status:
                st.caption(t("followed_caption", language))
            else:
                st.caption(t("not_followed_caption", language))

            impact = get_recommendation_impact(session, business_id, row["id"])
            if not impact["possible"]:
                st.caption(impact.get("reason", t("impact_default_reason", language)))
            else:
                if impact["improved"]:
                    st.success(
                        t(
                            "impact_improved", language,
                            before=f"{impact['before_cost']:,.2f}",
                            after=f"{impact['after_cost']:,.2f}",
                            saved=f"{abs(impact['change']):,.2f}",
                        )
                    )
                else:
                    st.warning(
                        t(
                            "impact_worsened", language,
                            before=f"{impact['before_cost']:,.2f}",
                            after=f"{impact['after_cost']:,.2f}",
                            increase=f"{impact['change']:,.2f}",
                        )
                    )

session.close()
