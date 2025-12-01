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
    QTextEdit, QVBoxLayout, QWidget)
import os

# ==============================================================================
# 2. DEFINICIÓN DE LA UI DEL MODULO GIC
# ==============================================================================

class GIC_Module(QWidget):
    """
    Clase que define la estructura visual y los widgets del módulo GIC.
    """
    def setupUi(self, GIC_Module):
        """
        Configura todos los widgets, sus propiedades (tamaño, estilo, nombre) 
        y la disposición del layout.
        """
        if not GIC_Module.objectName():
            GIC_Module.setObjectName(u"GIC_Module")
        
        # --- Propiedades de la Ventana Principal ---
        GIC_Module.resize(1000, 700)
        GIC_Module.setMinimumSize(QSize(800, 600))
        
        # --- Hoja de Estilos (CSS de Qt) ---
        GIC_Module.setStyleSheet(u"/* Estilo general del Módulo, similar al de MainWindow */\n"
"QWidget#GIC_Module {\n"
" \tbackground-color: #f0f0f0; /* Fondo gris muy claro */\n"
" \tfont-family: \"Segoe UI\", \"Helvetica\", Arial, sans-serif; \n"
" \tcolor: #2c3e50; /* Color de fuente base */\n"
"}\n"
"\n"
"/* Estilo para los QTextEdit (Árbol y Teoría) */\n"
"QTextEdit {\n"
" \tborder: 1px solid #bdc3c7;\n"
" \tborder-radius: 8px;\n"
" \tpadding: 10px;\n"
" \tbackground-color: white; \n"
" \tfont-size: 10pt;\n"
" \tcolor: #2c3e50; \n"
"}\n"
"\n"
"/* Estilo para QScrollArea (Contenedor de Reglas y Nuevo) */\n"
"QScrollArea {\n"
" \tborder: 1px solid #bdc3c7;\n"
" \tborder-radius: 8px;\n"
" \tbackground-color: white; \n"
"}\n"
"QWidget#rulesContainerWidget {\n"
" \tbackground-color: white; \n"
"}\n"
"/* Nuevo estilo para el ScrollArea de Estado/Ayuda */\n"
"QScrollArea#statusScrollArea {\n"
"    border: 2px solid #3498db; /* Borde más distintivo */\n"
"    background-color: white; /* Fondo ligeramente diferente */\n"
"}\n"
"QWidget#statusContentWidget {\n"
"    background-color: white; \n"
"    padding: 10px; /* Padding para separar el contenido de los bordes del scroll area */\n"
"}\n"
"\n"
"/* Estilo de Botones General (Azul) */\n"
"QPushButton {\n"
" \tbackground-color: #3498db;\n"
" \tcolor: white;\n"
" \tpadding: 10px;\n"
" \tborder-radius: 8px;\n"
" \tfont-weight: bold;\n"
" \tmin-height: 40px;\n"
" \tfont-size: 10pt;\n"
"}\n"
"QPushButton:hover {\n"
" \tbackground-color: #2980b9;\n"
"}\n"
"\n"
"/* Estilo específico para los nuevos botones dentro del área de estado */\n"
"QPushButton#actionButton4, QPushButton#actionButton5, QPushButton#actionButton6, QPushButton#actionButton1, QPushButton#actionButton2, QPushButton#actionButton3 {\n"
"    background-color: #2ecc71; /* Un color verde para destacar */\n"
"    margin: 10px 0px 10px 0px; /* Margen superior e inferior para separación */\n"
"    min-height: 35px;\n"
"}\n"
"QPushButton#actionButton4:hover, QPushButton#actionButton5:hover, QPushButton#actionButton6:hover, QPushButton#actionButton1:hover, QPushButton#actionButton2:hover, QPushButton#actionButton3:hover {\n"
"    background-color: #27ae60;\n"
"}\n"
"\n"
"/* ESTILOS ESPECÍFICOS DE BOTONES INFERIORES */\n"
"\n"
"/* Botón de Regreso/Navegación (Azul) */\n"
"QPushButton#backToMenuButton {\n"
" \tbackground-color: #3498db; \n"
" \tcolor: white;\n"
"}\n"
"QPushButton#backToMenuButton:hover {\n"
" \tbackground-color: #2980b9;\n"
"}\n"
"\n"
"/* Botón de Reiniciar/Acción Destructiva (Rojo/Naranja) */\n"
"QPushButton#resetButton {\n"
" \tbackground-color: #e74c3c; \n"
" \tcolor: white;\n"
"}\n"
"QPushButton#resetButton:hover {\n"
" \tbackground-color: #c0392b;\n"
"}\n"
"\n"
"/* Títulos de sección */\n"
"QLabel {\n"
" \tfont-size: 16pt;\n"
" \tfont-weight: bold;\n"
" \tcolor: #2c3e50; \n"
" \tmargin-bottom: 10px;\n"
"QPushButton#backToMenuButton, QPushButton#showTreeButton { /* Añade showTreeButton aquí */"
" 	background-color: #3498db; "
"	color: white;"
"}\n"
"QPushButton#backToMenuButton:hover, QPushButton#showTreeButton:hover { /* Añade showTreeButton aquí */"
" 	background-color: #2980b9;"
"}"

"}")
        
        # ======================================================================
        # 3. LAYOUT PRINCIPAL (HORIZONTAL)
        # ======================================================================
        self.horizontalLayout = QHBoxLayout(GIC_Module)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        # Establece márgenes internos de 20 píxeles
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        
        # ----------------------------------------------------------------------
        # 3.1. COLUMNA IZQUIERDA: TEORÍA y NAVEGACIÓN
        # ----------------------------------------------------------------------
        self.leftColumnWidget = QWidget(GIC_Module)
        self.leftColumnWidget.setObjectName(u"leftColumnWidget")
        self.leftColumnWidget.setMinimumSize(QSize(280, 0)) # Ancho mínimo de 280
        
        self.verticalLayout_1 = QVBoxLayout(self.leftColumnWidget)
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        
        # Etiqueta de Título de Teoría
        self.theoryTitle = QLabel(self.leftColumnWidget)
        self.theoryTitle.setObjectName(u"theoryTitle")
        self.theoryTitle.setWordWrap(True)
        self.verticalLayout_1.addWidget(self.theoryTitle)

        # Área de Texto para la Teoría/Explicación
        self.theoryTextDisplay = QTextEdit(self.leftColumnWidget)
        self.theoryTextDisplay.setObjectName(u"theoryTextDisplay")
        # Política de tamaño: Expandible horizontalmente, con peso vertical de 3
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setVerticalStretch(3)
        self.theoryTextDisplay.setSizePolicy(sizePolicy)
        self.theoryTextDisplay.setReadOnly(True) # Solo lectura
        self.verticalLayout_1.addWidget(self.theoryTextDisplay)

        # Etiqueta para la Palabra Objetivo a Generar
        self.targetWordLabel = QLabel(self.leftColumnWidget)
        self.targetWordLabel.setObjectName(u"targetWordLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.targetWordLabel.setSizePolicy(sizePolicy1) # Altura fija
        self.verticalLayout_1.addWidget(self.targetWordLabel)

        # Botón para Regresar al Menú Principal
        self.backToMenuButton = QPushButton(self.leftColumnWidget)
        self.backToMenuButton.setObjectName(u"backToMenuButton")
        self.verticalLayout_1.addWidget(self.backToMenuButton)

        self.horizontalLayout.addWidget(self.leftColumnWidget)

        # --- Separador Vertical 1 ---
        self.separator_1 = QFrame(GIC_Module)
        self.separator_1.setObjectName(u"separator_1")
        self.separator_1.setMaximumSize(QSize(1, 16777215)) # Ancho máximo de 1px
        self.separator_1.setStyleSheet(u"background-color: #bdc3c7;")
        self.separator_1.setFrameShape(QFrame.VLine)
        self.separator_1.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.separator_1)

        # ----------------------------------------------------------------------
        # 3.2. COLUMNA CENTRAL: DERIVACIÓN y VISUALIZACIÓN
        # ----------------------------------------------------------------------
        self.centerColumnWidget = QWidget(GIC_Module)
        self.centerColumnWidget.setObjectName(u"centerColumnWidget")
        self.centerColumnWidget.setMinimumSize(QSize(300, 0)) # Ancho mínimo de 300
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1) # Da un factor de estiramiento horizontal
        self.centerColumnWidget.setSizePolicy(sizePolicy2)
        
        self.verticalLayout_2 = QVBoxLayout(self.centerColumnWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        
        # Etiqueta de Título de Derivación
        self.derivationTitle = QLabel(self.centerColumnWidget)
        self.derivationTitle.setObjectName(u"derivationTitle")
        self.verticalLayout_2.addWidget(self.derivationTitle)

        # Área de Texto para mostrar la Derivación (Árbol o Forma Sentencial)
        self.derivationTextDisplay = QTextEdit(self.centerColumnWidget)
        self.derivationTextDisplay.setObjectName(u"derivationTextDisplay")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setVerticalStretch(1)
        self.derivationTextDisplay.setSizePolicy(sizePolicy3)
        self.derivationTextDisplay.setReadOnly(True)
        self.verticalLayout_2.addWidget(self.derivationTextDisplay)

        # Etiqueta de Título de Visualización
        self.visualTitle = QLabel(self.centerColumnWidget)
        self.visualTitle.setObjectName(u"visualTitle")
        self.verticalLayout_2.addWidget(self.visualTitle)

        # ÁREA DE VISUALIZACIÓN DE IMAGEN (REEMPLAZO DE QTextEdit)
        self.dollsVisualImage = QLabel(self.centerColumnWidget)
        self.dollsVisualImage.setObjectName(u"dollsVisualImage")
        self.dollsVisualImage.setSizePolicy(sizePolicy3) # Mantiene la política de tamaño Expanding
        self.dollsVisualImage.setStyleSheet(u"background-color: white; border: 1px solid #bdc3c7; border-radius: 8px; padding: 5px;")
        self.dollsVisualImage.setAlignment(Qt.AlignCenter) # Centra la imagen si es más pequeña que el widget
        self.verticalLayout_2.addWidget(self.dollsVisualImage)

        # Botón de Reinicio de Derivación
        self.resetButton = QPushButton(self.centerColumnWidget)
        self.resetButton.setObjectName(u"resetButton")
        self.verticalLayout_2.addWidget(self.resetButton)

        self.horizontalLayout.addWidget(self.centerColumnWidget)

        # --- Separador Vertical 2 ---
        self.separator_2 = QFrame(GIC_Module)
        self.separator_2.setObjectName(u"separator_2")
        self.separator_2.setMaximumSize(QSize(1, 16777215)) # Ancho máximo de 1px
        self.separator_2.setStyleSheet(u"background-color: #bdc3c7;")
        self.separator_2.setFrameShape(QFrame.VLine)
        self.separator_2.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.separator_2)

        # ----------------------------------------------------------------------
        # 3.3. COLUMNA DERECHA: SCROLL AREA DE ESTADO Y REGLAS
        # ----------------------------------------------------------------------
        self.rightColumnWidget = QWidget(GIC_Module)
        self.rightColumnWidget.setObjectName(u"rightColumnWidget")
        self.rightColumnWidget.setMinimumSize(QSize(300, 0)) # Ancho mínimo de 300
        self.rightColumnWidget.setStyleSheet(u"\n"
"/* Fondo de la columna de la derecha, hereda el color principal */\n"
"QWidget#rightColumnWidget {\n"
" \tbackground-color: #f0f0f0; \n"
"}\n"
"")
        
        self.verticalLayout_3 = QVBoxLayout(self.rightColumnWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        
        # Etiqueta de Título para el Nuevo Scroll Area (Estado/Ayuda)
        self.statusTitle = QLabel(self.rightColumnWidget)
        self.statusTitle.setObjectName(u"statusTitle")
        self.verticalLayout_3.addWidget(self.statusTitle)
        
        # ÁREA DE DESPLAZAMIENTO DE ESTADO
        self.statusScrollArea = QScrollArea(self.rightColumnWidget)
        self.statusScrollArea.setObjectName(u"statusScrollArea")
        self.statusScrollArea.setWidgetResizable(True)
        sizePolicy_status = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy_status.setVerticalStretch(2) # Le da una porción de espacio vertical
        self.statusScrollArea.setSizePolicy(sizePolicy_status)
        
        # Widget Contenedor dentro del Scroll Area
        self.statusContentWidget = QWidget()
        self.statusContentWidget.setObjectName(u"statusContentWidget")
        self.statusContentWidget.setGeometry(QRect(0, 0, 298, 100)) # Tamaño inicial de ejemplo
        
        self.statusContentLayout = QVBoxLayout(self.statusContentWidget)
        self.statusContentLayout.setObjectName(u"statusContentLayout")
        
        # AÑADIDO: Botones dentro del Scroll Area de Estado
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Botón 1
        self.actionButton1 = QPushButton(self.statusContentWidget)
        self.actionButton1.setObjectName(u"actionButton1")
        self.actionButton1.setSizePolicy(sizePolicy4)
        
        # Botón 2
        self.actionButton2 = QPushButton(self.statusContentWidget)
        self.actionButton2.setObjectName(u"actionButton2")
        self.actionButton2.setSizePolicy(sizePolicy4)

        # Botón 3
        self.actionButton3 = QPushButton(self.statusContentWidget)
        self.actionButton3.setObjectName(u"actionButton3")
        self.actionButton3.setSizePolicy(sizePolicy4)

        #Botón 4
        self.actionButton4 = QPushButton(self.statusContentWidget)
        self.actionButton4.setObjectName(u"actionButton4")
        self.actionButton4.setSizePolicy(sizePolicy4)

        #Botón 5
        self.actionButton5 = QPushButton(self.statusContentWidget)
        self.actionButton5.setObjectName(u"actionButton5")
        self.actionButton5.setSizePolicy(sizePolicy4)

        #Botón 6
        self.actionButton6 = QPushButton(self.statusContentWidget)
        self.actionButton6.setObjectName(u"actionButton6")
        self.actionButton6.setSizePolicy(sizePolicy4)
        
        # Es necesario establecer el Widget Contenedor antes de agregar el layout al ScrollArea
        self.statusScrollArea.setWidget(self.statusContentWidget)

        self.verticalLayout_3.addWidget(self.statusScrollArea)
        
        # Etiqueta de Título para las Reglas de Expansión
        self.rulesTitle = QLabel(self.rightColumnWidget)
        self.rulesTitle.setObjectName(u"rulesTitle")
        self.verticalLayout_3.addWidget(self.rulesTitle)

        # Área de Desplazamiento (QScrollArea) para contener los botones de las reglas
        self.rulesScrollArea = QScrollArea(self.rightColumnWidget)
        self.rulesScrollArea.setObjectName(u"rulesScrollArea")
        self.rulesScrollArea.setWidgetResizable(True)
        sizePolicy_rules = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy_rules.setVerticalStretch(1) # Le da el doble de espacio vertical que el de estado
        self.rulesScrollArea.setSizePolicy(sizePolicy_rules)
        
        # Widget Contenedor dentro del Scroll Area (donde se añadirán los botones de reglas dinámicamente)
        self.rulesContainerWidget = QWidget()
        self.rulesContainerWidget.setObjectName(u"rulesContainerWidget")
        self.rulesContainerWidget.setGeometry(QRect(0, 0, 298, 350))
        
        self.verticalLayout_4 = QVBoxLayout(self.rulesContainerWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.rulesDisplay = QTextEdit(self.rulesContainerWidget)
        self.rulesDisplay.setReadOnly(True)
        self.verticalLayout_4.addWidget(self.rulesDisplay)

        self.rulesScrollArea.setWidget(self.rulesContainerWidget)

        self.verticalLayout_3.addWidget(self.rulesScrollArea)

        # Botón para mostrar el Árbol de Derivación
        self.showTreeButton = QPushButton(self.rightColumnWidget)
        self.showTreeButton.setObjectName(u"showTreeButton")
        self.showTreeButton.setSizePolicy(sizePolicy4) # sizePolicy4 es Expanding, Fixed
        self.verticalLayout_3.addWidget(self.showTreeButton)

        self.horizontalLayout.addWidget(self.rightColumnWidget)

        # Conecta las señales y slots automáticamente por nombre
        self.retranslateUi(GIC_Module)
        
        self.horizontalLayout.addWidget(self.rightColumnWidget)

        # Conecta las señales y slots automáticamente por nombre
        self.retranslateUi(GIC_Module)
        QMetaObject.connectSlotsByName(GIC_Module)
    # Fin de setupUi

    # ======================================================================
    # 4. TRADUCCIÓN/TEXTOS DE LA INTERFAZ (SOLUCIÓN NATIVA CON QPainter)
    # ======================================================================
    def retranslateUi(self, GIC_Module):
        """
        Establece los textos (ahora iconos/imágenes para las reglas) visibles 
        para todos los widgets, usando QPainter nativo para dibujar los símbolos.
        """
        # --- FUNCIÓN AUXILIAR PARA CREAR ICONOS DE REGLAS NATIVA ---
        ICON_HEIGHT = 40
        SYMBOL_SIZE = 30 # Tamaño de las imágenes S, a, b
        ARROW_WIDTH = 30 # Espacio para ' → '
        FONT_SIZE = 18

        # Mapeo de Símbolos a Rutas de Archivo
        SYMBOL_PATHS = {
            "S": "Modules/assets/S_big.png",
            "a": "Modules/assets/a_blue.png",
            "b": "Modules/assets/b_red.png",
        }
        
        # Cargamos los QPixmap una sola vez para eficiencia
        pixmaps = {
            symbol: QPixmap(path) 
            for symbol, path in SYMBOL_PATHS.items()
        }

        def create_rule_icon_native(rule_string, min_width=200):
            """
            Dibuja la secuencia de símbolos e imágenes en un solo QPixmap.
            """
            
            current_x = 10 # Posición inicial para el dibujo
            elements = rule_string.split(' ') # Dividir la regla por espacios (ej. ['S', '→', 'a', 'S', 'b'])

            # Calcular un ancho más preciso o usar el mínimo
            content_width = 0
            for element in elements:
                if element in pixmaps:
                    content_width += SYMBOL_SIZE
                elif element == '→':
                    content_width += ARROW_WIDTH
                elif element == '\u03B5': # Épsilon
                    content_width += ARROW_WIDTH
                elif element: # Otros caracteres como 'ab' en "S→ab"
                    # Asumimos un ancho fijo para el texto no dividido
                    content_width += ARROW_WIDTH * (len(element) // 2)

            # Usamos el máximo entre el contenido real + padding y un ancho fijo
            ICON_WIDTH = max(min_width, content_width + 20) 
            
            pixmap = QPixmap(ICON_WIDTH, ICON_HEIGHT)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Configuramos la fuente para los símbolos de texto (flecha, épsilon)
            font = QFont("Arial", FONT_SIZE, QFont.Bold)
            painter.setFont(font)
            
            # Centro el dibujo si el contenido es menor que el ICON_WIDTH
            start_offset = (ICON_WIDTH - content_width) // 2
            current_x = start_offset
            
            # Dibujar cada elemento
            for element in elements:
                if not element: continue
                
                # 1. Dibujar Imagen (S, a, b)
                if element in pixmaps:
                    # Dibujar la imagen centrada verticalmente
                    y_pos = (ICON_HEIGHT - SYMBOL_SIZE) // 2
                    painter.drawPixmap(current_x, y_pos, SYMBOL_SIZE, SYMBOL_SIZE, pixmaps[element])
                    current_x += SYMBOL_SIZE
                    
                # 2. Dibujar Flecha (→)
                elif element == '→':
                    text_rect = QRect(current_x, 0, ARROW_WIDTH, ICON_HEIGHT)
                    painter.drawText(text_rect, Qt.AlignCenter, "→")
                    current_x += ARROW_WIDTH
                
                # 3. Dibujar Épsilon (ε)
                elif element == '\u03B5':
                    # Usamos una fuente más grande para el épsilon
                    epsilon_font = QFont("Arial", 20, QFont.Bold)
                    painter.setFont(epsilon_font)
                    text_rect = QRect(current_x, 0, ARROW_WIDTH, ICON_HEIGHT)
                    painter.drawText(text_rect, Qt.AlignCenter, "\u03B5")
                    painter.setFont(font) # Volvemos a la fuente original
                    current_x += ARROW_WIDTH
                    
                # 4. Dibujar Símbolos Terminales Agrupados (ej. 'ab' en S → ab)
                else: 
                    # Manejar casos como 'ab' sin espacios (si hubieran en alguna regla)
                    # Esto solo funciona si los símbolos se unen, si se desea el dibujo, hay que separarlos.
                    # En este caso, asumimos que 'ab' se dibujaría como 'a' y 'b' separados:
                    
                    # Dibujar 'a'
                    y_pos = (ICON_HEIGHT - SYMBOL_SIZE) // 2
                    painter.drawPixmap(current_x, y_pos, SYMBOL_SIZE, SYMBOL_SIZE, pixmaps['a'])
                    current_x += SYMBOL_SIZE
                    
                    # Dibujar 'b'
                    y_pos = (ICON_HEIGHT - SYMBOL_SIZE) // 2
                    painter.drawPixmap(current_x, y_pos, SYMBOL_SIZE, SYMBOL_SIZE, pixmaps['b'])
                    current_x += SYMBOL_SIZE


            painter.end()
            return QIcon(pixmap)

        # ----------------------------------------------------------------------
        
        # Títulos y Etiquetas de la columna izquierda
        GIC_Module.setWindowTitle(QCoreApplication.translate("GIC_Module", u"Módulo de Muñecas Rusas (GIC)", None))
        self.theoryTitle.setText(QCoreApplication.translate("GIC_Module", u"Gramáticas Independientes de Contexto (GIC)", None))
        self.targetWordLabel.setText(QCoreApplication.translate("GIC_Module", u"Meta a Generar: aaabbb", None))
        self.backToMenuButton.setText(QCoreApplication.translate("GIC_Module", u"← Menú Principal", None))
        
        # Títulos y Propiedades de la columna central
        self.derivationTitle.setText(QCoreApplication.translate("GIC_Module", u"Árbol de Derivación (Forma Sentencial)", None))
        self.visualTitle.setText(QCoreApplication.translate("GIC_Module", u"Visualización (Muñecas Rusas)", None))
        self.resetButton.setText(QCoreApplication.translate("GIC_Module", u"🔄 Empezar de Nuevo", None))
        
        # Títulos de la columna derecha
        self.statusTitle.setText(QCoreApplication.translate("GIC_Module", u"🪆 Elige la Regla para Abrir la Muñeca", None))
        self.rulesTitle.setText(QCoreApplication.translate("GIC_Module", u"📝 Pasos que has dado", None))
        self.showTreeButton.setText(QCoreApplication.translate("GIC_Module", u"🌳 Ver Árbol Mágico", None))

        # --- REGLAS: Se establecen los textos reales (para la lógica) y se crean los iconos ---
        
        # Regla 1 (Paso 1): S → a S b
        rule1_text = QCoreApplication.translate("GIC_Module", u"S → a S b", None)
        self.actionButton1.setText(rule1_text) 
        
        # Regla 2 (Paso 2): S → a S b (Corregido)
        rule2_text = QCoreApplication.translate("GIC_Module", u"S → a S b", None) 
        self.actionButton2.setText(rule2_text) 
        
        # Regla 3 (Paso 3): S → a b (Corregido)
        rule3_text = QCoreApplication.translate("GIC_Module", u"S → a b", None) 
        self.actionButton3.setText(rule3_text) 

        # Regla 4: Mantenemos el texto original
        rule4_text = QCoreApplication.translate("GIC_Module", u"b S b → a S a", None)
        self.actionButton4.setText(rule4_text) 
        
        # Regla 5: S → ε
        rule5_text = QCoreApplication.translate("GIC_Module", u"S → \u03B5", None)
        self.actionButton5.setText(rule5_text)
        
        # Regla 6: Mantenemos el texto original
        rule6_text = QCoreApplication.translate("GIC_Module", u"a b a b → S", None)
        self.actionButton6.setText(rule6_text)

        # 3. Asignar los iconos (utilizando la función nativa)
        
        icon1 = create_rule_icon_native(rule1_text)
        icon3 = create_rule_icon_native(rule3_text)
        icon4 = create_rule_icon_native(rule4_text)
        icon5 = create_rule_icon_native(rule5_text)
        icon6 = create_rule_icon_native(rule6_text)

        self.actionButton1.setIcon(icon1)
        self.actionButton1.setIconSize(icon1.actualSize(QSize(200, 40)))
        
        self.actionButton2.setIcon(icon1) # Usa el mismo icono S → a S b
        self.actionButton2.setIconSize(icon1.actualSize(QSize(200, 40)))
        
        self.actionButton3.setIcon(icon3)
        self.actionButton3.setIconSize(icon3.actualSize(QSize(200, 40)))

        self.actionButton4.setIcon(icon4)
        self.actionButton4.setIconSize(icon4.actualSize(QSize(200, 40)))
        
        self.actionButton5.setIcon(icon5)
        self.actionButton5.setIconSize(icon5.actualSize(QSize(200, 40)))
        
        self.actionButton6.setIcon(icon6)
        self.actionButton6.setIconSize(icon6.actualSize(QSize(200, 40)))
        
        # 4. Ajuste de Estilo: Ocultar el texto del botón.
        # Esto es necesario para que el texto de la regla no se superponga al icono.
        style_suffix = " text-align: left; padding-left: 0px; text-indent: -1000px;" 
        
        self.actionButton1.setStyleSheet(self.actionButton1.styleSheet() + style_suffix)
        self.actionButton2.setStyleSheet(self.actionButton2.styleSheet() + style_suffix)
        self.actionButton3.setStyleSheet(self.actionButton3.styleSheet() + style_suffix)
        self.actionButton4.setStyleSheet(self.actionButton4.styleSheet() + style_suffix)
        self.actionButton5.setStyleSheet(self.actionButton5.styleSheet() + style_suffix)
        self.actionButton6.setStyleSheet(self.actionButton6.styleSheet() + style_suffix)