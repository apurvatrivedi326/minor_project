import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QMessageBox, QProgressBar, QComboBox, QCheckBox
from PyQt5.QtGui import QIcon, QPalette, QColor
from PIL import Image
import os
import shutil

class ImageResizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window setup
        self.setWindowTitle('Image Resizer & Folder Compressor')
        self.setGeometry(100, 100, 400, 450)
        self.setWindowIcon(QIcon('icon.png'))  # Set your window icon here

        # Set the background color to black
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

        # Layout
        layout = QVBoxLayout()

        # Image file selection
        self.label = QLabel('Select Image:', self)
        self.label.setStyleSheet('color: white; font-size: 14px;')
        layout.addWidget(self.label)

        self.image_path_input = QLineEdit(self)
        self.image_path_input.setPlaceholderText('Image file path')
        self.image_path_input.setStyleSheet('background-color: #2E2E2E; color: white; padding: 5px; border-radius: 5px;')
        layout.addWidget(self.image_path_input)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.setStyleSheet('''background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;''')
        self.browse_button.clicked.connect(self.browse_image)
        layout.addWidget(self.browse_button)

        # Folder selection for batch processing
        self.folder_label = QLabel('Select Folder to Compress:', self)
        self.folder_label.setStyleSheet('color: white; font-size: 14px;')
        layout.addWidget(self.folder_label)

        self.folder_path_input = QLineEdit(self)
        self.folder_path_input.setPlaceholderText('Folder path')
        self.folder_path_input.setStyleSheet('background-color: #2E2E2E; color: white; padding: 5px; border-radius: 5px;')
        layout.addWidget(self.folder_path_input)

        self.browse_folder_button = QPushButton('Browse Folder', self)
        self.browse_folder_button.setStyleSheet('''background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;''')
        self.browse_folder_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_folder_button)

        # Width input or percentage input
        self.resize_mode = QComboBox(self)
        self.resize_mode.addItem("Resize by Width")
        self.resize_mode.addItem("Resize by Percentage")
        self.resize_mode.currentIndexChanged.connect(self.toggle_resize_input)
        layout.addWidget(self.resize_mode)

        # Width input
        self.width_label = QLabel('Enter desired width:', self)
        self.width_label.setStyleSheet('color: white; font-size: 14px;')
        layout.addWidget(self.width_label)

        self.width_input = QLineEdit(self)
        self.width_input.setPlaceholderText('Width in pixels')
        self.width_input.setStyleSheet('background-color: #2E2E2E; color: white; padding: 5px; border-radius: 5px;')
        layout.addWidget(self.width_input)

        # Percentage input
        self.percentage_input = QLineEdit(self)
        self.percentage_input.setPlaceholderText('Percentage')
        self.percentage_input.setStyleSheet('background-color: #2E2E2E; color: white; padding: 5px; border-radius: 5px;')
        self.percentage_input.setVisible(False)
        layout.addWidget(self.percentage_input)

        # File format selection
        self.format_label = QLabel('Select output format:', self)
        self.format_label.setStyleSheet('color: white; font-size: 14px;')
        layout.addWidget(self.format_label)

        self.format_combo = QComboBox(self)
        self.format_combo.addItems(['PNG', 'JPEG', 'BMP'])
        layout.addWidget(self.format_combo)

        # Black-and-white checkbox
        self.bw_checkbox = QCheckBox("Convert to Black & White")
        self.bw_checkbox.setStyleSheet('color: white; font-size: 14px;')
        layout.addWidget(self.bw_checkbox)

        # Resize button
        self.resize_button = QPushButton('Resize Image', self)
        self.resize_button.setStyleSheet('''background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;''')
        self.resize_button.clicked.connect(self.resize_image)
        layout.addWidget(self.resize_button)

        # Compress folder button
        self.compress_folder_button = QPushButton('Resize & Compress Folder', self)
        self.compress_folder_button.setStyleSheet('''background-color: #f44336; color: white; padding: 10px; border-radius: 5px;''')
        self.compress_folder_button.clicked.connect(self.compress_folder)
        layout.addWidget(self.compress_folder_button)

        # Progress bar for folder resizing
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Set layout
        self.setLayout(layout)

    def toggle_resize_input(self):
        """ Toggle between width input and percentage input """
        if self.resize_mode.currentIndex() == 0:
            self.width_input.setVisible(True)
            self.percentage_input.setVisible(False)
        else:
            self.width_input.setVisible(False)
            self.percentage_input.setVisible(True)

    def browse_image(self):
        """ Allow user to select an image file """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_path_input.setText(file_path)

    def browse_folder(self):
        """ Allow user to select a folder for batch resizing and compression """
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path_input.setText(folder_path)

    def resize_image(self):
        """ Resize a single image based on user input """
        image_path = self.image_path_input.text()
        try:
            # Check which resizing method is chosen
            if self.resize_mode.currentIndex() == 0:  # Resize by width
                mywidth = int(self.width_input.text())
            else:  # Resize by percentage
                percentage = int(self.percentage_input.text())

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid width or percentage.")
            return

        if not os.path.exists(image_path):
            QMessageBox.warning(self, "File Error", "Image file not found.")
            return

        try:
            img = Image.open(image_path)
            if self.resize_mode.currentIndex() == 0:  # Resize by width
                wpercent = (mywidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((mywidth, hsize), Image.Resampling.LANCZOS)
            else:  # Resize by percentage
                wsize = int(img.size[0] * (percentage / 100))
                hsize = int(img.size[1] * (percentage / 100))
                img = img.resize((wsize, hsize), Image.Resampling.LANCZOS)

            # Convert to black and white if checkbox is selected
            if self.bw_checkbox.isChecked():
                img = img.convert("L")

            # Save resized image in the user-selected format
            output_format = self.format_combo.currentText().lower()
            save_path = os.path.join(os.path.dirname(image_path), f'resized_image.{output_format}')
            img.save(save_path, output_format.upper())

            QMessageBox.information(self, "Success", f"Image resized successfully!\nSaved at {save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def compress_folder(self):
        """ Resize and compress all images in the selected folder """
        folder_path = self.folder_path_input.text()
        try:
            # Check which resizing method is chosen
            if self.resize_mode.currentIndex() == 0:  # Resize by width
                mywidth = int(self.width_input.text())
            else:  # Resize by percentage
                percentage = int(self.percentage_input.text())

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid width or percentage.")
            return

        if not os.path.exists(folder_path):
            QMessageBox.warning(self, "File Error", "Folder not found.")
            return

        # Create a new folder to save resized images
        compressed_folder = os.path.join(folder_path, 'compressed_images')
        if not os.path.exists(compressed_folder):
            os.makedirs(compressed_folder)

        # Initialize the progress bar
        self.progress_bar.setVisible(True)
        total_files = len([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
        self.progress_bar.setMaximum(total_files)
        self.progress_bar.setValue(0)

        try:
            for idx, file in enumerate(os.listdir(folder_path)):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    img_path = os.path.join(folder_path, file)
                    img = Image.open(img_path)

                    if self.resize_mode.currentIndex() == 0:  # Resize by width
                        wpercent = (mywidth / float(img.size[0]))
                        hsize = int((float(img.size[1]) * float(wpercent)))
                        img = img.resize((mywidth, hsize), Image.Resampling.LANCZOS)
                    else:  # Resize by percentage
                        wsize = int(img.size[0] * (percentage / 100))
                        hsize = int(img.size[1] * (percentage / 100))
                        img = img.resize((wsize, hsize), Image.Resampling.LANCZOS)

                    # Convert to black and white if checkbox is selected
                    if self.bw_checkbox.isChecked():
                        img = img.convert("L")

                    # Save resized image in the compressed folder
                    save_path = os.path.join(compressed_folder, f"resized_{file}")
                    img.save(save_path)

                    self.progress_bar.setValue(idx + 1)

            self.progress_bar.setVisible(False)
            QMessageBox.information(self, "Success", "All images have been resized and saved in the 'compressed_images' folder.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

# Run the application
app = QApplication(sys.argv)
window = ImageResizerApp()
window.show()
sys.exit(app.exec_())
