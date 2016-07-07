#!/bin/bash

echo "Digite o número da tabela novamente: "
read tabela
echo "Digite o número do fluxo novamente: "
read fluxo

#Comando para criar os fluxos de acordo com as regras passadas no arquivo regras.xml.
#O campo 'openflow:8796754962842' é referente ao SwitchVirtual conectado ao controlador.

curl -X PUT -d @regras.xml -H "Content-Type: application/xml" -H "Accept: application/xml" --user "admin":"admin" http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:8796754962842/flow-node-inventory:table/$tabela/flow/$fluxo
