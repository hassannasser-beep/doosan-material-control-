import streamlit as st
import pandas as pd

st.set_page_config(page_title="Doosan Material Control", layout="wide")

st.title("🏗️ نظام إدارة ومطابقة مواد مشروع الضبعة")
st.markdown("### لوحة تحكم شركة DOOSAN وشركة DAESUN")
st.write("---")

filepath = "MATERIAL CONTROL.xlsx"
try:
    df = pd.read_excel(filepath, sheet_name='Sheet1', skiprows=3)
    columns_layout = [
        'Index', 'Code', 'No', 'Sortation', 'Material_No', 'Items_Services', 'Size', 'Unit',
        'DOOSAN_Purchase', 'DOOSAN_Incoming', 'DOOSAN_Not_Come', 'DOOSAN_Other_Company', 'DOOSAN_Handover', 'DOOSAN_Balance',
        'DAESUN_Incoming', 'DAESUN_Install', 'DAESUN_Fabrication', 'DAESUN_Scrap_Faulty', 'DAESUN_Balance',
        'Remarks', 'Balance_In_Reality', 'PCS', 'Date'
    ]
    df.columns = columns_layout
    df = df[df['Code'].notna()].reset_index(drop=True)
    
    df['DAESUN_Balance'] = pd.to_numeric(df['DAESUN_Balance'], errors='coerce').fillna(0)
    df['Balance_In_Reality'] = pd.to_numeric(df['Balance_In_Reality'], errors='coerce').fillna(0)
    df['Variance'] = df['Balance_In_Reality'] - df['DAESUN_Balance']
except Exception as e:
    st.error(f"تأكد من رفع ملف الإكسل بالاسم الصحيح: {e}")

st.sidebar.header("📋 القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", ["لوحة التحكم العامة", "البحث والمطابقة", "تقرير الفروقات والتعديل"])

if page == "لوحة التحكم العامة":
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 إجمالي أنواع المواد", len(df))
    col2.metric("🚨 مواد بها عجز", len(df[df['Variance'] < 0]), delta_color="inverse")
    col3.metric("⚠️ مواد بها زيادة", len(df[df['Variance'] > 0]))
    
    st.write("### 📊 جدول البيانات الكامل للمشروع")
    st.dataframe(df[['Code', 'Items_Services', 'Size', 'Unit', 'DOOSAN_Purchase', 'DAESUN_Balance', 'Balance_In_Reality', 'Variance']])

elif page == "البحث والمطابقة":
    search_code = st.selectbox("اختر كود المادة للفحص:", df['Code'].unique())
    row = df[df['Code'] == search_code].iloc[0]
    
    st.info(f"**اسم المادة:** {row['Items_Services']} | **الحجم:** {row['Size']}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("رصيد دايسون الدفتري", f"{row['DAESUN_Balance']} {row['Unit']}")
    c2.metric("جردك الفعلي بالواقع", f"{row['Balance_In_Reality']} {row['Unit']}")
    
    v = row['Variance']
    if v == 0:
        c3.success("✅ متطابق تماماً")
    elif v < 0:
        c3.error(f"🚨 عجز بمقدار {abs(v)}")
    else:
        c3.warning(f"⚠️ زيادة بمقدار {v}")

elif page == "تقرير الفروقات والتعديل":
    st.subheader("📝 إرشادات التعديل وتحديث بيانات الجرد")
    st.markdown("""
    لإدخال جرد جديد أو التعديل على الكميات:
    1. افتح ملف **MATERIAL CONTROL.xlsx** على جهازك وعدل الأرقام في عمود `BALANCE IN REALITY` أو `PCS`.
    2. قم برفع الملف المحدث إلى حسابك في **GitHub** (بنفس الاسم تماماً).
    3. سيقوم الموقع بتحديث البيانات وتغيير نسب العجز والزيادة تلقائياً في نفس اللحظة!
    """)
