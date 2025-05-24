import streamlit as st
import struct
import json

st.set_page_config(page_title="STG Decoder", page_icon="🗂️", layout="centered")
st.title("🗂️ STG File Decoder")

uploaded_file = st.file_uploader("📥 Faça upload do arquivo .stg", type=["stg"])

if uploaded_file is not None:
    data = uploaded_file.read()
    offset = 0
    result = {}

    def read_string():
        nonlocal offset
        length = data[offset]
        offset += 1
        value = data[offset:offset+length].decode(errors='ignore')
        offset += length
        return value

    def read_int():
        nonlocal offset
        value = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        return value

    def read_float():
        nonlocal offset
        value = struct.unpack_from('<f', data, offset)[0]
        offset += 4
        return value

    try:
        result['Header'] = data[offset:offset+4].hex()
        offset += 4

        result['Name'] = read_string()

        result['Amplitude'] = read_float()
        result['MostrarTexto'] = read_int()
        result['TamanhoDoTexto'] = read_int()
        result['Media'] = read_float()

        st.subheader("📄 Dados Decodificados")
        st.json(result)

        json_data = json.dumps(result, indent=4, ensure_ascii=False)
        st.download_button("📥 Baixar JSON", data=json_data, file_name="decoded_stg.json")

    except Exception as e:
        st.error(f"Erro durante o parsing: {e}")
