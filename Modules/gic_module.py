from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal
# Importa la clase de diseño UI 
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
        # Instanciamos la clase de diseño de la UI
        self.ui = Ui_GIC_Module()
        # Configuramos la UI en esta instancia de QWidget (self)
        self.ui.setupUi(self) 
        
        # 3. Conectar el botón de regreso de la UI a la señal del controlador
        # El botón fue nombrado 'backToMenuButton' en gic_ui.py
        self.ui.backToMenuButton.clicked.connect(self.back_requested.emit)
        
        # 4. Configuración inicial de textos y componentes
        self.ui.theoryTextDisplay.setText(
            "La <b>Gramática Independiente del Contexto (GIC)</b> funciona de una manera muy sencilla.<br><br>"
            "Imagina que tienes unas muñecas rusas: una grande, y dentro de ella unas más pequeñas,"
            "y dentro de esa, otra todavía más pequeña.<br>"
            "Cada muñeca representa una regla que nos dice cómo continuar.<br><br>"

            "Una <b>GIC</b> funciona igual:<br>"
            "tiene un símbolo inicial (la muñeca grande) y unas reglas que nos dicen "
            "cómo debemos abrirla y qué aparecerá dentro.<br><br>"

            "Por ejemplo, si la regla dice:<br>"
            "<b> - S → a S b </b> <br>"
            "Significa que la muñeca grande S se abre y adentro aparece una parte a, <br>"
            "otra parte b, (otras muñecas) y hay otra muñeca S la cual se puede volver a abrir.<br>"
            "<b> - S → ab </b> <br>"
            "Esta regla es la muñeca más pequeña, que ya no se abre más.<br><br>"

            "Así, para formar la cadena aabb, hacemos: <br>"
            "1. Abrimos la muñeca grande: aparece a … b, y adentro otra S. <br>"
            "2. La muñeca de adentro es la más pequeña y nos da ab. <br>"
            "3. Si juntamos todo lo que apareció desde la muñeca más grande nos queda aabb. <br><br>"
            
            "<b>Reglas del juego</b><br>"
            "1. Empieza escogiendo un símbolo inicial (S) en la sección de seleccionar muñecas.<br>"
            "2. Una vez ubicado el símbolo inicial, escoge la manera en que se debe <br> seguir abriendo la muñeca con otras reglas<br>"
            "3. Cada vez que aparezca una S, puedes abrirla usando otra regla.<br>"
            "4. Cuando ya no haya S, has terminado.<br>"
            "5. Si la cadena final coincide con la que debes formar, ganaste"
        )

        # 5. Adición de Botones de seleccionar muñecas (reglas) al statusContentLayout
        # Los botones (actionButton1, actionButton2, actionButton3) ya están creados en gic_ui.py
        self.ui.statusContentLayout.addWidget(self.ui.actionButton1)
        self.ui.statusContentLayout.addWidget(self.ui.actionButton2)
        self.ui.statusContentLayout.addWidget(self.ui.actionButton3)
        
        # 6. Inicialización y adición de la etiqueta de estado
        self.status_label = QLabel("Este panel mostrará mensajes de estado y feedback durante la derivación. Utiliza los botones de arriba para comenzar la derivación o selecciona una muñeca (símbolo no terminal) que quieras expandir.")
        self.status_label.setWordWrap(True)
        # Aplicamos el estilo de la etiqueta de estado
        self.status_label.setStyleSheet("padding: 10px; font-size: 10pt; background-color: #ecf0f1; border-radius: 4px;")
        
        # Añadimos la etiqueta al layout debajo de los botones
        self.ui.statusContentLayout.addWidget(self.status_label)
        self.ui.statusContentLayout.addStretch(1) # Relleno vertical para alinear todo arriba