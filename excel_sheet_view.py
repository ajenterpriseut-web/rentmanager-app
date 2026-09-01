import streamlit as st
from database import get_supabase_client, DEFAULT_SHOPS, MONTHS_LIST, YEARS_LIST

def render_excel_sheet_view():
    supabase = get_supabase_client()
    st.subheader("📊 Excel Style Monthly Ledger Sheet & Filters")
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        filter_shop = st.selectbox("Filter by Shop", ["All Shops"] + DEFAULT_SHOPS, key="ledger_filter_shop")
    with col_f2:
        filter_month = st.selectbox("Filter by Month", ["All Months"] + MONTHS_LIST, key="ledger_filter_month")
    with col_f3:
        filter_year = st.selectbox("Filter by Year", ["All Years"] + YEARS_LIST, key="ledger_filter_year")
    with col_f4:
        st.write("")
        if st.button("🔄 Refresh Data"):
            st.rerun()
            
    if supabase:
        try:
            response = supabase.table("rent_records").select("*").order("created_at", desc=True).execute()
            if response.data:
                records = response.data
                
                filtered_records = []
                for item in records:
                    s_match = (filter_shop == "All Shops" or item.get("shop_name") == filter_shop)
                    item_month_year = item.get("month", "")
                    m_match = (filter_month == "All Months" or filter_month in item_month_year.upper())
                    y_match = (filter_year == "All Years" or filter_year in item_month_year)
                    
                    if s_match and m_match and y_match:
                        filtered_records.append(item)
                
                if filtered_records:
                    table_data = []
                    for item in filtered_records:
                        curr = float(item.get("curr_reading", 0) or 0)
                        prev = float(item.get("prev_reading", 0) or 0)
                        table_data.append({
                            "ID": item.get("id"),
                            "Date": item.get("entry_date"),
                            "Shop Name": item.get("shop_name"),
                            "Month": item.get("month"),
                            "Rent (BDT)": f"{float(item.get('rent', 0) or 0):,.2f}",
                            "Electricity": f"{float(item.get('electricity', 0) or 0):,.2f}",
                            "Water": f"{float(item.get('water', 0) or 0):,.2f}",
                            "Service": f"{float(item.get('service_charge', 0) or 0):,.2f}",
                            "Others": f"{float(item.get('other_expenses', 0) or 0):,.2f}",
                            "Total (BDT)": f"{float(item.get('total', 0) or 0):,.2f}",
                            "Curr": int(curr),
                            "Prev": int(prev),
                            "Used Unit": int(max(0, curr - prev))
                        })
                    
                    selected_row_id = st.selectbox("Select Record ID to Edit/Delete", options=[r["ID"] for r in table_data], format_func=lambda x: f"Record ID: {x}")
                    
                    col_ed1, col_ed2 = st.columns(2)
                    with col_ed1:
                        if st.button("✏️ Edit Selected Record"):
                            st.session_state.edit_record_id = selected_row_id
                    with col_ed2:
                        if st.button("🗑️ Delete Selected Record", type="secondary"):
                            supabase.table("rent_records").delete().eq("id", selected_row_id).execute()
                            st.success("Record deleted successfully!")
                            st.rerun()

                    if st.session_state.get("edit_record_id") == selected_row_id:
                        st.markdown("---")
                        st.write(f"**Editing Record ID: {selected_row_id}**")
                        rec_to_edit = next((r for r in filtered_records if r["id"] == selected_row_id), None)
                        if rec_to_edit:
                            e_curr = st.number_input("Edit Current Reading", value=float(rec_to_edit.get("curr_reading", 0)))
                            e_rent = st.number_input("Edit Rent", value=float(rec_to_edit.get("rent", 0)))
                            e_water = st.number_input("Edit Water Bill", value=float(rec_to_edit.get("water", 0)))
                            e_service = st.number_input("Edit Service Charge", value=float(rec_to_edit.get("service_charge", 0)))
                            e_others = st.number_input("Edit Other Expenses", value=float(rec_to_edit.get("other_expenses", 0)))
                            
                            if st.button("Update Changes"):
                                unit_rate = float(rec_to_edit.get("unit_rate", 20))
                                prev = float(rec_to_edit.get("prev_reading", 0))
                                elec = max(0, e_curr - prev) * unit_rate
                                total = e_rent + elec + e_water + e_service + e_others
                                
                                supabase.table("rent_records").update({
                                    "curr_reading": e_curr,
                                    "rent": e_rent,
                                    "water": e_water,
                                    "service_charge": e_service,
                                    "other_expenses": e_others,
                                    "electricity": elec,
                                    "total": total
                                }).eq("id", selected_row_id).execute()
                                st.success("Updated successfully!")
                                st.session_state.edit_record_id = None
                                st.rerun()

                    st.divider()
                    st.dataframe(table_data, use_container_width=True)
                else:
                    st.info("No records found matching the selected filters.")
            else:
                st.info("No records found in database.")
        except Exception as e:
            st.error(f"Error loading ledger: {e}")