#Ensure that your software packages are up to date
sudo yum update -y

#Add the Jenkins repo
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo\

#Import a key file from Jenkins-CI to enable installatio
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

#Install Java
sudo yum upgrade
sudo amazon-linux-extras install java-openjdk11 -y

#Install Jenkins
sudo yum install jenkins -y

#Enable the Jenkins service to start at boot
sudo systemctl enable jenkins

#Start Jenkins as a service
sudo systemctl start jenkins

