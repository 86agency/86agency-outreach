import streamlit as st
import pandas as pd
import anthropic
import time
from io import BytesIO

# Page config
st.set_page_config(
    page_title="86 Agency - Outreach Generator",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for 86 Agency branding
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e1b4b 0%, #581c87 50%, #1e1b4b 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #9333ea 0%, #ec4899 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #7e22ce 0%, #db2777 100%);
    }
    h1, h2, h3 {
        color: #e9d5ff;
    }
    .success-box {
        background: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_results' not in st.session_state:
    st.session_state.generated_results = None

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# ⚡ 86 Agency")
    st.markdown("### AI-Powered Outreach Generator")
    st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    api_key = st.text_input(
        "Claude API Key",
        type="password",
        help="Get your key from console.anthropic.com"
    )
    
    st.markdown("---")
    
    your_name = st.text_input("Your Name", value="Deepak Kumar")
    your_title = st.text_input("Your Title", value="Founder & CTO")
    your_company = st.text_input("Company", value="86 Agency")
    calendar_link = st.text_input("Calendar Link", value="https://calendly.com/86agency")
    
    st.markdown("---")
    st.markdown("### 📊 What You'll Get")
    st.markdown("- ✅ 4 Email Sequence")
    st.markdown("- ✅ LinkedIn Message")
    st.markdown("- ✅ Call Script")

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload & Generate", "📊 Results", "ℹ️ Help"])

with tab1:
    st.markdown("## Step 1: Upload Your Contact List")
    
    uploaded_file = st.file_uploader(
        "Upload CSV with Email, First Name, Last Name, Company columns",
        type=['csv'],
        help="Export from Apollo with Email, Name, and Company fields"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Auto-detect columns
            email_col = next((col for col in df.columns if 'email' in col.lower()), None)
            first_col = next((col for col in df.columns if 'first' in col.lower()), None)
            last_col = next((col for col in df.columns if 'last' in col.lower()), None)
            company_col = next((col for col in df.columns if 'company' in col.lower()), None)
            
            if not all([email_col, first_col, company_col]):
                st.error("❌ CSV must have Email, First Name, and Company columns")
            else:
                st.success(f"✅ Loaded {len(df)} contacts")
                
                with st.expander("Preview Data"):
                    st.dataframe(df.head(), use_container_width=True)
                
                st.markdown("---")
                st.markdown("## Step 2: Generate Outreach")
                
                num_contacts = st.slider(
                    "Number of contacts to process (demo limit)",
                    min_value=1,
                    max_value=min(10, len(df)),
                    value=min(5, len(df))
                )
                
                if st.button("🚀 Generate Outreach", use_container_width=True):
                    if not api_key:
                        st.error("❌ Please enter your Claude API key in the sidebar")
                    else:
                        generate_outreach(
                            df, 
                            num_contacts,
                            api_key,
                            your_name,
                            your_title,
                            your_company,
                            calendar_link,
                            email_col,
                            first_col,
                            last_col,
                            company_col
                        )
                        
        except Exception as e:
            st.error(f"❌ Error loading CSV: {str(e)}")

with tab2:
    if st.session_state.generated_results:
        st.markdown("## ✅ Generation Complete!")
        
        results_df = pd.DataFrame(st.session_state.generated_results)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Contacts Processed", len(results_df))
        with col2:
            st.metric("Total Emails", len(results_df) * 4)
        with col3:
            st.metric("LinkedIn + Calls", len(results_df))
        
        st.markdown("---")
        
        # Preview
        with st.expander("📧 Preview Results"):
            if len(results_df) > 0:
                sample = results_df.iloc[0]
                st.markdown(f"**Contact:** {sample['First_Name']} @ {sample['Company']}")
                st.markdown(f"**Email 1 Subject:** {sample['Email_1_Subject']}")
                st.text_area("Email 1 Body:", sample['Email_1_Body'], height=150)
        
        # Download button
        csv_buffer = BytesIO()
        results_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        csv_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Complete CSV",
            data=csv_buffer,
            file_name=f"86Agency_Outreach_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("👈 Generate outreach first to see results here")

with tab3:
    st.markdown("""
    ## 🚀 How to Use This App
    
    ### Step 1: Get Your Claude API Key
    1. Go to [console.anthropic.com](https://console.anthropic.com)
    2. Sign up or login
    3. Click "API Keys" → "Create Key"
    4. Copy the key (starts with `sk-ant-...`)
    5. Paste it in the sidebar
    
    ### Step 2: Prepare Your CSV
    Export from Apollo or create a CSV with:
    - **Email** (required)
    - **First Name** (required)
    - **Last Name** (optional)
    - **Company** (required)
    - Any other fields you want
    
    ### Step 3: Generate
    1. Upload your CSV
    2. Choose number of contacts
    3. Click "Generate Outreach"
    4. Wait for completion (takes 2-3 min per contact)
    
    ### Step 4: Download
    Get your complete CSV with:
    - 4 email sequences (Day 1, 3, 7, 10)
    - LinkedIn connection message
    - Call script with objections
    
    ---
    
    ### 💡 Tips
    - Start with 5-10 contacts to test
    - Each contact takes ~2-3 minutes
    - Keep the browser tab open during generation
    - Download CSV when complete
    
    ### 🆘 Troubleshooting
    **"API key invalid"** → Check you copied the full key  
    **"CSV error"** → Make sure you have Email, First Name, Company columns  
    **"Generation stuck"** → Refresh and try again with fewer contacts  
    
    ---
    
    **Built for 86 Agency • Powered by Claude AI**
    """)

def generate_outreach(df, num_contacts, api_key, your_name, your_title, your_company, calendar, 
                     email_col, first_col, last_col, company_col):
    """Generate outreach for contacts"""
    
    client = anthropic.Anthropic(api_key=api_key)
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(num_contacts):
        contact = df.iloc[i]
        first_name = contact[first_col]
        last_name = contact[last_col] if last_col else ""
        company = contact[company_col]
        email = contact[email_col]
        
        status_text.markdown(f"### Processing {i+1}/{num_contacts}: {first_name} @ {company}")
        
        try:
            # Generate 4 emails
            emails = []
            for email_num in range(1, 5):
                with st.spinner(f"Generating Email {email_num}..."):
                    prompt = build_email_prompt(first_name, company, email_num, your_name, your_title, your_company, calendar)
                    response = client.messages.create(
                        model="claude-sonnet-4-5-20250929",
                        max_tokens=400,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    email_text = response.content[0].text
                    subject, body = parse_email(email_text)
                    emails.append({"subject": subject, "body": body})
                    time.sleep(0.5)
            
            # Generate LinkedIn
            with st.spinner("Generating LinkedIn message..."):
                li_prompt = f"Write a LinkedIn connection message to {first_name} at {company}. Under 280 characters. Professional, friendly. Just the message."
                li_response = client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=150,
                    messages=[{"role": "user", "content": li_prompt}]
                )
                linkedin = li_response.content[0].text.strip()[:280]
                time.sleep(0.5)
            
            # Generate Call Script
            with st.spinner("Generating call script..."):
                call_prompt = f"Write a call script for {first_name} at {company} from {your_name} at {your_company}. Include: Opener, Value Prop, Discovery, 2 Objections, Close. Max 150 words."
                call_response = client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=600,
                    messages=[{"role": "user", "content": call_prompt}]
                )
                call_script = call_response.content[0].text.strip()
            
            # Compile results
            result = {
                "Email": email,
                "First_Name": first_name,
                "Last_Name": last_name,
                "Company": company,
                "Email_1_Subject": emails[0]["subject"],
                "Email_1_Body": emails[0]["body"],
                "Email_2_Day_3_Subject": emails[1]["subject"],
                "Email_2_Day_3_Body": emails[1]["body"],
                "Email_3_Day_7_Subject": emails[2]["subject"],
                "Email_3_Day_7_Body": emails[2]["body"],
                "Email_4_Day_10_Subject": emails[3]["subject"],
                "Email_4_Day_10_Body": emails[3]["body"],
                "LinkedIn_Message": linkedin,
                "Call_Script": call_script
            }
            
            results.append(result)
            progress_bar.progress((i + 1) / num_contacts)
            
        except Exception as e:
            st.error(f"Error processing {first_name}: {str(e)}")
    
    status_text.success(f"✅ Complete! Generated outreach for {len(results)} contacts")
    st.session_state.generated_results = results
    st.balloons()

def build_email_prompt(name, company, num, your_name, your_title, your_company, calendar):
    """Build email prompt based on sequence number"""
    strategies = {
        1: f"Write a cold email from {your_name} ({your_title} at {your_company}) to {name} at {company}. Mention we build scalable products. Max 75 words. Include {calendar}. Sign: {your_name}. Format: SUBJECT: [subject]\\n---\\n[body]",
        2: f"Write Day 3 follow-up from {your_name} to {name}. Add value, share insight. Max 60 words. Sign: {your_name}. Format: SUBJECT: [subject]\\n---\\n[body]",
        3: f"Write Day 7 follow-up from {your_name} to {name}. Different angle. Max 65 words. Sign: {your_name}. Format: SUBJECT: [subject]\\n---\\n[body]",
        4: f"Write Day 10 breakup from {your_name} to {name}. Easy yes/no. Max 50 words. Sign: {your_name}. Format: SUBJECT: [subject]\\n---\\n[body]"
    }
    return strategies[num]

def parse_email(text):
    """Parse email into subject and body"""
    subject = "Quick question"
    for line in text.split('\n'):
        if line.upper().startswith('SUBJECT:'):
            subject = line.split(':', 1)[1].strip()
            break
    parts = text.split('---')
    body = parts[1].strip() if len(parts) > 1 else text
    body = body.replace(f'SUBJECT: {subject}', '').strip()
    return subject, body

if __name__ == "__main__":
    pass
