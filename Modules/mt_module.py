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
            "<h2>🚂 Tren Mágico</h2><br>"
            "<b>Objetivo:</b> ordenar pelotas 🔴 y 🔵.<br><br>"
            "<b>Piezas:</b> 🔴 roja, 🔵 azul, □ vacío, 🟧 cabeza.<br><br>"
            "<b>Cómo usarlo:</b><br>"
            "1. Mira la cinta.<br>"
            "2. Pulsa <b>➡️ Siguiente Paso</b>.<br>"
            "3. Observa cómo el tren compara, cambia y avanza.<br><br>"
            "<b>Idea clave:</b> una Máquina de Turing lee, escribe y se mueve.<br><br>"
            
            "<b>💡 El Tren Mágico puede:</b><br>"
            "1. <b>👀 Ver</b> qué pelota hay en el vagón<br>"
            "2. <b>✏️ Cambiar</b> la pelota por otra<br>"
            "3. <b>🚂 Moverse</b> al siguiente vagón (← o →)<br><br>"
            
            "<b>🎓 ¿Qué es una Máquina de Turing?</b><br>"
            "Este tren es una <b>Máquina de Turing</b>, inventada por Alan Turing.<br>"
            "Es como una computadora muy simple que puede leer, escribir y moverse.<br><br>"
            
            "¡Todas las computadoras del mundo funcionan con este principio!<br><br>"
            
            "<i>Presiona '➡️ Siguiente Paso' para comenzar</i>"
        )
        
        # ======================================================================
        # ESTADO DE LA MÁQUINA DE TURING
        # ======================================================================
        
        # Cinta de 10 posiciones - agregamos un marcador especial al inicio
        self.tape = ['▶', 'R', 'A', 'R', 'A', 'R', 'A', 'R', 'A', '□']
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
                "¡Ya terminó! 🎉",
                "El tren ya ordenó todas las pelotas.<br>"
                "Pulsa <b>↻ Empezar de Nuevo</b> para repetirlo."
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
                "El tren se confundió y no sabe qué hacer.<br>"
                "Pulsa <b>↻ Empezar de Nuevo</b> para reiniciar."
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
                f"<b>El tren ordenó todas las pelotas.</b><br>"
                f"Resultado: {self.format_tape()}<br>"
                f"Pasos: <b>{self.step_count}</b><br>"
                f"Pulsa <b>↻ Empezar de Nuevo</b> para repetirlo."
            )

    def reset_machine(self):
        """Reinicia la Máquina de Turing al estado inicial."""
        self.tape = ['▶', 'R', 'A', 'R', 'A', 'R', 'A', 'R', 'A', '□']
        self.head_position = 1
        self.current_state = 'q0'
        self.step_count = 0
        self.halted = False
        self.update_display()
        self.show_info_message(
            "¡Listo para Empezar! 🚂",
            "El tren volvió al inicio con las pelotas desordenadas.<br>"
            "Pulsa <b>➡️ Siguiente Paso</b> para ver cómo las ordena."
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
            else:
                cell.setProperty("isHead", "false")
            
            # Forzar actualización del estilo
            cell.style().unpolish(cell)
            cell.style().polish(cell)
            cell.update()
        
        # Actualizar labels con información más clara
        self.ui.headPositionLabel.setText(f"🟧 Cabeza: vagón {self.head_position}")
        self.ui.stateLabel.setText(f"🎯 Estado: {self.format_state(self.current_state)}")
        self.ui.stepCounterLabel.setText(f"📊 Pasos: {self.step_count}")
        
        # Deshabilitar botón si terminó
        if self.halted:
            self.ui.nextStepButton.setEnabled(False)
        else:
            self.ui.nextStepButton.setEnabled(True)

    def update_instructions_display(self):
        """Muestra la tabla de instrucciones."""
        text = "<h3>📋 Cómo funciona</h3><br>"
        text += "<b>1. Busca rojas:</b> marca la 🔴 y avanza.<br>"
        text += "<b>2. Busca azules:</b> si encuentra 🔵, la cambia por 🔴 y regresa.<br>"
        text += "<b>3. Vuelve al inicio:</b> coloca la 🔵 donde quedó la marca.<br>"
        text += "<b>4. Limpia:</b> convierte las marcas en 🔴 y termina.<br><br>"
        text += "<b>Resultado:</b> todas las 🔴 juntas y todas las 🔵 juntas."
        
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
