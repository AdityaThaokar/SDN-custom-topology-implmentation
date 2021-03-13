from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Host 
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def myNetwork():

    net = Mininet(topo=None, link=TCLink, build=False, ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0', controller=RemoteController, ip='127.0.0.1', protocol='tcp', port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, h1, bw = 50, loss = 3)
    net.addLink(s1, h2, bw = 100, delay='2ms', loss = 0)
    net.addLink(s4, h3, bw = 50, delay='2ms', loss = 0)
    net.addLink(s4, h4, bw = 100, loss = 2)
    
    net.addLink(s1, s2, bw = 90, loss = 2)
    net.addLink(s1, s3, bw = 90, delay='2ms', loss = 0)
    net.addLink(s4, s2, bw = 40, loss = 3)
    net.addLink(s4, s3, bw = 40, delay='2ms',loss = 0)
    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])

    info( '*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
