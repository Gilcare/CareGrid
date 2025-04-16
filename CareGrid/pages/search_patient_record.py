def extract_patient_record():
    st.title("🔍 Patient Health Record Lookup")

    search_id = st.text_input("Enter Patient ID")

    if st.button("Search"):
        search_result = patient_data_collection.find_one({"personalDetails.patient_id": search_id})

        if search_result is None:
            st.error("Patient's Record Not Found")
        else:
            st.success("Patient Record Found")

            # Personal Details
            st.header("👤 Personal Details")
            pd = search_result.get("personalDetails", {})
            st.markdown(f"""
            - **Patient ID:** {pd.get("patient_id", "N/A")}
            - **Name:** {pd.get("name", "N/A")}
            - **Age:** {pd.get("age", "N/A")}
            - **Sex:** {pd.get("sex", "N/A")}
            - **Address:** {pd.get("address", "N/A")}
            - **Email:** {pd.get("email", "N/A")}
            - **Phone:** {pd.get("phone", "N/A")}
            - **Origin:** {pd.get("origin", "N/A")}
            - **Occupation:** {pd.get("occupation", "N/A")}
            - **Religion:** {pd.get("religion", "N/A")}
            - **Education Level:** {pd.get("education", "N/A")}
            """)

            # Clinical Notes
            st.header("🩺 Clinical Notes")
            st.write(search_result.get("clinicalNotes", "No clinical notes available."))

            # Lab Investigations
            st.header("🧪 Lab Investigations")
            lab_data = search_result.get("labInvestigations", [])
            if lab_data:
                for i, lab in enumerate(lab_data, 1):
                    st.markdown(f"**Investigation {i}:** {lab}")
            else:
                st.write("No lab investigations available.")

            # Medical Records
            st.header("📄 Medical Records")
            medical_records = search_result.get("medicalRecords", [])
            if medical_records:
                for i, record in enumerate(medical_records, 1):
                    st.markdown(f"**Record {i}:** {record}")
            else:
                st.write("No medical records available.")

            # Medical Images
            st.header("🖼️ Medical Images")
            medical_images = search_result.get("medicalImages", [])
            if medical_images:
                for i, img in enumerate(medical_images, 1):
                    st.markdown(f"**Image {i}:** {img}")  # Can be enhanced to display images if URLs or filepaths are present
            else:
                st.write("No medical images available.")

            # Other Details
            st.header("📌 Other Details")
            st.write(search_result.get("otherDetails", "No other details available."))



search_input = st.text_input("Search by Name or Patient ID")

if st.button("Search"):
    if search_input.startswith("P"):  # assuming patient IDs start with "P"
        results = [patient_data_collection.find_one({"personalDetails.patient_id": search_input})]
    else:
        results = list(patient_data_collection.find({"personalDetails.name": search_input}))

    if not results or results[0] is None:
        st.error("No matching patient records found.")
    elif len(results) == 1:
        display_patient_record(results[0])
    else:
        st.warning("Multiple records found. Please select the correct one.")
        selected = st.selectbox("Select patient", [f"{r['personalDetails']['name']} - {r['personalDetails']['age']} - {r['personalDetails']['patient_id']}" for r in results])
        chosen_id = selected.split(" - ")[-1]
        chosen_record = next((r for r in results if r['personalDetails']['patient_id'] == chosen_id), None)
        if chosen_record:
            display_patient_record(chosen_record)
      
