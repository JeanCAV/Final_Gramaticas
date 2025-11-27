import sys
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, QEvent, Qt, Signal 
import qtawesome as qta

# Importa la clase de la interfaz generada por uic
from GUI.main_Window import Ui_MainMenu 

class MenuPage(QWidget):
    """
    Widget de Menú Principal.
    """
    
    # Navegación a los módulos
    train_clicked = Signal()
    garden_clicked = Signal()
    dolls_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainMenu()
        self.ui.setupUi(self) 

        self.original_texts = {
            self.ui.trainButton: " El Tren Mágico",
            self.ui.gardenButton: " El Jardín Mágico",
            self.ui.dollsButton: " Las Muñecas Rusas"
        }
        
        self.hover_texts = {
            self.ui.trainButton: " Máquina de Turing",
            self.ui.gardenButton: " Gramáticas Dependientes de Contexto",
            self.ui.dollsButton: " Gramáticas Independientes de Contexto"
        }

        self.add_icons_and_fix_styles()
        
        self.ui.trainButton.installEventFilter(self)
        self.ui.gardenButton.installEventFilter(self)
        self.ui.dollsButton.installEventFilter(self)

        # Conexión de botones a la emisión de señales
        self.ui.trainButton.clicked.connect(self.train_clicked.emit)
        self.ui.gardenButton.clicked.connect(self.garden_clicked.emit)
        self.ui.dollsButton.clicked.connect(self.dolls_clicked.emit)


    def eventFilter(self, watched, event):
        """Hover para cambiar el texto de los botones."""
        if watched in self.original_texts:
            if event.type() == QEvent.Type.Enter:
                watched.setText(self.hover_texts[watched])

            elif event.type() == QEvent.Type.Leave:
                watched.setText(self.original_texts[watched])

        return super().eventFilter(watched, event)


    def add_icons_and_fix_styles(self):
        """Añade íconos a los botones"""
        icon_size = QSize(32, 32)
        
        # Tren Mágico (MT)
        icon_train = qta.icon('fa5s.train', color='white')
        self.ui.trainButton.setIcon(icon_train)
        self.ui.trainButton.setIconSize(icon_size)
        self.ui.trainButton.setMinimumHeight(100)
        
        # Jardín Mágico (GDC)
        icon_garden = qta.icon('fa5s.seedling', color='white')
        self.ui.gardenButton.setIcon(icon_garden)
        self.ui.gardenButton.setIconSize(icon_size)
        self.ui.gardenButton.setMinimumHeight(100)
        
        # Muñecas Rusas (GIC)
        icon_doll = qta.icon('fa5s.user-circle', color='white') 
        self.ui.dollsButton.setIcon(icon_doll)
        self.ui.dollsButton.setIconSize(icon_size)
        self.ui.dollsButton.setMinimumHeight(100)
        
        # Alineacion y padding
        current_style = self.styleSheet() 
        fixed_style = current_style.replace(
            "text-align: center;",
            "text-align: center"
        )
        self.setStyleSheet(fixed_style)


        