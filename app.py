import streamlit as st

import pandas as pd

from database import (
    create_database,
    save_review,
    get_reviews,
    save_detected_alert,
    get_detected_alerts
)


from securitychecker import check_failed_logins

create_database()

if "detected_alerts" not in st.session_state:
    st.session_state.detected_alerts = []

# Remember alerts created by the Security Checker
if "detected_alerts" not in st.session_state:
    st.session_state.detected_alerts = []


# Application settings
st.set_page_config(
    page_title="AI Security Assistant",
    page_icon="🛡️",
    layout="wide"
)


# Lesson 10: Modern sidebar styling
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #14243B;
    }

    [data-testid="stSidebar"] * {
        color: #F3F7FC;
    }

    [data-testid="stSidebar"] hr {
        border-color: #34465E;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar branding
st.sidebar.markdown("## 🛡️ AI Security Assistant")
st.sidebar.caption("Small Business Security Center")
st.sidebar.divider()



pages = [
    "Home",
    "Security Alerts",
    "Security Checker",
    "Protection Tips",
    "Action History",
    "Ask Assistant"
]

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

page = st.sidebar.radio(
    "MAIN MENU",
    pages,
    index=pages.index(st.session_state["selected_page"]),
    key="main_navigation"
)

st.session_state["selected_page"] = page



# Application heading
st.title("🛡️ AI Security Assistant")
st.write("Your Partner for a Safer Business")
st.divider()

# HOME PAGE
if page == "Home":

    st.header("Welcome to Your Security Dashboard")
    st.write(
        "See what's happening with your business security."
    )


    # Get saved security information
    detected_alerts = get_detected_alerts()
    reviews = get_reviews()

    # Calculate dashboard numbers
    detected_count = len(detected_alerts)
    reviewed_count = len(reviews)

    # Three original example alerts plus detected alerts
    total_count = 3 + detected_count


    # Create three colored dashboard cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#FDEBEC;
                        padding:24px;
                        border-radius:14px;
                        border-left:5px solid #DC3545;">
                <div style="color:#A52834;font-size:16px;">
                    🔴 Detected Alerts
                </div>
                <div style="color:#A52834;font-size:38px;
                            font-weight:bold;">
                    {detected_count}
                </div>
                <div style="color:#A52834;font-size:13px;">
                    Saved security warnings
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color:#EAF2FF;
                        padding:24px;
                        border-radius:14px;
                        border-left:5px solid #3478D4;">
                <div style="color:#245AA0;font-size:16px;">
                    🔵 Reviewed Alerts
                </div>
                <div style="color:#245AA0;font-size:38px;
                            font-weight:bold;">
                    {reviewed_count}
                </div>
                <div style="color:#245AA0;font-size:13px;">
                    Recorded alert reviews
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="background-color:#E9F8EF;
                        padding:24px;
                        border-radius:14px;
                        border-left:5px solid #28A56A;">
                <div style="color:#176B45;font-size:16px;">
                    🟢 Total Alerts
                </div>
                <div style="color:#176B45;font-size:38px;
                            font-weight:bold;">
                    {total_count}
                </div>
                <div style="color:#176B45;font-size:13px;">
                    Example + detected alerts
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # Security activity chart
    st.subheader("📈 Security Activity")

    if detected_alerts:
        activity = pd.DataFrame(
            detected_alerts,
            columns=[
                "id",
                "title",
                "severity",
                "explanation",
                "recommendation",
                "failed_attempts",
                "detected_at"
            ]
        )

        activity["date"] = pd.to_datetime(
            activity["detected_at"]
        ).dt.date

        daily_alerts = (
            activity.groupby("date")
            .size()
            .reset_index(name="Alerts")
        )

        daily_alerts["date"] = pd.to_datetime(
            daily_alerts["date"]
        )

        st.line_chart(
            daily_alerts,
            x="date",
            y="Alerts"
        )

        st.caption(
            "Warnings generated from sample sign-in activity."
        )

    else:
        st.info(
            "No security activity has been recorded yet."
        )



    st.info(
        "These numbers are examples. "
        "Real security monitoring will be added later."
    )


    # Show the three most recently detected warnings
    st.subheader("🔔 Recent Security Alerts")

    if detected_alerts:

        # The database returns newest alerts first
        recent_alerts = detected_alerts[:3]

        for alert in recent_alerts:
            (
                alert_id,
                title,
                severity,
                explanation,
                recommendation,
                failed_attempts,
                detected_at
            ) = alert

            with st.container(border=True):
                st.markdown(f"**🔴 {title}**")
                st.write(f"**Priority:** {severity}")
                st.caption(f"Detected: {detected_at}")
                st.write(explanation)

    else:
        st.info(
            "No warnings have been detected yet. "
            "Use the Security Checker to test sample activity."
        )

    st.caption(
        "These warnings are generated from sample "
        "security activity, not live business monitoring."
    )


    # Alert Status Overview
    st.subheader("🛡️ Alert Status Overview")

    # Get the IDs of all saved reviews
    reviewed_ids = {
        review[0] for review in get_reviews()
    }

    # Count detected warnings that have been reviewed
    detected_reviewed = sum(
        1 for alert in detected_alerts
        if f"detected_{alert[0]}" in reviewed_ids
    )

    # Count detected warnings that still need review
    needs_review = detected_count - detected_reviewed

    # Display the status counts
    status_col1, status_col2 = st.columns(2)

    with status_col1:
        st.metric("🔴 Needs Review", needs_review)

    with status_col2:
        st.metric("🟢 Reviewed", detected_reviewed)

    # Calculate review progress
    if detected_count > 0:
        review_progress = detected_reviewed / detected_count
    else:
        review_progress = 0

    st.progress(review_progress)

    st.caption(
        f"{detected_reviewed} of {detected_count} "
        "detected warnings have been reviewed."
    )


    # Quick Actions Panel
    st.subheader("⚡ Quick Actions")

    quick_col1, quick_col2 = st.columns(2)

    with quick_col1:
        if st.button(
            "🛡️ Run Security Check",
            use_container_width=True
        ):
            st.session_state["selected_page"] = "Security Checker"
            st.rerun()

        if st.button(
            "📚 Protection Tips",
            use_container_width=True
        ):
            st.session_state["selected_page"] = "Protection Tips"
            st.rerun()

    with quick_col2:
        if st.button(
            "🔔 View Security Alerts",
            use_container_width=True
        ):
            st.session_state["selected_page"] = "Security Alerts"
            st.rerun()

        if st.button(
            "💬 Ask Assistant",
            use_container_width=True
        ):
            st.session_state["selected_page"] = "Ask Assistant"
            st.rerun()




# SECURITY ALERTS PAGE
elif page == "Security Alerts":

    st.header("🔔 Security Alerts")
    st.write("Review possible security problems affecting your business.")

    
    # Display warnings found by the Security Checker
    st.subheader("🔍 Newly Detected Warnings")

    detected_alerts = get_detected_alerts()


    if detected_alerts:

        for alert in detected_alerts:

            alert_id, title, severity, explanation, recommendation, failed_attempts, detected_at = alert

            with st.expander(f"🔴 {title}"):

                st.write("**Priority:**", severity)

                st.write("**What happened?**")
                st.write(
                    f"We found {failed_attempts} "
                    "unsuccessful sign-in attempts."
                )

                st.write("**What does this mean?**")
                st.write(explanation)

                st.write("**What should you do?**")
                st.write(recommendation)

                st.caption(f"Detected on: {detected_at}")

                
                if st.button(
                    "Mark as Reviewed",
                    key=f"detected_{alert_id}"
                ):
                    save_review(
                        f"detected_{alert_id}",
                        title
                    )
                    
                    st.write(f"Saved review ID: detected_{alert_id}")

                    
                    st.success("You have reviewed this alert.")



    else:

        st.info("No new warnings have been detected yet.")


    st.divider()


    st.info("These are example alerts used to demonstrate the application.")

    # Create a place to remember reviewed alerts
    if "reviewed_alerts" not in st.session_state:
        st.session_state.reviewed_alerts = []

    # Alert 1
    with st.expander("🔴 Someone may be trying to guess a password"):

        st.write("**What happened?**")
        st.write(
            "Someone tried several times to sign in "
            "to an employee account without success."
        )

        st.write("**Why does this matter?**")
        st.write(
            "Someone might be trying to access your "
            "business information without permission."
        )

        st.write("**What should you do?**")
        st.write(
            "Ask the employee if they recognize the activity. "
            "If they don't, change the password and turn on "
            "extra sign-in protection."
        )


        if st.button("Mark as Reviewed", key="alert1"):

            save_review(
                "alert1",
                "Someone may be trying to guess a password"
            )

        reviewed_ids = [
            review[0] for review in get_reviews()
        ]

        if "alert1" in reviewed_ids:
            st.success("You have reviewed this alert.")


    # Alert 2
    with st.expander("🟠 Unusual sign-in activity"):

        st.write("**What happened?**")
        st.write(
            "An employee account was accessed "
            "from an unexpected location."
        )

        st.write("**Why does this matter?**")
        st.write(
            "This could be normal if the employee is traveling, "
            "but it could also mean someone else accessed the account."
        )

        st.write("**What should you do?**")
        st.write(
            "Contact the employee to confirm whether "
            "they signed in from that location."
        )


        if st.button("Mark as Reviewed", key="alert2"):

            save_review(
                "alert2",
                "Unusual sign-in activity"
            )

        reviewed_ids = [
            review[0] for review in get_reviews()
        ]

        if "alert2" in reviewed_ids:
            st.success("You have reviewed this alert.")


    # Alert 3
    with st.expander("🟡 A program needs an update"):

        st.write("**What happened?**")
        st.write(
            "A program may have a known security problem "
            "that can be fixed with an update."
        )

        st.write("**Why does this matter?**")
        st.write(
            "Outdated programs can sometimes make it "
            "easier for someone to access business information."
        )

        st.write("**What should you do?**")
        st.write(
            "Install the latest trusted update "
            "for the affected program."
        )


        if st.button("Mark as Reviewed", key="alert3"):

            save_review(
                "alert3",
                "A program needs an update"
            )

        reviewed_ids = [
            review[0] for review in get_reviews()
        ]

        if "alert3" in reviewed_ids:
            st.success("You have reviewed this alert.")


    st.divider()

    st.subheader("Your Review Progress")


    example_alert_ids = ["alert1", "alert2", "alert3"]

    reviewed_ids = [
        review[0] for review in get_reviews()
    ]

    reviewed = sum(
        1 for alert_id in example_alert_ids
        if alert_id in reviewed_ids
    )

    st.progress(reviewed / 3)

    st.write(
        f"You have reviewed {reviewed} of 3 example alerts."
    )



# SECURITY CHECKER PAGE
elif page == "Security Checker":

    st.header("🔍 Security Checker")

    st.write(
        "Check whether unsuccessful sign-in attempts "
        "could indicate a security problem."
    )

    st.info(
        "This is a demonstration using sample information. "
        "It is not monitoring real employee accounts yet."
    )

    st.subheader("Check Sign-in Activity")

    failed_attempts = st.number_input(
        "How many unsuccessful sign-in attempts occurred?",
        min_value=0,
        max_value=1000,
        value=0,
        step=1
    )

    if st.button("Check for Security Problems"):

        result = check_failed_logins(failed_attempts)

        # Remember warnings so they can appear
        # on the Security Alerts page
        if result["status"] == "Warning":

            new_alert = {
                "title": result["title"],
                "severity": result["severity"],
                "explanation": result["explanation"],
                "recommendation": result["recommendation"],
                "failed_attempts": failed_attempts
            }

            st.session_state.detected_alerts.append(new_alert)
            
            save_detected_alert(new_alert)


        st.divider()
        st.subheader("Security Check Results")

        if result["status"] == "Warning":
            st.error(result["title"])
        else:
            st.success(result["title"])

        st.write("**Priority:**", result["severity"])

        st.write("**What does this mean?**")
        st.write(result["explanation"])

        st.write("**What should you do?**")
        st.write(result["recommendation"])



# PROTECTION TIPS PAGE
elif page == "Protection Tips":

    st.header("🛡️ Protection Tips")
    st.write("Simple ways to keep your business safer.")

    st.success("Use strong, unique passwords.")
    st.success("Turn on extra sign-in protection.")
    st.success("Keep computers and programs updated.")
    st.success("Review who has access to business accounts.")



# ACTION HISTORY PAGE
elif page == "Action History":

    st.header("📋 Action History")

    st.write(
        "See which security alerts you have reviewed."
    )

    # Retrieve reviewed alerts from the database
    reviews = get_reviews()

    if reviews:

        st.success(
            f"You have reviewed {len(reviews)} alert(s)."
        )

        for alert_id, alert_name, reviewed_at in reviews:

            st.write(f"✅ Reviewed: {alert_name}")

            st.caption(
                f"Reviewed on: {reviewed_at}"
            )

            st.divider()

    else:

        st.info(
            "No alerts have been reviewed yet. "
            "Visit Security Alerts to get started."
        )



# ASK ASSISTANT PAGE
elif page == "Ask Assistant":

    st.header("🤖 Ask Your Security Assistant")
    st.write(
        "Ask questions about keeping your business safe."
    )

    question = st.text_input("What would you like to know?")

    if st.button("Ask Assistant"):
        if question:
            st.info(
                "You asked: " + question
                + "\n\nReal AI answers will be added later."
            )
        else:
            st.warning("Please enter a question.")
