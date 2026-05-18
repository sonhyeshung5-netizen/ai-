import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
a=st.text_input('이름이 뭐야')
b=st.selectbox('좋아하는게 뭐야',['!','한식','중식','일식','참께방 위에 순쇠고기페티 둘장 특별한 소스 양상추 치츠 피클 양파 까지'])
if st.button('반갑다'):
st.write(a+'님,안녕하세요')
