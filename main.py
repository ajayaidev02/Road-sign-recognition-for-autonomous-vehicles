from PyQt5 import QtCore, QtGui, QtWidgets
from keras.models import load_model
import numpy as np
from PIL import Image
import os

from utils import TRAFFIC_SIGNS, NUM_CLASSES, get_sign_name

cur_path = os.getcwd()  # To get current directory

# Global variables for training data
data = []
labels = []
X_train, X_test = None, None
y_train, y_test = None, None


#Retrieving the images and their labels
print("Obtaining Images & its Labels..............")
dataset_path = os.path.join(cur_path, 'dataset/train/')

# Check if dataset exists
if os.path.exists(dataset_path):
    images_path = os.path.join(dataset_path, 'images')
    labels_path = os.path.join(dataset_path, 'labels')
    
    if os.path.exists(images_path) and os.path.exists(labels_path):
        # Load images from YOLO format dataset
        image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for image_file in image_files:
            try:
                # Get corresponding label file
                label_file = os.path.splitext(image_file)[0] + '.txt'
                label_path = os.path.join(labels_path, label_file)
                
                if os.path.exists(label_path):
                    # Read the label file (YOLO format: class_id x_center y_center width height)
                    with open(label_path, 'r') as f:
                        line = f.readline().strip()
                        if line:
                            class_id = int(line.split()[0])
                            
                            # Load and process image
                            image = Image.open(os.path.join(images_path, image_file))
                            image = image.resize((30, 30))
                            image = np.array(image)
                            data.append(image)
                            labels.append(class_id)
                            print("{0} Loaded (Class: {1})".format(image_file, class_id))
                else:
                    print("Label file not found for {0}".format(image_file))
            except Exception as e:
                print("Error loading image {0}: {1}".format(image_file, str(e)))
        print("Dataset Loaded")
        
        #Converting lists into numpy arrays
        data_array = np.array(data)
        labels_array = np.array(labels)

        #Splitting training and testing dataset
        from sklearn.model_selection import train_test_split
        from keras.utils import to_categorical
        
        X_train, X_test, y_train, y_test = train_test_split(data_array, labels_array, test_size=0.2, random_state=42)

        #Converting the labels into one hot encoding
        y_train = to_categorical(y_train, NUM_CLASSES)
        y_test = to_categorical(y_test, NUM_CLASSES)
    else:
        print("Expected dataset/train/images and dataset/train/labels folders not found.")
        print("Using pre-trained model instead...")
        print("Run training/train.py to train a new model.")
else:
    print("Dataset folder not found. Using pre-trained model instead...")
    print("Run training/train.py to train a new model.")

#Class - 43
#o/p 2 - [0,0,1,0,0,......0]
#o/p 5 - [0,0,0,0,0,1,0,0,0.....]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BrowseImage = QtWidgets.QPushButton(self.centralwidget)
        self.BrowseImage.setGeometry(QtCore.QRect(160, 370, 151, 51))
        self.BrowseImage.setObjectName("BrowseImage")
        self.imageLbl = QtWidgets.QLabel(self.centralwidget)
        self.imageLbl.setGeometry(QtCore.QRect(200, 80, 361, 261))
        self.imageLbl.setFrameShape(QtWidgets.QFrame.Box)
        self.imageLbl.setText("")
        self.imageLbl.setObjectName("imageLbl")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 20, 621, 20))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.Classify = QtWidgets.QPushButton(self.centralwidget)
        self.Classify.setGeometry(QtCore.QRect(160, 450, 151, 51))
        self.Classify.setObjectName("Classify")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 370, 111, 16))
        self.label.setObjectName("label")
        self.Training = QtWidgets.QPushButton(self.centralwidget)
        self.Training.setGeometry(QtCore.QRect(400, 450, 151, 51))
        self.Training.setObjectName("Training")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(400, 390, 211, 51))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.BrowseImage.clicked.connect(self.loadImage)
        self.Classify.clicked.connect(self.classifyFunction)
        self.Training.clicked.connect(self.trainingFunction)        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.BrowseImage.setText(_translate("MainWindow", "Browse Image"))
        self.label_2.setText(_translate("MainWindow", "           ROAD SIGN RECOGNITION"))
        self.Classify.setText(_translate("MainWindow", "Classify"))
        self.label.setText(_translate("MainWindow", "Recognized Class"))
        self.Training.setText(_translate("MainWindow", "Training"))

    def loadImage(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)") # Ask for file
        if fileName: # If the user gives a file
            print(fileName)
            self.file=fileName
            pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.imageLbl.width(), self.imageLbl.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
            self.imageLbl.setPixmap(pixmap) # Set the pixmap onto the label
            self.imageLbl.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center

    def classifyFunction(self):
        model = load_model('my_model.h5')
        print("Loaded model from disk");
        path2=self.file
        print(path2)
        test_image = Image.open(path2)
        test_image = test_image.resize((30, 30))
        test_image = np.expand_dims(test_image, axis=0)
        test_image = np.array(test_image)

        result = model.predict(test_image)[0]
        predicted_class_index = result.argmax()
        sign = get_sign_name(predicted_class_index)
        print(sign)
        self.textEdit.setText(sign)

    def trainingFunction(self):
        # Check if dataset was loaded
        if len(data) == 0:
            self.textEdit.setText("Error: No training data available.\nRun: python training/train.py to train a new model")
            return
        
        self.textEdit.setText("Training under process...")
        
        from utils.model import create_model, compile_model
        
        model = create_model(num_classes=NUM_CLASSES)
        model = compile_model(model)
        print("Initialized model")

        # Compilation of the model (already done by compile_model)
        history = model.fit(X_train, y_train, batch_size=32, epochs=5, validation_data=(X_test, y_test))
        model.save("my_model_new.h5")

        import matplotlib.pyplot as plt
        
        plt.figure(0)
        plt.plot(history.history['accuracy'], label='training accuracy')
        plt.plot(history.history['val_accuracy'], label='val accuracy')
        plt.title('Accuracy')
        plt.xlabel('epochs')
        plt.ylabel('accuracy')
        plt.legend()
        plt.savefig('Accuracy1.png')

        plt.figure(1)
        plt.plot(history.history['loss'], label='training loss')
        plt.plot(history.history['val_loss'], label='val loss')
        plt.title('Loss')
        plt.xlabel('epochs')
        plt.ylabel('loss')
        plt.legend()
        plt.savefig('Loss1.png')
        self.textEdit.setText("Saved Model & Graph to disk")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

