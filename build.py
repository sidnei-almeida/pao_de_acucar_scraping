import PyInstaller.__main__
import os
import sys

def build_exe():
    """
    Cria o executável do projeto usando PyInstaller
    """
    # Diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Caminho para o ícone (opcional)
    # icon_path = os.path.join(script_dir, 'icon.ico')
    
    # Configurações do PyInstaller
    args = [
        'integrador.py',  # Script principal
        '--onefile',      # Criar um único arquivo executável
        '--name=PaoDeQueijo_Scraper',  # Nome do executável
        '--noconsole',    # Não mostrar console
        # '--icon=' + icon_path,  # Ícone (opcional)
        '--add-data=README.md;.',  # Incluir arquivos adicionais
        '--hidden-import=selenium',
        '--hidden-import=pandas',
        '--hidden-import=json',
        '--hidden-import=datetime',
    ]
    
    # Executar PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build_exe() 