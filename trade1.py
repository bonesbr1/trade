import streamlit as st
import struct
import json


class STGParser:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def read_string(self):
        length = self.data[self.offset]
        self.offset += 1
        value = self.data[self.offset:self.offset + length].decode(errors='ignore')
        self.offset += length
        return value

    def read_int(self):
        value = struct.unpack_from('<I', self.data, self.offset)[0]
        self.offset += 4
        return value

    def read_float(self):
        value = struct.unpack_from('<f', self.data, self.offset)[0]
        self.offset += 4
        return value

    def parse(self):
        result = {}
        try:
            result['Header'] = self.data[self.offset:self.offset + 4].hex()
            self.offset += 4

            result['Name'] = self.read_string()

            result['Amplitude'] = self.read_float()
            result['MostrarTexto'] = self.read_int()
            result['TamanhoDoTexto'] = self.read_int()
            result['Media'] = self.read_float()

        except Exception as e:
            result['error'] = str(e)

        return result


# ====== STREAMLIT APP ======

st.set_page_config(page_title="STG Decoder", page_icon="🗂️", layout="centered")
st.title("🗂️ STG File Decoder")

st.markdown("""
Faça upload do seu arquivo `.stg` para visualizar os dados decodificados.
""")

uploaded_file = st.file_uploader("📥 Upload do arquivo .stg", type=["stg"])

if uploaded_file is not None:
    data = uploaded_file.read()
    parser = STGParser(data)
    parsed_data = parser.parse()

    st.subheader("📄 Dados Decodificados")
    st.json(parsed_data)

    json_data = json.dumps(parsed_data, indent=4, ensure_ascii=False)

    st.download_button(
        label="📥 Baixar JSON",
        data=json_data,
        file_name="decoded_stg.json",
        mime="application/json"
    )
