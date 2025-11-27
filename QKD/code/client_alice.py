# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 15:54:38 2025

@author: python
"""

import socket
import binascii

def bin_ascii_conv(mex_to_conv):
    
    int_mex = int.from_bytes(mex_to_conv.encode())
    
    return int_mex

def read_key():
    path = 'C:\\Users\\python\\Desktop\\AuthenticationKey.dat'
    with open(path, 'r') as file:
        for line in file:
            key = line.strip()
            key = int(key, 2)
    return key

def read_otp():
    path = 'C:\\Users\\python\\Desktop\\keys\\0b0a1da4-142f-486c-b9b4-4d75b1f713d1.key'
    with open(path, 'rb') as file:
        for line in file:
            key = line.strip()
            key = int(key, 2)
    return key

def authenticate(password):
 
    int_pwd = bin_ascii_conv(password)
    
    key = read_key()
    
    encr = int_pwd ^ key
    
    auth_bytes = message.to_bytes(len(password) + 1)
    
    return auth_bytes

def encrypt(message):
 
    int_mes = bin_ascii_conv(message)
    
    key = read_otp()
    
    encr = int_mes ^ key
    
    encr_bytes = message.to_bytes(len(message) + 1)
    
    return encr_bytes


def client_program():
    host = '10.39.10.20'
    port = 1604  # socket server port number
    
    otp_name = '0b0a1da4-142f-486c-b9b4-4d75b1f713d1.key'

    #client_socket = socket.socket()  # instantiate
    #client_socket.connect((host, port))  # connect to the server
    
    
    message = input(" -> ")  # take input

    #client_socket.send(authenticate(password))
    
    #client_socket.send(otp_name.encode())
    
    print(otp_name.encode())
    
    #client_socket.send(encrypt(message))
    
    print(encrypt(message))
    
    data = client_socket.recv(1024).decode()  # receive response

    print('Received from server: ' + data)  # show in terminal
    
    return

    
    while password.lower().strip() != 'bye':
        #client_socket.send(message.encode())  # send message
        print("sto mandando")
        client_socket.send(prova)  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()