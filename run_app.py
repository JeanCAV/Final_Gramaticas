import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Signal, Qt

# IMPORTACIONES DE MÓDULOS
from GUI.menu_page import MenuPage 
# Importamos la clase de controlador, no la clase de UI.
from Modules.gic_module import GICModule
from Modules.gdc_module import GDCModule
from Modules.mt_module import MTModule


class ModulePlaceholder(QWidget):

    back_requested = Signal() 

    def __init__(self, title="Módulo en Construcción", parent=None):
        super().__init__(parent)
        
        # Layout central y alineación
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        # Título del Placeholder
        title_label = QLabel(f"{title} - En Construcción")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #34495e;")
        layout.addWidget(title_label)
        # Botón de regreso
        self.back_button = QPushButton("← Volver al Menú Principal")
        self.back_button.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px; border-radius: 8px;")
        self.back_button.setMaximumWidth(300)
        # Conexión del botón de regreso
        self.back_button.clicked.connect(self.back_requested.emit)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)


# 2. CLASE PRINCIPAL DE LA VENTANA 
class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gramaticas y Maquina de Turing")
        self.setGeometry(100, 100, 1000, 700) # Tamaño y posición inicial
        self.setMinimumSize(800, 600)
        self.setStyleSheet("QMainWindow { background-color: #f0f0f0; }")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        # Inicializar y añadir todas las páginas al stack
        self._init_pages()
        # Conectar las señales de navegación entre páginas
        self._connect_signals()
        # Mostrar el menú al inicio
        self.stack.setCurrentWidget(self.menu_page)

    def _init_pages(self):
        """Inicializa todas las vistas modulares"""
        
        self.menu_page = MenuPage()
        self.stack.addWidget(self.menu_page)
        
        # 1. Módulo MT (Tren Mágico) - Funcional
        self.mt_module = MTModule()
        self.stack.addWidget(self.mt_module)

        # 2. Módulo GDC (Jardín Mágico) - Funcional
        self.gdc_module = GDCModule()
        self.stack.addWidget(self.gdc_module)
        
        # 3. Módulo GIC (Muñecas Rusas) 
        # Instanciamos el controlador GICModule
        self.gic_module = GICModule() 
        self.stack.addWidget(self.gic_module)
        

    def _connect_signals(self):
        """logica para la navegación."""        
        # Conexión del Menú para abrir Módulos
        self.menu_page.train_clicked.connect(lambda: self.stack.setCurrentWidget(self.mt_module))
        self.menu_page.garden_clicked.connect(lambda: self.stack.setCurrentWidget(self.gdc_module))
        self.menu_page.dolls_clicked.connect(lambda: self.stack.setCurrentWidget(self.gic_module))
        
        # Conexión de los Módulos -> Navegar Hacia Atrás (Volver al menú)
        self.mt_module.back_requested.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        self.gdc_module.back_requested.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        # Conexión del botón de regreso del módulo GIC (ahora gestionado por GICModule)
        self.gic_module.back_requested.connect(lambda: self.stack.setCurrentWidget(self.menu_page))


# 3. FUNCIÓN DE INICIO
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()