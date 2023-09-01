## This folder will contains the Azure function code.

## Note:

- Before deploying, be sure to update your requirements.txt file by running `pip freeze > requirements.txt`
- Known issue, the python package `psycopg2` does not work directly in Azure; install `psycopg2-binary` instead to use the `psycopg2` library in Azure

The skelton of the `__init__.py` file will consist of the following logic:

```
import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database

    try:
        # TODO: Get notification message and subject from database using the notification_id

        # TODO: Get attendees email and name

        # TODO: Loop through each attendee and send an email with a personalized subject

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection
```

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Web App* | Basic Tier; 1 B3 (4 Core(s), 7 GB RAM, 10 GB Storage) x 730 Hours; Linux OS | $51.83 |
| *Azure Postgres Database* | Flexible Server Deployment, General Purpose Tier, 1 D2s v3 (2 vCores) x 730 Hours (Pay as you go), 100 GiB Storage, 0 Provisioned IOPS, 0 GiB Additional Backup storage - LRS redundancy, without High Availability | $156.15 |
| *Azure Service Bus*   | Basic tier: 1 million messaging operations | $0.05 |
| *Azure Storage Account*   | Queue Storage, General Purpose V1, LRS Redundancy, 100 GB Capacity, 1,000 Queue Class 1 operations, 1,000 Queue Class 2 operations | $5.22 |
| *Azure Function*  | Consumption tier, Pay as you go, 1024 MB memory, 100 milliseconds execution time, 1,000 executions/mo | $0.00 |
| *Total* |                                     | $213.25 |

## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.

- The Web App with the Basic tier is compatible for this application:
   + It doesn't require a high-performance machine, so the Basic tier is sufficient.
   + The Basic tier supports autoscaling, allowing the application to scale and handle user load at peak times.
- The Azure Function with the Consumption tier is cost-effective:
   + We only pay for the actual execution time and resource consumption of your functions. We are not billed for idle time, making it a cost-effective option for sporadic or low-traffic workloads.
   + When used with Azure Service Bus, it allows sending notifications to attendees asynchronously, preventing HTTP timeouts in the traditional architecture.
- In the new Azure architecture, the impact comes from the Azure Postgres Database. Although it uses the General Purpose tier with 100 GiB storage, it has a significantly higher cost compared to other services.
