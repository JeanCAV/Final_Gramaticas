# Importaciones de QtCore
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
# Importaciones de QtGui: Elementos visuales y de interacción
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
# Importaciones de QtWidgets
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget, QGridLayout)

# ==============================================================================
# DEFINICIÓN DE LA UI DEL MODULO GDC (Gramáticas Dependientes de Contexto)
# ==============================================================================

class GDC_Module(QWidget):
    """
    Clase que define la estructura visual y los widgets del módulo GDC.
    """
    def setupUi(self, GDC_Module):
        """
        Configura todos los widgets, sus propiedades (tamaño, estilo, nombre) 
        y la disposición del layout.
        """
        if not GDC_Module.objectName():
            GDC_Module.setObjectName(u"GDC_Module")
        
        # --- Propiedades de la Ventana Principal ---
        GDC_Module.resize(1000, 700)
        GDC_Module.setMinimumSize(QSize(800, 600))
        
        # --- Hoja de Estilos (CSS de Qt) ---
        GDC_Module.setStyleSheet(u"""
/* Estilo general del Módulo */
QWidget#GDC_Module {
    background-color: #f0f0f0;
    font-family: "Segoe UI", "Helvetica", Arial, sans-serif; 
    color: #2c3e50;
}

/* Estilo para los QTextEdit */
QTextEdit {
    border: 1px solid #bdc3c7;
    border-radius: 8px;
    padding: 10px;
    background-color: white; 
    font-size: 10pt;
    color: #2c3e50; 
}

/* Estilo para QScrollArea */
QScrollArea {
    border: 1px solid #bdc3c7;
    border-radius: 8px;
    background-color: white; 
}

/* Estilo de Botones General (Verde para Jardín) */
QPushButton {
    background-color: #2ecc71;
    color: white;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
    min-height: 40px;
    font-size: 10pt;
}
QPushButton:hover {
    background-color: #27ae60;
}

/* Botón de Regreso (Azul) */
QPushButton#backToMenuButton {
    background-color: #3498db;
}
QPushButton#backToMenuButton:hover {
    background-color: #2980b9;
}

/* Botón de Reiniciar (Rojo) */
QPushButton#resetButton {
    background-color: #e74c3c;
}
QPushButton#resetButton:hover {
    background-color: #c0392b;
}

/* Botón Siguiente Fase (Verde Oscuro) */
QPushButton#nextPhaseButton {
    background-color: #16a085;
    font-size: 12pt;
}
QPushButton#nextPhaseButton:hover {
    background-color: #138d75;
}

/* Área de plantas */
QLabel#gardenDisplay {
    background-color: #d5f4e6;
    border: 2px solid #27ae60;
    border-radius: 8px;
    padding: 20px;
    font-size: 48pt;
    font-family: "Courier New", monospace;
}

/* Contador de plantas */
QLabel#plantCounterLabel {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 8px;
    font-size: 11pt;
}

/* Títulos de sección */
QLabel {
    font-size: 16pt;
    font-weight: bold;
    color: #2c3e50; 
    margin-bottom: 10px;
}
""")
        
        # ======================================================================
        # LAYOUT PRINCIPAL (HORIZONTAL)
        # ======================================================================
        self.horizontalLayout = QHBoxLayout(GDC_Module)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        
        # ----------------------------------------------------------------------
        # COLUMNA IZQUIERDA: TEORÍA y NAVEGACIÓN
        # ----------------------------------------------------------------------
        self.leftColumnWidget = QWidget(GDC_Module)
        self.leftColumnWidget.setObjectName(u"leftColumnWidget")
        self.leftColumnWidget.setMinimumSize(QSize(280, 0))
        
        self.verticalLayout_1 = QVBoxLayout(self.leftColumnWidget)
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        
        # Etiqueta de Título de Teoría
        self.theoryTitle = QLabel(self.leftColumnWidget)
        self.theoryTitle.setObjectName(u"theoryTitle")
        self.theoryTitle.setWordWrap(True)
        self.verticalLayout_1.addWidget(self.theoryTitle)

        # Área de Texto para la Teoría
        self.theoryTextDisplay = QTextEdit(self.leftColumnWidget)
        self.theoryTextDisplay.setObjectName(u"theoryTextDisplay")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setVerticalStretch(3)
        self.theoryTextDisplay.setSizePolicy(sizePolicy)
        self.theoryTextDisplay.setReadOnly(True)
        self.verticalLayout_1.addWidget(self.theoryTextDisplay)

        # Etiqueta para el Patrón Objetivo
        self.targetPatternLabel = QLabel(self.leftColumnWidget)
        self.targetPatternLabel.setObjectName(u"targetPatternLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.targetPatternLabel.setSizePolicy(sizePolicy1)
        self.verticalLayout_1.addWidget(self.targetPatternLabel)

        # Botón para Regresar al Menú
        self.backToMenuButton = QPushButton(self.leftColumnWidget)
        self.backToMenuButton.setObjectName(u"backToMenuButton")
        self.verticalLayout_1.addWidget(self.backToMenuButton)

        self.horizontalLayout.addWidget(self.leftColumnWidget)

        # --- Separador Vertical 1 ---
        self.separator_1 = QFrame(GDC_Module)
        self.separator_1.setObjectName(u"separator_1")
        self.separator_1.setMaximumSize(QSize(1, 16777215))
        self.separator_1.setStyleSheet(u"background-color: #bdc3c7;")
        self.separator_1.setFrameShape(QFrame.VLine)
        self.separator_1.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.separator_1)

        # ----------------------------------------------------------------------
        # COLUMNA CENTRAL: VISUALIZACIÓN DEL JARDÍN
        # ----------------------------------------------------------------------
        self.centerColumnWidget = QWidget(GDC_Module)
        self.centerColumnWidget.setObjectName(u"centerColumnWidget")
        self.centerColumnWidget.setMinimumSize(QSize(300, 0))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        self.centerColumnWidget.setSizePolicy(sizePolicy2)
        
        self.verticalLayout_2 = QVBoxLayout(self.centerColumnWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        
        # Título del Jardín
        self.gardenTitle = QLabel(self.centerColumnWidget)
        self.gardenTitle.setObjectName(u"gardenTitle")
        self.verticalLayout_2.addWidget(self.gardenTitle)

        # Display del Jardín (fila de plantas)
        self.gardenDisplay = QLabel(self.centerColumnWidget)
        self.gardenDisplay.setObjectName(u"gardenDisplay")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setVerticalStretch(2)
        self.gardenDisplay.setSizePolicy(sizePolicy3)
        self.gardenDisplay.setAlignment(Qt.AlignCenter)
        self.gardenDisplay.setWordWrap(True)
        self.verticalLayout_2.addWidget(self.gardenDisplay)

        # Contador de Plantas
        self.plantCounterLabel = QLabel(self.centerColumnWidget)
        self.plantCounterLabel.setObjectName(u"plantCounterLabel")
        self.plantCounterLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.plantCounterLabel)

        # Botón Siguiente Fase
        self.nextPhaseButton = QPushButton(self.centerColumnWidget)
        self.nextPhaseButton.setObjectName(u"nextPhaseButton")
        self.verticalLayout_2.addWidget(self.nextPhaseButton)

        # Botón de Validación
        self.validateButton = QPushButton(self.centerColumnWidget)
        self.validateButton.setObjectName(u"validateButton")
        self.verticalLayout_2.addWidget(self.validateButton)

        # Botón de Reinicio
        self.resetButton = QPushButton(self.centerColumnWidget)
        self.resetButton.setObjectName(u"resetButton")
        self.verticalLayout_2.addWidget(self.resetButton)

        self.horizontalLayout.addWidget(self.centerColumnWidget)

        # --- Separador Vertical 2 ---
        self.separator_2 = QFrame(GDC_Module)
        self.separator_2.setObjectName(u"separator_2")
        self.separator_2.setMaximumSize(QSize(1, 16777215))
        self.separator_2.setStyleSheet(u"background-color: #bdc3c7;")
        self.separator_2.setFrameShape(QFrame.VLine)
        self.separator_2.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.separator_2)

        # ----------------------------------------------------------------------
        # COLUMNA DERECHA: REGLAS Y HISTORIAL
        # ----------------------------------------------------------------------
        self.rightColumnWidget = QWidget(GDC_Module)
        self.rightColumnWidget.setObjectName(u"rightColumnWidget")
        self.rightColumnWidget.setMinimumSize(QSize(300, 0))
        
        self.verticalLayout_3 = QVBoxLayout(self.rightColumnWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        
        # Título de Reglas
        self.rulesTitle = QLabel(self.rightColumnWidget)
        self.rulesTitle.setObjectName(u"rulesTitle")
        self.verticalLayout_3.addWidget(self.rulesTitle)

        # Display de Reglas
        self.rulesDisplay = QTextEdit(self.rightColumnWidget)
        self.rulesDisplay.setObjectName(u"rulesDisplay")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setVerticalStretch(1)
        self.rulesDisplay.setSizePolicy(sizePolicy4)
        self.rulesDisplay.setReadOnly(True)
        self.verticalLayout_3.addWidget(self.rulesDisplay)

        # Título de Historial
        self.historyTitle = QLabel(self.rightColumnWidget)
        self.historyTitle.setObjectName(u"historyTitle")
        self.verticalLayout_3.addWidget(self.historyTitle)

        # Display de Historial
        self.historyDisplay = QTextEdit(self.rightColumnWidget)
        self.historyDisplay.setObjectName(u"historyDisplay")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setVerticalStretch(2)
        self.historyDisplay.setSizePolicy(sizePolicy5)
        self.historyDisplay.setReadOnly(True)
        self.verticalLayout_3.addWidget(self.historyDisplay)

        # Selector de Nivel
        self.levelSelectorWidget = QWidget(self.rightColumnWidget)
        self.levelSelectorWidget.setObjectName(u"levelSelectorWidget")
        self.levelButtonsLayout = QHBoxLayout(self.levelSelectorWidget)
        self.levelButtonsLayout.setObjectName(u"levelButtonsLayout")
        
        self.level1Button = QPushButton(self.levelSelectorWidget)
        self.level1Button.setObjectName(u"level1Button")
        self.levelButtonsLayout.addWidget(self.level1Button)
        
        self.level2Button = QPushButton(self.levelSelectorWidget)
        self.level2Button.setObjectName(u"level2Button")
        self.levelButtonsLayout.addWidget(self.level2Button)
        
        self.verticalLayout_3.addWidget(self.levelSelectorWidget)

        self.horizontalLayout.addWidget(self.rightColumnWidget)

        # Conecta las señales y slots automáticamente
        self.retranslateUi(GDC_Module)
        QMetaObject.connectSlotsByName(GDC_Module)
    # Fin de setupUi

    # ======================================================================
    # TRADUCCIÓN/TEXTOS DE LA INTERFAZ
    # ======================================================================
    def retranslateUi(self, GDC_Module):
        """
        Establece los textos visibles para todos los widgets.
        """
        GDC_Module.setWindowTitle(QCoreApplication.translate("GDC_Module", u"🌱 El Jardín Mágico que Crece Junto", None))
        
        # Columna Izquierda
        self.theoryTitle.setText(QCoreApplication.translate("GDC_Module", u"📖 ¿Cómo Jugar?", None))
        self.targetPatternLabel.setText(QCoreApplication.translate("GDC_Module", u"🎯 Meta: Elige un nivel primero", None))
        self.backToMenuButton.setText(QCoreApplication.translate("GDC_Module", u"← Volver al Menú", None))
        
        # Columna Central
        self.gardenTitle.setText(QCoreApplication.translate("GDC_Module", u"🌳 Tu Jardín Mágico", None))
        self.gardenDisplay.setText(QCoreApplication.translate("GDC_Module", u"👇 Elige un nivel abajo para empezar 👇", None))
        self.plantCounterLabel.setText(QCoreApplication.translate("GDC_Module", u"📊 Aún no hay plantas", None))
        self.nextPhaseButton.setText(QCoreApplication.translate("GDC_Module", u"⏩ Siguiente Fase (Hacer Crecer)", None))
        self.validateButton.setText(QCoreApplication.translate("GDC_Module", u"✓ ¿Está Balanceado?", None))
        self.resetButton.setText(QCoreApplication.translate("GDC_Module", u"↻ Empezar de Nuevo", None))
        
        # Columna Derecha
        self.rulesTitle.setText(QCoreApplication.translate("GDC_Module", u"✨ Reglas Mágicas", None))
        self.historyTitle.setText(QCoreApplication.translate("GDC_Module", u"📜 Historia del Jardín", None))
        self.level1Button.setText(QCoreApplication.translate("GDC_Module", u"🌱 Nivel 1: Fácil", None))
        self.level2Button.setText(QCoreApplication.translate("GDC_Module", u"🌟 Nivel 2: Desafío", None))
    # retranslateUi
