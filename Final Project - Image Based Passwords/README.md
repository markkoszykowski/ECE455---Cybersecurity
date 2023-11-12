# Picture Password
### ECE455 - Cybersecurity
### Rebecca Gartenberg & Mark Koszykowski

Install requirements:
  
    pip3 install -r ${PROJECT_DIRECTORY}/requirements.txt

Run backend locally:

    export FLASK_APP="backend"
    flask run

Run frontend locally:
  
    cd  ~/${PROJECT_DIRECTORY}/frontend/
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    . ~/.nvm/nvm.sh
    nvm install 16.13.0
    npm install react-scripts

To host code on AWS (must have AWS credentials):
    
    ./aws/create_ec2.sh
    ./aws/deploy.sh
    // Edit ip address in /image-based-pw/frontend/src/components/Home.js
    ssh -i ~/.ssh/pems/ece455_FinalProject.pem ec2-user@<assigned_ip_address>
    ./aws/run.sh

To shutdown service:

    ./aws/terminate.sh

To download database file:

    scp -i ~/.ssh/pems/ece455_FinalProject.pem ec2-user@<assigned_ip_address>:~/image-based-pw/backend/db.sqlite ~/Desktop/
