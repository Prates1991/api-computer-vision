# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 19:59:58 2018

@author: Henrique Pereira
"""
##---------------------------------------------------------------------------------------------------------------------
## Importação de Bibliotecas
##---------------------------------------------------------------------------------------------------------------------
import cv2
from PyQt5 import  QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
import sys
import glob
import os
import numpy as np
import shutil
import datetime
import winsound

class interface(QDialog):
    def __init__(self):
        try:
            self.data_hora()
            
            
            #self.log_escrita.write("Data;Hora;Acao\n")          
            super(interface, self).__init__()
            loadUi('interface.ui', self)
            self.timer = QTimer(self)
            self.image = None
            self.image_log = None
            self.btn_camera.setCheckable(True)
            self.btn_camera.toggled.connect(self.liga_desliga_camera_cadastro)
            self.btn_camera_login.setCheckable(True)
            self.btn_camera_login.toggled.connect(self.liga_desliga_camera_login)
            self.status_camera = False
            self.btn_grava_senha.clicked.connect(self.seleciona_opcao)
            self.btn_grava_senha.setEnabled(False)
            # Radio buttons
            self.rb_cadastrar.setCheckable(True)
            self.rb_cadastrar.clicked.connect(self.rb_cadastrar_click)
            self.rb_alterar.setCheckable(True)
            self.rb_alterar.clicked.connect(self.rb_alterar_click)
            self.rb_deletar.setCheckable(True)
            self.rb_deletar.clicked.connect(self.rb_deletar_click)
            #self.btn_camera_login_2.setEnabled(False)
            self.pasta_cadastros = 'C:\\Users\\Henrique Pereira\\Python\\TCC\\00_API_SEGURANCA\\cadastro_usuarios\\'
            self.pasta_log_imagens = 'C:\\Users\\Henrique Pereira\\Python\\TCC\\00_API_SEGURANCA\\log\\imagens\\'
            #self.imgSobrepoeWebcam = cv2.imread('transparente.png')
            self.data_hora()
            self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
            self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                   "Sistema iniciado com sucesso\n")
            self.log_escrita.close()
            #self.tableWIdget
            #face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
            #header = self.tableWidget.horizontalHeader()
            #header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
            #header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            #header.setResizeMode(2, QtGui.QHeaderView.Stretch)
            
            header = self.tableWidget.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            
            self.flag = 0
            self.segundo_do_beep = datetime.datetime.now()
            self.tableWidget.cellClicked.connect(self.cellClick)
            
        except WindowsError:
            self.data_hora()
            self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                   "Erro ao iniciar o sistema\n")
            # Handle the case where the target dir already exist.
            pass
        self.leitura_log()
        
##########################################################################################
##########################################################################################
        
    def cellClick(self, row,col):
        #item = self.tableWidget.item(col, 0)
        #print("1,0: %s" % self.tableWidget.item(row, 1).text())
        #print("Click on " + str(row) + " " + str(col))
        
        if str(self.tableWidget.item(row, 2).text()) == "Sistema iniciado com sucesso":
            self.image_log = cv2.imread('transparente.png')
            self.image_log = cv2.resize(self.image_log, (320,240))
        else:
            self.image_log = cv2.imread(str(self.pasta_log_imagens) + str(self.tableWidget.item(row, 0).text()) + '\\' + str(self.tableWidget.item(row, 1).text()) +'.png')
            self.image_log = cv2.resize(self.image_log, (320,240))
        #self.display_image(self.image_log, 1)
        
        print('\n'+ str(self.pasta_log_imagens) + self.tableWidget.item(row, 0).text() + '\\' + str(self.tableWidget.item(row, 1).text()) +'.png\n')
        
        
        qformat = QImage.Format_Indexed8
        
        if len(self.image_log.shape) == 3:
            if self.image_log.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
                #print("4")
            else:
                qformat = QImage.Format_RGB888
                #print("4 else")
        #qformat = QImage.Format_RGB888
        outImage = QImage(self.image_log, self.image_log.shape[1], self.image_log.shape[0], self.image_log.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        
        
        self.imgLabel_log.setPixmap(QPixmap.fromImage(outImage))
        self.imgLabel_log.setScaledContents(True)
    
##########################################################################################
##########################################################################################        
        
    def leitura_log(self):
        shutil.copy2('log\\registros\\log_de_atividades.txt', 'log\\registros\\copia.txt')
        self.log_copia = open("log\\registros\\copia.txt", "r")
        log = self.log_copia.readlines()
        self.log_copia.close()
        
        conteudo = [x.strip() for x in log] 
        
        linha = [conteudo[x].split(';') for x in range(0, len(conteudo))]
        
        coluna_data = [linha[x][0] for x in range(0, len(linha))]
        coluna_hora = [linha[x][1] for x in range(0, len(linha))]
        coluna_acao = [linha[x][2] for x in range(0, len(linha))]
        
        print(str(coluna_data) + ' ' + str(coluna_hora) + ' ' + str(coluna_acao))
        
        for data, hora, ocorrido in zip(coluna_data, coluna_hora, coluna_acao):
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            # Add text to the row
            self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(data)))
            self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(hora)))
            self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(str(ocorrido)))
        
##########################################################################################
##########################################################################################
        
    def data_hora(self):
        if datetime.datetime.now().day < 10:
            dia = "0" + str(datetime.datetime.now().day)
        else:
            dia = str(datetime.datetime.now().day)
        
        if datetime.datetime.now().month < 10:
            mes = "0" + str(datetime.datetime.now().month)
        else:
            mes = str(datetime.datetime.now().month)
            
        self.data_atual = dia+"_"+ mes +"_"+ str(datetime.datetime.now().year)
        
        if datetime.datetime.now().hour < 10:
            hora = "0" + str(datetime.datetime.now().hour)
        else:
            hora = str(datetime.datetime.now().hour)
            
        if datetime.datetime.now().minute < 10:
            minuto = "0" + str(datetime.datetime.now().minute)
        else:
             minuto = str(datetime.datetime.now().minute)
            
        if datetime.datetime.now().second < 10:
            segundo = "0" + str(datetime.datetime.now().second)
        else:
            segundo = str(datetime.datetime.now().second)
            
        self.hora_atual = hora +"_"+ minuto +"_"+ segundo
            
    def rb_cadastrar_click(self):
        self.btn_grava_senha.setText("Cadastrar")
        
    def rb_alterar_click(self):
        self.btn_grava_senha.setText("Alterar")
        
    def rb_deletar_click(self):
        self.btn_grava_senha.setText("Deletar")
        
    def seleciona_opcao(self):
        if self.rb_cadastrar.isChecked():
            self.cadastro_usuario()
        elif self.rb_alterar.isChecked():
            self.alterar_usuario()
        elif self.rb_deletar.isChecked():
            self.deletar_usuario()
        
##########################################################################################
##########################################################################################
              
    def cadastro_usuario(self):
        global existe_cadastro
        new_dir = self.nomeUsuario_cadastro.toPlainText()
        
        if len(self.nomeUsuario_cadastro.toPlainText()) != 0:
            self.cria_listas_de_indices()
            self.existe_cadastro_cadastro()
            
            if existe_cadastro == 1:
                #new_dir = self.nomeUsuario_cadastro.toPlainText()
                msg = QMessageBox()
                msg.setText("Já existe um padrão com esse nome.\n Por favor, escolha outro nome.")
                msg.setWindowTitle("Atenção!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.data_hora()
                if os.path.exists(self.pasta_log_imagens + self.data_atual):
                    print("Diretorio já existe")
                else:
                    os.mkdir(self.pasta_log_imagens + self.data_atual)
                cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                       "Erro no cadastro do padrao " + str(new_dir) + ". Motivo: nome já cadastrado.\n")
                self.log_escrita.close()
                #currentRowCount = self.tableWidget.rowCount() #necessary even when there are no rows in the table
                #self.tableWidget.insertRow(currentRowCount, 0, self.QTableWidgetItem(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                #                                                                                 "Erro no cadastro do padrao. Motivo: nome já cadastrado.\n"))
                
                numRows = self.tableWidget.rowCount()
                self.tableWidget.insertRow(numRows)
                # Add text to the row
                self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Erro no cadastro do padrao " + str(new_dir) + ". Motivo: nome já cadastrado"))
                
            else:
                    
                self.desativa_camera()
                self.timer.stop()
            
                #cv2.imshow('Senha',self.image)
        
                #new_dir = self.nomeUsuario_cadastro.toPlainText()
                
                ###
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information) 
                ret = msg.question(self,'', "Deseja salvar a imagem selecionada como seu padrão de acesso?", msg.Yes | msg.No)
    
                if ret == msg.Yes:
                    print("yes")
                    try:
                        os.mkdir(self.pasta_cadastros+new_dir)
                        cv2.imwrite(self.pasta_cadastros + new_dir + '\\' + new_dir + '_1.png', self.image)
                        #cv2.flip(self.image, self.image, -1)   
                        (h, w) = self.image.shape[:2]
                        center = (w / 2, h / 2)
                        M = cv2.getRotationMatrix2D(center, 180, 1.0)
                        rotate = cv2.warpAffine(self.image, M, (w, h))
                        cv2.imwrite(self.pasta_cadastros + new_dir + '\\' + new_dir + '_2.png', rotate)
                        msg = QMessageBox()
                        msg.setText("Padrão cadastrado com sucesso!")
                        msg.setWindowTitle("Atenção!")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        self.data_hora()
                        if os.path.exists(self.pasta_log_imagens + self.data_atual):
                            print("Diretorio já existe")
                        else:
                            os.mkdir(self.pasta_log_imagens + self.data_atual)                       
                        cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)                       
                        self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                        self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                               "Cadastro do padrao " + new_dir + " realizado com sucesso" + "\n")
                        self.log_escrita.close()
                        numRows = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(numRows)
                        # Add text to the row
                        self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                        self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                        self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Cadastro do padrao " + new_dir + " realizado com sucesso"))
                        self.btn_camera.click()
                    except WindowsError:
                        # Handle the case where the target dir already exist.
                        pass
                else:
                    print("no")
                    self.data_hora()
                    if os.path.exists(self.pasta_log_imagens + self.data_atual):
                        print("Diretorio já existe")
                    else:
                        os.mkdir(self.pasta_log_imagens + self.data_atual)
                    cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                    self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                    self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                           "Abortou o cadastro do padrao " + new_dir +"\n")
                    self.log_escrita.close()
                    numRows = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(numRows)
                    # Add text to the row
                    self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                    self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                    self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Abortou o cadastro do padrao " + new_dir))

        else:
            #new_dir = self.nomeUsuario_cadastro.toPlainText()
            
            msg = QMessageBox()
            msg.setText("Por favor, digite um nome de padrão que seja válido.       ")
            msg.setWindowTitle("Atenção!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            print("no")
            self.data_hora()
            if os.path.exists(self.pasta_log_imagens + self.data_atual):
                print("Diretorio já existe")
            else:
                os.mkdir(self.pasta_log_imagens + self.data_atual)
            cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
            self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
            self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                   "Erro no cadastro do padrao. Motivo: nome não preenchido.\n")
            self.log_escrita.close()
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            # Add text to the row
            self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
            self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
            self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Erro no cadastro do padrao. Motivo: nome não preenchido"))

        print("Padrão cadastrado")

##########################################################################################
##########################################################################################
        
    def alterar_usuario(self):
        global existe_cadastro
        new_dir = self.nomeUsuario_cadastro.toPlainText()
        
        if len(self.nomeUsuario_cadastro.toPlainText()) != 0:
            self.cria_listas_de_indices()
            self.existe_cadastro_cadastro()
            
            if existe_cadastro == 1:
                
                self.desativa_camera()
                self.timer.stop()
                alt_dir = self.nomeUsuario_cadastro.toPlainText()
                
                #cv2.imshow('Senha',self.image)

                ###
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information) 
                ret = msg.question(self,'', "Deseja alterar esse padrão de acesso pela imagem atual da câmera?", msg.Yes | msg.No)
    
                if ret == msg.Yes:
                    print("yes")
                    try:
                        shutil.rmtree('cadastro_usuarios/'+ alt_dir)
                        os.mkdir(self.pasta_cadastros+alt_dir)
                        cv2.imwrite(self.pasta_cadastros + alt_dir + '\\' + alt_dir + '.png', self.image)
                        msg = QMessageBox()
                        msg.setText("Padrão alterado com sucesso!")
                        msg.setWindowTitle("Atenção!")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        self.data_hora()
                        if os.path.exists(self.pasta_log_imagens + self.data_atual):
                            print("Diretorio já existe")
                        else:
                            os.mkdir(self.pasta_log_imagens + self.data_atual)
                        cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                        self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                        self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                               "Alteração do padrao " + new_dir + " realizado com sucesso" + "\n")
                        self.log_escrita.close()
                        numRows = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(numRows)
                        # Add text to the row
                        self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                        self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                        self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Alteração do padrao " + new_dir + " realizado com sucesso"))
                        self.btn_camera.click()
                    except WindowsError:
                        # Handle the case where the target dir already exist.
                        pass
                else:
                    print("no")
                    self.data_hora()
                    if os.path.exists(self.pasta_log_imagens + self.data_atual):
                        print("Diretorio já existe")
                    else:
                        os.mkdir(self.pasta_log_imagens + self.data_atual)
                    cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                    self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                    self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                           "Abortou a alteração do padrao " + new_dir +"\n")
                    self.log_escrita.close()
                    numRows = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(numRows)
                    # Add text to the row
                    self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                    self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                    self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Abortou a alteração do padrao " + new_dir))
                    self.btn_camera.click()
                ###
                
            else:
                self.desativa_camera()
                self.timer.stop()
                alt_dir = self.nomeUsuario_cadastro.toPlainText()
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information) 
                ret = msg.question(self,'', "Não existe um padrão com esse registro.\nDeseja salvar a imagem selecionada como um novo padrão de acesso?" \
                                             , msg.Yes | msg.No)
                self.data_hora()
                if os.path.exists(self.pasta_log_imagens + self.data_atual):
                    print("Diretorio já existe")
                else:
                    os.mkdir(self.pasta_log_imagens + self.data_atual)
                cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                       "Erro na alteração do padrao. Motivo: nome não cadastrado.\n")
                self.log_escrita.close()
                numRows = self.tableWidget.rowCount()
                self.tableWidget.insertRow(numRows)
                # Add text to the row
                self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Erro na alteração do padrao. Motivo: nome não cadastrado"))
                if ret == msg.Yes:
                    print("yes")
                    try:
                        os.mkdir(self.pasta_cadastros+alt_dir)
                        cv2.imwrite(self.pasta_cadastros + alt_dir + '\\' + alt_dir + '.png', self.image)
                        msg = QMessageBox()
                        msg.setText("Padrão cadastrado com sucesso!")
                        msg.setWindowTitle("Atenção!")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        self.data_hora()
                        if os.path.exists(self.pasta_log_imagens + self.data_atual):
                            print("Diretorio já existe")
                        else:
                            os.mkdir(self.pasta_log_imagens + self.data_atual)
                        cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                        self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                        self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                               "Cadastro do padrao " + new_dir + " realizado com sucesso" + "\n")
                        self.log_escrita.close()
                        numRows = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(numRows)
                        # Add text to the row
                        self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                        self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                        self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Cadastro do padrao " + new_dir + " realizado com sucesso"))
                        self.btn_camera.click()                        
                    except WindowsError:
                        # Handle the case where the target dir already exist.
                        pass
                else:
                    print("no")
                    self.data_hora()
                    if os.path.exists(self.pasta_log_imagens + self.data_atual):
                        print("Diretorio já existe")
                    else:
                        os.mkdir(self.pasta_log_imagens + self.data_atual)
                    cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                    self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                    self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                           "Abortou o cadastro do padrao " + new_dir +"\n")
                    self.log_escrita.close()
                    numRows = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(numRows)
                    # Add text to the row
                    self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                    self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                    self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Abortou o cadastro do padrao " + new_dir))
                ###
                
        else:
            msg = QMessageBox()
            msg.setText("Por favor, digite um nome de padrão que seja válido.       ")
            msg.setWindowTitle("Atenção!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.data_hora()
            if os.path.exists(self.pasta_log_imagens + self.data_atual):
                print("Diretorio já existe")
            else:
                os.mkdir(self.pasta_log_imagens + self.data_atual)
            cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
            self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
            self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                   "Erro no cadastro do padrao. Motivo: nome não preenchido.\n")
            self.log_escrita.close()
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            # Add text to the row
            self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
            self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
            self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Erro no cadastro do padrao. Motivo: nome não preenchido"))
        
        print("Padrão alterado")
        
##########################################################################################
##########################################################################################
        
    def deletar_usuario(self):
        global existe_cadastro
        new_dir = self.nomeUsuario_cadastro.toPlainText()
        
        if len(self.nomeUsuario_cadastro.toPlainText()) != 0:
            self.cria_listas_de_indices()
            self.existe_cadastro_cadastro()
            
            if existe_cadastro == 1:
                
                self.desativa_camera()
                self.timer.stop()
        
                del_dir = self.nomeUsuario_cadastro.toPlainText()
                
                ###
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information) 
                ret = msg.question(self,'', "Deseja deletar esse padrão de acesso?", msg.Yes | msg.No)
    
                if ret == msg.Yes:
                    print("yes")
                    try:
                        shutil.rmtree('cadastro_usuarios/'+ del_dir)                        
                        msg = QMessageBox()
                        msg.setText("Padrão deletado com sucesso!")
                        msg.setWindowTitle("Atenção!")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        self.data_hora()
                        if os.path.exists(self.pasta_log_imagens + self.data_atual):
                            print("Diretorio já existe")
                        else:
                            os.mkdir(self.pasta_log_imagens + self.data_atual)
                        cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                        self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                        self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                               "Deleção do padrao " + new_dir + " realizado com sucesso" + "\n")
                        self.log_escrita.close()
                        numRows = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(numRows)
                        # Add text to the row
                        self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                        self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                        self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Deleção do padrao " + new_dir + " realizado com sucesso"))
                        self.btn_camera.click()
                    except WindowsError:
                        # Handle the case where the target dir already exist.
                        pass
                else:
                    print("no")
                    self.data_hora()
                    if os.path.exists(self.pasta_log_imagens + self.data_atual):
                        print("Diretorio já existe")
                    else:
                        os.mkdir(self.pasta_log_imagens + self.data_atual)
                    cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                    self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                    self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                           "Abortou a deleção do padrao " + new_dir +"\n")
                    self.log_escrita.close()
                    numRows = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(numRows)
                    # Add text to the row
                    self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                    self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                    self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Abortou a deleção do padrao " + new_dir))
                ###
                
            else:
                msg = QMessageBox()
                msg.setText("Não existe um padrão com esse registro.\n Por favor, escolha um nome de padrão existente.")
                msg.setWindowTitle("Atenção!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()   
                self.data_hora()
                if os.path.exists(self.pasta_log_imagens + self.data_atual):
                    print("Diretorio já existe")
                else:
                    os.mkdir(self.pasta_log_imagens + self.data_atual)
                cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                       "Erro na deleção do padrao. Motivo: nome não cadastrado.\n")
                self.log_escrita.close()
                numRows = self.tableWidget.rowCount()
                self.tableWidget.insertRow(numRows)
                # Add text to the row
                self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Erro na deleção do padrao. Motivo: nome não cadastrado"))
                
        else:
            msg = QMessageBox()
            msg.setText("Por favor, digite um nome de padrão que seja válido.       ")
            msg.setWindowTitle("Atenção!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            if os.path.exists(self.pasta_log_imagens + self.data_atual):
                print("Diretorio já existe")
            else:
                os.mkdir(self.pasta_log_imagens + self.data_atual)
            cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
            self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
            self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                   "Erro na deleção do padrao. Motivo: nome não preenchido.\n")
            self.log_escrita.close()
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            # Add text to the row
            self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
            self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
            self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Erro na deleção do padrao. Motivo: nome não preenchido"))
        
        print("Padrão deletado")
        
##########################################################################################
##########################################################################################
        
    def liga_desliga_camera_login(self, status):
        global existe_cadastro
        global primeiro_loop_camera_login
        existe_cadastro = 0
        primeiro_loop_camera_login = 0
        
        self.cria_listas_de_indices()
        self.existe_cadastro_login()
        if  existe_cadastro == 1:
            print("######################## existe_cadastro == 1")
            if self.btn_camera_login.text() == 'Ativar Câmera':
                self.nomeUsuario_cadastro.setText("")
                print("######################## ligou a camera")
                #self.cria_listas_de_indices()
                self.timer.timeout.connect(self.update_frame)
                self.ativa_camera()
                self.timer.start(5)
                self.btn_camera_login.setText('Desativar Câmera')          
                self.status_camera = True
                self.groupBox_Cadastro.setEnabled(False)
                self.nomeUsuario_login.setEnabled(False)
                
                #self.escreve_na_imagem()
                #self.existe_cadastro_login()
            else:
                print("######################## desligou a camera login")
                self.image = cv2.imread('transparente.png')
                self.image = cv2.resize(self.image, (640,480))
                self.display_image(self.image, 1)
                self.desativa_camera()
                self.timer.stop()
                self.btn_camera_login.setText('Ativar Câmera')
                self.status_camera = False
                self.groupBox_Cadastro.setEnabled(True)
                self.nomeUsuario_login.setEnabled(True)
                self.nomeUsuario_login.setText("")
        else:
            msg = QMessageBox()
            msg.setText("Padrão não cadastrado.")
            msg.setWindowTitle("Atenção!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

##########################################################################################
##########################################################################################
            
    def liga_desliga_camera_cadastro(self, status):
        
        if status:
            self.nomeUsuario_login.setText("")
            #self.btn_camera_login_2.hide()
            self.cria_listas_de_indices()
            #self.capture = cv2.VideoCapture(0)
            #self.capture = cv2.VideoCapture('http://192.168.137.33:4747/video')
            #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.ativa_camera()
            self.timer.start(5)
            self.btn_camera.setText('Desativar Câmera')          
            self.status_camera = True
            self.btn_grava_senha.setEnabled(True)
            self.groupBox_Login.setEnabled(False)
            self.existe_cadastro_cadastro()
        else:
            #self.btn_camera_login_2.show()
            print("######################## desligou a camera cadastro")
            self.image = cv2.imread('transparente.png')
            self.image = cv2.resize(self.image, (640,480))
            self.display_image(self.image, 1)
            self.desativa_camera()
            self.timer.stop()
            self.btn_camera.setText('Ativar Câmera')
            self.status_camera = False
            self.groupBox_Login.setEnabled(True)           
            self.btn_grava_senha.setEnabled(False)           
            self.nomeUsuario_cadastro.setText("")
            
##########################################################################################
##########################################################################################    
    
    def cria_listas_de_indices(self):
        pasta_atual = "C:\\Users\\Henrique Pereira\\Python\\TCC\\00_API_SEGURANCA\\cadastro_usuarios\\*"
        global lista_matriz_das_imagens_na_pasta
        global nome_das_subpastas
        global indices_das_imagens
        i = 0 #indice a ser adicionado na lista de indices das imagens
        #i2 = 0 #indice para salvar imagens de teste com nomes diferentes
        #i3 = 0
        
        lista_matriz_das_imagens_na_pasta.clear()
        nome_das_subpastas.clear()
        indices_das_imagens.clear()
        
        for diretorios in glob.glob(pasta_atual): #laço que percorre as subpastas dentro do diretório descrito na variável pasta_atual
            nome_da_subpasta = os.path.basename(diretorios) #lê o nome da subpasta a ser explorada e atribui à variável nome_da_pasta
            nome_das_subpastas.append(nome_da_subpasta) #adiciona o nome da subpasta à lista nome_das_subpastas
            for nome_imagem_na_pasta in glob.glob(diretorios+'\*.*'):  #laço que percorre as imagens presentes dentro de cada subpasta
                imagem_pasta = cv2.imread(nome_imagem_na_pasta, 0) #lê cada uma das imagens constantes na subpasta e converte a imagem para preto/branco
                #imagem_recortada = detecta_rosto(imagem_pasta) #chama função para selecionar apenas o rosto na imagem modelo
                lista_matriz_das_imagens_na_pasta.append(imagem_pasta) #adiciona o vetor da imagem para a lista
                indices_das_imagens.append(i) #adiciona o índice atual à lista de indices para vincular aos nomes das pessoas
            print(nome_da_subpasta)
            
            i += 1

        #chama função para ajustar o tamanho das imagens modelo para a altura e largura média encontrada entre elas
        #lista_matriz_das_imagens_alteradas_na_pasta, largura_media_imagens_modelo = ajusta_tamanho_das_imagens_de_modelo(lista_matriz_das_imagens_na_pasta)

##########################################################################################
##########################################################################################    
    
    def existe_cadastro_login(self):
        global existe_cadastro
        global primeiro_loop_camera_login
        existe_cadastro = 0
        nome_usuario = self.nomeUsuario_login.toPlainText()
        
        for nome_subpasta in nome_das_subpastas:
            if nome_subpasta == nome_usuario:
                existe_cadastro = 1
                print(existe_cadastro)
                print(nome_usuario)
                print(nome_subpasta)
     
    #def escreve_na_imagem(self):
        #if existe_cadastro == 1:
        if ((len(self.nomeUsuario_login.toPlainText()) != 0) and (primeiro_loop_camera_login != 0)):
            #self.cria_listas_de_indices()
            #self.existe_cadastro_login()
            #self.escreve_na_imagem()
            self.display_image(self.image, 1)
            self.calcula_erro_euclidiano()
        
        primeiro_loop_camera_login = primeiro_loop_camera_login + 1
        
##########################################################################################        
        
    def existe_cadastro_cadastro(self):
        global existe_cadastro
        existe_cadastro = 0
        nome_usuario = self.nomeUsuario_cadastro.toPlainText()
        
        for nome_subpasta in nome_das_subpastas:
            if nome_subpasta == nome_usuario:
                existe_cadastro = 1
                #print(existe_cadastro)
                #print(nome_usuario)
                #print(nome_subpasta)
        
##########################################################################################
##########################################################################################      
        
    def update_frame(self):
        ret, self.image = capture.read()
        #self.image = cv2.flip(self.image, 1)
        
        #img_preto_branco = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) 
        
        #face = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml').detectMultiScale(img_preto_branco,1.3,5)

        #for (x, y, w, h) in face:
        #    cv2.circle(self.image, (int(x+w*.5),int(y+h*.6)), int(w*.5), (0,255,255), 2) 
        
        self.display_image(self.image, 1)
        self.existe_cadastro_login()
        self.existe_cadastro_cadastro()
               
##########################################################################################
##########################################################################################
        
    def display_image(self, img, window = 1):
        
        qformat = QImage.Format_Indexed8
        
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
                #print("4")
            else:
                qformat = QImage.Format_RGB888
                #print("4 else")
        #qformat = QImage.Format_RGB888
        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        
        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
    

##########################################################################################
##########################################################################################
            
    def calcula_erro_euclidiano(self):
        global nome_das_subpastas, indices_das_imagens, lista_matriz_das_imagens_na_pasta
        resultado = 0
        indice_resposta = 999999999999
        acerto_porcentagem = 0
        new_dir = self.nomeUsuario_login.toPlainText()
        #imagem_webcam = cv2.resize(imagem_webcam, (largura_media_imagens_modelo, largura_media_imagens_modelo))
        
        resultado = 0
        i = 0
        menor = 9999999999999999999
        
        #total = largura_media_imagens_modelo * largura_media_imagens_modelo * 255
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        for img in lista_matriz_das_imagens_na_pasta:
            resultado = np.absolute(np.array(image.astype(int)) - np.array(img.astype(int)))
            erro = sum(sum(resultado))
            #percentual_acerto_euclidiano = 100 - ((erro / total) * 100)
            if erro < menor:
                menor = erro
                indice_resposta = i
            i += 1
        
        acerto_porcentagem = 100-(menor/((640*480)*255))*100
        print("##\n "+ str(acerto_porcentagem) + "\n " +nome_das_subpastas[indices_das_imagens[indice_resposta]] +"\n##")
        if acerto_porcentagem > 92:
            if nome_das_subpastas[indices_das_imagens[indice_resposta]] == self.nomeUsuario_login.toPlainText():
                
                #segundo_atual = datetime.datetime.now()
                
                #diferenca_tempo_beep = (self.segundo_do_beep - segundo_atual).seconds
                #print(diferenca_tempo_beep)
                
                if self.flag == 0:
                    b = winsound.Beep
                    b(5000,100)
                    #self.segundo_do_beep = datetime.datetime.now()
                    self.flag = 1
                
                    #self.nomeUsuario_login.setText("")                
                    #self.image = cv2.imread('transparente.png')
                    #self.image = cv2.resize(self.image, (640,480))
                    #self.display_image(self.image, 1)
                    #self.desativa_camera()
                    #self.timer.stop()
                    #self.btn_camera_login.setText('Ativar Câmera')
                    #self.status_camera = False
                    #self.groupBox_Cadastro.setEnabled(True)
                    #self.nomeUsuario_login.setEnabled(True)
                    #self.nomeUsuario_login.setText("")
                    self.data_hora()
                    if os.path.exists(self.pasta_log_imagens + self.data_atual):
                        print("Login com sucesso")
                    else:
                        os.mkdir(self.pasta_log_imagens + self.data_atual)
                    cv2.imwrite(self.pasta_log_imagens + self.data_atual + '\\' + self.hora_atual + '.png', self.image)
                    self.log_escrita = open("log\\registros\\log_de_atividades.txt", "a")
                    self.log_escrita.write(str(self.data_atual) +";"+ str(self.hora_atual)+";"+ \
                                           "Login realizado com sucesso. Padrao: " + new_dir +"\n")
                    self.log_escrita.close()
                    numRows = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(numRows)
                    # Add text to the row
                    self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.data_atual)))
                    self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.hora_atual)))
                    self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem("Login realizado com sucesso. Padrao: " + new_dir))
                    #time.sleep(3)
            else:
                self.flag = 0
        else:
            self.flag = 0
            
                
##########################################################################################
##########################################################################################
                
    def desativa_camera(self):
        global capture
        
        capture.release()
        
    def ativa_camera(self):
        global capture
        
        capture = cv2.VideoCapture('http://192.168.137.44:4747/video')
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

if __name__ == '__main__':

    lista_matriz_das_imagens_na_pasta = [] # lista para armazenar a matriz de cada imagem lida nas pastas e subpastas
    nome_das_subpastas = [] #lista para armazenar os nomes das subpastas
    indices_das_imagens = [] #indice das imagens que relaciona o nome de cada pessoa com a matriz da imagem
    existe_cadastro = 0
    primeiro_loop_camera_login = 0
    
    app = QApplication(sys.argv)
    window = interface()
    window.setWindowTitle('Controle de Acesso')
    window.show()
    sys.exit(app.exec_())

    
   