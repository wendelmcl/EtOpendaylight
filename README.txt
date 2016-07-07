# EtOpendaylight

############### INSTALAÇÃO DO CONTROLADOR OPENDAYLIGHT ###############

# sudo apt-get install openjdk-7-jdk

sudo mkdir -p /usr/local/apache-maven

wget http://ftp.wayne.edu/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz

sudo mv apache-maven-3.3.9-bin.tar.gz /usr/local/apache-maven

tar -xzvf /usr/local/apache-maven/apache-maven-3.3.9-bin.tar.gz -C /usr/local/apache-maven/

update-alternatives --install /usr/bin/mvn mvn /usr/local/apache-maven/apache-maven-3.3.9/bin/mvn 1

update-alternatives --config mvn

nano ~/.bashrc
Adicionar variaveis de ambiente
export M2_HOME=/usr/local/apache-maven/apache-maven-3.3.9
export MAVEN_OPTS="-Xms256m -Xmx512m" # Very important to put the "m" on the end
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-i386 # This matches sudo update-alternatives --config java

source ~/.bashrc

sudo apt-get install git

wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.3.4-Lithium-SR4/distribution-karaf-0.3.4-Lithium-SR4.tar.gz

tar -xzvf distribution-karaf-0.3.4-Lithium-SR4.tar.gz

cd distribution-karaf-0.3.4-Lithium-SR4

./bin/karaf

Caso a instalação aconteça corretamente, algo como o texto a seguir deve aparecer no terminal.

    ________                       ________                .__  .__       .__     __       
    \_____  \ ______   ____   ____ \______ \ _____  ___.__.|  | |__| ____ |  |___/  |_     
     /   |   \\____ \_/ __ \ /    \ |    |  \\__  \<   |  ||  | |  |/ ___\|  |  \   __\    
    /    |    \  |_> >  ___/|   |  \|    `   \/ __ \\___  ||  |_|  / /_/  >   Y  \  |      
    \_______  /   __/ \___  >___|  /_______  (____  / ____||____/__\___  /|___|  /__|      
            \/|__|        \/     \/        \/     \/\/            /_____/      \/          
                                                                                           

Hit '<tab>' for a list of available commands
and '[cmd] --help' for help on a specific command.
Hit '<ctrl-d>' or type 'system:shutdown' or 'logout' to shutdown OpenDaylight.

opendaylight-user@root>

Instalar as seguintes features:
feature:install odl-l2switch-switch-ui
feature:install odl-dlux-all
feature:install odl-restconf-all  
feature:install odl-aaa-authn  
feature:install odl-mdsal-apidocs
feature:install odl-netconf-mdsal
feature:install odl-openflowplugin-all
feature:install odl-netconf-connector-all

Para acessar o painel: http://<endereço ip>:8181/index.html

usuário e senha padrão: admin


############### INSTALAÇÃO DO SWITCH VIRTUAL - OPENVSWITCH ###############

1) Acessar o site:

https://launchpad.net/ubuntu/+source/openvswitch/2.1.3-0ubuntu1

Baixar 3 arquivos:

openvswitch_2.1.3.orig.tar.gz 	
openvswitch_2.1.3-0ubuntu1.debian.tar.xz 	
openvswitch_2.1.3-0ubuntu1.dsc 	

2) Instalar aplicações necessárias:

sudo apt-get install build-essential fakeroot dkms module-assistant dpkg-dev uuid-runtime autoconf automake libssl-dev dh-autoreconf python-all python-twisted-conch libtool debhelper python-qt4 python-zopeinterface hardening-wrapper 

linux-headers-3.2.0-24 linux-headers-3.2.0-24-virtual

3) Executar comando que cria o diretório e extrai o pacote:

dpkg-source -x openvswitch_2.1.3-0ubuntu1.dsc 

4) Contruir os .debs, verificando as dependências:

dpkg-buildpackage -rfakeroot -b

Instale todas as dependências que estiverem faltando.

5) Instalar OVS:

sudo dpkg -i openvswitch-common_2.1.3-0ubuntu1_amd64.deb
sudo dpkg -i openvswitch-switch_2.1.3-0ubuntu1_amd64.deb
sudo dpkg -i openvswitch-datapath-dkms_2.1.3-0ubuntu1_all.deb 
sudo dpkg -i openvswitch-datapath-source_2.1.3-0ubuntu1_all.deb

############### CRIAÇÃO DA BRIDGE ###############

sudo ovs-vsctl add-br <nome da bridge>
sudo ovs-vsctl add-port <nome da bridge> eth0
sudo ifconfig eth0 0
sudo ovs-vsctl show 

sudo ovs-vsctl set-manager tcp:127.0.0.1:6640
sudo ovs-vsctl list controller

#Conectando a bridge do OpenvSwitch ao Controlador
sudo ovs-vsctl set-controller <nome da bridge> tcp:127.0.0.1:6633

#Configurando o arquivo /etc/network/interfaces
auto <nome da bridge>
iface openflow inet static
address 192.168.2.2
netmask 255.255.255.0
bridge_ports eth0

#INSERINDO O PROTOCOLO NA BRIDGE SELECIONADA
sudo ovs-vsctl set bridge <nome da bridge> protocols=OpenFlow13

#VISUALIZANDO OS DADOS DAS BRIDGES CRIADAS
sudo ovs-vsctl show

#VISUALIZAR OS FLUXOS DA BRIDGE
ovs-ofctl dump-flows <nome da bridge>
ovs-ofctl dump-tables <nome da bridge>

#COMANDO NECESSÁRIO PARA AS MÁQUINAS GATEWAYS
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

############### CONFIGURAÇÃO DAS MÁQUINAS VIRTUAIS ###############
CONTROLADOR/OPENVSWITCH
auto eth0
iface eth0 inet static
address 192.168.2.2
netmask 255.255.255.0


GATEWAY 1
auto eth0
iface eth0 inet dhcp

auto eth1
iface eth1 inet static
address 192.168.2.3
netmask 255.255.255.0


GATEWAY2
auto eth0
iface eth0 inet dhcp

auto eth1
iface eth1 inet static
address 192.168.2.4
netmask 255.255.255.0


CLIENTE 1
auto eth0
iface eth0 inet static
address 192.168.2.5
netmask 255.255.255.0
gateway 192.168.2.2
dns-nameservers 8.8.8.8

CLIENTE 2
auto eth0
iface eth0 inet static
address 192.168.2.6
netmask 255.255.255.0
gateway 192.168.2.2
dns-nameservers 8.8.8.8

CLIENTE 3
auto eth0
iface eth0 inet static
address 192.168.2.7
netmask 255.255.255.0
gateway 192.168.2.2
dns-nameservers 8.8.8.8

