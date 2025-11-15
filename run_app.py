# main.py
import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QSize, QEvent, Qt  # NUEVO: QEvent y Qt
import qtawesome as qta

# Importa la clase de tu archivo generado
from GUI.main_Window import Ui_MainMenu 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

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

        self.ui.trainButton.installEventFilter(self)
        self.ui.gardenButton.installEventFilter(self)
        self.ui.dollsButton.installEventFilter(self)
        self.add_icons_and_fix_styles()
        self.ui.trainButton.setMinimumHeight(100)
        self.ui.gardenButton.setMinimumHeight(100)
        self.ui.dollsButton.setMinimumHeight(100)


    def eventFilter(self, watched, event):
        if watched in self.original_texts:
            if event.type() == QEvent.Type.Enter:
                watched.setText(self.hover_texts[watched])

            elif event.type() == QEvent.Type.Leave:
                watched.setText(self.original_texts[watched])

        return super().eventFilter(watched, event)


    def add_icons_and_fix_styles(self):
        icon_size = QSize(32, 32)
        
        icon_train = qta.icon('fa5s.train', color='white')
        self.ui.trainButton.setIcon(icon_train)
        self.ui.trainButton.setIconSize(icon_size)
        
        icon_garden = qta.icon('fa5s.seedling', color='white')
        self.ui.gardenButton.setIcon(icon_garden)
        self.ui.gardenButton.setIconSize(icon_size)
        
        icon_doll = qta.icon('fa5s.user-circle', color='white')
        self.ui.dollsButton.setIcon(icon_doll)
        self.ui.dollsButton.setIconSize(icon_size)
        
        current_style = self.styleSheet() 
        fixed_style = current_style.replace(
            "text-align: center;", 
            "text-align: left; padding-left: 25px;"
        )
        self.setStyleSheet(fixed_style)


def main():
    """Función principal para lanzar la app."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()