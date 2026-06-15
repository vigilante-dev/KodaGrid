"""Batch 9: AWS, Azure, Google Cloud, Android Studio, Flutter, React Native, MySQL, Firebase, Dart"""
import textwrap
from django.core.management.base import BaseCommand
from academy.models import LearningPath, Lesson


def upsert(path, order, title, objective, content, exercise, quiz_q, project, notes, mins):
    qs = Lesson.objects.filter(learning_path=path, order=order)
    if qs.count() > 1:
        keep = qs.first().pk
        qs.exclude(pk=keep).delete()
        qs = Lesson.objects.filter(pk=keep)
    lesson = qs.first()
    if lesson:
        lesson.title = title; lesson.objective = objective
        lesson.content = content; lesson.exercise_prompt = exercise
        lesson.quiz_question = quiz_q; lesson.project_prompt = project
        lesson.notes = notes; lesson.estimated_minutes = mins
        lesson.save()
        return False
    Lesson.objects.create(
        learning_path=path, order=order, title=title, objective=objective,
        content=content, exercise_prompt=exercise, quiz_question=quiz_q,
        project_prompt=project, notes=notes, estimated_minutes=mins,
        slug=f"{path.slug}-lesson-{order}",
    )
    return True


class Command(BaseCommand):
    help = "Batch 9: populate placeholder lessons for cloud, mobile, database paths"

    def handle(self, *args, **options):
        created = updated = 0

        # ── AWS ──────────────────────────────────────────────────────────
        aws = LearningPath.objects.get(slug='aws')

        r = upsert(aws, 1,
            "AWS Core Services — IAM, EC2 & S3",
            "Understand AWS's global infrastructure, create IAM users and policies, launch EC2 instances, and manage files with S3.",
            textwrap.dedent("""\
            ## What is AWS?
            Amazon Web Services (AWS) is the world's largest cloud platform, offering 200+ services from data centres globally. You pay only for what you use — no upfront hardware costs.

            ## AWS Global Infrastructure
            - **Regions** — independent geographic areas (e.g. `us-east-1`, `eu-west-1`)
            - **Availability Zones (AZs)** — isolated data centres inside a region (minimum 3 per region)
            - **Edge Locations** — CDN nodes used by CloudFront

            ## Identity & Access Management (IAM)
            IAM controls *who* can do *what* in your AWS account.

            ### Key concepts
            | Concept | Description |
            |---|---|
            | Root account | Full access — never use for daily work |
            | IAM User | A named identity with long-term credentials |
            | IAM Group | Collection of users sharing the same permissions |
            | IAM Role | Temporary credentials assumed by services or users |
            | Policy | JSON document listing allowed/denied actions |

            ### Creating a least-privilege policy
            ```json
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Effect": "Allow",
                  "Action": ["s3:GetObject", "s3:PutObject"],
                  "Resource": "arn:aws:s3:::my-bucket/*"
                }
              ]
            }
            ```

            ## EC2 — Elastic Compute Cloud
            EC2 provides resizable virtual machines (instances).

            ### Launching an instance (AWS CLI)
            ```bash
            aws ec2 run-instances \\
              --image-id ami-0abcdef1234567890 \\
              --instance-type t3.micro \\
              --key-name my-key-pair \\
              --security-group-ids sg-0123456789abcdef0 \\
              --subnet-id subnet-0123456789abcdef0 \\
              --count 1
            ```

            ### Key EC2 concepts
            - **AMI** — Amazon Machine Image; the OS template
            - **Instance type** — CPU/RAM combination (t3.micro = 2 vCPU, 1 GB RAM — free tier eligible)
            - **Security Group** — stateful firewall at the instance level
            - **Key Pair** — SSH public/private key for login
            - **Elastic IP** — static public IPv4 address

            ## S3 — Simple Storage Service
            S3 stores objects (files) in **buckets**. It is globally unique, durable (11 nines), and infinitely scalable.

            ```bash
            # Create a bucket
            aws s3 mb s3://my-academy-bucket-2024

            # Upload a file
            aws s3 cp index.html s3://my-academy-bucket-2024/

            # List objects
            aws s3 ls s3://my-academy-bucket-2024/

            # Make a file public (for static website)
            aws s3 website s3://my-academy-bucket-2024/ \\
              --index-document index.html --error-document error.html
            ```

            ### S3 Storage Classes
            | Class | Use case |
            |---|---|
            | Standard | Frequently accessed data |
            | Standard-IA | Infrequent access, rapid retrieval |
            | Glacier | Long-term archival (minutes to hours retrieval) |
            | Intelligent-Tiering | Auto-moves objects between tiers |
            """),
            "Create an IAM user named `academy-dev` with only S3 read/write permissions. Then create a bucket, upload 3 files, and verify you can access them using the new user's credentials.",
            "What is the minimum number of Availability Zones in an AWS Region?\nA) 1  B) 2  C) 3  D) 5",
            "Host a static portfolio website on S3: enable static website hosting, upload an index.html and styles.css, configure a bucket policy for public read, and record the website endpoint URL.",
            "Always enable MFA on your root account immediately. Use IAM roles instead of access keys wherever possible — roles rotate credentials automatically.",
            55)
        created += r; updated += not r

        r = upsert(aws, 2,
            "AWS Networking, RDS & Lambda",
            "Design a VPC with public and private subnets, set up a managed RDS database, and build a serverless function with Lambda.",
            textwrap.dedent("""\
            ## Virtual Private Cloud (VPC)
            A VPC is a logically isolated network in AWS. You control IP ranges, subnets, routing, and security.

            ### VPC components
            | Component | Role |
            |---|---|
            | CIDR block | IP address range (e.g. `10.0.0.0/16`) |
            | Public subnet | Has route to Internet Gateway — for web servers |
            | Private subnet | No direct internet route — for databases |
            | Internet Gateway | Allows public subnet traffic to reach the internet |
            | NAT Gateway | Lets private subnet instances reach the internet (outbound only) |
            | Route Table | Rules mapping destination IPs to targets |
            | Security Group | Instance-level stateful firewall |
            | Network ACL | Subnet-level stateless firewall |

            ### Creating a VPC with two subnets (CLI)
            ```bash
            # VPC
            aws ec2 create-vpc --cidr-block 10.0.0.0/16

            # Public subnet
            aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24 \\
              --availability-zone us-east-1a

            # Private subnet
            aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.2.0/24 \\
              --availability-zone us-east-1b
            ```

            ## RDS — Relational Database Service
            RDS manages MySQL, PostgreSQL, MariaDB, Oracle, and SQL Server — AWS handles patching, backups, and failover.

            ```bash
            aws rds create-db-instance \\
              --db-instance-identifier academy-db \\
              --db-instance-class db.t3.micro \\
              --engine mysql \\
              --master-username admin \\
              --master-user-password SecurePass123! \\
              --allocated-storage 20 \\
              --no-publicly-accessible
            ```

            ### Connecting from EC2
            ```python
            import pymysql
            conn = pymysql.connect(
                host='academy-db.xxxx.us-east-1.rds.amazonaws.com',
                user='admin', password='SecurePass123!',
                database='myapp', port=3306
            )
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            print(cursor.fetchone())
            ```

            ## Lambda — Serverless Functions
            Lambda runs code without provisioning servers. You pay per invocation and duration (100ms increments).

            ```python
            # handler.py — simple Lambda function
            import json

            def lambda_handler(event, context):
                name = event.get('name', 'World')
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': f'Hello, {name} from Lambda!'})
                }
            ```

            ### Deploying with AWS CLI
            ```bash
            # Package
            zip function.zip handler.py

            # Create function
            aws lambda create-function \\
              --function-name hello-academy \\
              --runtime python3.12 \\
              --handler handler.lambda_handler \\
              --role arn:aws:iam::123456789:role/lambda-role \\
              --zip-file fileb://function.zip

            # Invoke
            aws lambda invoke \\
              --function-name hello-academy \\
              --payload '{"name":"Student"}' \\
              response.json
            ```

            ### Lambda + API Gateway
            Combining Lambda with API Gateway creates a fully serverless REST API with no server management.
            """),
            "Build a VPC with one public and one private subnet. Place an EC2 web server in the public subnet and an RDS instance in the private subnet. Verify the web server can reach the database but the database is not reachable from the internet.",
            "Which AWS service lets private subnet instances reach the internet for updates without being reachable from the internet?\nA) Internet Gateway  B) VPC Peering  C) NAT Gateway  D) VPN Gateway",
            "Build a serverless contact form: API Gateway POST endpoint triggers a Lambda function that validates input and saves it to a DynamoDB table. Return a JSON success/error response.",
            "Place databases in private subnets and never expose RDS publicly. Use parameter groups to tune database settings without manual configuration.",
            60)
        created += r; updated += not r

        r = upsert(aws, 3,
            "Project: Deploy a Full-Stack App on AWS",
            "Deploy a Django app on EC2 behind an Application Load Balancer, store uploads on S3, and use RDS for the database — following AWS Well-Architected principles.",
            textwrap.dedent("""\
            ## Project Architecture
            ```
            Internet
                |
            Route 53 (DNS)
                |
            CloudFront (CDN + HTTPS)
                |
            Application Load Balancer
               /    \\
            EC2 AZ-a  EC2 AZ-b   (Auto Scaling Group)
               |
            RDS Multi-AZ (MySQL)
               |
            S3 (media uploads, static files)
            ```

            ## Step 1 — Prepare the Application
            ```bash
            # On your EC2 instance
            sudo apt update && sudo apt install python3-pip nginx -y
            pip install django gunicorn psycopg2-binary boto3 whitenoise

            # settings.py — use environment variables for secrets
            import os
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': os.environ['DB_NAME'],
                    'USER': os.environ['DB_USER'],
                    'PASSWORD': os.environ['DB_PASSWORD'],
                    'HOST': os.environ['DB_HOST'],
                }
            }
            AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET']
            DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
            ```

            ## Step 2 — Gunicorn + Nginx
            ```nginx
            # /etc/nginx/sites-available/academy
            server {
                listen 80;
                server_name _;
                location /static/ { alias /home/ubuntu/academy/staticfiles/; }
                location / {
                    proxy_pass http://127.0.0.1:8000;
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                }
            }
            ```
            ```bash
            gunicorn config.wsgi:application --workers 3 --bind 0.0.0.0:8000 --daemon
            ```

            ## Step 3 — Auto Scaling Group + ALB
            - Create a Launch Template with your AMI
            - Create a Target Group pointing to port 80
            - Create an ALB in two public subnets
            - Attach the Target Group to the ALB
            - Create Auto Scaling Group: min=2, desired=2, max=6

            ## Step 4 — CloudFront + HTTPS
            - Request an ACM certificate for your domain
            - Create a CloudFront distribution pointing to the ALB
            - Set HTTPS redirect

            ## Step 5 — Monitoring
            ```bash
            # CloudWatch alarm: CPU > 70% for 2 minutes -> scale out
            aws cloudwatch put-metric-alarm \\
              --alarm-name high-cpu \\
              --metric-name CPUUtilization \\
              --namespace AWS/EC2 \\
              --statistic Average \\
              --period 120 \\
              --threshold 70 \\
              --comparison-operator GreaterThanThreshold \\
              --evaluation-periods 1
            ```
            """),
            "Draw (on paper or in a diagram tool) the architecture you deployed. Label each AWS service, the VPC subnets, security groups, and data flow arrows.",
            "Which AWS service distributes incoming traffic across multiple EC2 instances in different Availability Zones?\nA) CloudFront  B) Route 53  C) Application Load Balancer  D) NAT Gateway",
            "Deploy the CodeSavannah Academy Django app to AWS: EC2 + RDS + S3 + ALB. Document each step with screenshots and record the load-balanced URL.",
            "Use AWS Secrets Manager or Parameter Store for credentials — never hardcode them. Tag all resources with project, environment, and owner for cost tracking.",
            75)
        created += r; updated += not r

        # ── AZURE ─────────────────────────────────────────────────────────
        azure = LearningPath.objects.get(slug='azure')

        r = upsert(azure, 1,
            "Azure Fundamentals — Portal, Entra ID & Core Services",
            "Navigate the Azure Portal, manage identities with Entra ID, understand resource groups and subscriptions, and use core compute and storage services.",
            textwrap.dedent("""\
            ## What is Microsoft Azure?
            Azure is Microsoft's cloud platform with 200+ services across compute, storage, AI, networking, and more. It integrates deeply with Microsoft 365, Active Directory, and Windows Server environments.

            ## Azure Hierarchy
            ```
            Management Group
                |
            Subscription (billing boundary)
                |
            Resource Group (logical container)
                |
            Resources (VMs, databases, storage...)
            ```

            ## Azure Entra ID (formerly Active Directory)
            Entra ID is Azure's identity and access management service.

            | Concept | Description |
            |---|---|
            | Tenant | An organisation's dedicated Entra ID instance |
            | User | Individual identity with email + password |
            | Group | Collection of users for bulk permissions |
            | Service Principal | App identity (equivalent to IAM Role in AWS) |
            | RBAC Role | Permission set (Owner, Contributor, Reader) |

            ### Assigning a role with Azure CLI
            ```bash
            az role assignment create \\
              --assignee user@example.com \\
              --role Contributor \\
              --scope /subscriptions/<sub-id>/resourceGroups/academy-rg
            ```

            ## Azure CLI Essentials
            ```bash
            # Login
            az login

            # Set default subscription
            az account set --subscription "My Subscription"

            # Create a resource group
            az group create --name academy-rg --location eastus

            # List resources in a group
            az resource list --resource-group academy-rg --output table
            ```

            ## Azure Virtual Machines
            ```bash
            az vm create \\
              --resource-group academy-rg \\
              --name academy-vm \\
              --image Ubuntu2204 \\
              --admin-username azureuser \\
              --generate-ssh-keys \\
              --size Standard_B1s
            ```

            ## Azure Blob Storage
            ```bash
            # Create storage account
            az storage account create \\
              --name academystorage2024 \\
              --resource-group academy-rg \\
              --sku Standard_LRS

            # Create container
            az storage container create \\
              --name uploads \\
              --account-name academystorage2024 \\
              --public-access blob

            # Upload file
            az storage blob upload \\
              --container-name uploads \\
              --file ./index.html \\
              --name index.html \\
              --account-name academystorage2024
            ```
            """),
            "Create a resource group named `academy-rg` in East US. Create a storage account, upload 3 files, and make them publicly accessible. Share the blob URLs.",
            "What is the correct Azure hierarchy from broadest to most specific?\nA) Subscription > Tenant > Resource Group > Resource\nB) Management Group > Subscription > Resource Group > Resource\nC) Tenant > Management Group > Subscription > Resource\nD) Resource Group > Subscription > Management Group > Tenant",
            "Build an Azure static website: create a storage account, enable static website hosting, upload an HTML/CSS portfolio, and configure a custom domain using Azure CDN.",
            "Always apply resource locks to production resource groups to prevent accidental deletion: `az lock create --name no-delete --lock-type CanNotDelete`",
            50)
        created += r; updated += not r

        r = upsert(azure, 2,
            "Azure Compute, App Service & SQL Database",
            "Deploy web apps with Azure App Service, manage containers with Azure Container Instances, and set up a managed Azure SQL Database.",
            textwrap.dedent("""\
            ## Azure App Service
            App Service is a fully managed platform for web apps — no VM management, built-in CI/CD, auto-scaling, and SSL.

            ```bash
            # Create App Service plan
            az appservice plan create \\
              --name academy-plan \\
              --resource-group academy-rg \\
              --sku B1 --is-linux

            # Create web app
            az webapp create \\
              --resource-group academy-rg \\
              --plan academy-plan \\
              --name academy-webapp-2024 \\
              --runtime "PYTHON:3.11"

            # Deploy from local Git
            az webapp deployment source config-local-git \\
              --name academy-webapp-2024 --resource-group academy-rg
            ```

            ### Configuring environment variables
            ```bash
            az webapp config appsettings set \\
              --resource-group academy-rg \\
              --name academy-webapp-2024 \\
              --settings SECRET_KEY="mysecret" DATABASE_URL="..."
            ```

            ## Azure SQL Database
            ```bash
            # Create SQL server
            az sql server create \\
              --name academy-sqlserver \\
              --resource-group academy-rg \\
              --location eastus \\
              --admin-user sqladmin \\
              --admin-password Academy@2024!

            # Create database
            az sql db create \\
              --resource-group academy-rg \\
              --server academy-sqlserver \\
              --name academydb \\
              --service-objective S0

            # Allow Azure services to connect
            az sql server firewall-rule create \\
              --resource-group academy-rg \\
              --server academy-sqlserver \\
              --name AllowAzure \\
              --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0
            ```

            ### Connecting from Python
            ```python
            import pyodbc
            conn_str = (
                "DRIVER={ODBC Driver 18 for SQL Server};"
                "SERVER=academy-sqlserver.database.windows.net;"
                "DATABASE=academydb;UID=sqladmin;PWD=Academy@2024!"
            )
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            print(cursor.fetchone())
            ```

            ## Azure Container Instances (ACI)
            ACI runs Docker containers without managing servers — ideal for batch jobs and quick deployments.

            ```bash
            az container create \\
              --resource-group academy-rg \\
              --name academy-api \\
              --image nginx:latest \\
              --ports 80 \\
              --dns-name-label academy-api-2024 \\
              --os-type Linux

            # Get public URL
            az container show \\
              --resource-group academy-rg \\
              --name academy-api \\
              --query ipAddress.fqdn
            ```
            """),
            "Deploy a Python Flask or Django app to Azure App Service using the Azure CLI. Set at least two environment variables via App Settings. Verify the app loads via its azurewebsites.net URL.",
            "Which Azure service provides a fully managed web application platform without managing underlying VMs?\nA) Azure VM  B) Azure App Service  C) Azure Container Registry  D) Azure Kubernetes Service",
            "Build and deploy a REST API using Azure App Service + Azure SQL Database. The API should have at least 3 endpoints: create, read, and delete a record.",
            "Use Azure Application Insights for monitoring — it auto-detects performance issues, exceptions, and slow queries with minimal configuration.",
            60)
        created += r; updated += not r

        r = upsert(azure, 3,
            "Project: Deploy a Production App on Azure",
            "Deploy a full Django application using Azure App Service, Azure SQL, Blob Storage, and Azure CDN with HTTPS and CI/CD from GitHub.",
            textwrap.dedent("""\
            ## Architecture
            ```
            GitHub Repo
                |
            GitHub Actions (CI/CD)
                |
            Azure App Service (Django + Gunicorn)
                |         |
            Azure SQL   Azure Blob Storage
                |
            Azure CDN (static files + HTTPS)
            ```

            ## Step 1 — GitHub Actions Workflow
            ```yaml
            # .github/workflows/deploy.yml
            name: Deploy to Azure
            on:
              push:
                branches: [main]
            jobs:
              deploy:
                runs-on: ubuntu-latest
                steps:
                  - uses: actions/checkout@v4
                  - uses: actions/setup-python@v4
                    with: { python-version: '3.11' }
                  - run: pip install -r requirements.txt
                  - run: python manage.py test
                  - uses: azure/webapps-deploy@v2
                    with:
                      app-name: academy-webapp-2024
                      publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
            ```

            ## Step 2 — Django settings for Azure
            ```python
            # settings.py
            import os
            DATABASES = {
                'default': {
                    'ENGINE': 'mssql',
                    'NAME': os.environ['AZURE_DB_NAME'],
                    'USER': os.environ['AZURE_DB_USER'],
                    'PASSWORD': os.environ['AZURE_DB_PASSWORD'],
                    'HOST': os.environ['AZURE_DB_HOST'],
                }
            }
            DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
            AZURE_ACCOUNT_NAME = os.environ['AZURE_STORAGE_ACCOUNT']
            AZURE_ACCOUNT_KEY = os.environ['AZURE_STORAGE_KEY']
            AZURE_CONTAINER = 'media'
            ```

            ## Step 3 — Custom Domain + HTTPS
            ```bash
            # Map custom domain
            az webapp config hostname add \\
              --webapp-name academy-webapp-2024 \\
              --resource-group academy-rg \\
              --hostname www.yourdomain.com

            # Create free App Service Managed Certificate
            az webapp config ssl create \\
              --resource-group academy-rg \\
              --name academy-webapp-2024 \\
              --hostname www.yourdomain.com

            # Bind certificate
            az webapp config ssl bind \\
              --certificate-thumbprint <thumbprint> \\
              --ssl-type SNI \\
              --name academy-webapp-2024 \\
              --resource-group academy-rg
            ```

            ## Step 4 — Cost Management
            ```bash
            # Set a budget alert at $20/month
            az consumption budget create \\
              --budget-name AcademyBudget \\
              --amount 20 \\
              --time-grain Monthly \\
              --start-date 2024-01-01 \\
              --end-date 2024-12-31
            ```
            """),
            "Push a working Django app to GitHub. Set up a GitHub Actions workflow that runs tests and deploys to Azure App Service automatically on every push to main.",
            "Which Azure feature enables zero-downtime deployments by routing traffic between two identical environments before making the new version live?\nA) Blue-Green slots  B) Deployment slots  C) Traffic Manager  D) Load Balancer",
            "Complete project: Deploy CodeSavannah Academy to Azure with App Service + SQL + Blob Storage. Set up CI/CD from GitHub, configure a custom domain with HTTPS, and add Application Insights monitoring.",
            "Use Deployment Slots for zero-downtime releases: deploy to staging slot, warm it up, then swap to production. If issues arise, swap back instantly.",
            70)
        created += r; updated += not r

        # ── GOOGLE CLOUD ──────────────────────────────────────────────────
        gcp = LearningPath.objects.get(slug='google-cloud')

        r = upsert(gcp, 1,
            "GCP Fundamentals — Console, IAM & Core Services",
            "Navigate the Google Cloud Console, manage projects and billing, configure IAM permissions, and use core GCP services including Compute Engine and Cloud Storage.",
            textwrap.dedent("""\
            ## What is Google Cloud Platform (GCP)?
            GCP is Google's cloud platform powering Search, YouTube, and Gmail — now available as public cloud services. Key strengths include data analytics (BigQuery), machine learning (Vertex AI), and Kubernetes (GKE, invented at Google).

            ## GCP Resource Hierarchy
            ```
            Organisation
                |
            Folder (optional grouping)
                |
            Project (billing + IAM boundary)
                |
            Resources (VMs, buckets, databases...)
            ```

            ## IAM — Identity & Access Management
            GCP IAM uses **principals** (who) and **roles** (what).

            | Role type | Example |
            |---|---|
            | Basic | roles/viewer, roles/editor, roles/owner |
            | Predefined | roles/compute.instanceAdmin |
            | Custom | Your own combination of permissions |

            ```bash
            # Bind a role to a user
            gcloud projects add-iam-policy-binding my-project \\
              --member="user:student@gmail.com" \\
              --role="roles/storage.objectViewer"

            # Create a service account
            gcloud iam service-accounts create academy-sa \\
              --display-name="Academy Service Account"

            # Download key (use Workload Identity in production instead)
            gcloud iam service-accounts keys create key.json \\
              --iam-account=academy-sa@my-project.iam.gserviceaccount.com
            ```

            ## Compute Engine
            ```bash
            # Create a VM
            gcloud compute instances create academy-vm \\
              --zone=us-central1-a \\
              --machine-type=e2-micro \\
              --image-family=ubuntu-2204-lts \\
              --image-project=ubuntu-os-cloud \\
              --tags=http-server

            # SSH into the VM
            gcloud compute ssh academy-vm --zone=us-central1-a

            # Allow HTTP traffic
            gcloud compute firewall-rules create allow-http \\
              --allow=tcp:80 --target-tags=http-server
            ```

            ## Cloud Storage
            ```bash
            # Create a bucket
            gsutil mb -l us-central1 gs://academy-bucket-2024

            # Upload files
            gsutil cp index.html gs://academy-bucket-2024/
            gsutil cp -r ./static gs://academy-bucket-2024/

            # Make bucket publicly readable
            gsutil iam ch allUsers:objectViewer gs://academy-bucket-2024

            # Host a static website
            gsutil web set -m index.html -e 404.html gs://academy-bucket-2024
            ```
            """),
            "Create a GCP project, enable billing, and use the Cloud Shell to create a Cloud Storage bucket. Upload a static HTML page and serve it publicly. Share the URL.",
            "In GCP, what is the boundary for billing and IAM policies?\nA) Organisation  B) Folder  C) Project  D) Resource",
            "Host a static portfolio on GCP: create a Cloud Storage bucket, upload HTML/CSS, make it public, set up a custom domain via Cloud DNS, and secure it with an SSL certificate via Cloud CDN.",
            "Use Cloud Shell (browser-based terminal) for learning — it comes with gcloud, gsutil, and 5 GB free home directory storage, always up-to-date.",
            50)
        created += r; updated += not r

        r = upsert(gcp, 2,
            "GCP App Engine, Cloud SQL & BigQuery",
            "Deploy web apps to App Engine, manage a Cloud SQL database, and run analytics queries with BigQuery.",
            textwrap.dedent("""\
            ## App Engine
            App Engine is GCP's fully managed PaaS. You push code; Google handles servers, scaling, and patching.

            ```yaml
            # app.yaml
            runtime: python311
            entrypoint: gunicorn -b :$PORT config.wsgi:application
            env_variables:
              SECRET_KEY: "your-secret-key"
              DATABASE_URL: "postgres://user:pass@/dbname?host=/cloudsql/project:region:instance"
            beta_settings:
              cloud_sql_instances: project:region:instance-name
            ```

            ```bash
            # Deploy
            gcloud app deploy app.yaml

            # View logs
            gcloud app logs tail -s default

            # Browse the app
            gcloud app browse
            ```

            ## Cloud SQL
            Cloud SQL manages MySQL, PostgreSQL, and SQL Server.

            ```bash
            # Create a PostgreSQL instance
            gcloud sql instances create academy-db \\
              --database-version=POSTGRES_15 \\
              --tier=db-f1-micro \\
              --region=us-central1

            # Create a database and user
            gcloud sql databases create academydb --instance=academy-db
            gcloud sql users set-password postgres \\
              --instance=academy-db --password=SecurePass123

            # Connect via Cloud SQL Proxy
            ./cloud-sql-proxy project:region:academy-db &
            psql -h 127.0.0.1 -U postgres -d academydb
            ```

            ## BigQuery — Serverless Data Warehouse
            BigQuery analyses petabytes of data using SQL. You pay per query (first 1 TB/month free).

            ```sql
            -- Query public dataset: GitHub activity
            SELECT
              repo_name,
              COUNT(*) AS push_events
            FROM `githubarchive.month.202401`
            WHERE type = 'PushEvent'
            GROUP BY repo_name
            ORDER BY push_events DESC
            LIMIT 10;
            ```

            ```python
            from google.cloud import bigquery

            client = bigquery.Client()
            query = (
                "SELECT name, SUM(number) AS total "
                "FROM `bigquery-public-data.usa_names.usa_1910_2013` "
                "WHERE state = 'TX' "
                "GROUP BY name ORDER BY total DESC LIMIT 5"
            )
            results = client.query(query).result()
            for row in results:
                print(f"{row.name}: {row.total:,}")
            ```

            ## Cloud Functions (Serverless)
            ```python
            # main.py
            import functions_framework

            @functions_framework.http
            def hello_academy(request):
                name = request.args.get('name', 'World')
                return f'Hello {name} from GCP Cloud Functions!'
            ```

            ```bash
            gcloud functions deploy hello-academy \\
              --runtime python311 \\
              --trigger-http \\
              --allow-unauthenticated
            ```
            """),
            "Deploy a simple Python Flask app to App Engine. Create a Cloud SQL PostgreSQL database, connect the app to it, and demonstrate create/read operations through the deployed URL.",
            "Which GCP service is a serverless, petabyte-scale data warehouse that uses SQL for analysis?\nA) Cloud SQL  B) Cloud Spanner  C) BigQuery  D) Firestore",
            "Build a BigQuery analytics dashboard: load a public dataset, write 3 SQL queries answering real questions, and visualise results with Google Looker Studio (free).",
            "BigQuery bills per TB of data scanned. Use column partitioning and clustering to reduce costs — a partitioned table can reduce query costs by 80% or more.",
            60)
        created += r; updated += not r

        r = upsert(gcp, 3,
            "Project: Deploy a Containerised App on Google Kubernetes Engine",
            "Containerise a Django application with Docker, push to Artifact Registry, and deploy to a GKE cluster with auto-scaling and a load balancer.",
            textwrap.dedent("""\
            ## Step 1 — Containerise with Docker
            ```dockerfile
            # Dockerfile
            FROM python:3.11-slim
            WORKDIR /app
            COPY requirements.txt .
            RUN pip install --no-cache-dir -r requirements.txt
            COPY . .
            RUN python manage.py collectstatic --noinput
            EXPOSE 8000
            CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
            ```

            ```bash
            # Build and test locally
            docker build -t academy-app .
            docker run -p 8000:8000 academy-app
            ```

            ## Step 2 — Push to Artifact Registry
            ```bash
            # Create registry
            gcloud artifacts repositories create academy-repo \\
              --repository-format=docker \\
              --location=us-central1

            # Tag and push
            docker tag academy-app \\
              us-central1-docker.pkg.dev/PROJECT_ID/academy-repo/academy-app:v1

            gcloud auth configure-docker us-central1-docker.pkg.dev

            docker push \\
              us-central1-docker.pkg.dev/PROJECT_ID/academy-repo/academy-app:v1
            ```

            ## Step 3 — Create a GKE Cluster
            ```bash
            gcloud container clusters create academy-cluster \\
              --num-nodes=2 \\
              --machine-type=e2-small \\
              --zone=us-central1-a \\
              --enable-autoscaling \\
              --min-nodes=1 \\
              --max-nodes=5

            gcloud container clusters get-credentials academy-cluster \\
              --zone=us-central1-a
            ```

            ## Step 4 — Kubernetes Manifests
            ```yaml
            # deployment.yaml
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: academy-deployment
            spec:
              replicas: 2
              selector:
                matchLabels: { app: academy }
              template:
                metadata:
                  labels: { app: academy }
                spec:
                  containers:
                  - name: academy
                    image: us-central1-docker.pkg.dev/PROJECT_ID/academy-repo/academy-app:v1
                    ports:
                    - containerPort: 8000
                    env:
                    - name: SECRET_KEY
                      valueFrom:
                        secretKeyRef: { name: academy-secrets, key: secret-key }
            ---
            apiVersion: v1
            kind: Service
            metadata:
              name: academy-service
            spec:
              type: LoadBalancer
              selector: { app: academy }
              ports:
              - port: 80
                targetPort: 8000
            ```

            ```bash
            kubectl apply -f deployment.yaml
            kubectl get services  # wait for EXTERNAL-IP
            ```

            ## Step 5 — Rolling Updates
            ```bash
            # Deploy new version with zero downtime
            kubectl set image deployment/academy-deployment \\
              academy=us-central1-docker.pkg.dev/PROJECT_ID/academy-repo/academy-app:v2

            # Monitor rollout
            kubectl rollout status deployment/academy-deployment

            # Rollback if needed
            kubectl rollout undo deployment/academy-deployment
            ```
            """),
            "Containerise any web app you've built previously, push it to Artifact Registry, and deploy it to GKE. Scale the deployment to 3 replicas and confirm all pods are running with `kubectl get pods`.",
            "Which Kubernetes object ensures a specified number of pod replicas are always running?\nA) Service  B) ConfigMap  C) Deployment  D) Ingress",
            "Deploy the Academy app to GKE with: 2-node cluster, Cloud SQL backend via Cloud SQL Proxy sidecar, Cloud Storage for media, and a managed SSL certificate via Google-managed certificate on an Ingress.",
            "Enable Workload Identity on GKE to allow pods to access GCP services without downloading service account keys — it is the most secure approach for production.",
            75)
        created += r; updated += not r

        # ── ANDROID STUDIO ───────────────────────────────────────────────
        android = LearningPath.objects.get(slug='android-studio')

        r = upsert(android, 1,
            "Android Fundamentals — Activities, Layouts & XML",
            "Set up Android Studio, understand the Activity lifecycle, build UI layouts with XML, and handle user interactions with click listeners.",
            textwrap.dedent("""\
            ## Android Development Overview
            Android apps are built with **Kotlin** (recommended) or Java, using the Android SDK and Android Studio IDE. Apps run on the Dalvik/ART virtual machine on Android devices.

            ## Project Structure
            ```
            app/
            ├── src/main/
            │   ├── java/com/example/academy/
            │   │   └── MainActivity.kt
            │   ├── res/
            │   │   ├── layout/activity_main.xml
            │   │   ├── values/strings.xml
            │   │   └── drawable/
            │   └── AndroidManifest.xml
            └── build.gradle
            ```

            ## Activity Lifecycle
            ```
            onCreate() → onStart() → onResume() → [Running]
                                                      ↓
                                               onPause() → onStop() → onDestroy()
                                                      ↑
                                               onResume() ← onRestart()
            ```

            ## Your First Activity (Kotlin)
            ```kotlin
            // MainActivity.kt
            class MainActivity : AppCompatActivity() {

                override fun onCreate(savedInstanceState: Bundle?) {
                    super.onCreate(savedInstanceState)
                    setContentView(R.layout.activity_main)

                    val btnGreet = findViewById<Button>(R.id.btnGreet)
                    val tvResult = findViewById<TextView>(R.id.tvResult)

                    btnGreet.setOnClickListener {
                        tvResult.text = "Hello from CodeSavannah!"
                    }
                }
            }
            ```

            ## XML Layout
            ```xml
            <!-- res/layout/activity_main.xml -->
            <?xml version="1.0" encoding="utf-8"?>
            <LinearLayout
                xmlns:android="http://schemas.android.com/apk/res/android"
                android:layout_width="match_parent"
                android:layout_height="match_parent"
                android:orientation="vertical"
                android:padding="16dp">

                <TextView
                    android:id="@+id/tvResult"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Welcome to Academy"
                    android:textSize="20sp"/>

                <EditText
                    android:id="@+id/etName"
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:hint="Enter your name"
                    android:inputType="textPersonName"/>

                <Button
                    android:id="@+id/btnGreet"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Greet Me"
                    android:layout_gravity="center"/>
            </LinearLayout>
            ```

            ## Reading User Input
            ```kotlin
            btnGreet.setOnClickListener {
                val name = etName.text.toString().trim()
                if (name.isEmpty()) {
                    tvResult.text = "Please enter your name"
                } else {
                    tvResult.text = "Hello, $name!"
                }
            }
            ```

            ## ConstraintLayout (modern alternative)
            ```xml
            <androidx.constraintlayout.widget.ConstraintLayout ...>
                <TextView
                    android:id="@+id/tvTitle"
                    app:layout_constraintTop_toTopOf="parent"
                    app:layout_constraintStart_toStartOf="parent"
                    app:layout_constraintEnd_toEndOf="parent"
                    android:text="Academy App"/>
            </androidx.constraintlayout.widget.ConstraintLayout>
            ```
            """),
            "Build an Android app with two Activities. The first has a form with name and course fields plus a Submit button. The second displays the submitted information. Pass data between activities using Intent extras.",
            "Which Android lifecycle method is called when an Activity becomes visible to the user?\nA) onCreate()  B) onStart()  C) onResume()  D) onRestart()",
            "Build a simple quiz app: 5 questions with 4 multiple-choice options each, a score tracker, and a results screen showing the final score with a retry button.",
            "Always call `super.onCreate()` before `setContentView()`. Avoid heavy work in `onCreate()` — use background threads or coroutines for database/network operations.",
            55)
        created += r; updated += not r

        r = upsert(android, 2,
            "RecyclerView, Intents & Runtime Permissions",
            "Display lists efficiently with RecyclerView, navigate between screens using Intents, and request runtime permissions for camera and location.",
            textwrap.dedent("""\
            ## RecyclerView
            RecyclerView efficiently renders large lists by recycling view holders instead of creating new views for every item.

            ### 1. Add dependency (build.gradle)
            ```groovy
            dependencies {
                implementation 'androidx.recyclerview:recyclerview:1.3.2'
            }
            ```

            ### 2. Data class
            ```kotlin
            data class Course(val id: Int, val title: String, val level: String)
            ```

            ### 3. Adapter
            ```kotlin
            class CourseAdapter(
                private val courses: List<Course>,
                private val onClick: (Course) -> Unit
            ) : RecyclerView.Adapter<CourseAdapter.CourseViewHolder>() {

                inner class CourseViewHolder(view: View) : RecyclerView.ViewHolder(view) {
                    val tvTitle: TextView = view.findViewById(R.id.tvTitle)
                    val tvLevel: TextView = view.findViewById(R.id.tvLevel)
                }

                override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
                    CourseViewHolder(
                        LayoutInflater.from(parent.context)
                            .inflate(R.layout.item_course, parent, false)
                    )

                override fun onBindViewHolder(holder: CourseViewHolder, position: Int) {
                    val course = courses[position]
                    holder.tvTitle.text = course.title
                    holder.tvLevel.text = course.level
                    holder.itemView.setOnClickListener { onClick(course) }
                }

                override fun getItemCount() = courses.size
            }
            ```

            ### 4. Activity setup
            ```kotlin
            val courses = listOf(
                Course(1, "Python Programming", "Beginner"),
                Course(2, "Django Web Dev", "Intermediate"),
                Course(3, "Machine Learning", "Advanced"),
            )

            val recyclerView = findViewById<RecyclerView>(R.id.rvCourses)
            recyclerView.layoutManager = LinearLayoutManager(this)
            recyclerView.adapter = CourseAdapter(courses) { course ->
                val intent = Intent(this, CourseDetailActivity::class.java)
                intent.putExtra("COURSE_ID", course.id)
                intent.putExtra("COURSE_TITLE", course.title)
                startActivity(intent)
            }
            ```

            ## Explicit vs Implicit Intents
            ```kotlin
            // Explicit — specific Activity
            val intent = Intent(this, ProfileActivity::class.java)
            intent.putExtra("USER_NAME", "Alice")
            startActivity(intent)

            // Implicit — system picks the handler
            val shareIntent = Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"
                putExtra(Intent.EXTRA_TEXT, "Check out CodeSavannah Academy!")
            }
            startActivity(Intent.createChooser(shareIntent, "Share via"))
            ```

            ## Runtime Permissions (Android 6+)
            ```kotlin
            private val requestPermissionLauncher =
                registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
                    if (granted) openCamera() else showPermissionDeniedMessage()
                }

            fun requestCameraPermission() {
                when {
                    ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                        == PackageManager.PERMISSION_GRANTED -> openCamera()
                    else -> requestPermissionLauncher.launch(Manifest.permission.CAMERA)
                }
            }
            ```
            """),
            "Build a contacts app: a RecyclerView listing 10 contacts (name, phone). Clicking a contact opens a detail screen. Add a FAB button that opens a dialog to add a new contact to the list.",
            "What is the primary advantage of RecyclerView over ListView?\nA) Simpler code  B) View recycling reduces memory and improves scroll performance  C) Built-in animations  D) No adapter required",
            "Build a camera app that requests camera permission, captures a photo, displays it full-screen, and lets the user save it to the gallery.",
            "Use `ActivityResultContracts` (not deprecated `startActivityForResult`) for modern permission and result handling.",
            60)
        created += r; updated += not r

        r = upsert(android, 3,
            "Project: Notes App with Room Database & ViewModel",
            "Build a full CRUD notes app using Room for local persistence, ViewModel for state management, and LiveData for reactive UI updates.",
            textwrap.dedent("""\
            ## Architecture: MVVM + Room
            ```
            UI (Activity/Fragment)
                |
            ViewModel (survives rotation)
                |
            Repository (single source of truth)
                |
            Room Database (SQLite wrapper)
            ```

            ## 1. Add dependencies
            ```groovy
            dependencies {
                def room_version = "2.6.1"
                implementation "androidx.room:room-runtime:$room_version"
                kapt "androidx.room:room-compiler:$room_version"
                implementation "androidx.room:room-ktx:$room_version"
                implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0"
                implementation "androidx.lifecycle:lifecycle-livedata-ktx:2.7.0"
            }
            ```

            ## 2. Entity
            ```kotlin
            @Entity(tableName = "notes")
            data class Note(
                @PrimaryKey(autoGenerate = true) val id: Int = 0,
                val title: String,
                val content: String,
                val createdAt: Long = System.currentTimeMillis()
            )
            ```

            ## 3. DAO
            ```kotlin
            @Dao
            interface NoteDao {
                @Query("SELECT * FROM notes ORDER BY createdAt DESC")
                fun getAllNotes(): LiveData<List<Note>>

                @Insert(onConflict = OnConflictStrategy.REPLACE)
                suspend fun insert(note: Note)

                @Update
                suspend fun update(note: Note)

                @Delete
                suspend fun delete(note: Note)
            }
            ```

            ## 4. Database
            ```kotlin
            @Database(entities = [Note::class], version = 1)
            abstract class AppDatabase : RoomDatabase() {
                abstract fun noteDao(): NoteDao

                companion object {
                    @Volatile private var INSTANCE: AppDatabase? = null

                    fun getInstance(context: Context): AppDatabase =
                        INSTANCE ?: synchronized(this) {
                            Room.databaseBuilder(
                                context.applicationContext,
                                AppDatabase::class.java, "notes_db"
                            ).build().also { INSTANCE = it }
                        }
                }
            }
            ```

            ## 5. ViewModel
            ```kotlin
            class NoteViewModel(application: Application) : AndroidViewModel(application) {
                private val dao = AppDatabase.getInstance(application).noteDao()
                val allNotes: LiveData<List<Note>> = dao.getAllNotes()

                fun insert(note: Note) = viewModelScope.launch { dao.insert(note) }
                fun update(note: Note) = viewModelScope.launch { dao.update(note) }
                fun delete(note: Note) = viewModelScope.launch { dao.delete(note) }
            }
            ```

            ## 6. Activity observing LiveData
            ```kotlin
            viewModel.allNotes.observe(this) { notes ->
                adapter.submitList(notes)
            }
            ```
            """),
            "Extend the Notes app: add search functionality that filters notes in real-time as the user types, and add colour labels (red/yellow/green) that are stored in the database.",
            "In Android's MVVM architecture, which component survives configuration changes (screen rotation) and holds the UI state?\nA) Activity  B) Fragment  C) ViewModel  D) Repository",
            "Build the complete Notes app described above: full CRUD, Room database, ViewModel + LiveData, search bar, and note colour labels. Submit the GitHub repository link.",
            "Use `ListAdapter` with `DiffUtil` instead of a plain adapter for RecyclerView — it calculates list diffs on a background thread and animates changes automatically.",
            70)
        created += r; updated += not r

        # ── FLUTTER ───────────────────────────────────────────────────────
        flutter = LearningPath.objects.get(slug='flutter')

        r = upsert(flutter, 1,
            "Flutter Fundamentals — Widgets, State & Hot Reload",
            "Set up Flutter, understand the widget tree, build stateless and stateful widgets, and use hot reload for rapid development.",
            textwrap.dedent("""\
            ## What is Flutter?
            Flutter is Google's open-source UI toolkit for building natively compiled apps from a **single codebase** targeting iOS, Android, Web, and Desktop. Apps are written in Dart and rendered by Flutter's own Skia/Impeller engine — not using platform UI components.

            ## Project Structure
            ```
            lib/
            ├── main.dart           # Entry point
            ├── screens/
            │   └── home_screen.dart
            └── widgets/
                └── course_card.dart
            ```

            ## main.dart
            ```dart
            import 'package:flutter/material.dart';

            void main() => runApp(const AcademyApp());

            class AcademyApp extends StatelessWidget {
              const AcademyApp({super.key});

              @override
              Widget build(BuildContext context) {
                return MaterialApp(
                  title: 'CodeSavannah Academy',
                  theme: ThemeData(
                    colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
                    useMaterial3: true,
                  ),
                  home: const HomeScreen(),
                );
              }
            }
            ```

            ## StatelessWidget — no mutable state
            ```dart
            class CourseCard extends StatelessWidget {
              final String title;
              final String level;
              const CourseCard({super.key, required this.title, required this.level});

              @override
              Widget build(BuildContext context) {
                return Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(title, style: Theme.of(context).textTheme.titleLarge),
                        const SizedBox(height: 4),
                        Chip(label: Text(level)),
                      ],
                    ),
                  ),
                );
              }
            }
            ```

            ## StatefulWidget — mutable state
            ```dart
            class CounterWidget extends StatefulWidget {
              const CounterWidget({super.key});
              @override
              State<CounterWidget> createState() => _CounterWidgetState();
            }

            class _CounterWidgetState extends State<CounterWidget> {
              int _count = 0;

              @override
              Widget build(BuildContext context) {
                return Column(
                  children: [
                    Text('Count: $_count', style: const TextStyle(fontSize: 24)),
                    ElevatedButton(
                      onPressed: () => setState(() => _count++),
                      child: const Text('Increment'),
                    ),
                  ],
                );
              }
            }
            ```

            ## Common Layout Widgets
            | Widget | Purpose |
            |---|---|
            | `Column` / `Row` | Vertical / horizontal arrangement |
            | `Stack` | Overlapping layers |
            | `Container` | Box with padding, margin, decoration |
            | `Expanded` | Fills remaining space in Row/Column |
            | `ListView` | Scrollable list |
            | `GridView` | Scrollable grid |
            """),
            "Build a Flutter app with a custom `CourseCard` widget that displays title, level, and duration. Show at least 5 cards in a `ListView`. Add a FloatingActionButton that shows a SnackBar when tapped.",
            "What is the key difference between StatelessWidget and StatefulWidget?\nA) StatelessWidget uses Dart; StatefulWidget uses JavaScript\nB) StatefulWidget has mutable state that triggers rebuilds via setState()\nC) StatelessWidget can only show text\nD) StatefulWidget runs faster",
            "Build a Flutter to-do app: add tasks via a TextField + button, display tasks in a ListView with checkboxes, allow deletion by swiping, and persist tasks using the `shared_preferences` package.",
            "Hot reload (r) updates the UI without restarting — state is preserved. Hot restart (R) restarts the app fully. Use hot reload during UI development for instant feedback.",
            55)
        created += r; updated += not r

        r = upsert(flutter, 2,
            "Flutter Navigation, Lists & HTTP",
            "Navigate between screens with named routes, display dynamic lists with ListView.builder, and fetch data from a REST API using the http package.",
            textwrap.dedent("""\
            ## Named Route Navigation
            ```dart
            // In MaterialApp
            MaterialApp(
              initialRoute: '/',
              routes: {
                '/': (context) => const HomeScreen(),
                '/courses': (context) => const CoursesScreen(),
                '/lesson': (context) => const LessonScreen(),
              },
            )

            // Navigate
            Navigator.pushNamed(context, '/courses');

            // Pass arguments
            Navigator.pushNamed(
              context, '/lesson',
              arguments: {'id': 1, 'title': 'Python Basics'},
            );

            // Receive in destination
            final args = ModalRoute.of(context)!.settings.arguments as Map;
            ```

            ## Go Router (recommended for complex apps)
            ```yaml
            # pubspec.yaml
            dependencies:
              go_router: ^13.0.0
            ```
            ```dart
            final router = GoRouter(routes: [
              GoRoute(path: '/', builder: (ctx, state) => const HomeScreen()),
              GoRoute(path: '/course/:id', builder: (ctx, state) {
                final id = state.pathParameters['id']!;
                return CourseScreen(id: id);
              }),
            ]);
            ```

            ## ListView.builder — efficient large lists
            ```dart
            ListView.builder(
              itemCount: courses.length,
              itemBuilder: (context, index) {
                final course = courses[index];
                return ListTile(
                  leading: const Icon(Icons.school),
                  title: Text(course.title),
                  subtitle: Text(course.level),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () => Navigator.pushNamed(context, '/lesson',
                    arguments: course),
                );
              },
            )
            ```

            ## HTTP Requests
            ```yaml
            dependencies:
              http: ^1.2.0
            ```

            ```dart
            import 'package:http/http.dart' as http;
            import 'dart:convert';

            class ApiService {
              static const baseUrl = 'https://jsonplaceholder.typicode.com';

              static Future<List<Map<String, dynamic>>> fetchPosts() async {
                final response = await http.get(Uri.parse('$baseUrl/posts'));
                if (response.statusCode == 200) {
                  return List<Map<String, dynamic>>.from(
                    json.decode(response.body)
                  );
                }
                throw Exception('Failed to load posts: ${response.statusCode}');
              }
            }
            ```

            ## FutureBuilder — async data in UI
            ```dart
            FutureBuilder<List<Map<String, dynamic>>>(
              future: ApiService.fetchPosts(),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const CircularProgressIndicator();
                }
                if (snapshot.hasError) {
                  return Text('Error: ${snapshot.error}');
                }
                final posts = snapshot.data!;
                return ListView.builder(
                  itemCount: posts.length,
                  itemBuilder: (ctx, i) => ListTile(title: Text(posts[i]['title'])),
                );
              },
            )
            ```
            """),
            "Build a Flutter news app: fetch articles from a free news API (NewsAPI or similar), display headlines in a ListView, and show the full article when tapped. Handle loading and error states.",
            "Which Flutter widget is best for displaying a large list efficiently, creating item widgets on demand?\nA) Column  B) ListView  C) ListView.builder  D) Stack",
            "Build a Flutter app that fetches learning paths from the CodeSavannah API (or mock JSON), displays them in a categorised list with filter chips, and navigates to a lesson detail screen.",
            "Always use `const` constructors for widgets that don't change — Flutter skips rebuilding `const` widgets during setState calls, significantly improving performance.",
            60)
        created += r; updated += not r

        r = upsert(flutter, 3,
            "Project: Weather App with OpenWeatherMap API",
            "Build a complete Flutter weather app: search cities, display current conditions and a 5-day forecast, handle errors gracefully, and support dark/light theme.",
            textwrap.dedent("""\
            ## Project Structure
            ```
            lib/
            ├── main.dart
            ├── models/weather.dart
            ├── services/weather_service.dart
            ├── screens/
            │   ├── home_screen.dart
            │   └── forecast_screen.dart
            └── widgets/
                ├── weather_card.dart
                └── forecast_tile.dart
            ```

            ## Weather Model
            ```dart
            class Weather {
              final String city;
              final double temperature;
              final String description;
              final String icon;
              final int humidity;
              final double windSpeed;

              Weather({
                required this.city, required this.temperature,
                required this.description, required this.icon,
                required this.humidity, required this.windSpeed,
              });

              factory Weather.fromJson(Map<String, dynamic> json) => Weather(
                city: json['name'],
                temperature: (json['main']['temp'] as num).toDouble() - 273.15,
                description: json['weather'][0]['description'],
                icon: json['weather'][0]['icon'],
                humidity: json['main']['humidity'],
                windSpeed: (json['wind']['speed'] as num).toDouble(),
              );
            }
            ```

            ## Weather Service
            ```dart
            class WeatherService {
              static const apiKey = 'YOUR_API_KEY';
              static const baseUrl = 'https://api.openweathermap.org/data/2.5';

              Future<Weather> getWeather(String city) async {
                final url = Uri.parse('$baseUrl/weather?q=$city&appid=$apiKey');
                final response = await http.get(url);
                if (response.statusCode == 200) {
                  return Weather.fromJson(json.decode(response.body));
                } else if (response.statusCode == 404) {
                  throw Exception('City not found');
                }
                throw Exception('API error: ${response.statusCode}');
              }
            }
            ```

            ## Home Screen with Search
            ```dart
            class HomeScreen extends StatefulWidget {
              const HomeScreen({super.key});
              @override
              State<HomeScreen> createState() => _HomeScreenState();
            }

            class _HomeScreenState extends State<HomeScreen> {
              final _controller = TextEditingController();
              final _service = WeatherService();
              Weather? _weather;
              String? _error;
              bool _loading = false;

              Future<void> _search() async {
                setState(() { _loading = true; _error = null; });
                try {
                  final w = await _service.getWeather(_controller.text.trim());
                  setState(() { _weather = w; });
                } catch (e) {
                  setState(() { _error = e.toString(); });
                } finally {
                  setState(() { _loading = false; });
                }
              }

              @override
              Widget build(BuildContext context) => Scaffold(
                appBar: AppBar(title: const Text('Weather')),
                body: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(children: [
                    TextField(
                      controller: _controller,
                      decoration: InputDecoration(
                        labelText: 'City',
                        suffixIcon: IconButton(
                          icon: const Icon(Icons.search), onPressed: _search),
                      ),
                      onSubmitted: (_) => _search(),
                    ),
                    if (_loading) const CircularProgressIndicator(),
                    if (_error != null) Text(_error!, style: const TextStyle(color: Colors.red)),
                    if (_weather != null) WeatherCard(weather: _weather!),
                  ]),
                ),
              );
            }
            ```
            """),
            "Add a 5-day forecast screen to the weather app using the `/forecast` endpoint from OpenWeatherMap. Display min/max temperatures and weather icons for each day.",
            "Which Flutter pattern separates UI from business logic by placing API calls and data transformation in dedicated classes outside widgets?\nA) InheritedWidget  B) Provider/BLoC/Service layer  C) StatefulWidget  D) FutureBuilder",
            "Complete the weather app: search, current weather, 5-day forecast, error handling, and a theme toggle (dark/light). Publish to GitHub and include a README with setup instructions.",
            "Use `dotenv` or `flutter_secure_storage` for API keys — never commit keys to Git. Add `.env` to `.gitignore` and load keys at runtime.",
            65)
        created += r; updated += not r

        # ── REACT NATIVE ──────────────────────────────────────────────────
        rn = LearningPath.objects.get(slug='react-native')

        r = upsert(rn, 1,
            "React Native Fundamentals — Components & StyleSheet",
            "Set up React Native with Expo, build core UI components, apply styles with StyleSheet, and understand the bridge between JavaScript and native APIs.",
            textwrap.dedent("""\
            ## What is React Native?
            React Native lets you build iOS and Android apps using React and JavaScript. Unlike Flutter, it uses real native components (not a custom renderer), so apps look and feel native on each platform.

            ## Quick Start with Expo
            ```bash
            npx create-expo-app AcademyApp --template blank
            cd AcademyApp
            npx expo start
            ```
            Expo Go app lets you preview on your physical device by scanning a QR code.

            ## Core Components
            | React Native | Web equivalent |
            |---|---|
            | `<View>` | `<div>` |
            | `<Text>` | `<p>` / `<span>` |
            | `<TextInput>` | `<input>` |
            | `<Image>` | `<img>` |
            | `<ScrollView>` | `<div style="overflow:scroll">` |
            | `<FlatList>` | Virtualised list (no direct web equivalent) |
            | `<TouchableOpacity>` | `<button>` |
            | `<Pressable>` | `<button>` (recommended modern alternative) |

            ## App.js
            ```jsx
            import { View, Text, StyleSheet, Pressable, Alert } from 'react-native';

            export default function App() {
              return (
                <View style={styles.container}>
                  <Text style={styles.title}>CodeSavannah Academy</Text>
                  <Text style={styles.subtitle}>Learn to code, build the future</Text>
                  <Pressable
                    style={styles.button}
                    onPress={() => Alert.alert('Welcome!', 'Ready to learn?')}
                  >
                    <Text style={styles.buttonText}>Get Started</Text>
                  </Pressable>
                </View>
              );
            }

            const styles = StyleSheet.create({
              container: {
                flex: 1,
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: '#0a1628',
                padding: 24,
              },
              title: {
                fontSize: 28,
                fontWeight: '800',
                color: '#ffffff',
                marginBottom: 8,
              },
              subtitle: {
                fontSize: 16,
                color: '#94a3b8',
                marginBottom: 32,
                textAlign: 'center',
              },
              button: {
                backgroundColor: '#10b981',
                paddingHorizontal: 32,
                paddingVertical: 14,
                borderRadius: 12,
              },
              buttonText: {
                color: '#fff',
                fontWeight: '700',
                fontSize: 16,
              },
            });
            ```

            ## Flexbox in React Native
            React Native uses Flexbox by default (no CSS grid). Key differences from web:
            - Default `flexDirection` is `column` (not `row`)
            - Dimensions are in density-independent pixels (no `px`, `em`, `rem`)

            ```jsx
            <View style={{ flexDirection: 'row', gap: 12 }}>
              <View style={{ flex: 1, backgroundColor: '#1e3a5f', height: 60 }} />
              <View style={{ flex: 2, backgroundColor: '#10b981', height: 60 }} />
            </View>
            ```
            """),
            "Build a React Native profile card component: avatar image, name, role, and a 'Follow' button that toggles between Follow/Following with colour change on press.",
            "What does `flex: 1` mean on a React Native View inside a parent with `flex: 1`?\nA) Font size of 1px  B) The view takes all remaining space  C) Display block  D) Margin of 1",
            "Build a React Native onboarding flow: 3 screens with illustrations, headings, and descriptions. Use a horizontal ScrollView with page dots. A 'Get Started' button on the last screen navigates to the main app.",
            "Use `Pressable` over `TouchableOpacity` in new code — it supports more press states (hovered, focused, pressed) and is the recommended modern primitive.",
            50)
        created += r; updated += not r

        r = upsert(rn, 2,
            "React Native Navigation, FlatList & AsyncStorage",
            "Set up React Navigation for screen routing, display dynamic lists with FlatList, and persist data locally with AsyncStorage.",
            textwrap.dedent("""\
            ## React Navigation Setup
            ```bash
            npm install @react-navigation/native @react-navigation/native-stack
            npx expo install react-native-screens react-native-safe-area-context
            ```

            ```jsx
            // App.js
            import { NavigationContainer } from '@react-navigation/native';
            import { createNativeStackNavigator } from '@react-navigation/native-stack';
            import HomeScreen from './screens/HomeScreen';
            import CourseScreen from './screens/CourseScreen';

            const Stack = createNativeStackNavigator();

            export default function App() {
              return (
                <NavigationContainer>
                  <Stack.Navigator initialRouteName="Home">
                    <Stack.Screen name="Home" component={HomeScreen} />
                    <Stack.Screen name="Course" component={CourseScreen}
                      options={({ route }) => ({ title: route.params.title })} />
                  </Stack.Navigator>
                </NavigationContainer>
              );
            }
            ```

            ```jsx
            // HomeScreen.js — navigate with params
            function HomeScreen({ navigation }) {
              return (
                <Pressable onPress={() => navigation.navigate('Course', {
                  id: 1, title: 'Python Programming'
                })}>
                  <Text>Open Python Course</Text>
                </Pressable>
              );
            }
            ```

            ## FlatList — virtualised, memory-efficient
            ```jsx
            const courses = [
              { id: '1', title: 'Python', level: 'Beginner' },
              { id: '2', title: 'React', level: 'Intermediate' },
            ];

            <FlatList
              data={courses}
              keyExtractor={item => item.id}
              renderItem={({ item }) => (
                <Pressable onPress={() => navigation.navigate('Course', item)}
                  style={styles.card}>
                  <Text style={styles.title}>{item.title}</Text>
                  <Text style={styles.level}>{item.level}</Text>
                </Pressable>
              )}
              ItemSeparatorComponent={() => <View style={{ height: 8 }} />}
              ListEmptyComponent={<Text>No courses found</Text>}
            />
            ```

            ## AsyncStorage — local key-value persistence
            ```bash
            npx expo install @react-native-async-storage/async-storage
            ```

            ```jsx
            import AsyncStorage from '@react-native-async-storage/async-storage';

            // Save
            await AsyncStorage.setItem('user_name', 'Alice');
            await AsyncStorage.setItem('progress', JSON.stringify({ python: 3, react: 1 }));

            // Read
            const name = await AsyncStorage.getItem('user_name');
            const raw = await AsyncStorage.getItem('progress');
            const progress = raw ? JSON.parse(raw) : {};

            // Delete
            await AsyncStorage.removeItem('user_name');
            ```
            """),
            "Build a bookmarks app: a FlatList of articles, each with a bookmark toggle icon. Persist bookmarked items in AsyncStorage so they survive app restarts.",
            "Which React Native component should you use instead of ScrollView when rendering a large, unknown-length list?\nA) View  B) FlatList  C) SectionList  D) ScrollView",
            "Build a grocery list app: add items via TextInput, check them off, delete by swipe gesture, persist to AsyncStorage, and show a progress bar of checked/total items.",
            "Never call `AsyncStorage` in the render function — call it inside `useEffect` on mount. Wrap calls in try/catch since storage can fail on low-memory devices.",
            60)
        created += r; updated += not r

        r = upsert(rn, 3,
            "Project: Movie Browser App with TMDB API",
            "Build a polished React Native movie browser: search movies, view details, manage a watchlist, and handle pagination — using The Movie Database (TMDB) free API.",
            textwrap.dedent("""\
            ## Project Architecture
            ```
            src/
            ├── api/tmdb.js         # API calls
            ├── screens/
            │   ├── HomeScreen.js   # Trending movies
            │   ├── SearchScreen.js # Search
            │   └── DetailScreen.js # Movie detail
            ├── components/
            │   └── MovieCard.js
            └── store/
                └── watchlist.js    # AsyncStorage helpers
            ```

            ## TMDB API Service
            ```javascript
            const API_KEY = 'YOUR_TMDB_API_KEY';
            const BASE = 'https://api.themoviedb.org/3';
            const IMG = 'https://image.tmdb.org/t/p/w500';

            export const getTrending = async (page = 1) => {
              const res = await fetch(`${BASE}/trending/movie/week?api_key=${API_KEY}&page=${page}`);
              return res.json();
            };

            export const searchMovies = async (query, page = 1) => {
              const res = await fetch(
                `${BASE}/search/movie?api_key=${API_KEY}&query=${encodeURIComponent(query)}&page=${page}`
              );
              return res.json();
            };

            export const getMovieDetail = async (id) => {
              const res = await fetch(`${BASE}/movie/${id}?api_key=${API_KEY}`);
              return res.json();
            };

            export const posterUrl = (path) => path ? `${IMG}${path}` : null;
            ```

            ## Home Screen with Pagination
            ```jsx
            export default function HomeScreen({ navigation }) {
              const [movies, setMovies] = useState([]);
              const [page, setPage] = useState(1);
              const [loading, setLoading] = useState(false);

              const loadMore = useCallback(async () => {
                if (loading) return;
                setLoading(true);
                const data = await getTrending(page);
                setMovies(prev => [...prev, ...data.results]);
                setPage(p => p + 1);
                setLoading(false);
              }, [page, loading]);

              useEffect(() => { loadMore(); }, []);

              return (
                <FlatList
                  data={movies}
                  keyExtractor={item => item.id.toString()}
                  numColumns={2}
                  renderItem={({ item }) => (
                    <MovieCard movie={item}
                      onPress={() => navigation.navigate('Detail', { id: item.id })} />
                  )}
                  onEndReached={loadMore}
                  onEndReachedThreshold={0.5}
                  ListFooterComponent={loading && <ActivityIndicator />}
                />
              );
            }
            ```

            ## Tab Navigation + Bottom Bar
            ```bash
            npm install @react-navigation/bottom-tabs
            ```
            ```jsx
            const Tab = createBottomTabNavigator();
            <Tab.Navigator>
              <Tab.Screen name="Home" component={HomeScreen}
                options={{ tabBarIcon: ({ color }) => <Ionicons name="home" color={color} size={24} /> }} />
              <Tab.Screen name="Search" component={SearchScreen}
                options={{ tabBarIcon: ({ color }) => <Ionicons name="search" color={color} size={24} /> }} />
              <Tab.Screen name="Watchlist" component={WatchlistScreen}
                options={{ tabBarIcon: ({ color }) => <Ionicons name="bookmark" color={color} size={24} /> }} />
            </Tab.Navigator>
            ```
            """),
            "Add a genre filter to the Home screen: fetch genres from the TMDB `/genre/movie/list` endpoint and display filter chips. Filtering by genre should reload the list using the `/discover/movie` endpoint.",
            "Which React Navigation pattern should you use for main app sections that users switch between frequently (like Home, Search, Profile)?\nA) Stack Navigator  B) Drawer Navigator  C) Bottom Tab Navigator  D) Modal Navigator",
            "Complete the Movie Browser app: trending + search + detail + watchlist + genre filter + pagination. Publish to GitHub with an Expo QR code in the README so the reviewer can test on their phone.",
            "Register for a free TMDB API key at themoviedb.org. Store it in a `.env` file and access via `process.env.EXPO_PUBLIC_TMDB_KEY` — never commit API keys.",
            70)
        created += r; updated += not r

        # ── MYSQL ─────────────────────────────────────────────────────────
        mysql = LearningPath.objects.get(slug='mysql')

        r = upsert(mysql, 1,
            "MySQL Fundamentals — DDL, DML & Queries",
            "Install MySQL, create databases and tables with DDL, insert and query data with DML, and use WHERE, ORDER BY, LIMIT, and aggregate functions.",
            textwrap.dedent("""\
            ## What is MySQL?
            MySQL is the world's most popular open-source relational database. It powers WordPress, Facebook, Twitter, and millions of web apps. It stores data in tables with rows and columns, and you query it with SQL (Structured Query Language).

            ## Installation & First Connection
            ```bash
            # Install (Ubuntu)
            sudo apt install mysql-server
            sudo mysql_secure_installation

            # Connect
            mysql -u root -p
            ```

            ## DDL — Data Definition Language
            DDL defines the *structure* of your database.

            ```sql
            -- Create database
            CREATE DATABASE academy;
            USE academy;

            -- Create table
            CREATE TABLE students (
                id        INT AUTO_INCREMENT PRIMARY KEY,
                name      VARCHAR(100) NOT NULL,
                email     VARCHAR(150) UNIQUE NOT NULL,
                course    VARCHAR(80),
                level     ENUM('beginner','intermediate','advanced') DEFAULT 'beginner',
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            -- Modify table
            ALTER TABLE students ADD COLUMN score INT DEFAULT 0;
            ALTER TABLE students MODIFY COLUMN course VARCHAR(120);

            -- Delete table
            DROP TABLE IF EXISTS old_table;
            ```

            ## DML — Data Manipulation Language
            DML reads and modifies the *data* in tables.

            ```sql
            -- INSERT
            INSERT INTO students (name, email, course, level)
            VALUES ('Alice Osei', 'alice@example.com', 'Python', 'beginner'),
                   ('Brian Mwangi', 'brian@example.com', 'Django', 'intermediate'),
                   ('Grace Njeri', 'grace@example.com', 'Machine Learning', 'advanced');

            -- SELECT
            SELECT * FROM students;
            SELECT name, course FROM students WHERE level = 'beginner';
            SELECT * FROM students WHERE name LIKE 'A%' ORDER BY joined_at DESC;
            SELECT * FROM students LIMIT 10 OFFSET 20;

            -- UPDATE
            UPDATE students SET score = 85 WHERE email = 'alice@example.com';

            -- DELETE
            DELETE FROM students WHERE score = 0;
            ```

            ## Aggregate Functions
            ```sql
            SELECT COUNT(*) AS total_students FROM students;
            SELECT AVG(score) AS avg_score FROM students;
            SELECT MAX(score), MIN(score) FROM students;
            SELECT level, COUNT(*) AS count, AVG(score) AS avg
            FROM students
            GROUP BY level
            HAVING AVG(score) > 60
            ORDER BY avg DESC;
            ```
            """),
            "Create an `academy` database with `students`, `courses`, and `enrollments` tables. Insert 10 students and 5 courses. Write queries to find: (1) all students in a specific course, (2) average score per course, (3) top 3 students by score.",
            "Which SQL clause filters groups created by GROUP BY — similar to WHERE but applied after aggregation?\nA) HAVING  B) WHERE  C) FILTER  D) ORDER BY",
            "Design a complete `school` database: tables for teachers, subjects, classes, and grades. Insert realistic sample data and write 5 queries answering questions like 'Which teacher has the highest average grade?'",
            "Always use parameterised queries in application code (`%s` placeholders) — never concatenate user input into SQL strings. Raw concatenation causes SQL injection vulnerabilities.",
            50)
        created += r; updated += not r

        r = upsert(mysql, 2,
            "MySQL Joins, Indexes, Transactions & Stored Procedures",
            "Write multi-table JOIN queries, create indexes for performance, manage data integrity with transactions, and automate logic with stored procedures and triggers.",
            textwrap.dedent("""\
            ## JOIN Types
            ```sql
            -- Sample tables
            -- students(id, name, email)
            -- enrollments(id, student_id, course_id, grade)
            -- courses(id, title, instructor)

            -- INNER JOIN — only matching rows
            SELECT s.name, c.title, e.grade
            FROM students s
            INNER JOIN enrollments e ON s.id = e.student_id
            INNER JOIN courses c ON e.course_id = c.id
            WHERE e.grade >= 70;

            -- LEFT JOIN — all students, even unenrolled
            SELECT s.name, c.title
            FROM students s
            LEFT JOIN enrollments e ON s.id = e.student_id
            LEFT JOIN courses c ON e.course_id = c.id;

            -- Self JOIN — find students in the same course
            SELECT a.name AS student1, b.name AS student2, c.title
            FROM students a
            JOIN enrollments ea ON a.id = ea.student_id
            JOIN enrollments eb ON ea.course_id = eb.course_id AND ea.student_id <> eb.student_id
            JOIN students b ON eb.student_id = b.id
            JOIN courses c ON ea.course_id = c.id;
            ```

            ## Indexes — query performance
            ```sql
            -- Add index on frequently queried column
            CREATE INDEX idx_students_email ON students(email);
            CREATE INDEX idx_enroll_student ON enrollments(student_id);

            -- Composite index for multi-column WHERE clauses
            CREATE INDEX idx_enroll_composite ON enrollments(student_id, course_id);

            -- Check index usage with EXPLAIN
            EXPLAIN SELECT * FROM students WHERE email = 'alice@example.com';

            -- Show all indexes on a table
            SHOW INDEX FROM students;
            ```

            ## Transactions — ACID guarantees
            ```sql
            START TRANSACTION;

            INSERT INTO enrollments (student_id, course_id) VALUES (1, 3);
            UPDATE courses SET enrolled_count = enrolled_count + 1 WHERE id = 3;

            -- Commit if everything succeeded
            COMMIT;

            -- Or rollback if something failed
            ROLLBACK;
            ```

            ## Stored Procedures
            ```sql
            DELIMITER //

            CREATE PROCEDURE EnrollStudent(
                IN p_student_id INT,
                IN p_course_id INT,
                OUT p_result VARCHAR(50)
            )
            BEGIN
                DECLARE already INT DEFAULT 0;
                SELECT COUNT(*) INTO already
                FROM enrollments
                WHERE student_id = p_student_id AND course_id = p_course_id;

                IF already > 0 THEN
                    SET p_result = 'already_enrolled';
                ELSE
                    INSERT INTO enrollments (student_id, course_id) VALUES (p_student_id, p_course_id);
                    SET p_result = 'enrolled';
                END IF;
            END //

            DELIMITER ;

            -- Call it
            CALL EnrollStudent(1, 3, @result);
            SELECT @result;
            ```

            ## Triggers — automatic actions
            ```sql
            CREATE TRIGGER after_enrollment_insert
            AFTER INSERT ON enrollments
            FOR EACH ROW
            BEGIN
                UPDATE courses
                SET enrolled_count = enrolled_count + 1
                WHERE id = NEW.course_id;
            END;
            ```
            """),
            "Write a JOIN query finding the top-performing student in each course (highest grade per course_id). Then create an index that speeds up this query and verify with EXPLAIN.",
            "Which JOIN type returns all rows from the left table plus matching rows from the right table, with NULLs for unmatched right rows?\nA) INNER JOIN  B) RIGHT JOIN  C) LEFT JOIN  D) CROSS JOIN",
            "Build a stored procedure `TransferCredits` that moves a student from one course to another in a single transaction: delete the old enrollment, insert the new one, update both course enrollment counts — rollback if any step fails.",
            "Index columns used in WHERE, JOIN ON, and ORDER BY clauses. Avoid over-indexing — each index slows INSERT/UPDATE. Use `EXPLAIN` to verify indexes are being used.",
            60)
        created += r; updated += not r

        r = upsert(mysql, 3,
            "Project: Library Management System in MySQL",
            "Design and build a complete relational database for a library: books, members, loans, and fines — with full CRUD, stored procedures, and reporting queries.",
            textwrap.dedent("""\
            ## Schema Design
            ```sql
            CREATE DATABASE library;
            USE library;

            CREATE TABLE books (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                isbn        VARCHAR(20) UNIQUE,
                title       VARCHAR(200) NOT NULL,
                author      VARCHAR(150),
                genre       VARCHAR(60),
                total_copies INT DEFAULT 1,
                available   INT DEFAULT 1,
                added_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE members (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                name        VARCHAR(100) NOT NULL,
                email       VARCHAR(150) UNIQUE NOT NULL,
                phone       VARCHAR(20),
                joined_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
                status      ENUM('active','suspended') DEFAULT 'active'
            );

            CREATE TABLE loans (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                book_id     INT NOT NULL,
                member_id   INT NOT NULL,
                loaned_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
                due_date    DATETIME NOT NULL,
                returned_at DATETIME,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (member_id) REFERENCES members(id)
            );

            CREATE TABLE fines (
                id        INT AUTO_INCREMENT PRIMARY KEY,
                loan_id   INT NOT NULL,
                amount    DECIMAL(6,2) NOT NULL,
                paid      BOOLEAN DEFAULT FALSE,
                issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (loan_id) REFERENCES loans(id)
            );
            ```

            ## Key Stored Procedures
            ```sql
            -- Borrow a book
            DELIMITER //
            CREATE PROCEDURE BorrowBook(IN p_book INT, IN p_member INT, IN p_days INT)
            BEGIN
                DECLARE avail INT;
                SELECT available INTO avail FROM books WHERE id = p_book FOR UPDATE;
                IF avail < 1 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No copies available';
                END IF;
                UPDATE books SET available = available - 1 WHERE id = p_book;
                INSERT INTO loans (book_id, member_id, due_date)
                VALUES (p_book, p_member, DATE_ADD(NOW(), INTERVAL p_days DAY));
            END //
            DELIMITER ;
            ```

            ## Reporting Queries
            ```sql
            -- Overdue loans with member details
            SELECT m.name, b.title, l.due_date,
                   DATEDIFF(NOW(), l.due_date) AS days_overdue
            FROM loans l
            JOIN members m ON l.member_id = m.id
            JOIN books b ON l.book_id = b.id
            WHERE l.returned_at IS NULL AND l.due_date < NOW()
            ORDER BY days_overdue DESC;

            -- Most borrowed books
            SELECT b.title, b.author, COUNT(l.id) AS times_borrowed
            FROM books b LEFT JOIN loans l ON b.id = l.book_id
            GROUP BY b.id ORDER BY times_borrowed DESC LIMIT 10;

            -- Members with unpaid fines
            SELECT m.name, m.email, SUM(f.amount) AS total_owed
            FROM members m
            JOIN loans l ON m.id = l.member_id
            JOIN fines f ON l.id = f.loan_id
            WHERE f.paid = FALSE
            GROUP BY m.id ORDER BY total_owed DESC;
            ```
            """),
            "Add a `ReturnBook` stored procedure that: marks the loan returned, restores book availability, calculates a fine (KSh 5/day overdue) if late, and inserts into the fines table.",
            "Which MySQL constraint ensures that a loan's book_id must match an existing book in the books table?\nA) UNIQUE  B) CHECK  C) FOREIGN KEY  D) NOT NULL",
            "Complete the Library Management System: seed with 20 books, 10 members, 15 loans (some overdue). Write a Python script using mysql-connector-python to call BorrowBook and ReturnBook procedures and print a daily overdue report.",
            "Use `FOREIGN KEY` constraints with `ON DELETE RESTRICT` to prevent orphaned records. Test referential integrity by trying to delete a book that has active loans — it should fail.",
            65)
        created += r; updated += not r

        # ── FIREBASE ──────────────────────────────────────────────────────
        firebase = LearningPath.objects.get(slug='firebase')

        r = upsert(firebase, 1,
            "Firebase Fundamentals — Firestore & Authentication",
            "Set up a Firebase project, authenticate users with Email/Password and Google Sign-In, and read/write data to Cloud Firestore.",
            textwrap.dedent("""\
            ## What is Firebase?
            Firebase is Google's Backend-as-a-Service (BaaS) platform. It provides authentication, real-time databases, file storage, cloud functions, and hosting — with SDKs for web, iOS, Android, and Flutter.

            ## Project Setup
            1. Go to console.firebase.google.com
            2. Create a project → add a web app
            3. Copy the config object

            ```bash
            npm create vite@latest academy-app -- --template react
            cd academy-app
            npm install firebase
            ```

            ```javascript
            // src/firebase.js
            import { initializeApp } from 'firebase/app';
            import { getFirestore } from 'firebase/firestore';
            import { getAuth } from 'firebase/auth';

            const firebaseConfig = {
              apiKey: import.meta.env.VITE_API_KEY,
              authDomain: "academy-app.firebaseapp.com",
              projectId: "academy-app",
              storageBucket: "academy-app.appspot.com",
              messagingSenderId: "123456789",
              appId: "1:123456789:web:abcdef"
            };

            const app = initializeApp(firebaseConfig);
            export const db = getFirestore(app);
            export const auth = getAuth(app);
            ```

            ## Authentication
            ```javascript
            import {
              createUserWithEmailAndPassword,
              signInWithEmailAndPassword,
              signInWithPopup,
              GoogleAuthProvider,
              signOut,
              onAuthStateChanged
            } from 'firebase/auth';

            // Register
            const register = async (email, password) => {
              const { user } = await createUserWithEmailAndPassword(auth, email, password);
              return user;
            };

            // Login
            const login = async (email, password) => {
              const { user } = await signInWithEmailAndPassword(auth, email, password);
              return user;
            };

            // Google Sign-In
            const googleSignIn = async () => {
              const provider = new GoogleAuthProvider();
              const { user } = await signInWithPopup(auth, provider);
              return user;
            };

            // Listen for auth state
            onAuthStateChanged(auth, (user) => {
              if (user) console.log('Logged in:', user.email);
              else console.log('Logged out');
            });
            ```

            ## Cloud Firestore CRUD
            ```javascript
            import {
              collection, doc,
              addDoc, setDoc, getDoc, getDocs,
              updateDoc, deleteDoc,
              query, where, orderBy, limit
            } from 'firebase/firestore';

            // CREATE
            await addDoc(collection(db, 'courses'), {
              title: 'Python Programming',
              level: 'beginner',
              createdAt: new Date(),
              authorId: auth.currentUser.uid
            });

            // READ one
            const snap = await getDoc(doc(db, 'courses', 'doc-id'));
            if (snap.exists()) console.log(snap.data());

            // READ many with query
            const q = query(
              collection(db, 'courses'),
              where('level', '==', 'beginner'),
              orderBy('createdAt', 'desc'),
              limit(10)
            );
            const snapshot = await getDocs(q);
            snapshot.forEach(doc => console.log(doc.id, doc.data()));

            // UPDATE
            await updateDoc(doc(db, 'courses', 'doc-id'), { level: 'intermediate' });

            // DELETE
            await deleteDoc(doc(db, 'courses', 'doc-id'));
            ```
            """),
            "Build a React app with Firebase Auth (email/password + Google). After login, show a protected dashboard that lists the user's saved courses from Firestore. Implement logout.",
            "Which Firebase feature listens for real-time changes to a document or collection without polling?\nA) getDocs()  B) onSnapshot()  C) getDoc()  D) runTransaction()",
            "Build a bookmarks app: authenticated users can save/unsave URLs with titles and tags. Each user only sees their own bookmarks (use Firestore security rules: `request.auth.uid == resource.data.userId`).",
            "Set Firestore Security Rules before going to production. The default `allow read, write: if false` blocks everything — write rules that match your authentication model.",
            50)
        created += r; updated += not r

        r = upsert(firebase, 2,
            "Firestore Real-Time, Cloud Storage & Cloud Functions",
            "Use onSnapshot for live data updates, store and retrieve files with Cloud Storage, and run server-side logic with Cloud Functions.",
            textwrap.dedent("""\
            ## Real-Time Listeners with onSnapshot
            ```javascript
            import { onSnapshot, collection, query, orderBy } from 'firebase/firestore';

            // Listen to a collection in real-time
            const unsubscribe = onSnapshot(
              query(collection(db, 'messages'), orderBy('createdAt', 'asc')),
              (snapshot) => {
                const messages = snapshot.docs.map(doc => ({
                  id: doc.id, ...doc.data()
                }));
                setMessages(messages);
              },
              (error) => console.error('Listener error:', error)
            );

            // Cleanup on component unmount
            useEffect(() => unsubscribe, []);
            ```

            ## Cloud Storage — file uploads
            ```javascript
            import { getStorage, ref, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage';

            const storage = getStorage();

            // Upload a file
            const uploadFile = async (file, path) => {
              const storageRef = ref(storage, path);
              const snapshot = await uploadBytes(storageRef, file);
              const downloadURL = await getDownloadURL(snapshot.ref);
              return downloadURL;
            };

            // Usage in React
            const handleUpload = async (e) => {
              const file = e.target.files[0];
              if (!file) return;
              const url = await uploadFile(file, `avatars/${auth.currentUser.uid}`);
              await updateDoc(doc(db, 'users', auth.currentUser.uid), { avatar: url });
            };
            ```

            ## Cloud Functions (Node.js)
            ```bash
            npm install -g firebase-tools
            firebase login
            firebase init functions
            ```

            ```javascript
            // functions/index.js
            const { onCall, HttpsError } = require('firebase-functions/v2/https');
            const { onDocumentCreated } = require('firebase-functions/v2/firestore');
            const admin = require('firebase-admin');
            admin.initializeApp();

            // Callable function (from client SDK)
            exports.sendWelcomeEmail = onCall(async (request) => {
              const { email, name } = request.data;
              if (!request.auth) throw new HttpsError('unauthenticated', 'Must be logged in');
              // Send email via SendGrid, Mailgun, etc.
              return { success: true, message: `Welcome email sent to ${email}` };
            });

            // Firestore trigger
            exports.onNewMessage = onDocumentCreated('messages/{msgId}', async (event) => {
              const msg = event.data.data();
              console.log('New message:', msg.text, 'by', msg.authorId);
              // Update message count, send push notification, etc.
            });
            ```

            ```javascript
            // Call from client
            import { getFunctions, httpsCallable } from 'firebase/functions';
            const functions = getFunctions();
            const sendWelcome = httpsCallable(functions, 'sendWelcomeEmail');
            await sendWelcome({ email: 'user@example.com', name: 'Alice' });
            ```
            """),
            "Build a real-time note-taking app: notes update live (without refresh) using onSnapshot. Allow attaching images via Cloud Storage. Show a loading spinner while the image uploads.",
            "What is the correct way to clean up a Firestore onSnapshot listener when a React component unmounts?\nA) Call firestore.cleanup()  B) Return the unsubscribe function from useEffect  C) Use useCallback  D) Listeners clean up automatically",
            "Build a real-time collaborative to-do list using Firestore onSnapshot: multiple browser tabs show the same list, updating live. Add Cloud Functions to send an email when a task is marked done.",
            "onSnapshot listeners continue billing even if the tab is hidden. Unsubscribe in useEffect cleanup and re-subscribe on page visibility to reduce Firestore read costs.",
            60)
        created += r; updated += not r

        r = upsert(firebase, 3,
            "Project: Real-Time Chat App with Firebase",
            "Build a fully-featured chat app: room-based messaging, user authentication, file sharing, message reactions, read receipts, and push notifications.",
            textwrap.dedent("""\
            ## Firestore Data Model
            ```
            rooms/
              {roomId}/
                name: "General"
                createdBy: "uid123"
                members: ["uid1", "uid2", "uid3"]
                lastMessage: { text, authorName, createdAt }
                messages/                    ← subcollection
                  {messageId}/
                    text: "Hello everyone!"
                    authorId: "uid123"
                    authorName: "Alice"
                    authorAvatar: "https://..."
                    createdAt: Timestamp
                    reactions: { "❤️": ["uid2", "uid3"] }
                    readBy: ["uid1", "uid2"]
                    fileUrl: null
            ```

            ## Chat Room Component
            ```jsx
            function ChatRoom({ roomId }) {
              const [messages, setMessages] = useState([]);
              const [text, setText] = useState('');
              const bottomRef = useRef(null);

              useEffect(() => {
                const q = query(
                  collection(db, `rooms/${roomId}/messages`),
                  orderBy('createdAt', 'asc'), limit(50)
                );
                return onSnapshot(q, snap => {
                  setMessages(snap.docs.map(d => ({ id: d.id, ...d.data() })));
                  bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
                });
              }, [roomId]);

              const sendMessage = async () => {
                if (!text.trim()) return;
                await addDoc(collection(db, `rooms/${roomId}/messages`), {
                  text: text.trim(),
                  authorId: auth.currentUser.uid,
                  authorName: auth.currentUser.displayName,
                  createdAt: serverTimestamp(),
                  reactions: {},
                  readBy: [auth.currentUser.uid],
                });
                setText('');
              };

              return (
                <div className="chat-room">
                  <div className="messages">
                    {messages.map(msg => <MessageBubble key={msg.id} msg={msg} roomId={roomId} />)}
                    <div ref={bottomRef} />
                  </div>
                  <div className="input-bar">
                    <input value={text} onChange={e => setText(e.target.value)}
                      onKeyDown={e => e.key === 'Enter' && sendMessage()} />
                    <button onClick={sendMessage}>Send</button>
                  </div>
                </div>
              );
            }
            ```

            ## Firestore Security Rules
            ```javascript
            rules_version = '2';
            service cloud.firestore {
              match /databases/{database}/documents {
                match /rooms/{roomId} {
                  allow read: if request.auth != null && request.auth.uid in resource.data.members;
                  allow create: if request.auth != null;
                  match /messages/{msgId} {
                    allow read: if request.auth != null
                      && request.auth.uid in get(/databases/$(database)/documents/rooms/$(roomId)).data.members;
                    allow create: if request.auth != null
                      && request.resource.data.authorId == request.auth.uid;
                  }
                }
              }
            }
            ```
            """),
            "Add emoji reactions to the chat: clicking a reaction toggles the user's UID in the `reactions[emoji]` array using Firestore's `arrayUnion`/`arrayRemove` operations.",
            "Which Firestore operation should you use to add an item to an array field without overwriting the entire array?\nA) updateDoc with the array value  B) arrayUnion  C) setDoc with merge  D) arrayPush",
            "Complete the chat app: authentication, multiple rooms, real-time messages, file uploads, emoji reactions, read receipts, and Firebase Hosting deployment. Share the live URL.",
            "Use Firestore subcollections for messages (not arrays) — subcollections can hold unlimited documents, while an array field in a document is capped at 1 MB.",
            70)
        created += r; updated += not r

        # ── DART ─────────────────────────────────────────────────────────
        dart = LearningPath.objects.get(slug='dart')

        r = upsert(dart, 1,
            "Dart Fundamentals — Syntax, Types & Functions",
            "Learn Dart's type system, variables, control flow, functions, and null safety — the foundation needed before learning Flutter.",
            textwrap.dedent("""\
            ## Why Dart?
            Dart is Google's programming language powering Flutter. It's statically typed, AOT-compiled for fast native execution, and JIT-compiled for hot reload during development. Dart 3 introduced 100% sound null safety.

            ## Variables & Types
            ```dart
            // Explicit types
            String name = 'Alice';
            int age = 20;
            double gpa = 3.75;
            bool isEnrolled = true;

            // Type inference
            var course = 'Python';        // inferred as String
            final maxScore = 100;         // immutable at runtime
            const piValue = 3.14159;      // compile-time constant

            // Null safety — must declare nullable explicitly
            String? nickname;             // nullable (can be null)
            String fullName = 'Bob';      // non-nullable (cannot be null)
            ```

            ## Collections
            ```dart
            // List (ordered, indexed)
            List<String> courses = ['Python', 'Dart', 'Flutter'];
            courses.add('React');
            courses.removeWhere((c) => c.startsWith('R'));
            print(courses.length);

            // Map (key-value)
            Map<String, int> scores = {'Alice': 90, 'Bob': 75};
            scores['Carol'] = 85;
            scores.forEach((name, score) => print('$name: $score'));

            // Set (unique, unordered)
            Set<String> tags = {'dart', 'flutter', 'mobile'};
            tags.add('dart');  // duplicate ignored
            ```

            ## Control Flow
            ```dart
            // if / else if / else
            int score = 82;
            String grade;
            if (score >= 90)       grade = 'A';
            else if (score >= 80)  grade = 'B';
            else if (score >= 70)  grade = 'C';
            else                   grade = 'F';

            // for loop
            for (int i = 1; i <= 5; i++) print('Lesson $i');

            // for-in
            for (var course in courses) print(course);

            // while
            int attempts = 0;
            while (attempts < 3) { attempts++; }

            // switch
            switch (grade) {
              case 'A': print('Distinction'); break;
              case 'B': print('Merit'); break;
              default:  print('Pass');
            }
            ```

            ## Functions
            ```dart
            // Regular function
            int add(int a, int b) => a + b;

            // Optional named parameters
            void greet({required String name, String prefix = 'Student'}) {
              print('Hello, $prefix $name!');
            }
            greet(name: 'Alice');
            greet(name: 'Bob', prefix: 'Dr.');

            // First-class functions
            List<int> scores = [45, 82, 91, 67, 55];
            var passing = scores.where((s) => s >= 60).toList();
            var doubled = scores.map((s) => s * 2).toList();
            var total = scores.reduce((a, b) => a + b);

            // Arrow function
            bool isPass(int s) => s >= 60;
            ```

            ## Null Safety Operators
            ```dart
            String? name;

            // Null-aware access
            print(name?.toUpperCase());    // null if name is null

            // Null coalescing
            String display = name ?? 'Anonymous';

            // Null assertion (throws if null)
            print(name!.toUpperCase());   // use only when sure it's not null

            // Late initialisation
            late String config;           // initialised before first use
            ```
            """),
            "Write a Dart function `gradeReport(Map<String, int> scores)` that returns a formatted string listing each student's name, score, and letter grade. Test it with 5 students.",
            "What does the `??` operator do in Dart?\nA) Divides by zero safely  B) Returns the right operand if the left is null  C) Compares two nullable values  D) Throws an exception if null",
            "Build a Dart CLI grade calculator: read student names and marks from a List, compute mean/median/highest/lowest, and print a formatted report. Use map, where, and reduce.",
            "Prefer `final` over `var` for variables that are assigned once — it documents intent and prevents accidental reassignment. Use `const` for compile-time constants.",
            45)
        created += r; updated += not r

        r = upsert(dart, 2,
            "Dart OOP, Async/Await & Collections",
            "Build classes with inheritance and mixins, handle asynchronous operations with Future and Stream, and use advanced collection operations.",
            textwrap.dedent("""\
            ## Classes & Inheritance
            ```dart
            class Animal {
              final String name;
              final int age;

              Animal({required this.name, required this.age});

              String speak() => '...';

              @override
              String toString() => '$name (age $age)';
            }

            class Dog extends Animal {
              final String breed;
              Dog({required super.name, required super.age, required this.breed});

              @override
              String speak() => 'Woof!';

              void fetch(String item) => print('$name fetches the $item!');
            }

            Dog rex = Dog(name: 'Rex', age: 3, breed: 'German Shepherd');
            print(rex.speak());   // Woof!
            print(rex);           // Rex (age 3)
            ```

            ## Abstract Classes & Interfaces
            ```dart
            abstract class Shape {
              double area();
              double perimeter();
              void describe() => print('Area: ${area().toStringAsFixed(2)}');
            }

            class Circle extends Shape {
              final double radius;
              Circle(this.radius);

              @override double area() => 3.14159 * radius * radius;
              @override double perimeter() => 2 * 3.14159 * radius;
            }

            class Rectangle extends Shape {
              final double w, h;
              Rectangle(this.w, this.h);

              @override double area() => w * h;
              @override double perimeter() => 2 * (w + h);
            }
            ```

            ## Mixins
            ```dart
            mixin Serialisable {
              Map<String, dynamic> toJson();
              String toJsonString() => toJson().toString();
            }

            class Course with Serialisable {
              final String title;
              final int lessons;
              Course(this.title, this.lessons);

              @override
              Map<String, dynamic> toJson() => {'title': title, 'lessons': lessons};
            }
            ```

            ## Async / Await & Future
            ```dart
            Future<String> fetchData(String url) async {
              await Future.delayed(Duration(seconds: 1));  // simulate network
              return '{"status": "ok", "url": "$url"}';
            }

            void main() async {
              print('Fetching...');
              final result = await fetchData('https://api.example.com/courses');
              print('Got: $result');
            }

            // Error handling
            Future<void> safeLoad() async {
              try {
                final data = await fetchData('invalid-url');
                print(data);
              } catch (e) {
                print('Error: $e');
              }
            }
            ```

            ## Streams — continuous async data
            ```dart
            Stream<int> countdown(int from) async* {
              for (int i = from; i >= 0; i--) {
                await Future.delayed(Duration(seconds: 1));
                yield i;
              }
            }

            void main() async {
              await for (int tick in countdown(5)) {
                print(tick == 0 ? 'Launch!' : '$tick...');
              }
            }
            ```

            ## Advanced Collections
            ```dart
            final numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

            // Chained operations
            final result = numbers
              .where((n) => n.isEven)       // [2, 4, 6, 8, 10]
              .map((n) => n * n)             // [4, 16, 36, 64, 100]
              .where((n) => n > 20)          // [36, 64, 100]
              .toList();

            // Spread operator
            final a = [1, 2, 3];
            final b = [0, ...a, 4, 5];      // [0, 1, 2, 3, 4, 5]

            // Collection if/for
            bool showBonus = true;
            final items = [
              'item1', 'item2',
              if (showBonus) 'bonus',
              for (int i = 0; i < 3; i++) 'extra$i',
            ];
            ```
            """),
            "Model a university system in Dart: `Person` base class, `Student` and `Lecturer` subclasses, a `Gradable` mixin with `calculateGrade()`. Create 3 students and 2 lecturers and print a formatted roster.",
            "What is a Dart mixin used for?\nA) Importing external packages  B) Adding reusable functionality to classes without inheritance  C) Declaring abstract methods  D) Creating singletons",
            "Build a Dart library system simulation: `Book` class, `Library` class with add/borrow/return methods, async `searchBooks(String query)` that simulates a 500ms network delay, and a Stream that emits overdue books every 5 seconds.",
            "Use `async*` and `yield` for generators that produce values over time (Streams). Use `sync*` and `yield` for lazy synchronous sequences — both avoid loading everything into memory.",
            55)
        created += r; updated += not r

        r = upsert(dart, 3,
            "Project: CLI Task Manager in Dart",
            "Build a command-line task manager: add, list, complete, and delete tasks — with file persistence, due dates, priority levels, and category filters.",
            textwrap.dedent("""\
            ## Project Structure
            ```
            task_manager/
            ├── bin/main.dart        # CLI entry point
            ├── lib/
            │   ├── task.dart        # Task model
            │   ├── task_store.dart  # Persistence
            │   └── cli.dart         # Command parser
            └── pubspec.yaml
            ```

            ## pubspec.yaml
            ```yaml
            name: task_manager
            version: 1.0.0
            environment:
              sdk: '>=3.0.0 <4.0.0'
            dependencies:
              args: ^2.4.0
            ```

            ## Task Model
            ```dart
            // lib/task.dart
            enum Priority { low, medium, high }

            class Task {
              final String id;
              String title;
              String category;
              Priority priority;
              DateTime? dueDate;
              bool isDone;
              final DateTime createdAt;

              Task({
                required this.title,
                this.category = 'general',
                this.priority = Priority.medium,
                this.dueDate,
                this.isDone = false,
                DateTime? createdAt,
              }) : id = DateTime.now().millisecondsSinceEpoch.toString(),
                   createdAt = createdAt ?? DateTime.now();

              Map<String, dynamic> toJson() => {
                'id': id, 'title': title, 'category': category,
                'priority': priority.name, 'dueDate': dueDate?.toIso8601String(),
                'isDone': isDone, 'createdAt': createdAt.toIso8601String(),
              };

              factory Task.fromJson(Map<String, dynamic> j) => Task(
                title: j['title'], category: j['category'],
                priority: Priority.values.byName(j['priority']),
                dueDate: j['dueDate'] != null ? DateTime.parse(j['dueDate']) : null,
                isDone: j['isDone'], createdAt: DateTime.parse(j['createdAt']),
              )..id_override(j['id']);
            }
            ```

            ## CLI Entry Point
            ```dart
            // bin/main.dart
            import 'dart:io';
            import 'package:args/args.dart';
            import '../lib/task.dart';
            import '../lib/task_store.dart';

            void main(List<String> args) async {
              final store = TaskStore('tasks.json');
              await store.load();

              final parser = ArgParser()
                ..addCommand('add', ArgParser()
                  ..addOption('category', abbr: 'c', defaultsTo: 'general')
                  ..addOption('priority', abbr: 'p', defaultsTo: 'medium')
                  ..addOption('due', abbr: 'd'))
                ..addCommand('list', ArgParser()
                  ..addOption('filter', abbr: 'f'))
                ..addCommand('done')
                ..addCommand('delete');

              final results = parser.parse(args);

              switch (results.command?.name) {
                case 'add':
                  final title = results.command!.rest.join(' ');
                  if (title.isEmpty) { print('Usage: add <title>'); exit(1); }
                  store.add(Task(
                    title: title,
                    category: results.command!['category'],
                    priority: Priority.values.byName(results.command!['priority']),
                    dueDate: results.command!['due'] != null
                        ? DateTime.parse(results.command!['due']) : null,
                  ));
                  await store.save();
                  print('Added: $title');

                case 'list':
                  final filter = results.command?['filter'];
                  final tasks = filter != null
                      ? store.tasks.where((t) => t.category == filter).toList()
                      : store.tasks;
                  for (final t in tasks) {
                    final done = t.isDone ? '[x]' : '[ ]';
                    final due = t.dueDate != null ? ' (due ${t.dueDate!.toLocal().toString().split(' ')[0]})' : '';
                    print('$done ${t.id.substring(0,6)} [${t.priority.name}] ${t.title}$due');
                  }

                default:
                  print('Commands: add, list, done <id>, delete <id>');
              }
            }
            ```

            ## Running
            ```bash
            dart run bin/main.dart add "Learn Flutter" --category mobile --priority high
            dart run bin/main.dart list
            dart run bin/main.dart done 123456
            dart run bin/main.dart list --filter mobile
            ```
            """),
            "Add a `stats` command to the task manager that prints: total tasks, done vs pending, tasks per category, overdue count, and highest-priority pending task.",
            "Which Dart feature allows a class to gain behaviour from multiple sources without using multiple inheritance?\nA) Extends  B) Implements  C) Mixins  D) Abstract classes",
            "Complete the task manager: add, list, done, delete, stats, and due-date reminders (print overdue tasks on startup). Compile to a native executable with `dart compile exe` and submit the binary.",
            "Compile Dart to a native executable with `dart compile exe bin/main.dart -o task_manager`. The binary runs without the Dart SDK installed — great for distributing CLI tools.",
            60)
        created += r; updated += not r

        self.stdout.write(self.style.SUCCESS(
            f"Batch 9 complete: {created} created, {updated} updated"
        ))
