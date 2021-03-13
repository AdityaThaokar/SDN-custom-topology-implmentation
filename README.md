# SDN-custom-topology-implmentation
## Tools Required for the implemntation : 
 1. Mininet
 2. POX 
 
 ## Topology :
 ![AssignmentTopo](https://user-images.githubusercontent.com/30742223/111028953-06a18280-8420-11eb-8347-f4df3681c224.png)
 
## How to run the topology ?
 1. Save CustomTopology.py in mininet/custom directory
 2. In new terminal, run it using command: python CustomTopology.py
 3. It will add the hosts, switches and a default controller.
 4. To terminate, use exit command 
 5. At last, clean using command:   sudo mn -c

## How to run the topology with controller 1 ?
 1. In new terminal run Controller1.py 
 2. Once it starts running, in another terminal run the topology file. 
 
 ## About Controller 1 : 
 It is a controller which pushes flow rules on switches to satisfy following traffic constraints :
 1.  No traffic should be allowed between H3 and H1.
 2.  The HTTP traffic between H4 and H1 should be routed through Switch S2 and any other traffic between H4 and H1 should be routed through Switch S3.
 3.  The traffic between H3 and H2 should be routed through Switch S3.
 4.  The traffic between remaining nodes should follow shortest path.
 
 ## About Controller 2 :
 Once the flow rules are pushed, create necessary traffic flows to calculate instantaneous bandwidth for the following:
 1. Measurement and printing the instantaneous bandwidth on the links connected to the Switch S2.

## About Controller 3 :
 1. Calculation of the packet loss count between the switches S4 and S1 for the HTTP traffic flow
     #### H4 ---S4 --- S2 --- S1 --- H1
 2. Calculation of the packet loss count between the switches S4 and S1 for the non-HTTP traffic flow
     #### H4 ---S4 --- S3 --- S1 --- H1
 
 
 
