import os
import shutil
import subprocess
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGroupBox, QGridLayout
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QSize

class OtimizadorPC(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛠️ Otimizador Aoxy")
        self.setGeometry(200, 100, 800, 550)
        self.setFixedSize(800, 550)
        self.setAutoFillBackground(True)

        # Paleta de cores
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # Estilo geral
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
                margin: 5px;
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
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
            }
        """)

        # Layout principal vertical
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Título
        self.label_titulo = QLabel("🧰 Otimizador de PC")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_titulo)

        # Grupos de botões
        self.box_limpeza = self.criar_grupo("🧹 Limpeza", [
            "🧹 Limpar Temporários",
            "🗑️ Esvaziar Lixeira",
            "🧹 Limpar cache do Windows Update",
            "🧹 Limpar Prefetch",
            "📦 Limpar Pontos de Restauração"
        ])

        self.box_desempenho = self.criar_grupo("🚀 Desempenho", [
            "🔄 Ativar Modo Desempenho (efeitos off)",
            "🧯 Desativar Serviços Desnecessários",
            "🚫 Mostrar Programas de Inicialização",
            "🎭 Desativar Efeitos de Transparência",
            "🚀 Ativar Plano Alto Desempenho",
            "🎭 Desativar Animações Extras",
            "💨 Liberar RAM"
        ])

        self.box_avancado = self.criar_grupo("⚙️ Avançado", [
            "🛠️ Otimizar Inicialização",
            "🔍 Verificar Integridade do Sistema (sfc)",
            "💾 Desfragmentar Disco"
        ])

        # Layout horizontal para grupos
        grupos_layout = QHBoxLayout()
        grupos_layout.addWidget(self.box_limpeza)
        grupos_layout.addWidget(self.box_desempenho)
        grupos_layout.addWidget(self.box_avancado)
        main_layout.addLayout(grupos_layout)

        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("color: #444444;")
        main_layout.addWidget(separador)

        # Status
        self.status_label = QLabel("✅ Pronto para otimizar!")
        self.status_label.setObjectName("status")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # Conectar funções
        self.botoes = {
            "🧹 Limpar Temporários": self.limpar_temporarios,
            "🗑️ Esvaziar Lixeira": self.esvaziar_lixeira,
            "🧹 Limpar cache do Windows Update": self.limpar_cache_windows_update,
            "🧹 Limpar Prefetch": self.limpar_prefetch,
            "📦 Limpar Pontos de Restauração": self.limpar_pontos_restauracao,
            "🔄 Ativar Modo Desempenho (efeitos off)": self.desativar_efeitos_visuais,
            "🧯 Desativar Serviços Desnecessários": self.desativar_servicos,
            "🚫 Mostrar Programas de Inicialização": self.mostrar_programas_inicio,
            "🎭 Desativar Efeitos de Transparência": self.desativar_transparencia,
            "🚀 Ativar Plano Alto Desempenho": self.ativar_plano_alto_desempenho,
            "🎭 Desativar Animações Extras": self.desativar_animacoes_extra,
            "💨 Liberar RAM": self.liberar_ram,
            "🛠️ Otimizar Inicialização": self.otimizar_inicializacao,
            "🔍 Verificar Integridade do Sistema (sfc)": self.verificar_integridade_sistema,
            "💾 Desfragmentar Disco": self.desfragmentar_disco
        }
        self.conectar_botoes()

    def criar_grupo(self, titulo, botoes_lista):
        grupo = QGroupBox(titulo)
        layout = QGridLayout()
        grupo.setLayout(layout)
        grupo.botoes = {}
        for i, texto in enumerate(botoes_lista):
            botao = QPushButton(texto)
            botao.setIconSize(QSize(24, 24))
            layout.addWidget(botao, i // 2, i % 2)
            grupo.botoes[texto] = botao
        return grupo

    def conectar_botoes(self):
        for texto, func in self.botoes.items():
            for grupo in [self.box_limpeza, self.box_desempenho, self.box_avancado]:
                if texto in grupo.botoes:
                    grupo.botoes[texto].clicked.connect(func)

    # ---------------- Funções reais ----------------

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

    def desativar_servicos(self):
        self.status_label.setText("Função de desativar serviços ainda não implementada.")

    def mostrar_programas_inicio(self):
        self.status_label.setText("Função de mostrar programas de inicialização ainda não implementada.")

    def desativar_transparencia(self):
        self.status_label.setText("Função de desativar transparência ainda não implementada.")    

    def ativar_plano_alto_desempenho(self):
        self.status_label.setText("Função de ativar plano de alto desempenho ainda não implementada.") 

    def verificar_integridade_sistema(self):
        self.status_label.setText("Função de verificar integridade do sistema ainda não implementada.")      

    def desfragmentar_disco(self):
        self.status_label.setText("Função de desfragmentar disco ainda não implementada.")

    def otimizar_inicializacao(self):
        self.status_label.setText("Função de otimizar inicialização ainda não implementada.")

    def limpar_cache_windows_update(self):
        self.status_label.setText("Função de limpar cache do Windows Update ainda não implementada.")       

    def desativar_animacoes_extra(self):
        self.status_label.setText("Função de desativar animações extras ainda não implementada.")  

    def liberar_ram(self):
        self.status_label.setText("Função de liberar RAM ainda não implementada.")   

    def limpar_prefetch(self):
        self.status_label.setText("Função de limpar Prefetch ainda não implementada.")

    def limpar_pontos_restauracao(self):
        self.status_label.setText("Função de limpar pontos de restauração ainda não implementada.")

if __name__ == "__main__":
    app = QApplication([])
    janela = OtimizadorPC()
    janela.show()
    app.exec_()
