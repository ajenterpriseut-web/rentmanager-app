import streamlit as st
import datetime
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from database import get_supabase_client, DEFAULT_SHOPS, MONTHS_LIST, YEARS_LIST

FONT_NAME = "Helvetica"
try:
    from reportlab.pdfbase.ttfonts import TTFFont
    font_path = "SolaimanLipi.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFFont('BanglaFont', font_path))
        FONT_NAME = 'BanglaFont'
    else:
        sys_font = "C:/Windows/Fonts/SolaimanLipi.ttf"
        if os.path.exists(sys_font):
            pdfmetrics.registerFont(TTFFont('BanglaFont', sys_font))
            FONT_NAME = 'BanglaFont'
except Exception as e:
    print("Font registration warning:", e)

def number_to_words(amount):
    return "One Lakh Ten Thousand Nine Hundred Fifteen Taka Only"

def generate_pdf_bytes(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    start_y = 700 
    
    # Header Box
    c.setFillColorRGB(0.12, 0.40, 0.70)
    c.rect(40, start_y + 35, 532, 38, fill=1, stroke=0)
    
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_NAME, 13)
    c.drawCentredString(width / 2.0, start_y + 55, "LATIF MANSION")
    
    c.setFont(FONT_NAME, 8)
    c.drawCentredString(width / 2.0, start_y + 41, "House # 18, Road # 7/D, Sector # 09, Uttara, Abdullahpur, Dhaka-1230. Mobile: 01720-171798")
    
    c.setFillColorRGB(0.18, 0.50, 0.82)
    c.rect(40, start_y + 15, 532, 18, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_NAME, 9)
    c.drawCentredString(width / 2.0, start_y + 20, "RENT RECEIPT")
    
    # Meta Info Box
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.rect(40, start_y - 42, 532, 55, fill=0, stroke=1)
    
    c.setFillColorRGB(0, 0, 0)
    c.setFont(FONT_NAME, 9)
    c.drawString(48, start_y + 1, f"Receipt No: {data.get('receipt_no', '')}")
    c.drawString(340, start_y + 1, f"Issue Date: {data.get('issue_date', '')}")
    
    c.drawString(48, start_y - 17, f"Shop Name: {data.get('shop_name', '')}")
    c.drawString(340, start_y - 17, f"Rent Month: {str(data.get('month', '')).upper()} {data.get('year', '')}")
    c.drawString(48, start_y - 34, f"Shop No: {data.get('shop_no', '')}")
    
    # Table Header
    y = start_y - 62
    c.setFillColorRGB(0.12, 0.40, 0.70)
    c.rect(40, y, 532, 18, fill=1, stroke=1)
    
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_NAME, 8)
    c.drawString(48, y + 5, "SL")
    c.drawString(115, y + 5, "Description")
    c.drawString(240, y + 5, "Curr Unit")
    c.drawString(315, y + 5, "Prev Unit")
    c.drawString(385, y + 5, "Used Unit")
    c.drawString(465, y + 5, "Rate")
    c.drawString(530, y + 5, "Amount")
    
    y -= 18
    items = [
        ("1", "Shop Rent", "-", "-", "-", "-", f"{data.get('rent', 0):,.0f}"),
        ("2", "Electricity Bill", str(data.get('curr_reading', '-')), str(data.get('prev_reading', '-')), str(data.get('used_units', '-')), str(data.get('unit_rate', '-')), f"{data.get('electricity', 0):,.0f}"),
        ("3", "Water Bill", "-", "-", "-", "-", f"{data.get('water', 0):,.0f}"),
        ("4", "Service Charge", "-", "-", "-", "-", f"{data.get('service', 0):,.0f}"),
        ("5", "Festival Bonus / Special", "-", "-", "-", "-", f"{data.get('bonus', 0):,.0f}"),
        ("6", "Other Expenses", "-", "-", "-", "-", f"{data.get('other', 0):,.0f}")
    ]
    
    c.setFillColorRGB(0, 0, 0)
    c.setFont(FONT_NAME, 8)
    for sl, desc, cu, pu, uu, ur, amt in items:
        c.rect(40, y, 532, 18, fill=0, stroke=1)
        c.drawString(48, y + 5, sl)
        c.drawString(115, y + 5, desc)
        c.drawString(255, y + 5, cu)
        c.drawString(335, y + 5, pu)
        c.drawString(405, y + 5, uu)
        c.drawString(480, y + 5, ur)
        c.drawString(520, y + 5, amt)
        y -= 18
        
    c.rect(40, y, 532, 18, fill=0, stroke=1)
    c.setFont(FONT_NAME, 8)
    c.drawString(430, y + 5, "Total Amount:")
    c.drawString(515, y + 5, f"{data.get('total', 0):,.0f}")
    y -= 22
    
    c.rect(40, y, 532, 18, fill=0, stroke=1)
    c.setFont(FONT_NAME, 8)
    c.drawString(48, y + 5, f"Taka in Words: {data.get('in_words', '')}")
    y -= 35
    
    c.setFont(FONT_NAME, 8)
    c.drawString(50, y, "----------------------------------------")
    c.drawString(50, y - 10, "Receiver By")
    
    c.drawString(410, y, "----------------------------------------")
    c.drawString(410, y - 10, "Authorized By")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def render_receipt_generator():
    supabase = get_supabase_client()
    st.subheader("1. Shop, Date & Period Selection")
    
    if "shops_list" not in st.session_state:
        st.session_state.shops_list = list(DEFAULT_SHOPS)
        
    c_s1, c_s2 = st.columns([4, 1])
    with c_s1:
        selected_shop = st.selectbox("Shop Name", st.session_state.shops_list, key="form_shop_select")
    with c_s2:
        st.write("")
        if st.button("+ New Shop"):
            st.session_state.show_new_shop_box = True

    if st.session_state.get("show_new_shop_box", False):
        new_shop_name = st.text_input("Enter New Shop Name")
        if st.button("Save Shop"):
            if new_shop_name and new_shop_name not in st.session_state.shops_list:
                st.session_state.shops_list.append(new_shop_name)
                st.session_state.show_new_shop_box = False
                st.rerun()

    auto_prev_reading = 0.0
    if supabase:
        try:
            res = supabase.table("rent_records").select("curr_reading").eq("shop_name", selected_shop).order("created_at", desc=True).limit(1).execute()
            if res.data and len(res.data) > 0:
                auto_prev_reading = float(res.data[0].get("curr_reading", 0) or 0)
        except:
            pass

    col1, col2 = st.columns(2)
    with col1:
        entry_date = st.text_input("Entry Date (DD-MMM-YYYY)", datetime.datetime.now().strftime("%d-%b-%Y").upper())
        month = st.selectbox("Month", MONTHS_LIST)
    with col2:
        receipt_no = st.text_input("Receipt No (e.g., 2026-01)", "2026-01")
        year = st.selectbox("Year", YEARS_LIST)

    st.subheader("2. Rent Details")
    rent = st.number_input("Shop Rent (Taka)", value=90000.0)
    
    st.subheader("3. Electricity Meter Reading & Bill")
    col3, col4 = st.columns(2)
    with col3:
        curr_reading = st.number_input("Current Reading", value=0.0)
    with col4:
        prev_reading = st.number_input("Previous Reading (Auto-loaded)", value=auto_prev_reading)
        
    unit_rate = st.number_input("Rate Per Unit", value=20.0)
    
    st.subheader("4. Other Bills & Charges")
    col5, col6 = st.columns(2)
    with col5:
        water = st.number_input("Water Bill", value=5000.0)
        bonus = st.number_input("Festival Bonus / Special", value=0.0)
    with col6:
        service = st.number_input("Service Charge", value=2000.0)
        other = st.number_input("Other Expenses", value=0.0)

    used_units = max(0.0, curr_reading - prev_reading)
    electricity = used_units * unit_rate
    total = rent + electricity + water + service + bonus + other
    in_words = number_to_words(total)

    if st.button("💾 Save Data to Database", type="primary", use_container_width=True):
        try:
            record = {
                "shop_name": selected_shop,
                "shop_no": receipt_no,
                "entry_date": entry_date,
                "month": f"{month} {year}",
                "rent": rent,
                "curr_reading": curr_reading,
                "prev_reading": prev_reading,
                "unit_rate": unit_rate,
                "electricity": electricity,
                "water": water,
                "service_charge": service,
                "other_expenses": other + bonus,
                "total": total
            }

            if supabase:
                supabase.table("rent_records").insert(record).execute()
                st.success("Data saved successfully to Database!")
        except Exception as e:
            st.error(f"Error saving data: {e}")

    pdf_bytes = generate_pdf_bytes({
        "shop_name": selected_shop,
        "receipt_no": receipt_no,
        "shop_no": receipt_no,
        "issue_date": entry_date,
        "month": month,
        "year": year,
        "rent": rent,
        "curr_reading": int(curr_reading) if curr_reading else "-",
        "prev_reading": int(prev_reading) if prev_reading else "-",
        "used_units": int(used_units) if used_units > 0 else "-",
        "unit_rate": unit_rate if unit_rate else "-",
        "electricity": electricity,
        "water": water,
        "service": service,
        "bonus": bonus,
        "other": other,
        "total": total,
        "in_words": in_words
    })

    st.download_button(
        label="📥 Download PDF Receipt",
        data=pdf_bytes,
        file_name=f"Receipt_{selected_shop.replace(' ', '_')}_{month}_{year}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
