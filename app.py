import streamlit as st

st.title('دستیار هوشمند حقوقی پژوهش و فناوری ایران')

question = st.text_input('سوال خود را اینجا بپرسید:')

if st.button('ارسال'):
    st.write(f'پرسش شما: {question}')
    # TODO: Connect to the legal assistant core
    st.info('پاسخ در اینجا نمایش داده خواهد شد.')
