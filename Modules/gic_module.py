from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

# Importa la clase de diseño UI (asumimos que gic_ui.py está en el mismo paquete)
from .gic_ui import GIC_Module as Ui_GIC_Module 

class GICModule(QWidget):
    """
    Clase de controlador que hereda de QWidget y gestiona la lógica
    del Módulo GIC, cargando la interfaz visual de gic_ui.py.
    """
    # 1. Definición de la señal de navegación requerida por MainWindow
    back_requested = Signal() 

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 2. Cargar e Iniciar la interfaz visual
        self.ui = Ui_GIC_Module()
        self.ui.setupUi(self) 
        
        # 3. Conectar el botón de regreso de la UI a la señal del controlador
        self.ui.backToMenuButton.clicked.connect(self.back_requested.emit)
        
        # 4. Configuración inicial de textos y componentes
        self.ui.theoryTextDisplay.setText(
            "<h2>🪆 Muñecas Rusas</h2><br>"
            "<b>Objetivo:</b> formar <b>aaabbb</b>.<br><br>"
            "<b>Piezas:</b> 🪆 S = muñeca que se abre, 🔵 a = azul, 🔴 b = roja.<br><br>"
            "<b>Cómo usarlo:</b><br>"
            "1. Elige una regla.<br>"
            "2. Abre la muñeca paso a paso.<br>"
            "3. Sigue hasta que no quede ninguna 🪆.<br><br>"
            "<b>Idea clave:</b> cada muñeca se abre igual sin importar lo que hay alrededor.<br><br>"
            "<i>Selecciona una regla para comenzar</i>"
        )

        # 5. Adición de Botones de seleccionar muñecas (reglas) al statusContentLayout
        
        self.ui.statusContentLayout.addWidget(self.ui.actionButton2)#2
        self.ui.statusContentLayout.addWidget(self.ui.actionButton4)
        self.ui.statusContentLayout.addWidget(self.ui.actionButton1)#1
        self.ui.statusContentLayout.addWidget(self.ui.actionButton3)#3
        self.ui.statusContentLayout.addWidget(self.ui.actionButton5)
        self.ui.statusContentLayout.addWidget(self.ui.actionButton6)
        
        # 6. Inicialización y adición de la etiqueta de estado
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("padding: 10px; font-size: 10pt; background-color: #ecf0f1; border-radius: 4px;")
        
        self.ui.statusContentLayout.addWidget(self.status_label)
        self.ui.statusContentLayout.addStretch(1) # Relleno vertical

        # ======================================================================
        # PASO 1: INICIALIZAR ESTADO DE DERIVACIÓN
        # ======================================================================
        self.derivation_step = 0  # 0: Espera 1, 1: Espera 1, 2: Espera 3, 3: Finalizado
        self.derivation_history = []
        
        # Inicializar las pantallas de visualización
        self.reset_derivation() 
        
        # ======================================================================
        # PASO 2: CONECTAR BOTONES A LA FUNCIÓN DE MANEJO
        # ======================================================================
        # Usamos lambda para pasar el identificador del botón (1, 2 o 3)
        self.ui.actionButton1.clicked.connect(lambda: self.handle_derivation_step(1))
        self.ui.actionButton2.clicked.connect(lambda: self.handle_derivation_step(2))
        self.ui.actionButton3.clicked.connect(lambda: self.handle_derivation_step(3))
        self.ui.actionButton4.clicked.connect(lambda: self.show_incorrect_derivation_dialog())
        self.ui.actionButton5.clicked.connect(lambda: self.show_incorrect_derivation_dialog())
        self.ui.actionButton6.clicked.connect(lambda: self.show_incorrect_derivation_dialog())
        
        # Conectar el botón de reinicio
        self.ui.resetButton.clicked.connect(self.reset_derivation)

        #Conectar el botón de mostrar árbol
        self.ui.showTreeButton.clicked.connect(self.handle_show_tree)

    def reset_derivation(self):
        """
        Reinicia el estado de la derivación y limpia las pantallas.
        """
        self.derivation_step = 0
        self.derivation_history = []
        self.update_derivation_display()
        self.ui.rulesDisplay.setText("🪆 Selecciona una regla para abrir la primera muñeca.")

    # ======================================================================
    # PASO 4: FUNCIÓN AUXILIAR DE VISUALIZACIÓN
    # ======================================================================
    def update_derivation_display(self):
        """
        Actualiza el QTextEdit de derivación con la secuencia de reglas.
        """
        # Título de la sección
        text = " "
        
        if not self.derivation_history:
            # Texto guía al inicio
            text += "🪆 Pasos:\n\n"
            text += "1. Elige la regla correcta.\n"
            text += "2. Observa qué aparece al abrir la muñeca.\n"
            text += "3. Si aparece otra 🪆, vuelve a abrirla.\n"
            text += "4. Termina cuando formes aaabbb.\n"
        else:
            # Lista de reglas aplicadas
            for i, rule in enumerate(self.derivation_history):
                # Formato: 1. S → a S b
                text += f"{i+1}. {rule}\n"
        
        # Mostrar el texto en el QTextEdit
        self.ui.rulesDisplay.setText(text)
        
    def show_incorrect_derivation_dialog(self):
        """
        Muestra un QMeessageBox con un mensaje de error de derivación.
        """
        msg = QMessageBox(self)
        
        # Aplicamos estilos CSS (QSS) al cuadro de diálogo para fondo blanco
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #000000;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                min-width: 120px;   /* Más ancho */
                max-width: 120px;   /* Controla ancho exacto */
                min-height: 22px;   /* Más bajo */
                padding: 4px 8px;   /* Ajusta relleno (vertical, horizontal) */
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #cfcfcf;
            }
        """)

        
        msg.setIcon(QMessageBox.Icon.Critical) # Usamos ícono de error
        msg.setWindowTitle("¡Error!") 
        msg.setText("Derivación Incorrecta") 
        msg.setInformativeText("La regla seleccionada es incorrecta para esta derivación. Intenta nuevamente.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Muestra la ventana
        msg.exec() 

    def show_dialog_message(self, title, informative_text, icon=QMessageBox.Icon.Information):
        """
        Muestra un QMeessageBox con un mensaje personalizado.
        """
        msg = QMessageBox(self)
        
        # Aplicamos estilos CSS (QSS) al cuadro de diálogo
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #000000;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                min-width: 120px;
                max-width: 120px;
                min-height: 22px;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #cfcfcf;
            }
        """)

        
        msg.setIcon(icon) 
        msg.setWindowTitle(title) 
        msg.setText(title) 
        msg.setInformativeText(informative_text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Muestra la ventana
        msg.exec() 

    # Modificar show_incorrect_derivation_dialog para usar la nueva función
    def show_incorrect_derivation_dialog(self):
        """
        Muestra un QMeessageBox con un mensaje de error de derivación.
        """
        self.show_dialog_message(
            "¡Ups! 🤔",
            "Esa no es la regla correcta para este paso.<br>"
            "Intenta de nuevo y piensa en cómo formar <b>aaabbb</b>.",
            QMessageBox.Icon.Warning
        )
        # El reinicio va después de mostrar el mensaje, en la función de manejo
        self.reset_derivation() # Mueve el reinicio aquí si no estaba.


    # ======================================================================
    # PASO 3: FUNCIÓN CENTRAL DE MANEJO DE PASOS (Slot)
    # ======================================================================
    def handle_derivation_step(self, button_id):
        """
        Maneja la lógica de la secuencia de derivación (1 -> 1 -> 3).
        """
        # Si ya está terminado, no hacer nada (hasta que se reinicie)
        if self.derivation_step == 3:
            self.status_label.setText("¡Derivación completa!")
            return

        # Obtener el texto de la regla presionada para mostrarlo en el historial
        if button_id == 1:
            rule_text = self.ui.actionButton1.text()
        elif button_id == 2:
            rule_text = self.ui.actionButton2.text()
        elif button_id == 3:
            rule_text = self.ui.actionButton3.text()
        else:
            # Caso inesperado, aunque la conexión solo envía 1, 2 o 3
            return

        is_correct = False
        next_step_prompt = ""
        
        # --- LÓGICA DE LA SECUENCIA 1 - 1 - 3 ---
        
        if self.derivation_step == 0 and button_id == 1:
            # Paso 1/3: Espera el Botón 1 (S → a S b)
            self.derivation_step = 1
            is_correct = True
            
        elif self.derivation_step == 1 and button_id == 2:
            # Paso 2/3: Espera el Botón 1 (S → a S b)
            self.derivation_step = 2
            is_correct = True

        elif self.derivation_step == 2 and button_id == 3:
            # Paso 3/3: Espera el Botón 3 (S → ab)
            self.derivation_step = 3
            is_correct = True
            next_step_prompt = "\n✨ ¡Felicidades! ✨\n\nAbriste todas las muñecas correctamente.\nFormaste el patrón: aaabbb (🔵🔵🔵🔴🔴🔴)\n\n¡Ahora puedes ver el árbol mágico!"
            
        # --- Manejo de la Acción Correcta / Incorrecta ---
        
        if is_correct:
            self.derivation_history.append(rule_text)
            self.update_derivation_display()
            self.ui.rulesDisplay.append(next_step_prompt)
        else:
            # Cualquier otra acción es incorrecta (incluyendo botón 2 en cualquier momento)
            self.show_incorrect_derivation_dialog()
            self.reset_derivation() # Reinicia el juego después del error.

    # ======================================================================
    # PASO 5: FUNCIÓN DE MANEJO DEL BOTÓN VER ÁRBOL
    # ======================================================================
    def handle_show_tree(self):
        """
        Muestra el árbol de derivación solo si la derivación está terminada (derivation_step == 3).
        """
        # Comprobar si la derivación está completa
        if self.derivation_step < 3:
            # Derivación incompleta: Muestra la ventana emergente de error
            self.show_dialog_message(
                "¡Todavía no! ⏳", 
                "Primero termina de abrir todas las muñecas 🪆.<br>"
                "Cuando formes <b>aaabbb</b>, podrás ver el árbol mágico.",
                QMessageBox.Icon.Information
            )
        else:
            # Derivación completa: Muestra el mensaje de debug
            debug_message = "DEBUG: Árbol de Derivación Visualizado (Derivación Completa)"
            
            
            # Muñecas Rusas
            image_path = "Modules/assets/arbol.png"
            
            # a) Cargar la imagen
            pixmap = QPixmap(image_path)
            
            if pixmap.isNull():
                # Si la imagen no se carga, mostrar un mensaje de error en el QLabel
                self.ui.dollsVisualImage.setText(f"ERROR: No se pudo cargar la imagen:\n{image_path}")
                return
            
            # b) Obtener el tamaño del widget (el tamaño incluye el padding/margen de 5px)
            target_size = self.ui.dollsVisualImage.size()
            
            # c) Escalar la imagen para ajustarla al tamaño del widget (KeepAspectRatio asegura que la imagen no se distorsione)
            scaled_pixmap = pixmap.scaled(
                target_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation # Para un escalado de mejor calidad
            )
            
            # d) Establecer la imagen escalada en el QLabel
            self.ui.dollsVisualImage.setPixmap(scaled_pixmap)
            
            # Forma sentencial
            self.ui.derivationTextDisplay.setText(
                f"Visualización del Árbol de Derivación:\n\n"
                f"      S\n"
                f"  /   |    \\ \n"
                f"a     S     b \n"
                f"   /  |  \\ \n"
                f"  a   S   b \n"
                f"    /   \\ \n"
                f"   a     b \n"
                
            )