#!/bin/bash
source "/vagrant/scripts/common.sh"

function installR {
	echo "install R"
	yum install -y R
	yum install -y libxml2-devel libcurl-devel 
	Rscript /vagrant/resources/install-packages.R
}

echo "setup R"
installR