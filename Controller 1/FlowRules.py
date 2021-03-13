'''
Roll no : 2020H1030132P
referred documentation : https://openflow.stanford.edu/display/ONL/POX+Wiki.html
'''
from pox.core import core
from pox.lib.util import dpid_to_str
import pox.openflow.libopenflow_01 as of

log = core.getLogger()
s1_dpid=0
s2_dpid=0
s3_dpid=0
s4_dpid=0

'''
handle ConnectionUp :
fired in response to the establishment of a new control channel with a switch.
'''
def _handle_ConnectionUp(event):
	global s1_dpid, s2_dpid, s3_dpid, s4_dpid
	for swprt in event.connection.features.ports:
		if swprt.name == "s1-eth1":
			s1_dpid = event.connection.dpid
			print("s1_dpid=", s1_dpid)
		elif swprt.name == "s2-eth1":
			s2_dpid = event.connection.dpid
			print("s2_dpid=", s2_dpid)
		elif swprt.name == "s3-eth1":
			s3_dpid = event.connection.dpid
			print("s3_dpid=", s3_dpid)
		elif swprt.name == "s4-eth1":
			s4_dpid = event.connection.dpid
			print("s4_dpid=", s4_dpid)


'''
handle packetIn : 
Fired when the controller receives an OpenFlow packet-in messagefrom a switch, 
which indicates that a packet arriving at a switch port has either failed to match all entries in the table, 
or the matching entry included an action specifying to send the packet to the controller.
'''
def _handle_PacketIn(event):
	global s0_dpid, s1_dpid, s2_dpid, s3_dpid
	print("PacketIn: ", dpid_to_str(event.connection.dpid))
	dpid = event.connection.dpid
	inport = event.port
	packet = event.parsed
	if not packet.parsed:
		log.warning("%i %i ignoring unparsed packet", dpid, inport)

	if dpid==s1_dpid:
		#ofp_flow_mod is Flow table modification
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.match.dl_type = 0x0806
		msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))  
		event.connection.send(msg)
		
		#no traffic from h1 to h3
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_src = "10.0.0.1"
		msg.match.nw_dst = "10.0.0.3"
		#No action means bydefault drop []
		event.connection.send(msg)
		
		#HTTP flow from h1 to h4 via s2
		msg = of.ofp_flow_mod()
		msg.priority = 2
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.tp_dst = 80			#specifying http flow
		msg.match.nw_proto = 6          #and tcp protocol 
		msg.match.nw_src = "10.0.0.1"
		msg.match.nw_dst = "10.0.0.4"
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)
		
		#Non-HTTP flow from h1 to h4
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_src = "10.0.0.1"
		msg.match.nw_dst = "10.0.0.4"
		msg.actions.append(of.ofp_action_output(port = 4))
		event.connection.send(msg)
		
		#Flow from h2 to h3 via s3
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_src = "10.0.0.2"
		msg.match.nw_dst = "10.0.0.3"
		msg.actions.append(of.ofp_action_output(port = 4))
		event.connection.send(msg)
		
		#Remaining path h1,h3,h4 to h2
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_dst = "10.0.0.2"
		msg.actions.append(of.ofp_action_output(port = 2))
		event.connection.send(msg)	
		
		#Remaining path h2,h3,h4 to h1
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_dst = "10.0.0.1"
		msg.actions.append(of.ofp_action_output(port = 1))
		event.connection.send(msg)
		
		#shortest path from h2 to h4 via s2
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_src = "10.0.0.2"
		msg.match.nw_dst = "10.0.0.4"
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)


	elif dpid==s2_dpid:
		#forwarding from s1 to s4
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.in_port = 1
		msg.actions.append(of.ofp_action_output(port = 2 ))
		event.connection.send(msg)

		#forwarding from s4 to s1
		msg = of.ofp_flow_mod()
		msg.priority =10
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.in_port = 2
		msg.actions.append(of.ofp_action_output(port = 1 ))
		event.connection.send(msg)	
		

	elif dpid==s3_dpid:
		#forwarding from s1 to s4
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.in_port = 1
		msg.actions.append(of.ofp_action_output(port = 2 ))
		event.connection.send(msg)

		#forwarding from s4 to s1
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.in_port = 2
		msg.actions.append(of.ofp_action_output(port = 1 ))
		event.connection.send(msg)						
		

	elif dpid==s4_dpid:
		msg = of.ofp_flow_mod()
		msg.priority =1
		msg.match.dl_type = 0x0806
		msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))  #1
		event.connection.send(msg)
		
		#no traffic from h3 to h1
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_src = "10.0.0.3"
		msg.match.nw_dst = "10.0.0.1"
		#No action means bydefault drop []
		event.connection.send(msg)
		
		#HTTP flow from h4 to h1 via s2
		msg = of.ofp_flow_mod()
		msg.priority = 2
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.tp_dst = 80			#specifying http flow
		msg.match.nw_proto = 6          #and tcp protocol 
		msg.match.nw_src = "10.0.0.4"
		msg.match.nw_dst = "10.0.0.1"
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)
		
		#Non-HTTP flow from h4 to h1 via s3
		msg = of.ofp_flow_mod()
		msg.priority =10
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_src = "10.0.0.4"
		msg.match.nw_dst = "10.0.0.1"
		msg.actions.append(of.ofp_action_output(port = 4))
		event.connection.send(msg)	
		
		#Flow from h3 to h2 via s3
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_src = "10.0.0.3"
		msg.match.nw_dst = "10.0.0.2"
		msg.actions.append(of.ofp_action_output(port = 4))
		event.connection.send(msg)

		#Remaining path h1,h2,h4 to h3
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_dst = "10.0.0.3"
		msg.actions.append(of.ofp_action_output(port = 1))
		event.connection.send(msg)	
		
		#Remaining path h2,h3,h1 to h4
		msg = of.ofp_flow_mod()
		msg.priority =10
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_dst = "10.0.0.4"
		msg.actions.append(of.ofp_action_output(port = 2))
		event.connection.send(msg)
		
		#Shortest path from h4 to h2 via s2
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.idle_timeout = 90
		msg.hard_timeout = 120
		msg.match.dl_type = 0x0800
		msg.match.nw_src = "10.0.0.4"
		msg.match.nw_dst = "10.0.0.2"
		msg.actions.append(of.ofp_action_output(port = 3))
		event.connection.send(msg)


'''
launch :
Its the main method
'''				
def launch():
	core.openflow.addListenerByName("ConnectionUp",_handle_ConnectionUp)
	core.openflow.addListenerByName("PacketIn",_handle_PacketIn)
