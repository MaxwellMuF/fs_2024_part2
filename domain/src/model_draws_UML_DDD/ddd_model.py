from diagrams import Diagram, Cluster, Edge
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.security import WAFFilteringRule
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.general import Users
from diagrams.aws.analytics import KinesisDataStreams

# Create the diagram
with Diagram("DDD Model for Application Domain", show=False, direction="TB"):
    # User Interaction Context
    with Cluster("User Interaction Context"):
        user = Users("Users")
        ui = SagemakerModel("UI")

        with Cluster("Pages"):
            page1 = EC2("Page 1")
            page2 = EC2("Page 2")
            page3 = EC2("Page 3")

        user >> Edge(label="Interacts with", color="green") >> ui
        ui >> Edge(label="Navigates to", color="green") >> page1
        ui >> Edge(label="Navigates to", color="green") >> page2
        ui >> Edge(label="Navigates to", color="green") >> page3

    # Event Management Context
    with Cluster("Event Management Context"):
        event_searching = WAFFilteringRule("Event Searching")
        event_rating = KinesisDataStreams("Event Rating")
        event_saving = RDS("Event Saving")
        event_filtering = WAFFilteringRule("Event Filtering")

        ui >> Edge(label="Search Events", color="blue") >> event_searching
        ui >> Edge(label="Apply User Filters", color="blue") >> event_filtering
        ui >> Edge(label="Rate Events", color="blue") >> event_rating
        ui >> Edge(label="Save Event Commands", color="blue") >> event_saving
