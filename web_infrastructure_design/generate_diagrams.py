from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx, HAProxy
from diagrams.onprem.database import MySQL
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.generic.network import Firewall
from diagrams.generic.os import Ubuntu
from diagrams.aws.network import Route53
from diagrams.saas.chat import Discord
from diagrams.generic.device import Mobile
from diagrams.generic.blank import Blank

# Task 0 - Simple Web Stack
with Diagram("Task_0_Simple_Web_Stack", show=False, filename="task0_simple_web_stack", direction="TB", graph_attr={"pad": "0.5", "nodesep": "0.6", "ranksep": "1.2"}):
    user = Mobile("User Browser")
    dns = Route53("DNS\nwww.foobar.com\nA → 8.8.8.8")
    
    with Cluster("Server (8.8.8.8)"):
        nginx = Nginx("Nginx\nWeb Server")
        app = Server("Application\nServer")
        code = Ubuntu("Application\nFiles (Code)")
        db = MySQL("MySQL\nDatabase")
        
    user >> Edge(label="HTTP") >> dns >> Edge(label="TCP/IP") >> nginx >> app >> db
    code >> Edge(style="dashed") >> app

# Task 1 - Distributed Web Infrastructure
with Diagram("Task_1_Distributed", show=False, filename="task1_distributed", direction="TB", graph_attr={"pad": "0.5", "nodesep": "0.6", "ranksep": "1.2"}):
    user = Mobile("User Browser")
    dns = Route53("DNS\nwww.foobar.com")
    lb = HAProxy("HAproxy\nLoad Balancer\nRound Robin")
    
    with Cluster("Server 1"):
        nginx1 = Nginx("Nginx")
        app1 = Server("App Server")
        code1 = Ubuntu("App Files")
        
    with Cluster("Server 2"):
        nginx2 = Nginx("Nginx")
        app2 = Server("App Server")
        code2 = Ubuntu("App Files")
        
    with Cluster("Database"):
        primary = MySQL("MySQL\nPrimary (Write)")
        replica = MySQL("MySQL\nReplica (Read)")
        primary >> Edge(style="dashed", label="Replication") >> replica
        
    user >> dns >> lb
    lb >> Edge(label="Active-Active") >> nginx1 >> app1 >> primary
    lb >> Edge(label="Active-Active") >> nginx2 >> app2 >> primary
    
    app1 >> Edge(style="dashed") >> replica
    app2 >> Edge(style="dashed") >> replica
    code1 >> Edge(style="dashed") >> app1
    code2 >> Edge(style="dashed") >> app2

# Task 2 - Secured and Monitored
with Diagram("Task_2_Secured_Monitored", show=False, filename="task2_secured_monitored", direction="TB", graph_attr={"pad": "0.5", "nodesep": "0.6", "ranksep": "1.2"}):
    user = Mobile("User Browser")
    dns = Route53("DNS")
    fw1 = Firewall("Firewall 1")
    lb = HAProxy("HAproxy\nSSL / HTTPS")
    
    with Cluster("Server 1"):
        nginx1 = Nginx("Nginx")
        app1 = Server("App Server")
        code1 = Ubuntu("App Files")
        mon1 = Grafana("Monitoring\nClient")
        
    with Cluster("Server 2"):
        nginx2 = Nginx("Nginx")
        app2 = Server("App Server")
        code2 = Ubuntu("App Files")
        mon2 = Grafana("Monitoring\nClient")
        
    with Cluster("Database"):
        fw2 = Firewall("Firewall 3")
        db = MySQL("MySQL")
        mon3 = Grafana("Monitoring\nClient")
        
    user >> dns >> fw1 >> lb
    
    with Cluster("", graph_attr={"pencolor": "transparent"}):
        fw_app = Firewall("Firewall 2")
        lb >> fw_app
        fw_app >> nginx1 >> app1 >> fw2 >> db
        fw_app >> nginx2 >> app2 >> fw2
        
    code1 >> Edge(style="dashed") >> app1
    code2 >> Edge(style="dashed") >> app2
    mon1 >> Edge(style="dotted") >> nginx1
    mon2 >> Edge(style="dotted") >> nginx2
    mon3 >> Edge(style="dotted") >> db

# Task 3 - Scale Up
with Diagram("Task_3_Scale_Up", show=False, filename="task3_scale_up", direction="TB", graph_attr={"pad": "0.5", "nodesep": "0.8", "ranksep": "1.5"}):
    user = Mobile("User Browser")
    dns = Route53("DNS")
    fw1 = Firewall("Firewall")
    
    with Cluster("Load Balancer Cluster"):
        lb1 = HAProxy("HAproxy 1")
        lb2 = HAProxy("HAproxy 2")
        lb1 >> Edge(style="dashed", label="Cluster") << lb2
        
    fw2 = Firewall("Firewall")
    
    with Cluster("Separated Tiers"):
        web = Nginx("Web Server\nNginx")
        app = Server("Application\nServer")
        db = MySQL("Database\nMySQL")
        
    user >> dns >> fw1 >> lb1
    lb1 >> fw2 >> web >> app >> db
    lb2 >> fw2

print("4 diagrams generated: task0_simple_web_stack.png, task1_distributed.png, task2_secured_monitored.png, task3_scale_up.png")
