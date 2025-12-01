# Importaciones de QtCore
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
# Importaciones de QtGui
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
# Importaciones de QtWidgets
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget, QGridLayout)

# ==============================================================================
# DEFINICIÓN DE LA UI DEL MODULO MT (Máquina de Turing)
# ==============================================================================

class MT_Module(QWidget):
    """
    Clase que define la estructura visual y los widgets del módulo MT.
    """
    def setupUi(self, MT_Module):
        """
        Configura todos los widgets, sus propiedades y la disposición del layout.
        """
        if not MT_Module.objectName():
            MT_Module.setObjectName(u"MT_Module")
        
        # --- Propiedades de la Ventana Principal ---
        MT_Module.resize(1000, 700)
        MT_Module.setMinimumSize(QSize(800, 600))
        
        # --- Hoja de Estilos (CSS de Qt) ---
        MT_Module.setStyleSheet(u"""
/* Estilo general del Módulo */
QWidget#MT_Module {
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

/* Estilo de Botones General (Azul para Tren) */
QPushButton {
    background-color: #3498db;
    color: white;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
    min-height: 40px;
    font-size: 10pt;
}
QPushButton:hover {
    background-color: #2980b9;
}

/* Botón de Regreso */
QPushButton#backToMenuButton {
    background-color: #95a5a6;
}
QPushButton#backToMenuButton:hover {
    background-color: #7f8c8d;
}

/* Botón de Reiniciar (Rojo) */
QPushButton#resetButton {
    background-color: #e74c3c;
}
QPushButton#resetButton:hover {
    background-color: #c0392b;
}

/* Botón Siguiente Paso (Verde) */
QPushButton#nextStepButton {
    background-color: #27ae60;
    font-size: 12pt;
}
QPushButton#nextStepButton:hover {
    background-color: #229954;
}

/* Casillas de la cinta */
QLabel.tapeCell {
    background-color: white;
    border: 2px solid #3498db;
    border-radius: 4px;
    font-size: 20pt;
    font-weight: bold;
    min-width: 60px;
    max-width: 60px;
    min-height: 60px;
    max-height: 60px;
}

QLabel.tapeCell[isHead="true"] {
    background-color: #f39c12;
    border: 3px solid #e67e22;
}

/* Contador y estado */
QLabel#stateLabel, QLabel#stepCounterLabel {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 8px;
    font-size: 12pt;
    font-weight: bold;
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
        self.horizontalLayout = QHBoxLayout(MT_Module)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        
        # ----------------------------------------------------------------------
        # COLUMNA IZQUIERDA: TEORÍA y NAVEGACIÓN
        # ----------------------------------------------------------------------
        self.leftColumnWidget = QWidget(MT_Module)
        self.leftColumnWidget.setObjectName(u"leftColumnWidget")
        self.leftColumnWidget.setMinimumSize(QSize(280, 0))
        
        self.verticalLayout_1 = QVBoxLayout(self.leftColumnWidget)
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        
        # Etiqueta de Título
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

        # Botón para Regresar al Menú
        self.backToMenuButton = QPushButton(self.leftColumnWidget)
        self.backToMenuButton.setObjectName(u"backToMenuButton")
        self.verticalLayout_1.addWidget(self.backToMenuButton)

        self.horizontalLayout.addWidget(self.leftColumnWidget)

        # --- Separador Vertical 1 ---
        self.separator_1 = QFrame(MT_Module)
        self.separator_1.setObjectName(u"separator_1")
        self.separator_1.setMaximumSize(QSize(1, 16777215))
        self.separator_1.setStyleSheet(u"background-color: #bdc3c7;")
        self.separator_1.setFrameShape(QFrame.VLine)
        self.separator_1.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.separator_1)

        # ----------------------------------------------------------------------
        # COLUMNA CENTRAL: VISUALIZACIÓN DE LA CINTA Y CONTROLES
        # ----------------------------------------------------------------------
        self.centerColumnWidget = QWidget(MT_Module)
        self.centerColumnWidget.setObjectName(u"centerColumnWidget")
        self.centerColumnWidget.setMinimumSize(QSize(400, 0))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        self.centerColumnWidget.setSizePolicy(sizePolicy2)
        
        self.verticalLayout_2 = QVBoxLayout(self.centerColumnWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        
        # Título del Tren/Cinta
        self.tapeTitle = QLabel(self.centerColumnWidget)
        self.tapeTitle.setObjectName(u"tapeTitle")
        self.verticalLayout_2.addWidget(self.tapeTitle)

        # Contenedor de la Cinta (Grid Layout para 10 casillas)
        self.tapeWidget = QWidget(self.centerColumnWidget)
        self.tapeWidget.setObjectName(u"tapeWidget")
        self.tapeLayout = QHBoxLayout(self.tapeWidget)
        self.tapeLayout.setObjectName(u"tapeLayout")
        self.tapeLayout.setSpacing(5)
        
        # Crear 10 casillas de cinta
        self.tapeCells = []
        for i in range(10):
            cell = QLabel(self.tapeWidget)
            cell.setObjectName(f"tapeCell_{i}")
            cell.setProperty("class", "tapeCell")
            cell.setProperty("isHead", "false")
            cell.setAlignment(Qt.AlignCenter)
            cell.setText("□")
            self.tapeCells.append(cell)
            self.tapeLayout.addWidget(cell)
        
        self.verticalLayout_2.addWidget(self.tapeWidget)

        # Indicador de Posición del Cabezal
        self.headPositionLabel = QLabel(self.centerColumnWidget)
        self.headPositionLabel.setObjectName(u"headPositionLabel")
        self.headPositionLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.headPositionLabel)

        # Estado Actual
        self.stateLabel = QLabel(self.centerColumnWidget)
        self.stateLabel.setObjectName(u"stateLabel")
        self.stateLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.stateLabel)

        # Contador de Pasos
        self.stepCounterLabel = QLabel(self.centerColumnWidget)
        self.stepCounterLabel.setObjectName(u"stepCounterLabel")
        self.stepCounterLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.stepCounterLabel)

        # Botón Siguiente Paso
        self.nextStepButton = QPushButton(self.centerColumnWidget)
        self.nextStepButton.setObjectName(u"nextStepButton")
        self.verticalLayout_2.addWidget(self.nextStepButton)

        # Botón de Reinicio
        self.resetButton = QPushButton(self.centerColumnWidget)
        self.resetButton.setObjectName(u"resetButton")
        self.verticalLayout_2.addWidget(self.resetButton)

        self.horizontalLayout.addWidget(self.centerColumnWidget)

        # --- Separador Vertical 2 ---
        self.separator_2 = QFrame(MT_Module)
        self.separator_2.setObjectName(u"separator_2")
        self.separator_2.setMaximumSize(QSize(1, 16777215))
        self.separator_2.setStyleSheet(u"background-color: #bdc3c7;")
        self.separator_2.setFrameShape(QFrame.VLine)
        self.separator_2.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.separator_2)

        # ----------------------------------------------------------------------
        # COLUMNA DERECHA: TABLA DE INSTRUCCIONES
        # ----------------------------------------------------------------------
        self.rightColumnWidget = QWidget(MT_Module)
        self.rightColumnWidget.setObjectName(u"rightColumnWidget")
        self.rightColumnWidget.setMinimumSize(QSize(280, 0))
        
        self.verticalLayout_3 = QVBoxLayout(self.rightColumnWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        
        # Título de Instrucciones
        self.instructionsTitle = QLabel(self.rightColumnWidget)
        self.instructionsTitle.setObjectName(u"instructionsTitle")
        self.verticalLayout_3.addWidget(self.instructionsTitle)

        # Display de Instrucciones/Reglas
        self.instructionsDisplay = QTextEdit(self.rightColumnWidget)
        self.instructionsDisplay.setObjectName(u"instructionsDisplay")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setVerticalStretch(2)
        self.instructionsDisplay.setSizePolicy(sizePolicy3)
        self.instructionsDisplay.setReadOnly(True)
        self.verticalLayout_3.addWidget(self.instructionsDisplay)

        self.horizontalLayout.addWidget(self.rightColumnWidget)

        # Conecta las señales y slots automáticamente
        self.retranslateUi(MT_Module)
        QMetaObject.connectSlotsByName(MT_Module)
    # Fin de setupUi

    # ======================================================================
    # TRADUCCIÓN/TEXTOS DE LA INTERFAZ
    # ======================================================================
    def retranslateUi(self, MT_Module):
        """
        Establece los textos visibles para todos los widgets.
        """
        MT_Module.setWindowTitle(QCoreApplication.translate("MT_Module", u"🚂 El Tren Mágico que Ordena Juguetes", None))
        
        # Columna Izquierda
        self.theoryTitle.setText(QCoreApplication.translate("MT_Module", u"📖 ¿Cómo Jugar?", None))
        self.backToMenuButton.setText(QCoreApplication.translate("MT_Module", u"← Volver al Menú", None))
        
        # Columna Central
        self.tapeTitle.setText(QCoreApplication.translate("MT_Module", u"🚂 Los Vagones del Tren", None))
        self.headPositionLabel.setText(QCoreApplication.translate("MT_Module", u"👆 Cabeza del Tren en posición: 0", None))
        self.stateLabel.setText(QCoreApplication.translate("MT_Module", u"Estado: Inicio", None))
        self.stepCounterLabel.setText(QCoreApplication.translate("MT_Module", u"Pasos: 0", None))
        self.nextStepButton.setText(QCoreApplication.translate("MT_Module", u"➡️ Siguiente Paso", None))
        self.resetButton.setText(QCoreApplication.translate("MT_Module", u"↻ Empezar de Nuevo", None))
        
        # Columna Derecha
        self.instructionsTitle.setText(QCoreApplication.translate("MT_Module", u"📋 Instrucciones del Tren", None))
    # retranslateUi
