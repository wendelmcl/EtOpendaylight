# Autor: Francisco Wendel de Lima Maciel
# Data: 06/07/2016
# Linguagem: Python

#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
import time
import os
import sys
import string
import MySQLdb
import commands
import urllib2
import pycurl
import subprocess
from xml.dom import minidom
from xml.dom.minidom import Document
from xml.dom.minidom import parse
from codecs import open

i=int(1)
j=int(1)

#Função das opções do Usuário
def opcaoUsuario():
    opcao = int(raw_input("\nEscolha sua opcao: \n 1 - Cliente \n 2 - Gateway \n 3 - Inserir fluxo \n 4 - Listar fluxos\n 5 - Excluir fluxos \n 6 - Sair\n\n"))
    try:
        opcao = int(opcao)
        if opcao<1 or opcao>6:
            os.system("clear");
            print "Opção inválida!"
            time.sleep(2)
            opcaoUsuario()
    except:
        os.system("clear");
        print "Opção inválida!"
        time.sleep(2)
        opcaoUsuario()

    if opcao == 1:
        op=int(raw_input("\nEscolha sua opção \n 1 - Listar os Clientes \n 2 - Adicionar um Cliente \n 3 - Atualizar Cliente \n 4 - Deletar Cliente \n 5 - Sair:\n \n"))

        if op==1:
            conecta = conectaBanco()
            listarCliente(conecta)

        elif op==2:
            conecta = conectaBanco()
            inserirCliente(conecta)

        elif op==3:
            conecta = conectaBanco()
            atualizarCliente(conecta)

        elif op==4:
            conecta = conectaBanco()
            deletarCliente(conecta)
        
        elif op==5:
            opcaoUsuario()

    elif opcao == 2:
        op2 =  int(raw_input("\nEscolha sua opção: \n 1 - Listar os Gateways \n 2 - Adicionar um Gateway \n 3 - Atualizar Gateway \n 4 - Deletar Gateway: \n 5 - Sair \n \n"))

        if op2==1:
            conecta = conectaBanco()
            listarGateway(conecta)

        elif op2==2:
            conecta = conectaBanco()
            inserirGateway(conecta)

        elif op2==3:
            conecta = conectaBanco()
            atualizarGateway(conecta)

        elif op2==4:
            conecta = conectaBanco()
            deletarGateway(conecta)
        
        elif op2==5:
            opcaoUsuario()

    elif opcao == 3:
        conecta = conectaBanco()
        opcaoFluxo(conecta)

    elif opcao==4:
        os.system('sudo ovs-ofctl -O Openflow13 dump-flows br0')
        opcaoUsuario()

    elif opcao==5:
        tabela = raw_input("Digite a tabela do fluxo a ser excluído: ")
        os.system('sudo ovs-ofctl -O Openflow13 del-flows br0 table='+tabela)
        opcaoUsuario()

    elif opcao == 6:
        sys.exit()

#Função para conectar ao Banco.
def conectaBanco():
    try:
        conecta = MySQLdb.connect(host="127.0.0.1", user="root", passwd="admin", db="projeto")
        cursor = conecta.cursor()
 
    except MySQLdb.Error, e:
        print "Erro: O banco especificado não foi encontrado...",e
        menu = raw_input()
        os.system("clear")
        opcaoUsuario()
 
    return conecta

########################## Cliente ##########################

def listarCliente(conecta):
    cursor = conecta.cursor()
    sql="SELECT * FROM projeto.cliente"

    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print "--------------------------------------------------"
        print "| ID  Nome  	      MAC                        |"
        print "--------------------------------------------------"
        for row in cursor.fetchall():
            print " ",row[0]," ",row[1]," ",row[2]
        conecta.commit()
 
    except MySQLdb.Error, e:
         print "Erro: " + sql
         print e
    conecta.close()
    opcaoUsuario()

def inserirCliente(conecta):
    ide=raw_input("Escreva o ID do Cliente: ")
    nome=raw_input("Escreva o nome do Cliente: ")
    mac=raw_input("Escreva o MAC do Cliente: ")
    cursor = conecta.cursor()
 
    sql="INSERT INTO projeto.cliente (id,nome,mac) VALUES ('"+ide+"','"+nome+"','"+mac+"')"
 
    try:
        cursor.execute(sql)
        conecta.commit()

    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e
 
    print "\nCliente inserido com sucesso!"
    conecta.close()
    menu = raw_input()
    os.system("clear")
    opcaoUsuario()

