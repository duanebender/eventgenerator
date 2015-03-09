#!/bin/bash
source "/vagrant/scripts/common.sh"

function installLocalRStudio {
	echo "installing RStudio from local file"
	yum -y install openssl098e
	yum -y install --nogpgcheck /vagrant/resources/$RSTUDIO_ARCHIVE
}

function installRemoteRStudio {
	echo "installing RStudio"
	yum -y install openssl098e
	curl -o /vagrant/resources/$RSTUDIO_ARCHIVE -O -L $RSTUDIO_MIRROR_DOWNLOAD
	yum -y install --nogpgcheck /vagrant/resources/$RSTUDIO_ARCHIVE
}

function installRStudio {
	if resourceExists $RSTUDIO_ARCHIVE; then
		installLocalRStudio
	else
		installRemoteRStudio
	fi
	mkdir /vagrant/share
}

echo "setup RStudio"
installRStudio