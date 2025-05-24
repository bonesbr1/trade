import struct
import json


class STGParser:
    """
    Classe para decodificar arquivos .stg utilizados para armazenar configurações.
    """

    def __init__(self, data):
        self.data = data
        self.offset = 0

    def read_string(self):
        """Lê uma string do arquivo com tamanho prefixado"""
        length = self.data[self.offset]
        self.offset += 1
        value = self.data[self.offset:self.offset + length].decode(errors='ignore')
        self.offset += length
        return value

    def read_int(self):
        """Lê um inteiro de 4 bytes"""
        value = struct.unpack_from('<I', self.data, self.offset)[0]
        self.offset += 4
        return value

    def read_float(self):
        """Lê um float de 4 bytes"""
        value = struct.unpack_from('<f', self.data, self.offset)[0]
        self.offset += 4
        return value

    def parse(self):
        """Executa o parser completo do arquivo"""
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


if __name__ == "__main__":
    # Substituir pelo caminho do seu arquivo local
    file_path = 'CapitalWize_RENKO.stg'

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        parser = STGParser(data)
        parsed_data = parser.parse()

        # Salvar como JSON
        output_file = 'decoded_stg.json'
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)

        print(f"Arquivo decodificado salvo como {output_file}")
        print(json.dumps(parsed_data, indent=4, ensure_ascii=False))

    except FileNotFoundError:
        print("Arquivo não encontrado. Verifique o caminho informado.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
