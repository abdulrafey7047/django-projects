#Perform a quick update on your instance:
sudo yum update -y
 
#Install git in your EC2 instance
sudo yum install git -y
 
#Check git version
echo "GIT VERSION:" | git version
