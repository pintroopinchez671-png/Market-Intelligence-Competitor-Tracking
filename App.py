import os
import difflib
import requests
from bs4 import BeautifulSoup
import streamlit as st
from supabase import create_client, Client

# 1. Page Configuration
st.set_page_config(page_title="Market Intelligence & Competitor Tracker", layout="centered")
st.title("🔍 Market Intelligence & Competitor Tracker")
st.markdown("Monitor rival websites for changes on autopilot.")

# Initialize Supabase Client from Streamlit secrets
try:
    supabase_url = st.secrets["supabase"]["url"]
    supabase_key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    st.error("Missing Supabase secrets. Please configure your .streamlit/secrets.toml or Streamlit Cloud Secrets.")
    st.stop()

# Stripe Payment Link Configuration
PAYMENT_LINK = "https://buy.stripe.com/test_YOUR_STRIPE_LINK_HERE" # Replace with your actual Stripe link

# Session State for User Auth
if "user" not in st.session_state:
    st.session_state.user = None

# --- AUTHENTICATION FLOW ---
if not st.session_state.user:
    st.subheader("Login or Create an Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log In"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")
                
    with col2:
        if st.button("Sign Up"):
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.success("Signup successful! Check your email to confirm.")
            except Exception as e:
                st.error(f"Signup failed: {e}")

# --- DASHBOARD & GATEKEEPING (LOGGED IN) ---
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.user.email}**")
    if st.sidebar.button("Log Out"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

    user_id = st.session_state.user.id

    # Check Stripe subscription status in Supabase
    try:
        sub_check = supabase.table("user_subscriptions").select("is_active").eq("user_id", user_id).execute()
        is_subscribed = sub_check.data[0]["is_active"] if sub_check.data else False
    except Exception:
        is_subscribed = False

    # --- MONETIZATION GATEKEEPER ---
    if not is_subscribed:
        st.warning("⚠️ Free Tier / Unpaid Account")
        st.write("Upgrade to Pro to unlock automated competitor tracking and instant alerts.")
        
        # Append user_id to Stripe link to track who paid via webhook later
        checkout_url = f"{PAYMENT_LINK}?client_reference_id={user_id}"
        st.markdown(f"[👉 **Upgrade to Pro ($29/mo)**]({checkout_url})", unsafe_allow_html=True)
        st.info("Already paid? Refresh this page once your payment completes.")
    
    else:
        st.success("✅ Pro Subscription Active")
        
        st.header("Track Competitor URLs")
        new_url = st.text_input("Enter competitor URL to track:")
        
        if st.button("Add URL"):
            if new_url:
                try:
                    response = requests.get(new_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Remove noise elements
                    for element in soup(["script", "style", "iframe"]):
                        element.decompose()
                    content = soup.get_text()[:1000] # Store first 1000 chars

                    # Save to Supabase (RLS ensures user privacy)
                    supabase.table("tracked_urls").insert({
                        "user_id": user_id,
                        "url": new_url,
                        "last_content": content
                    }).execute()
                    
                    st.success("URL added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error fetching URL: {e}")

        # View tracked URLs
        st.subheader("Your Monitored URLs")
        response = supabase.table("tracked_urls").select("*").execute()
        tracked = response.data

        if tracked:
            for item in tracked:
                with st.expander(item["url"]):
                    st.write(f"**Added on:** {item['created_at']}")
                    st.caption(f"**Content Preview:** {item['last_content']}")
        else:
            st.info("No URLs tracked yet. Add one above to start monitoring.")