def atualizarCliente(conecta):
    cursor = conecta.cursor()
    ide = (raw_input("Digite o ID do Cliente que você deseja atualizar: "))
    cursor.execute("SELECT * FROM projeto.cliente WHERE id='"+ide+"'")
    numrows = int(cursor.rowcount)
    print "--------------------------------------------------"
    print "| ID  Nome  	      MAC                        |"
    print "--------------------------------------------------"
    for row in cursor.fetchall():
        print " ",row[0]," ",row[1]," ",row[2]
    nome=raw_input("\nEscreva o novo nome do Cliente: ")
    mac=raw_input("\nEscreva o novo MAC do Cliente: ")
    sql="UPDATE projeto.cliente SET nome='"+nome+"', mac='"+mac+"' WHERE id='"+ide+"'"
    try:
        cursor.execute(sql)
        conecta.commit()
 
    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e
 
    print "\nCliente alterado com sucesso."
    conecta.close()
    os.system("clear")
    opcaoUsuario()

def deletarCliente(conecta):
    cursor = conecta.cursor()
    cursor.execute("SELECT * FROM projeto.cliente")
    numrows = int(cursor.rowcount)
    print "--------------------------------------------------"
    print "| ID  Nome  	      MAC                        |"
    print "--------------------------------------------------"
    for row in cursor.fetchall():
        print " ",row[0]," ",row[1]," ",row[2]
    ide = raw_input("\nDigite o ID do Cliente que você deseja excluir: ")
    sql="DELETE FROM projeto.cliente WHERE id='"+ide+"'"
    try:
        cursor.execute(sql)
        conecta.commit()
 
    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e
 
    print "\nCliente excluído com Sucesso.\n"
    conecta.close()
    opcaoUsuario()

########################## Gateway ##########################

def listarGateway(conecta):
    cursor = conecta.cursor()
    sql="SELECT * FROM projeto.gateway"

    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print "--------------------------------------------------"
        print "| ID  Nome  	      MAC                        |"
        print "--------------------------------------------------"
        for row in cursor.fetchall():
            print " ",row[0]," ",row[1]," ",row[2]
        conecta.commit()
 
    except MySQLdb.Error, e:
         print "Erro: " + sql
         print e
    conecta.close()
    opcaoUsuario()

def inserirGateway(conecta):
    ide=raw_input("Escreva o ID do Gateway: ")
    nome=raw_input("Escreva o nome do Gateway: ")
    mac=raw_input("Escreva o MAC do Gateway: ")
    cursor = conecta.cursor()
 
    sql="INSERT INTO projeto.gateway (id,nome,mac) VALUES ('"+ide+"','"+nome+"','"+mac+"')"
 
    try:
        cursor.execute(sql)
        conecta.commit()

    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e
 
    print "\nGateway inserido com sucesso!"
    conecta.close()
    opcaoUsuario()

def atualizarGateway(conecta):
    cursor = conecta.cursor()
    ide = (raw_input("Digite o ID do Gateway que você deseja atualizar: "))
    cursor.execute("SELECT * FROM projeto.gateway WHERE id='"+ide+"'")
    numrows = int(cursor.rowcount)
    print "--------------------------------------------------"
    print "| ID  Nome  	      MAC                        |"
    print "--------------------------------------------------"
    for row in cursor.fetchall():
        print " ",row[0]," ",row[1]," ",row[2]
    nome=raw_input("\nEscreva o novo nome do Gateway: ")
    mac=raw_input("\nEscreva o novo MAC do Gateway: ")
    sql="UPDATE projeto.gateway SET nome='"+nome+"', mac='"+mac+"' WHERE id='"+ide+"'"
    try:
        cursor.execute(sql)
        conecta.commit()
 
    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e
 
    print "\nGateway alterado com sucesso."
    conecta.close()
    opcaoUsuario()

def deletarGateway(conecta):
    cursor = conecta.cursor()
    cursor.execute("SELECT * FROM projeto.gateway")
    numrows = int(cursor.rowcount)
    print "--------------------------------------------------"
    print "| ID  Nome  	      MAC                        |"
    print "--------------------------------------------------"
    for row in cursor.fetchall():
        print " ",row[0]," ",row[1]," ",row[2]
    ide = raw_input("\nDigite o ID do Gateway que você deseja excluir: ")
    sql="DELETE FROM projeto.gateway WHERE id='"+ide+"'"
    try:
        cursor.execute(sql)
        conecta.commit()
 
    except MySQLdb.Error, e:
        print "Erro: " + sql
        print e
 
    print "\nGateway excluído com Sucesso.\n"
    conecta.close()
    opcaoUsuario()

