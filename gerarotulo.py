import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QWidget, QMessageBox, QSizePolicy, QHBoxLayout,
    QAction, QMenu, QMenuBar, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings, QDateTime

class MinhaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Configurando os elementos da interface
        self.label = QLabel('Olá, PyQt!', self)
        self.label.setAlignment(Qt.AlignCenter)  # Alinhamento central
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_nome = QLineEdit(self)
        self.input_nome.setPlaceholderText('Digite seu nome')

        self.botao_saudacao = QPushButton('Saudação Personalizada', self)
        self.botao_saudacao.setIcon(QIcon('icon_saudacao.png'))
        self.botao_saudacao.clicked.connect(self.mostrarSaudacao)
        self.botao_saudacao.setShortcut('Ctrl+S')

        self.botao_padrao = QPushButton('Restaurar Padrão', self)
        self.botao_padrao.setIcon(QIcon('icon_padrao.png'))
        self.botao_padrao.clicked.connect(self.restaurarPadrao)
        self.botao_padrao.setShortcut('Ctrl+R')

        self.botao_fechar = QPushButton('Fechar', self)
        self.botao_fechar.setIcon(QIcon('icon_fechar.png'))
        self.botao_fechar.clicked.connect(self.fecharAplicacao)
        self.botao_fechar.setShortcut('Ctrl+Q')

        self.botao_limpar = QPushButton('Limpar', self)
        self.botao_limpar.setIcon(QIcon('icon_limpar.png'))
        self.botao_limpar.clicked.connect(self.limparCampos)
        self.botao_limpar.setShortcut('Ctrl+L')

        self.botao_copiar = QPushButton('Copiar para Área de Transferência', self)
        self.botao_copiar.setIcon(QIcon('icon_copiar.png'))
        self.botao_copiar.clicked.connect(self.copiarParaAreaTransferencia)

        self.botao_salvar = QPushButton('Salvar em Arquivo', self)
        self.botao_salvar.setIcon(QIcon('icon_salvar.png'))
        self.botao_salvar.clicked.connect(self.salvarEmArquivo)

        self.botao_carregar = QPushButton('Carregar de Arquivo', self)
        self.botao_carregar.setIcon(QIcon('icon_carregar.png'))
        self.botao_carregar.clicked.connect(self.carregarDeArquivo)

        self.botao_tela_cheia = QPushButton('Modo de Tela Cheia', self)
        self.botao_tela_cheia.setIcon(QIcon('icon_tela_cheia.png'))
        self.botao_tela_cheia.clicked.connect(self.ativarModoTelaCheia)

        # Adicionando uma barra de status
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Bem-vindo à Minha Aplicação PyQt!', 3000)

        # Configurando o layout vertical
        layout_vertical = QVBoxLayout()
        layout_vertical.addWidget(self.label)
        layout_vertical.addWidget(self.input_nome)
        layout_vertical.addWidget(self.botao_saudacao)
        layout_vertical.addWidget(self.botao_padrao)

        # Criando um layout horizontal para os botões inferiores
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.botao_fechar)
        layout_horizontal.addWidget(self.botao_limpar)
        layout_horizontal.addWidget(self.botao_copiar)
        layout_horizontal.addWidget(self.botao_salvar)
        layout_horizontal.addWidget(self.botao_carregar)
        layout_horizontal.addWidget(self.botao_tela_cheia)

        # Adicionando os layouts ao widget central
        central_widget = QWidget()
        central_widget.setLayout(layout_vertical)
        central_widget.layout().addLayout(layout_horizontal)
        self.setCentralWidget(central_widget)

        # Configurando a janela principal
        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('Minha Aplicação PyQt')

        # Adicionando uma barra de menu
        self.criarMenu()

        # Carregando configurações salvas
        self.carregarConfiguracoes()

        self.show()

    def criarMenu(self):
        menubar = self.menuBar()

        # Criando o menu Arquivo
        menu_arquivo = menubar.addMenu('Arquivo')

        # Adicionando ação para fechar
        acao_fechar = QAction('Fechar', self)
        acao_fechar.setShortcut('Ctrl+Q')
        acao_fechar.setStatusTip('Fechar a aplicação')
        acao_fechar.triggered.connect(self.fecharAplicacao)
        menu_arquivo.addAction(acao_fechar)

        # Adicionando ação para salvar configurações
        acao_salvar = QAction('Salvar Configurações', self)
        acao_salvar.setStatusTip('Salvar o estado atual da aplicação')
        acao_salvar.triggered.connect(self.salvarConfiguracoes)
        menu_arquivo.addAction(acao_salvar)

        # Adicionando o menu Ajuda
        menu_ajuda = menubar.addMenu('Ajuda')

        # Adicionando ação para mostrar informações sobre a aplicação
        acao_sobre = QAction('Sobre', self)
        acao_sobre.setStatusTip('Informações sobre a aplicação')
        acao_sobre.triggered.connect(self.mostrarSobre)
        menu_ajuda.addAction(acao_sobre)

    def mostrarSaudacao(self):
        nome = self.input_nome.text()
        if nome:
            QMessageBox.information(self, 'Saudação Personalizada', f'Bem-vindo, {nome}!')
        else:
            QMessageBox.warning(self, 'Erro', 'Por favor, insira um nome antes de clicar no botão.')

    def restaurarPadrao(self):
        self.input_nome.clear()
        self.label.setText('Olá, PyQt!')
        self.input_nome.setFocus()

    def fecharAplicacao(self):
        resposta = QMessageBox.question(self, 'Fechar Aplicação', 'Tem certeza que deseja fechar a aplicação?', QMessageBox.Yes | QMessageBox.No)
        if resposta == QMessageBox.Yes:
            self.salvarConfiguracoes()
            self.close()

    def mostrarSobre(self):
        QMessageBox.about(self, 'Sobre', 'Minha Aplicação PyQt\nVersão 1.0\nDesenvolvida por [Seu Nome]')

    def salvarConfiguracoes(self):
        settings = QSettings('config.ini', QSettings.IniFormat)
        settings.setValue('Nome', self.input_nome.text())
        settings.sync()

        # Atualizando a última vez que a aplicação foi salva na barra de status
        self.status_bar.showMessage(f'Configurações salvas em {QDateTime.currentDateTime().toString()}')

    def carregarConfiguracoes(self):
        settings = QSettings('config.ini', QSettings.IniFormat)
        nome_salvo = settings.value('Nome', '')
        if nome_salvo:
            self.input_nome.setText(nome_salvo)

    def limparCampos(self):
        self.input_nome.clear()
        self.label.setText('Olá, PyQt!')
        self.input_nome.setFocus()

        # Adicionando a saudação ao histórico
        historico = self.carregarHistorico()
        historico.append(f'Saudação Limpa em {QDateTime.currentDateTime().toString()}')
        self.salvarHistorico(historico)

    def copiarParaAreaTransferencia(self):
        saudacao = self.label.text()
        QApplication.clipboard().setText(saudacao)
        self.status_bar.showMessage('Saudação copiada para a Área de Transferência')

    def salvarEmArquivo(self):
        saudacao = self.label.text()
        nome_arquivo, _ = QFileDialog.getSaveFileName(self, 'Salvar Saudação em Arquivo', '', 'Arquivos de Texto (*.txt);;Todos os Arquivos (*)')
        if nome_arquivo:
            with open(nome_arquivo, 'w') as file:
                file.write(saudacao)
            self.status_bar.showMessage(f'Saudação salva em "{nome_arquivo}"')

    def carregarDeArquivo(self):
        nome_arquivo, _ = QFileDialog.getOpenFileName(self, 'Carregar Saudação de Arquivo', '', 'Arquivos de Texto (*.txt);;Todos os Arquivos (*)')
        if nome_arquivo:
            with open(nome_arquivo, 'r') as file:
                saudacao = file.read()
                self.label.setText(saudacao)
                self.status_bar.showMessage(f'Saudação carregada de "{nome_arquivo}"')

    def ativarModoTelaCheia(self):
        if not self.isFullScreen():
            self.showFullScreen()
            self.status_bar.showMessage('Modo de Tela Cheia ativado')
        else:
            self.showNormal()
            self.status_bar.showMessage('Modo de Tela Cheia desativado')

    def mostrarHistorico(self):
        historico = self.carregarHistorico()
        if historico:
            QMessageBox.information(self, 'Histórico', '\n'.join(historico))
        else:
            QMessageBox.information(self, 'Histórico', 'Histórico vazio.')

    def salvarHistorico(self, historico):
        with open('historico.txt', 'a') as file:
            for item in historico:
                file.write(item + '\n')

    def carregarHistorico(self):
        try:
            with open('historico.txt', 'r') as file:
                historico = file.readlines()
            return [item.strip() for item in historico]
        except FileNotFoundError:
            return []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    minha_app = MinhaApp()
    sys.exit(app.exec_())
