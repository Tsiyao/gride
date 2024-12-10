import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Student Grade Analysis")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file with student grades", type="csv")

if uploaded_file:
    # Load the dataset
    data = pd.read_csv(uploaded_file)
    st.subheader("Uploaded Data")
    st.write(data.head())
    
    # Ensure required columns are present
    if "Student Name" in data.columns and "Grade" in data.columns:
        # Grade Distribution
        st.subheader("Grade Distribution")
        fig, ax = plt.subplots()
        sns.histplot(data['Grade'], kde=True, bins=10, color="blue", ax=ax)
        ax.set_title("Grade Distribution")
        ax.set_xlabel("Grade")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
        
        # Top Performers
        st.subheader("Top Performers")
        top_performers = data.nlargest(5, "Grade")[["Student Name", "Grade"]]
        st.table(top_performers)
        
        # Average Grade
        avg_grade = data['Grade'].mean()
        st.metric(label="Average Grade", value=f"{avg_grade:.2f}")
        
        # Pass/Fail Analysis
        pass_threshold = st.slider("Set Pass Threshold", min_value=0, max_value=100, value=50)
        data['Result'] = data['Grade'].apply(lambda x: "Pass" if x >= pass_threshold else "Fail")
        
        pass_fail_counts = data['Result'].value_counts()
        st.subheader("Pass/Fail Analysis")
        fig, ax = plt.subplots()
        sns.barplot(x=pass_fail_counts.index, y=pass_fail_counts.values, palette="viridis", ax=ax)
        ax.set_title("Pass/Fail Counts")
        ax.set_xlabel("Result")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.error("The uploaded file must contain 'Student Name' and 'Grade' columns.")
else:
    st.info("Please upload a CSV file to begin analysis.")
