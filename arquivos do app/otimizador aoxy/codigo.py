import os
import shutil
import subprocess
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QSize

class otimizadorPC(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛠️ Otimizador Aoxy")
        self.setGeometry(100, 100, 550, 550)
        self.setFixedSize(550, 550)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #2d89ef;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 14px;
                font-size: 15px;
                font-weight: bold;
                margin-bottom: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1b65b8;
            }
            QLabel#titulo {
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
            }
            QLabel#status {
                font-size: 13px;
                color: #cccccc;
            }
            QFrame {
                color: #444444;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        self.label_titulo = QLabel("🧰 Otimizador de PC")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_titulo)
        layout.addSpacing(10)

        botoes_layout = QVBoxLayout()
        botoes_layout.setSpacing(12)

        self.botoes = {
            "🧹 Limpar Temporários": self.limpar_temporarios,
            "🗑️ Esvaziar Lixeira": self.esvaziar_lixeira,
            "🔄 Ativar Modo Desempenho (efeitos off)": self.desativar_efeitos_visuais,
            "🧯 Desativar Serviços Desnecessários": self.desativar_servicos,
            "🚫 Mostrar Programas de Inicialização": self.mostrar_programas_inicio,
            "🎭 Desativar Efeitos de Transparência": self.desativar_transparencia,
            "Plano de Energia: Alto Desempenho": self.ativar_plano_alto_desempenho,
            "Verificar Integridade do Sistema (sfc)": self.verificar_integridade_sistema,
            "Desfragmentar Disco": self.desfragmentar_disco,
            "Otimizar Inicialização": self.otimizar_inicializacao,
            "Limpar cache do Windows Update": self.limpar_cache_windows_update,
            "Desativar Serviços Inúteis": self.desativar_servicos_inuteis,
            "Desativar Animações Extras": self.desativar_animacoes_extra,
            "Liberar RAM": self.liberar_ram,
            "Limpar Prefetch": self.limpar_prefetch,
            "Limpar Pontos de Restauração": self.limpar_pontos_restauracao,
        }

        for texto, func in self.botoes.items():
            botao = QPushButton(texto)
            botao.setIconSize(QSize(24, 24))
            botao.clicked.connect(func)
            botoes_layout.addWidget(botao)

        layout.addLayout(botoes_layout)

        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        layout.addWidget(separador)

        self.status_label = QLabel("✅ Pronto para otimizar!")
        self.status_label.setObjectName("status")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def limpar_temporarios(self):
        self.status_label.setText("🧹 Limpando arquivos temporários...")
        pastas_temp = [tempfile.gettempdir(), os.path.expandvars(r"%SystemRoot%\Temp")]
        arquivos_apagados = 0

        for pasta in pastas_temp:
            if os.path.exists(pasta):
                try:
                    for item in os.listdir(pasta):
                        caminho = os.path.join(pasta, item)
                        try:
                            if os.path.isfile(caminho) or os.path.islink(caminho):
                                os.remove(caminho)
                                arquivos_apagados += 1
                            elif os.path.isdir(caminho):
                                shutil.rmtree(caminho, ignore_errors=True)
                                arquivos_apagados += 1
                        except:
                            pass
                except:
                    pass

        self.status_label.setText(f"✅ {arquivos_apagados} arquivos temporários apagados!")

    def esvaziar_lixeira(self):
        try:
            subprocess.run('powershell.exe -Command "Clear-RecycleBin -Force"', check=True)
            self.status_label.setText("🗑️ Lixeira esvaziada com sucesso!")
        except:
            self.status_label.setText("⚠️ Não foi possível esvaziar a lixeira.")

    def desativar_efeitos_visuais(self):
        try:
            cmd = (
                'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f & '
                'reg add "HKCU\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f'
            )
            subprocess.run(cmd, shell=True)
            self.status_label.setText("🔄 Efeitos visuais desativados para melhor desempenho!")
        except:
            self.status_label.setText("⚠️ Não foi possível aplicar essa otimização.")

    # Resto das funções aqui

    def limpar_pontos_restauracao(self):
        try:
            subprocess.run('powershell.exe -Command "Checkpoint-Computer -Description \'Ponto de Restauração Manual\' -RestorePointType \'MODIFY_SETTINGS\'"', shell=True)
            self.status_label.setText("Ponto de restauração criado com sucesso!")
        except:
            self.status_label.setText("Não foi possível criar o ponto de restauração.")

if __name__ == '__main__':
    app = QApplication([])
    janela = otimizadorPC()
    janela.show()
    app.exec_()
