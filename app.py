import streamlit as st
from db import fetch_query, execute_query
import queries as q

st.markdown(
        """
        <style>
        .stApp {
            background-color: #d0e7ff;
        }
        .title {
            color: #004080;
            font-size: 40px;
            font-weight: bold;
            text-align: center;
        }
        .subheader {
            color: #0066cc;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="Food Wastage Management", layout="wide")
st.title("🍽 Food Wastage Management System ")

menu = ["Home", "Providers", "Receivers", "Food Listings", "Claims", "Analytics Dashboard"]
choice = st.sidebar.selectbox("Scroll Down", menu)

# ---------------- Home Page ----------------
if choice == "Home":
    st.header("ℹ️  About")
    
    # Chef Image Centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("chef.png", width=300)

    # Impact Counters
    col4, col5, col6 = st.columns(3)
    col4.metric("🥗 Total Food Saved", "1,250 kg")
    col5.metric("👨‍👩‍👧 People Fed", "3,400+")
    col6.metric("🏢 Providers", "120")



    st.markdown ("""
    ### 🌱 Welcome to the Food Wastage Management System!
    Food wastage is a significant issue, with households and restaurants discarding surplus food 
    while many people face hunger.  
    Our mission is to **connect surplus food providers with those in need** through a structured platform.

    ### 💡 Our Mission
    Reduce food wastage by connecting surplus food providers with those in need.
    
    We partner with **restaurants, grocery stores, NGOs, and individuals** to make sure
    good food reaches hungry mouths instead of landfills.

    
    #### 🚀 What We Do
    - **List Surplus Food** from restaurants, grocery stores, and households.
    - **Enable NGOs & Individuals** to claim available food.
    - **Track & Analyze Trends** to reduce food waste.
    - **Real-time Access** via an easy-to-use web interface.

    #### 📊 Key Features
    - CRUD operations for food listings.
    - Contact details for providers and receivers.
    - Analytics dashboard with 15 insightful SQL queries.
    - Data-driven decision making for better food distribution.

    #### 💡 Impact
    - Reduce food waste.
    - Feed the needy efficiently.
    - Promote community engagement.
    """)

    st.success("Together, we can turn surplus into smiles! 😊")

    st.info("💡 Tip: Use the menu on the left to navigate through the system.")



# ---------------- Providers ----------------
elif choice == "Providers":
    col1, col2, col3 = st.columns([1, 2, 1])  # 1:2:1 ratio
    with col2:
        st.image("chef.png", width=300)
    st.subheader("📋 Providers Table")
    st.dataframe(fetch_query(q.GET_ALL_PROVIDERS))

    with st.expander("➕ Add Provider"):
        col1, col2 = st.columns(2)
        with col1:
            pid = st.number_input("Provider ID", step=1)
            name = st.text_input("Name")
            ptype = st.text_input("Type")
        with col2:
            address = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            # Add Provider
        if st.button("Add Provider"):
           execute_query(q.INSERT_PROVIDER, (pid, name, ptype, address, city, contact))
           st.success("Provider added successfully!")

            # Update Provider 
    with st.expander("✏ Update Provider"):
        col1, col2 = st.columns(2)
        with col1:
            pid = st.number_input("Provider ID to Update", step=1)
            name = st.text_input("New Name")
            ptype = st.text_input("New Type")
        with col2:
            address = st.text_input("New Address")
            city = st.text_input("New City")
            contact = st.text_input("New Contact")
        if st.button("Update Provider"):
           execute_query(q.UPDATE_PROVIDER, (name, ptype, address, city, contact, pid))
           st.success("Provider updated successfully!")
           # delete Provider
    with st.expander("🗑 Delete Provider"):
        delete_id = st.number_input("Enter Provider ID to Delete", step=1)

        if st.button("Delete Provider"):
           execute_query(q.DELETE_PROVIDER, (delete_id,))
           st.success(f"Provider with ID {delete_id} deleted successfully!")

# ---------------- Receivers ----------------
elif choice == "Receivers":
    col1, col2, col3 = st.columns([1, 2, 1])  # 1:2:1 ratio
    with col2:
        st.image("chef.png", width=300)
    st.subheader("📋 Receivers Table")
    st.dataframe(fetch_query(q.GET_ALL_RECEIVERS))

    with st.expander("➕ Add Receiver"):
        rid = st.number_input("Receiver ID", step=1)
        name = st.text_input("Name")
        rtype = st.text_input("Type")
        city = st.text_input("City")
        contact = st.text_input("Contact")
        if st.button("Add Receiver"):
            execute_query(q.INSERT_RECEIVER, (rid, name, rtype, city, contact))
            st.success("Receiver added successfully!")

          # Update receiver
    with st.expander("✏ Update Receiver"):
        rid = st.number_input("Receiver ID to Update", step=1)
        name = st.text_input("New Name")
        rtype = st.text_input("New Type")
        city = st.text_input("New City")
        contact = st.text_input("New Contact")
        if st.button("Update Receiver"):
            execute_query(q.UPDATE_RECEIVER, (rid, name, rtype, city, contact))
            st.success("Receiver Update successfully!")

          # Delete Receiver
    with st.expander("🗑 Delete Receiver"):
        delete_id = st.number_input("Enter Receiver ID to delete", step=1)

        if st.button("Delete Receiver"):
           execute_query(q.DELETE_RECEIVER, (delete_id,))
           st.success(f"Receiver with ID {delete_id} deleted successfully!")

# ---------------- Food Listings ----------------
elif choice == "Food Listings":
    col1, col2, col3 = st.columns([1, 2, 1])  # 1:2:1 ratio
    with col2:
        st.image("chef.png", width=300)
    st.subheader("📋 Food Listings Table")
    st.dataframe(fetch_query(q.GET_ALL_FOOD_LISTINGS))

    with st.expander("➕ Add Food Listing"):
        fname = st.text_input("Food Name")
        qty = st.number_input("Quantity", step=1)
        expiry = st.date_input("Expiry Date")
        pid = st.number_input("Provider ID", step=1)
        ptype = st.text_input("Provider Type")
        location = st.text_input("Location")
        ftype = st.text_input("Food Type")
        mtype = st.text_input("Meal Type")
        if st.button("Add Food Listing"):
            execute_query(q.INSERT_FOOD_LISTING, (fname, qty, expiry, pid, ptype, location, ftype, mtype))
            st.success("Food Listing added successfully!")

           # Update Food Listing
    with st.expander("✏ Update Food Listing"):
        fname = st.text_input("new Food Name")
        qty = st.number_input("new Quantity to update", step=1)
        expiry = st.date_input("new Expiry Date")
        pid = st.number_input("new Provider ID to update", step=1)
        ptype = st.text_input("new Provider Type")
        location = st.text_input("new Location")
        ftype = st.text_input("new Food Type")
        mtype = st.text_input("new Meal Type")
        if st.button("Update Food Listing"):
            execute_query(q.UPDATE_FOOD_LISTING, (fname, qty, expiry, pid, ptype, location, ftype, mtype))
            st.success("Food Listing Update successfully!")

             # delete Food Listing
    with st.expander("🗑 Delete Food Listing"):
        delete_id = st.number_input("Enter Provider ID to delete", step=1)

        if st.button("Delete Food Listing"):
           execute_query(q.DELETE_FOOD_LISTING, (delete_id,))
           st.success(f"Food Listing with ID {delete_id} deleted successfully!")

# ---------------- Claims ----------------
elif choice == "Claims":
    col1, col2, col3 = st.columns([1, 2, 1])  # 1:2:1 ratio
    with col2:
        st.image("chef.png", width=300)
    st.subheader("📋 Claims Table")
    st.dataframe(fetch_query(q.GET_ALL_CLAIMS))

    with st.expander("➕ Add Claim"):
        cid = st.number_input("Claim ID", step=1)
        fid = st.number_input("Food ID", step=1)
        rid = st.number_input("Receiver ID", step=1)
        status = st.selectbox("Status", ["Pending", "Completed"])
        claim_date = st.date_input("Claim Date")
        claim_time = st.time_input("Claim Time")
        if st.button("Add Claim"):
            execute_query(q.INSERT_CLAIM, (cid, fid, rid, status, claim_date, claim_time))
            st.success("Claim added successfully!")

            # Update Claim
    with st.expander("✏ Update Claim"):
        cid = st.number_input("New Claim ID", step=1)
        fid = st.number_input("New Food ID", step=1)
        rid = st.number_input("New Receiver ID", step=1)
        status = st.selectbox("New Status", ["Pending", "Completed"])
        claim_date = st.date_input("New Claim Date")
        claim_time = st.time_input("New Claim Time")
        if st.button("Update Claim"):
            execute_query(q.UPDATE_CLAIM, (cid, fid, rid, status, claim_date, claim_time))
            st.success("Claim Update successfully!") 

             # delete claim
    with st.expander("🗑 Delete Claim"):
        delete_id = st.number_input("Enter Claim ID to delete", step=1)

        if st.button("Delete Claim"):
           execute_query(q.DELETE_CLAIM, (delete_id,))
           st.success(f"Claim with ID {delete_id} deleted successfully!")


# ---------------- Analytics Dashboard ----------------
elif choice == "Analytics Dashboard":
    col1, col2, col3 = st.columns([1, 2, 1])  # 1:2:1 ratio
    with col2:
        st.image("chef.png", width=300)
    st.header("📊 Analytics Dashboard")
# --- Providers & Receivers ---
    st.markdown("### 🏢 Providers & Receivers")

    col1, col2 = st.columns(2)
    with col1:
         df_prov = fetch_query(q.PROVIDERS_PER_CITY)
         st.bar_chart(df_prov.set_index("City"))
    with col2:
        df_recv = fetch_query(q.RECEIVERS_PER_CITY)
        st.bar_chart(df_recv.set_index("City"))

    st.metric("🏆 Top Provider Type by Food Quantity",
              fetch_query(q.TOP_PROVIDER_TYPE_BY_FOOD)["Provider_Type"].iloc[0])

    city_input = st.text_input("🔍 Enter City to View Providers' Contact Info")

    if st.button("Search Contacts"):
        st.dataframe(fetch_query(q.PROVIDERS_CONTACT_BY_CITY, city_input))

    st.dataframe(fetch_query(q.RECEIVERS_WITH_MOST_CLAIMS))

    # --- Food Listings & Availability ---
    st.markdown("### 🍽 Food Listings & Availability")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Total Food Quantity", int(fetch_query(q.TOTAL_FOOD_QUANTITY)["Total_Quantity"].iloc[0]))
    with col4:
        city_top = fetch_query(q.CITY_WITH_MOST_LISTINGS)
        st.metric("City with Most Listings", city_top["Location"].iloc[0])

    st.bar_chart(fetch_query(q.MOST_COMMON_FOOD_TYPES).set_index("Food_Type"))

    # --- Claims & Distribution ---
    st.markdown("### 📦 Claims & Distribution")

    st.bar_chart(fetch_query(q.CLAIMS_PER_FOOD_ITEM).set_index("Food_Name"))

    st.metric("Top Provider with Most Completed Claims", 
              fetch_query(q.PROVIDER_WITH_MOST_COMPLETED_CLAIMS)["Name"].iloc[0])

    st.dataframe(fetch_query(q.CLAIM_STATUS_PERCENTAGE))

    # --- Analysis & Insights ---
    st.markdown("### 📈 Analysis & Insights")

    st.dataframe(fetch_query(q.AVG_QUANTITY_CLAIMED_PER_RECEIVER))

    st.metric("Most Claimed Meal Type", 
              fetch_query(q.MOST_CLAIMED_MEAL_TYPE)["Meal_Type"].iloc[0])

    st.dataframe(fetch_query(q.TOTAL_DONATED_BY_PROVIDER))