####################CRIAR XML#########################

#Função para criar o .XML com as regras dos fluxos.
def criarXMLRegras(conecta):
    global i
    doc = parse('politicas.xml')
    xml = doc.documentElement
    policy=xml.getElementsByTagName('policy')
    cursor = conecta.cursor()
    print "Criando fluxos..."
    while i <= len((policy)):
        time.sleep(2)
        for politica in policy:
            if int(politica.getAttribute('id')) == i:
                protocolos=politica.getElementsByTagName('protocolo')
                for protocolo in protocolos:
                    if protocolo.firstChild.nodeValue == 'http':	
                        port="80"
                    elif protocolo.firstChild.nodeValue == 'ftp':
                        port="20"
                    elif protocolo.firstChild.nodeValue == 'ssh':
                        port="22"
		    elif protocolo.firstChild.nodeValue == 'telnet':	
                        port="23"
                    elif protocolo.firstChild.nodeValue == 'imap':
                        port="143"
                    elif protocolo.firstChild.nodeValue == 'pop':
                        port="110"
		    elif protocolo.firstChild.nodeValue == 'smtp':
                        port="25"
                    print "Porta: "+port
	        clientes=politica.getElementsByTagName('cliente')
                for cliente in clientes:
                    if cliente.firstChild.nodeValue == 'cliente1':
                        sql="SELECT mac FROM projeto.cliente WHERE nome='cliente1'"
                    elif cliente.firstChild.nodeValue == 'cliente2':
		        sql="SELECT mac FROM projeto.cliente WHERE nome='cliente2'"
		    elif cliente.firstChild.nodeValue == 'cliente3':
		        sql="SELECT mac FROM projeto.cliente WHERE nome='cliente3'"    
                try:
                    cursor.execute(sql)
                    numrows = int(cursor.rowcount)
                    for cliente in cursor.fetchall():
                        macC = cliente[0]
                        print "MAC do Cliente: "+macC
                    conecta.commit()
 
                except MySQLdb.Error, e:
                    print "Erro: " + sql
                    print e
            
                gateways=politica.getElementsByTagName('gateway')
                for gateway in gateways:
                    if gateway.firstChild.nodeValue == 'gateway1':
                        sql="SELECT mac FROM projeto.gateway WHERE nome='gateway1'"
                    elif gateway.firstChild.nodeValue == 'gateway2':
		        sql="SELECT mac FROM projeto.gateway WHERE nome='gateway2'"	    
                try:
                    cursor.execute(sql)
                    numrows = int(cursor.rowcount)
                    for gateway in cursor.fetchall():
                       macG = gateway[0]
                       print "MAC do Gateway: "+macG
                    conecta.commit()
 
                except MySQLdb.Error, e:
                     print "Erro: " + sql
                     print e

        root = minidom.Document()
        productChild = root.createElement('flow')
        productChild.setAttribute('xmlns', 'urn:opendaylight:flow:inventory')
        root.appendChild(productChild)

        idflow = root.createElement('id')
        idflow.appendChild(root.createTextNode(str(i)))
        productChild.appendChild(idflow)

        table_id = root.createElement('table_id')
        table_id.appendChild(root.createTextNode(str(i)))
        productChild.appendChild(table_id)

        priority = root.createElement('priority')
        priority.appendChild(root.createTextNode('1'))
        productChild.appendChild(priority)

        instructions = root.createElement('instructions')
        instruction = root.createElement('instruction')
        order0 = root.createElement('order')
        order0.appendChild(root.createTextNode('1'))
        instruction.appendChild(order0)

    	applyactions = root.createElement('apply-actions')

    	action = root.createElement('action')
    	order = root.createElement('order')
    	order.appendChild(root.createTextNode('1'))
    	outputaction = root.createElement('output-action')

    	outputnodeconnector = root.createElement('output-node-connector')
    	outputnodeconnector.appendChild(root.createTextNode('INPORT'))
    	maxlenght1 = root.createElement('max-length')
    	maxlenght1.appendChild(root.createTextNode('60'))
    	action.appendChild(order)
    	action.appendChild(outputaction)
    	outputaction.appendChild(outputnodeconnector)
    	outputaction.appendChild(maxlenght1)
    	applyactions.appendChild(action)
    	instruction.appendChild(applyactions)

    	instructions.appendChild(instruction)
    	productChild.appendChild(instructions)

    	match = root.createElement('match')
    	tcpSource = root.createElement('tcp-source-port')
    	tcpSource.appendChild(root.createTextNode('1'))
    	tcpDest = root.createElement('tcp-destination-port')
    	tcpDest.appendChild(root.createTextNode(port))
    	ethernetmatch = root.createElement('ethernet-match')
    	ethernettype = root.createElement('ethernet-type')
    	type1 = root.createElement('type')
    	type1.appendChild(root.createTextNode('2048'))

    	inport = root.createElement('in-port')
    	inport.appendChild(root.createTextNode('1'))

    	ethernetDest = root.createElement('ethernet-destination')
    	addressDest = root.createElement('address')
    	addressDest.appendChild(root.createTextNode(macG))
    	ethernetDest.appendChild(addressDest)

    	ethernetSour = root.createElement('ethernet-source')
    	addressSour = root.createElement('address')
    	addressSour.appendChild(root.createTextNode(macC))
    	ethernetSour.appendChild(addressSour)

    	ipmatch = root.createElement('ip-match')
    	ipprotocol = root.createElement('ip-protocol')
    	ipprotocol.appendChild(root.createTextNode('6'))

    	match.appendChild(ethernetmatch)
    	ethernettype.appendChild(type1)
    	ethernetmatch.appendChild(ethernettype)
    	ethernetmatch.appendChild(ethernetDest)
    	ethernetmatch.appendChild(ethernetSour)
    	ipmatch.appendChild(ipprotocol)
    	match.appendChild(ipmatch)
    	match.appendChild(tcpSource)
    	match.appendChild(tcpDest)
    	match.appendChild(inport)
    	productChild.appendChild(match)

    	xml_str = root.toprettyxml(indent="")

    	save_path_file = "regras.xml"
    	with open(save_path_file, "w") as f:
            f.write(xml_str)
        time.sleep(2)
	#Comando para gerar o fluxo através da leitura do arquivo regras.xml.
	#O campo "openflow:8796754962842" é referente ao SwitchVirtua conectado ao controlador.
	os.system('curl -X PUT -d @regras.xml -H "Content-Type: application/xml" -H "Accept: application/xml" --user "admin":"admin" http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:8796754962842/flow-node-inventory:table/'+str(i)+'/flow/'+str(i))
        #os.system('./script3.sh')
        time.sleep(2)
	#Retorno da criação do Fluxo. 200 OK ou Bad Request caso retorne outro valor.
        try:
            from io import BytesIO
        except ImportError:
            from StringIO import StringIO as BytesIO
        buffer = BytesIO()
        user_pwd = 'admin:admin'
        c = pycurl.Curl() 
        c.setopt(c.URL, 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:8796754962842/flow-node-inventory:table/'+str(i)+'/flow/'+str(i))
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/xml', 'Accept: application/xml'])
        c.setopt(pycurl.USERPWD, user_pwd)
        c.setopt(c.CUSTOMREQUEST, "GET")
        c.setopt(c.WRITEDATA, buffer)
        c.perform()

        if c.getinfo(c.RESPONSE_CODE)!=200:
            print('Status: %d Bad Request' % c.getinfo(c.RESPONSE_CODE))
        else:
       # HTTP response code, e.g. 200.
           print('Status: %d OK' % c.getinfo(c.RESPONSE_CODE))
       # Elapsed time for the transfer.
           print('Status: %f' % c.getinfo(c.TOTAL_TIME))
	#getinfo must be called before close.
        i=i+1   

####################CRIAR FLUXO DEFAULT#########################

def criarFluxoDefault(conecta):
    global j
    doc = parse('politicasDef.xml')
    xml = doc.documentElement
    policy=xml.getElementsByTagName('policy')
    cursor = conecta.cursor()
    polis=str(raw_input("Digite: default1, default2 ou default3: "))
    #while j <= len((policy)):
    time.sleep(2)
    for politica in policy:
        if str(politica.getAttribute('id'))==polis and polis=="default1":
            cliente="192.168.1.6"
	    porta="80"
	    gateway="08:00:27:35:2b:99"
            print cliente,"\n",gateway
	    os.system('sudo ovs-ofctl -O Openflow13 add-flow br0 priority=6,dl_type=0x0800,nw_proto=*,nw_src='+cliente+',actions=mod_dl_dst='+gateway+',in_port')
	    print "Fluxo Default adicionado com sucesso !"
		
	elif str(politica.getAttribute('id'))==polis and polis=="default2":
            cliente="192.168.1.7"
	    porta="110"
	    gateway="08:00:27:35:2b:99"
	    print cliente,"\n",gateway
	    os.system('sudo ovs-ofctl -O Openflow13 add-flow br0 priority=6,dl_type=0x0800,nw_proto=*,nw_src='+cliente+',actions=mod_dl_dst='+gateway+',in_port')
	    print "Fluxo Default adicionado com sucesso !"
		
	elif str(politica.getAttribute('id'))==polis and polis=="default3":
            cliente="192.168.1.8"
	    porta="25"
	    gateway="08:00:27:af:17:fd"
	    print cliente,"\n",gateway 
	    os.system('sudo ovs-ofctl -O Openflow13 add-flow br0 priority=6,dl_type=0x0800,nw_proto=*,nw_src='+cliente+',actions=mod_dl_dst='+gateway+',in_port')
	    print "Fluxo Default adicionado com sucesso !"
		
    	#else:
            #print "Opção incorreta!"
	    #menu=raw_input("")
	    #os.system("clear")
	    #criarDefault(conecta)
        #j=j+1
	#break
    opcaoUsuario()

####################CRIAR XML2#########################

def opcaoFluxo(conecta):
    doc = parse('politicas.xml')
    xml = doc.documentElement
    policy=xml.getElementsByTagName('policy')
    cursor = conecta.cursor()
    fs=raw_input("Digite sua opção:\n 1 - Para inserir fluxo manualmente:\n 2 - Para criar fluxo default:\n 3 - para Voltar: \n")
    if fs=="1":
        print "Lista de Clientes: \n"
        cursor = conecta.cursor()
        sql="SELECT * FROM projeto.cliente"

        try:
            cursor.execute(sql)
            numrows = int(cursor.rowcount)
            print "--------------------------------------------------"
            print "| ID  Nome  	      MAC                        |"
            print "--------------------------------------------------"
            for clientes in cursor.fetchall():
                print " ",clientes[0]," ",clientes[1]," ",clientes[2],"\n"
            conecta.commit()
 
        except MySQLdb.Error, e:
             print "Erro: " + sql
             print e

        print "Lista de Gateways: \n"
        cursor = conecta.cursor()
        sql="SELECT * FROM projeto.gateway"

        try:
            cursor.execute(sql)
            numrows = int(cursor.rowcount)
            print "--------------------------------------------------"
            print "| ID  Nome  	      MAC                        |"
            print "--------------------------------------------------"
            for gateways in cursor.fetchall():
                print " ",gateways[0]," ",gateways[1]," ",gateways[2],"\n"
            conecta.commit()
 
        except MySQLdb.Error, e:
            print "Erro: " + sql
            print e

        print "Lista de Protocolos: Http (Porta=80), Ftp: (Porta=20), Ssh: (porta=22), Telnet: (Porta=23), Imap: (Porta=143), Pop: (Porta=110), Smtp: (Porta=25) \n"
 
        cliente = raw_input("Digite o Mac do cliente: \n")
        gateway = raw_input("Digite o Mac do Gateway: \n")
        porta = raw_input("Digite a Porta: ")
 
        tabela = str(raw_input("Digite o número da tabela: "))
        fluxo = str(raw_input("Digite o número do fluxo: "))
        root = minidom.Document()
        productChild = root.createElement('flow')
        productChild.setAttribute('xmlns', 'urn:opendaylight:flow:inventory')
        root.appendChild(productChild)

        idflow = root.createElement('id')
        idflow.appendChild(root.createTextNode(fluxo))
        productChild.appendChild(idflow)

        table_id = root.createElement('table_id')
        table_id.appendChild(root.createTextNode(tabela))
        productChild.appendChild(table_id)

        priority = root.createElement('priority')
        priority.appendChild(root.createTextNode('1'))
        productChild.appendChild(priority)

        instructions = root.createElement('instructions')
        instruction = root.createElement('instruction')
        order0 = root.createElement('order')
        order0.appendChild(root.createTextNode('1'))
        instruction.appendChild(order0)

    	applyactions = root.createElement('apply-actions')

    	action = root.createElement('action')
    	order = root.createElement('order')
    	order.appendChild(root.createTextNode('1'))
    	outputaction = root.createElement('output-action')

    	outputnodeconnector = root.createElement('output-node-connector')
    	outputnodeconnector.appendChild(root.createTextNode('INPORT'))
    	maxlenght1 = root.createElement('max-length')
    	maxlenght1.appendChild(root.createTextNode('60'))
    	action.appendChild(order)
    	action.appendChild(outputaction)
    	outputaction.appendChild(outputnodeconnector)
    	outputaction.appendChild(maxlenght1)
    	applyactions.appendChild(action)
    	instruction.appendChild(applyactions)

    	instructions.appendChild(instruction)
    	productChild.appendChild(instructions)

    	match = root.createElement('match')
    	tcpSource = root.createElement('tcp-source-port')
    	tcpSource.appendChild(root.createTextNode('1'))
    	tcpDest = root.createElement('tcp-destination-port')
    	tcpDest.appendChild(root.createTextNode(porta))
    	ethernetmatch = root.createElement('ethernet-match')
    	ethernettype = root.createElement('ethernet-type')
    	type1 = root.createElement('type')
    	type1.appendChild(root.createTextNode('2048'))

    	inport = root.createElement('in-port')
    	inport.appendChild(root.createTextNode('1'))

    	ethernetDest = root.createElement('ethernet-destination')
    	addressDest = root.createElement('address')
    	addressDest.appendChild(root.createTextNode(gateway))
    	ethernetDest.appendChild(addressDest)

    	ethernetSour = root.createElement('ethernet-source')
    	addressSour = root.createElement('address')
    	addressSour.appendChild(root.createTextNode(cliente))
    	ethernetSour.appendChild(addressSour)

    	ipmatch = root.createElement('ip-match')
    	ipprotocol = root.createElement('ip-protocol')
    	ipprotocol.appendChild(root.createTextNode('6'))

    	match.appendChild(ethernetmatch)
    	ethernettype.appendChild(type1)
    	ethernetmatch.appendChild(ethernettype)
    	ethernetmatch.appendChild(ethernetDest)
    	ethernetmatch.appendChild(ethernetSour)
    	ipmatch.appendChild(ipprotocol)
    	match.appendChild(ipmatch)
    	match.appendChild(tcpSource)
    	match.appendChild(tcpDest)
    	match.appendChild(inport)
    	productChild.appendChild(match)
        conecta.close()

    	xml_str = root.toprettyxml(indent="")

    	save_path_file = "regras.xml"
    	with open(save_path_file, "w") as f:
            f.write(xml_str)
        time.sleep(2)
        os.system('./script3.sh')
        time.sleep(2)
        try:
            from io import BytesIO
        except ImportError:
            from StringIO import StringIO as BytesIO
        buffer = BytesIO()
        user_pwd = 'admin:admin'
        c = pycurl.Curl() 
        c.setopt(c.URL, 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:8796754962842/flow-node-inventory:table/'+tabela+'/flow/'+fluxo)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/xml', 'Accept: application/xml'])
        c.setopt(pycurl.USERPWD, user_pwd)
        c.setopt(c.CUSTOMREQUEST, "GET")
        c.setopt(c.WRITEDATA, buffer)
        c.perform()

        if c.getinfo(c.RESPONSE_CODE)!=200:
            print('Status: %d Bad Request' % c.getinfo(c.RESPONSE_CODE))
        else:
       # HTTP response code, e.g. 200.
           print('Status: %d OK' % c.getinfo(c.RESPONSE_CODE))
       # Elapsed time for the transfer.
           print('Status: %f' % c.getinfo(c.TOTAL_TIME))
       # getinfo must be called before close.
        c.close()
        opcaoUsuario()
    elif fs=="2":
	conecta = conectaBanco()
	criarFluxoDefault(conecta)
        opcaoUsuario()
    elif fs=="3":
        opcaoUsuario()

#os.system('sudo ovs-ofctl -O Openflow13 del-flows br0')
time.sleep(2)
#Chama a função criarXML para criar os fluxos automáticamente.
conecta = conectaBanco()
criarXMLRegras(conecta)
#Após criar os fluxos automaticamente, é chamada a função referente as opções do usuário.
opcaoUsuario()
