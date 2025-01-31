from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.general import Users
from diagrams.aws.management import Cloudwatch

# Create the diagram
with Diagram("Project UML Model", show=False, direction="LR"):
    # Entities
    user = Users("User")
    ui = EC2("User Interface")  # UI entity
    processed_data = Cloudwatch("Processed Data")  # Processed Data
    data_download = RDS("Data Downloader")  # Data Downloader

    # Relationships
    user >> Edge(label="Interacts with", color="blue") >> ui
    user << Edge(color="blue") << ui
    ui >> Edge(label="Fetches Data", color="green") >> processed_data
    processed_data >> Edge(label="Relies on", color="green") >> data_download
    processed_data >> Edge(label="Collects User Input", color="green", style="dashed") >> ui
