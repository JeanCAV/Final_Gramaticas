from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal

# Importa la clase de diseño UI
from .gdc_ui import GDC_Module as Ui_GDC_Module

class GDCModule(QWidget):
    """
    Clase controlador que gestiona la lógica del Módulo GDC
    (Gramáticas Dependientes de Contexto - Jardín Mágico).
    """
    # Señal de navegación requerida por MainWindow
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Cargar e iniciar la interfaz visual
        self.ui = Ui_GDC_Module()
        self.ui.setupUi(self)
        
        # Conectar el botón de regreso
        self.ui.backToMenuButton.clicked.connect(self.back_requested.emit)
        
        # ======================================================================
        # CONFIGURACIÓN INICIAL
        # ======================================================================
        
        # Establecer el texto de teoría
        self.ui.theoryTextDisplay.setText(
            "<h2>🌱 El Jardín Mágico que Crece Junto</h2><br>"
            
            "<b>🌱 Las Plantas:</b><br>"
            "• <span style='font-size:20pt'>🌱</span> = Semilla mágica (S)<br>"
            "• <span style='font-size:20pt'>🌿</span> = Planta verde (a)<br>"
            "• <span style='font-size:20pt'>🌸</span> = Flor rosada (b)<br><br>"
            
            "<b>🎮 ¿Cómo jugar?</b><br>"
            "1. Elige un nivel (Nivel 1 o 2)<br>"
            "2. Mira tu semilla 🌱 en el centro<br>"
            "3. Presiona '⏩ Siguiente Fase' para verla crecer<br>"
            "4. Sigue hasta tener el patrón completo<br>"
            "5. Presiona '✓ Validar' para verificar<br><br>"
            
            "<b>🎯 Meta:</b> Formar 🌿🌿🌿🌸🌸🌸 (aaabbb)<br><br>"
            
            "<b>💡 La Magia del Jardín:</b><br>"
            "En este jardín, las plantas miran a sus vecinas antes de crecer.<br>"
            "¡Necesitan compañía para transformarse!<br><br>"
            
            "<b>🎓 ¿Por qué es Dependiente de Contexto?</b><br>"
            "Las plantas miran quién está a su lado (su contexto) antes de crecer.<br><br>"
            
            "<b>Nivel 1:</b> 🌸🌱🌸 → 🌸🌿🌸 (necesita estar entre flores)<br>"
            "<b>Nivel 2:</b> 🌿🌱 → 🌿🌿🌸 (necesita una planta verde al lado)<br><br>"
            
            "<i>¡Elige un nivel para empezar!</i>"
        )
        
        # Estado del módulo
        self.current_garden = ""
        self.current_level = None
        self.transformation_history = []
        self.phase_count = 0
        
        # Símbolos para representar las plantas
        self.SYMBOL_A = "🌿"  # Planta tipo A (verde)
        self.SYMBOL_B = "🌸"  # Planta tipo B (rosa)
        self.SYMBOL_S = "🌱"  # Semilla inicial
        
        # ======================================================================
        # DEFINICIÓN DE NIVELES Y REGLAS
        # ======================================================================
        
        # NIVEL 1: Patrón simple con dependencia de contexto básica
        self.level1_rules = [
            ("bSb", "bab"),    # Contexto: S entre dos b se convierte en 'a'
            ("S", "bSb"),      # S se expande a bSb
        ]
        self.level1_initial = "S"
        self.level1_target = "bbabbb"
        
        # NIVEL 2: Patrón a^n b^n con dependencia de contexto más compleja
        self.level2_rules = [
            ("aS", "aSb"),    # Contexto: si hay 'a' antes de S, añade 'b' después
            ("S", "ab"),      # Caso base
        ]
        self.level2_initial = "aS"
        self.level2_target = "aaabbb"
        
        # ======================================================================
        # CONECTAR SEÑALES
        # ======================================================================
        
        self.ui.level1Button.clicked.connect(lambda: self.load_level(1))
        self.ui.level2Button.clicked.connect(lambda: self.load_level(2))
        self.ui.nextPhaseButton.clicked.connect(self.apply_next_phase)
        self.ui.validateButton.clicked.connect(self.validate_balance)
        self.ui.resetButton.clicked.connect(self.reset_garden)
        
        # Deshabilitar botones hasta que se seleccione un nivel
        self.ui.nextPhaseButton.setEnabled(False)
        self.ui.validateButton.setEnabled(False)
        self.ui.resetButton.setEnabled(False)
        
        # Inicializar displays
        self.update_display()

    # ==========================================================================
    # GESTIÓN DE NIVELES
    # ==========================================================================
    
    def load_level(self, level):
        """Carga el nivel seleccionado y reinicia el jardín."""
        self.current_level = level
        self.phase_count = 0
        self.transformation_history = []
        
        if level == 1:
            self.current_garden = self.level1_initial
            self.current_rules = self.level1_rules
            self.target_pattern = self.level1_target
            self.ui.targetPatternLabel.setText(f"🎯 Meta: {self.format_pattern(self.target_pattern)}")
            self.ui.rulesDisplay.setText(
                "<h3>✨ Reglas Mágicas del Nivel 1:</h3><br>"
                
                "<b>🔮 Regla Especial (con Vecinas):</b><br>"
                "Si una semilla 🌱 está <b>rodeada de dos flores rosadas</b> 🌸🌱🌸, "
                "entonces algo mágico pasa:<br>"
                "• Las flores 🌸 de los lados se quedan<br>"
                "• La semilla 🌱 se convierte en una planta verde 🌿<br><br>"
                
                "Ejemplo: 🌸🌱🌸 se convierte en 🌸🌿🌸<br><br>"
                
                "<b>Regla Normal:</b><br>"
                "Si la semilla 🌱 está sola (sin vecinas), se expande a: 🌸🌱🌸<br><br>"
                
                "<b>🎓 ¿Por qué es Dependiente de Contexto?</b><br>"
                "¡Fíjate bien! La semilla 🌱 cambia de manera diferente dependiendo "
                "de si tiene vecinas flores 🌸 o no.<br><br>"
                
                "• <b>Con contexto</b> (🌸🌱🌸): Se convierte en 🌿 (planta verde)<br>"
                "• <b>Sin contexto</b> (🌱 sola): Se expande a 🌸🌱🌸<br><br>"
                
                "¡La transformación <b>DEPENDE</b> de lo que está alrededor! "
                "Por eso se llama <b>Dependiente de Contexto</b>.<br><br>"
                
                "<b>📝 Consejo:</b><br>"
                "Observa bien cómo la semilla 'mira' a sus vecinas antes de crecer."
            )
        elif level == 2:
            self.current_garden = self.level2_initial
            self.current_rules = self.level2_rules
            self.target_pattern = self.level2_target
            self.ui.targetPatternLabel.setText(f"🎯 Meta: {self.format_pattern(self.target_pattern)}")
            self.ui.rulesDisplay.setText(
                "<h3>✨ Reglas Mágicas del Nivel 2:</h3><br>"
                
                "<b>🔮 Regla Especial (con Amigos):</b><br>"
                "Si ya tienes una planta verde 🌿 y al lado hay una semilla 🌱, "
                "entonces pasa algo mágico:<br>"
                "• La planta verde 🌿 se queda<br>"
                "• La semilla 🌱 también se queda<br>"
                "• Pero ahora aparece una flor rosada 🌸 al final<br><br>"
                
                "Ejemplo: 🌿🌱 se convierte en 🌿🌱🌸<br><br>"
                
                "<b>Regla Normal:</b><br>"
                "Si la semilla 🌱 está sola (sin planta verde al lado), "
                "se convierte simplemente en: 🌿🌸<br><br>"
                
                "<b>🎓 ¿Por qué es Dependiente de Contexto?</b><br>"
                "¡Este es un ejemplo perfecto! La semilla 🌱 se comporta diferente "
                "según tenga o no una planta 🌿 a su izquierda:<br><br>"
                
                "• <b>Con contexto</b> (🌿🌱): Añade 🌸 al final → 🌿🌱🌸<br>"
                "• <b>Sin contexto</b> (🌱 sola): Se convierte en 🌿🌸<br><br>"
                
                "La regla <b>revisa primero</b> si hay una 🌿 al lado antes de aplicarse. "
                "¡Por eso es Dependiente de Contexto!<br><br>"
                
                "<b>📝 Consejo:</b><br>"
                "Este nivel es especial porque muestra cómo la posición de las vecinas "
                "cambia completamente lo que pasa. ¡Observa bien!"
            )
        
        # Habilitar botones
        self.ui.nextPhaseButton.setEnabled(True)
        self.ui.validateButton.setEnabled(True)
        self.ui.resetButton.setEnabled(True)
        
        # Actualizar visualización
        self.update_display()
        self.show_info_message(
            "¡Nivel Listo! 🎮", 
            f"¡Perfecto! Has elegido el Nivel {level}.<br><br>"
            f"Ahora mira el centro de la pantalla y presiona el botón verde "
            f"<b>'⏩ Siguiente Fase'</b> para ver cómo crece tu jardín.<br><br>"
            f"🎯 Tu meta es llegar a: {self.format_pattern(self.target_pattern)}"
        )

    def reset_garden(self):
        """Reinicia el jardín al estado inicial del nivel actual."""
        if self.current_level:
            self.load_level(self.current_level)
        else:
            self.current_garden = ""
            self.transformation_history = []
            self.phase_count = 0
            self.ui.nextPhaseButton.setEnabled(False)
            self.ui.validateButton.setEnabled(False)
            self.ui.resetButton.setEnabled(False)
            self.update_display()

    # ==========================================================================
    # LÓGICA DE TRANSFORMACIONES
    # ==========================================================================
    
    def apply_next_phase(self):
        """Aplica las transformaciones correspondientes según las reglas."""
        if not self.current_level:
            return
        
        previous_garden = self.current_garden
        transformed = False
        
        # Aplicar reglas según el nivel
        if self.current_level == 1:
            # Nivel 1: Dependencia de contexto con bSb
            if "bSb" in self.current_garden:
                # Aplicar bSb → bab (con contexto: S rodeada de 'b')
                self.current_garden = self.current_garden.replace("bSb", "bab", 1)
                self.add_to_history(f"✨ La semilla 🌱 estaba rodeada de flores 🌸, se convirtió en planta 🌿")
                transformed = True
            elif "S" in self.current_garden:
                # Aplicar S → bSb (expandir)
                self.current_garden = self.current_garden.replace("S", "bSb", 1)
                self.add_to_history(f"🌱 La semilla creció: aparecieron flores 🌸 a ambos lados")
                transformed = True
        
        elif self.current_level == 2:
            # Nivel 2: Dependiente de contexto (limitado a 3 fases)
            if self.phase_count < 2:
                # Fases 1 y 2: Aplicar aS → aSb (añadir más 'b')
                if "aS" in self.current_garden:
                    self.current_garden = self.current_garden.replace("aS", "aSb", 1)
                    self.add_to_history(f"✨ La semilla 🌱 tenía una amiga 🌿, entonces apareció 🌸 al final")
                    transformed = True
            else:
                # Fase 3: Terminar con S → ab
                if "S" in self.current_garden:
                    self.current_garden = self.current_garden.replace("S", "ab", 1)
                    self.add_to_history(f"🌱 La semilla se convirtió en 🌿🌸 (terminado)")
                    transformed = True
        
        if transformed:
            self.phase_count += 1
            self.update_display()
            
            # Verificar si ya no hay más transformaciones posibles
            if "S" not in self.current_garden:
                if self.current_garden == self.target_pattern:
                    self.show_success_message(
                        "🎉 ¡Felicidades! 🎉",
                        f"¡Lo lograste! Tu jardín está perfecto:<br><br>"
                        f"<span style='font-size:24pt'>{self.format_pattern(self.current_garden)}</span><br><br>"
                        f"Has conseguido exactamente {self.format_pattern(self.target_pattern)}<br><br>"
                        f"¡Eres un excelente jardinero! 🌟"
                    )
                else:
                    self.show_info_message(
                        "Jardín Completo 🌱",
                        f"Tu jardín terminó de crecer.<br><br>"
                        f"<b>Tu jardín:</b> {self.format_pattern(self.current_garden)}<br>"
                        f"<b>Meta:</b> {self.format_pattern(self.target_pattern)}<br><br>"
                        f"¿Quieres intentarlo de nuevo?"
                    )
        else:
            self.show_warning_message(
                "Jardín Completo 🏁",
                "Tu jardín ya no puede crecer más. Ya no quedan semillas 🌱 para transformar.<br><br>"
                "Presiona '↻ Reiniciar' si quieres empezar de nuevo."
            )

    def add_to_history(self, message):
        """Añade una entrada al historial de transformaciones."""
        self.transformation_history.append(f"Fase {self.phase_count + 1}: {message}")

    # ==========================================================================
    # VALIDACIÓN
    # ==========================================================================
    
    def validate_balance(self):
        """Valida si el patrón actual está balanceado."""
        # Contar símbolos 'a' y 'b'
        count_a = self.current_garden.count('a')
        count_b = self.current_garden.count('b')
        has_s = 'S' in self.current_garden
        
        message = f"<h3>📊 Análisis de tu Jardín:</h3><br>"
        message += f"<span style='font-size:16pt'>{self.format_pattern(self.current_garden)}</span><br><br>"
        message += f"• Plantas verdes 🌿: <b>{count_a}</b><br>"
        message += f"• Flores rosadas 🌸: <b>{count_b}</b><br>"
        message += f"• Semillas por crecer 🌱: <b>{'Sí' if has_s else 'No'}</b><br><br>"
        
        if has_s:
            message += "⏳ <b>Tu jardín todavía puede crecer más</b><br>"
            message += "Presiona 'Siguiente Fase' para seguir creciendo."
        elif count_a == count_b:
            message += "✅ <b>¡Perfecto! Tu jardín está balanceado!</b><br>"
            message += f"Tienes la misma cantidad de plantas verdes 🌿 ({count_a}) y flores rosadas 🌸 ({count_b})."
        else:
            message += "❌ <b>Tu jardín no está balanceado</b><br>"
            message += f"Tienes diferentes cantidades: {count_a} 🌿 y {count_b} 🌸"
        
        self.show_info_message("🔍 Validación del Jardín", message)

    # ==========================================================================
    # ACTUALIZACIÓN DE INTERFAZ
    # ==========================================================================
    
    def update_display(self):
        """Actualiza todas las áreas de visualización."""
        # Actualizar el jardín
        if self.current_garden:
            formatted = self.format_pattern(self.current_garden)
            self.ui.gardenDisplay.setText(formatted)
        else:
            self.ui.gardenDisplay.setText("Selecciona un nivel para comenzar")
        
        # Actualizar contador
        if self.current_garden:
            count_a = self.current_garden.count('a')
            count_b = self.current_garden.count('b')
            count_s = self.current_garden.count('S')
            self.ui.plantCounterLabel.setText(
                f"Plantas: a={count_a}, b={count_b}, S={count_s} | Fase: {self.phase_count}"
            )
        else:
            self.ui.plantCounterLabel.setText("Plantas: -")
        
        # Actualizar historial
        if self.transformation_history:
            history_text = "<h3>📜 Historia de tu Jardín:</h3><br>"
            for entry in self.transformation_history:
                history_text += f"• {entry}<br>"
            self.ui.historyDisplay.setText(history_text)
        else:
            self.ui.historyDisplay.setText(
                "<i>Aquí aparecerá la historia de cómo crece tu jardín.<br><br>"
                "Presiona 'Siguiente Fase' para comenzar.</i>"
            )

    def format_pattern(self, pattern):
        """Formatea el patrón con símbolos visuales."""
        # Reemplazar símbolos con emojis para mejor visualización
        formatted = pattern.replace('a', self.SYMBOL_A)
        formatted = formatted.replace('b', self.SYMBOL_B)
        formatted = formatted.replace('S', self.SYMBOL_S)
        return formatted

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
