import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = "https://dazbgpsrdnurwmqnwvni.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRhemJncHNyZG51cndtcW53dm5pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgyMDU0MTksImV4cCI6MjEwMzc4MTQxOX0.VfboLIZ-eHK88_KMazrCWEP5M60TNM5Hx1cfUU1pdb0"

@st.cache_resource
def get_supabase_client() -> Client:
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

DEFAULT_SHOPS = [
    "Seba Green Line Transport", "Ena Transport", "Hanif Enterprise",
    "Shyamoli NR Travels", "Ahnaf Labiba Transport", "Ekota Transport",
    "Hanif VIP Transport", "Shyamoli Transport", "Shah Fateh Ali",
    "Shah Sultan", "Hotel", "Karimun", "Munna Jewel"
]

MONTHS_LIST = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
YEARS_LIST = ["2026", "2027", "2028", "2029", "2030"]