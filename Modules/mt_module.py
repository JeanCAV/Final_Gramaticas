from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal

# Importa la clase de diseño UI
from .mt_ui import MT_Module as Ui_MT_Module

class MTModule(QWidget):
    """
    Clase controlador que gestiona la lógica del Módulo MT
    (Máquina de Turing - El Tren Mágico que Ordena Juguetes).
    """
    # Señal de navegación requerida por MainWindow
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Cargar e iniciar la interfaz visual
        self.ui = Ui_MT_Module()
        self.ui.setupUi(self)
        
        # Conectar el botón de regreso
        self.ui.backToMenuButton.clicked.connect(self.back_requested.emit)
        
        # ======================================================================
        # CONFIGURACIÓN INICIAL
        # ======================================================================
        
        # Establecer el texto de teoría
        self.ui.theoryTextDisplay.setText(
            "<h2>🚂 El Tren Mágico que Ordena Juguetes</h2><br>"
            
            "<b>¿De qué trata este juego?</b><br>"
            "Imagina un tren mágico con 10 vagones. En cada vagón hay "
            "juguetes de colores que están desordenados. ¡El tren mágico "
            "los va a ordenar!<br><br>"
            
            "<b>🎨 Los Juguetes:</b><br>"
            "• <span style='font-size:20pt'>🔴</span> = Pelota Roja<br>"
            "• <span style='font-size:20pt'>🔵</span> = Pelota Azul<br>"
            "• <span style='font-size:20pt'>□</span> = Vagón vacío<br><br>"
            
            "<b>🎮 ¿Cómo jugar?</b><br><br>"
            
            "<b>Paso 1:</b> Mira los vagones del tren en el centro<br>"
            "Verás las pelotas desordenadas: 🔴🔵🔴🔵<br><br>"
            
            "<b>Paso 2:</b> Observa la casilla naranja 🟧<br>"
            "Esa es la cabeza del tren. Ahí está mirando el tren ahora mismo<br><br>"
            
            "<b>Paso 3:</b> Presiona el botón verde '➡️ Siguiente Paso'<br>"
            "¡El tren moverá las pelotas para ordenarlas!<br><br>"
            
            "<b>Paso 4:</b> Sigue presionando 'Siguiente Paso'<br>"
            "Observa cómo el tren cambia las pelotas de lugar<br><br>"
            
            "<b>Paso 5:</b> Al final verás todas las rojas juntas<br>"
            "Y todas las azules juntas: 🔴🔴🔵🔵<br><br>"
            
            "<b>💡 ¿Qué hace el Tren Mágico?</b><br>"
            "El tren tiene una cabeza inteligente que puede:<br>"
            "1. <b>👀 Ver</b> qué pelota hay en el vagón<br>"
            "2. <b>✏️ Cambiar</b> la pelota por otra<br>"
            "3. <b>🚂 Moverse</b> al siguiente vagón (← o →)<br><br>"
            
            "El tren sigue reglas especiales para saber qué hacer:<br>"
            "• Si veo pelota roja 🔴 → haz esto<br>"
            "• Si veo pelota azul 🔵 → haz aquello<br><br>"
            
            "<b>🎯 Tu Meta:</b><br>"
            "Ver cómo el tren ordena las pelotas paso a paso<br>"
            "De: 🔴🔵🔴🔵 → A: 🔴🔴🔵🔵<br><br>"
            
            "<b>🎓 ¿Qué es una Máquina de Turing?</b><br>"
            "Este tren mágico es una <b>Máquina de Turing</b>, inventada por "
            "un señor muy inteligente llamado Alan Turing hace muchos años.<br><br>"
            
            "Una Máquina de Turing es como una computadora súper simple que puede:<br>"
            "• Leer y escribir cosas en una cinta (nuestros vagones 🚃)<br>"
            "• Moverse por la cinta para ver cada parte<br>"
            "• Seguir reglas para resolver problemas<br><br>"
            
            "¡Todas las computadoras del mundo (tu celular, tablets, videojuegos) "
            "funcionan con este mismo principio que inventó Alan Turing!<br><br>"
            
            "<b>✨ Dato curioso:</b><br>"
            "Alan Turing usó esta idea para ayudar en la Segunda Guerra Mundial "
            "y después ayudó a crear las primeras computadoras. ¡Es un héroe de la ciencia!<br><br>"
            
            "<i>¡Presiona el botón verde '➡️ Siguiente Paso' para ver la magia!</i>"
        )
        
        # ======================================================================
        # ESTADO DE LA MÁQUINA DE TURING
        # ======================================================================
        
        # Cinta de 10 posiciones - agregamos un marcador especial al inicio
        self.tape = ['▶', 'R', 'A', 'R', 'A', '□', '□', '□', '□', '□']
        self.head_position = 1  # Empezamos en posición 1 (después del marcador)
        self.current_state = 'q0'
        self.step_count = 0
        self.halted = False
        
        # Símbolos visuales
        self.SYMBOL_RED = '🔴'
        self.SYMBOL_BLUE = '🔵'
        self.SYMBOL_BLANK = '□'
        self.SYMBOL_START = '▶'  # Marcador de inicio
        
        # ======================================================================
        # TABLA DE TRANSICIONES
        # ======================================================================
        # Formato: (estado_actual, símbolo_leído) -> (nuevo_estado, símbolo_escribir, dirección)
        # Dirección: 'R' = Right (derecha), 'L' = Left (izquierda), 'S' = Stay (quedarse)
        
        self.transitions = {
            # Estado inicial: buscar primer R
            ('q0', 'R'): ('q1', 'X', 'R'),  # Marcar R como procesado
            ('q0', 'A'): ('q0', 'A', 'R'),  # Saltar A
            ('q0', '□'): ('q3', '□', 'L'),  # Si encontramos vacío, empezar limpieza
            
            # q1: Buscar A para intercambiar
            ('q1', 'R'): ('q1', 'R', 'R'),  # Saltar otros R
            ('q1', 'A'): ('q2', 'R', 'L'),  # Encontró A, intercambiar
            ('q1', '□'): ('q3', '□', 'L'),  # No hay más A, empezar limpieza
            
            # q2: Regresar a la X
            ('q2', 'R'): ('q2', 'R', 'L'),
            ('q2', 'A'): ('q2', 'A', 'L'),
            ('q2', 'X'): ('q0', 'A', 'R'),  # Completar intercambio y continuar
            
            # q3: Limpiar marcas X (convertir X a R)
            ('q3', 'R'): ('q3', 'R', 'L'),
            ('q3', 'A'): ('q3', 'A', 'L'),
            ('q3', 'X'): ('q3', 'R', 'L'),
            ('q3', '□'): ('q3', '□', 'L'),  # Seguir limpiando
            ('q3', '▶'): ('qf', '▶', 'S'),  # Al llegar al inicio, terminar
        }
        
        # ======================================================================
        # MOSTRAR INSTRUCCIONES
        # ======================================================================
        self.update_instructions_display()
        
        # ======================================================================
        # CONECTAR SEÑALES
        # ======================================================================
        self.ui.nextStepButton.clicked.connect(self.execute_step)
        self.ui.resetButton.clicked.connect(self.reset_machine)
        
        # Actualizar visualización inicial
        self.update_display()

    # ==========================================================================
    # LÓGICA DE LA MÁQUINA DE TURING
    # ==========================================================================
    
    def execute_step(self):
        """Ejecuta un paso de la Máquina de Turing."""
        if self.halted:
            self.show_info_message(
                "¡Ya Terminamos! 🎉",
                "El tren ya ordenó todas las pelotas.<br><br>"
                "¿Quieres verlo otra vez?<br>"
                "Presiona el botón rojo '↻ Empezar de Nuevo'"
            )
            return
        
        # Leer símbolo actual
        current_symbol = self.tape[self.head_position]
        
        # Buscar transición
        key = (self.current_state, current_symbol)
        
        if key not in self.transitions:
            # No hay transición definida, la máquina se detiene
            self.halted = True
            self.show_warning_message(
                "¡Ups! 😕",
                f"El tren se confundió y no sabe qué hacer.<br><br>"
                f"Esto no debería pasar. Intenta presionar<br>"
                f"el botón '↻ Empezar de Nuevo' para reiniciar."
            )
            return
        
        # Obtener transición
        new_state, write_symbol, direction = self.transitions[key]
        
        # Ejecutar acciones
        old_symbol = current_symbol
        self.tape[self.head_position] = write_symbol
        
        # Mover cabezal
        old_position = self.head_position
        if direction == 'R' and self.head_position < 9:
            self.head_position += 1
        elif direction == 'L' and self.head_position > 0:
            self.head_position -= 1
        # Si direction == 'S', no se mueve
        
        # Actualizar estado
        self.current_state = new_state
        self.step_count += 1
        
        # Verificar si llegó al estado final
        if new_state == 'qf':
            self.halted = True
        
        # Actualizar visualización
        self.update_display()
        
        # Mostrar mensaje si terminó
        if self.halted:
            self.show_success_message(
                "¡Felicidades! 🎉🎊",
                f"<b>¡El tren ordenó todas las pelotas perfectamente!</b><br><br>"
                f"Resultado final: {self.format_tape()}<br><br>"
                f"Lo hizo en <b>{self.step_count} pasos</b><br><br>"
                f"Todas las rojas 🔴🔴 quedaron juntas<br>"
                f"Y todas las azules 🔵🔵 quedaron juntas<br><br>"
                f"<i>¿Quieres verlo otra vez? Presiona '↻ Empezar de Nuevo'</i>"
            )

    def reset_machine(self):
        """Reinicia la Máquina de Turing al estado inicial."""
        self.tape = ['▶', 'R', 'A', 'R', 'A', '□', '□', '□', '□', '□']
        self.head_position = 1
        self.current_state = 'q0'
        self.step_count = 0
        self.halted = False
        self.update_display()
        self.show_info_message(
            "¡Listo para Empezar! 🚂",
            "El tren volvió al inicio con las pelotas desordenadas.<br><br>"
            "Las pelotas están así: 🔴🔵🔴🔵<br><br>"
            "Presiona el botón verde '➡️ Siguiente Paso'<br>"
            "para ver cómo el tren las ordena"
        )

    # ==========================================================================
    # ACTUALIZACIÓN DE INTERFAZ
    # ==========================================================================
    
    def update_display(self):
        """Actualiza toda la visualización."""
        # Actualizar casillas de la cinta
        for i, cell in enumerate(self.ui.tapeCells):
            symbol = self.tape[i]
            cell.setText(self.format_symbol(symbol))
            
            # Marcar cabezal
            if i == self.head_position:
                cell.setProperty("isHead", "true")
                cell.setStyleSheet(cell.styleSheet())  # Forzar actualización
            else:
                cell.setProperty("isHead", "false")
                cell.setStyleSheet(cell.styleSheet())
        
        # Actualizar labels con información más clara
        self.ui.headPositionLabel.setText(f"🟧 La cabeza del tren está mirando el vagón número: {self.head_position + 1}")
        self.ui.stateLabel.setText(f"🎯 Qué está haciendo: {self.format_state(self.current_state)}")
        self.ui.stepCounterLabel.setText(f"📊 Pasos completados: {self.step_count}")
        
        # Deshabilitar botón si terminó
        if self.halted:
            self.ui.nextStepButton.setEnabled(False)
        else:
            self.ui.nextStepButton.setEnabled(True)

    def update_instructions_display(self):
        """Muestra la tabla de instrucciones."""
        text = "<h3>📋 ¿Cómo Ordena el Tren las Pelotas?</h3><br>"
        text += "<b>El tren sigue estas reglas mágicas:</b><br><br>"
        
        text += "<b>🔍 Buscando Rojas:</b><br>"
        text += "El tren busca pelotas rojas 🔴 para ponerlas al inicio<br>"
        text += "• Si encuentra 🔴 → La marca con ✖️ y avanza →<br>"
        text += "• Si encuentra 🔵 → Solo avanza →<br>"
        text += "• Si encuentra □ → Ya terminó, ¡felicidades!<br><br>"
        
        text += "<b>🔄 Buscando Azul para Intercambiar:</b><br>"
        text += "Después de marcar una roja, busca una azul<br>"
        text += "• Si encuentra 🔴 → Sigue buscando →<br>"
        text += "• Si encuentra 🔵 → ¡La cambia por 🔴! y regresa ←<br>"
        text += "• Si encuentra □ → Empieza a limpiar las marcas ←<br><br>"
        
        text += "<b>⬅️ Regresando a la Marca:</b><br>"
        text += "El tren regresa para completar el intercambio<br>"
        text += "• Sigue regresando ← hasta encontrar la marca ✖️<br>"
        text += "• Cuando encuentra ✖️ → Pone la 🔵 ahí y continúa →<br><br>"
        
        text += "<b>🧹 Limpiando Marcas:</b><br>"
        text += "Al final, cambia todas las ✖️ por 🔴<br>"
        text += "• Cada ✖️ se convierte en 🔴<br>"
        text += "• Cuando llega a □ → ¡Todo listo!<br><br>"
        
        text += "<b>🎯 Resultado Final:</b><br>"
        text += "Todas las pelotas rojas 🔴🔴 quedan juntas al inicio<br>"
        text += "Y todas las azules 🔵🔵 quedan juntas al final<br><br>"
        
        text += "<b>💡 Observa:</b> La casilla naranja 🟧 te muestra dónde está "
        text += "mirando el tren en cada momento."
        
        self.ui.instructionsDisplay.setText(text)

    def format_symbol(self, symbol):
        """Formatea un símbolo para visualización."""
        if symbol == 'R':
            return self.SYMBOL_RED
        elif symbol == 'A':
            return self.SYMBOL_BLUE
        elif symbol == 'X':
            return '✖️'
        elif symbol == '▶':
            return '▶'  # Marcador de inicio
        else:
            return self.SYMBOL_BLANK

    def format_tape(self):
        """Formatea la cinta completa para visualización."""
        return ' '.join([self.format_symbol(s) for s in self.tape])

    def format_state(self, state):
        """Formatea el nombre del estado."""
        state_names = {
            'q0': '🔍 Buscando Roja',
            'q1': '🔄 Buscando Azul',
            'q2': '⬅️ Regresando',
            'q3': '🧹 Limpiando',
            'qf': '✅ ¡Terminado!'
        }
        return state_names.get(state, state)

    # ==========================================================================
    # MENSAJES DE DIÁLOGO
    # ==========================================================================
    
    def show_info_message(self, title, message):
        """Muestra un mensaje informativo."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
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
                min-height: 22px;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #cfcfcf;
            }
        """)
        msg.exec()

    def show_warning_message(self, title, message):
        """Muestra un mensaje de advertencia."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
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
                min-height: 22px;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #cfcfcf;
            }
        """)
        msg.exec()

    def show_success_message(self, title, message):
        """Muestra un mensaje de éxito."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #d4edda;
            }
            QMessageBox QLabel {
                color: #155724;
                font-size: 14px;
                font-weight: bold;
            }
            QMessageBox QPushButton {
                background-color: #28a745;
                color: #ffffff;
                min-width: 120px;
                min-height: 22px;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #218838;
            }
        """)
        msg.exec()
