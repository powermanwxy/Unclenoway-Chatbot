#!/bin/bash

function install_mongodb() {
    case "$OSTYPE" in
	    (*linux-gnu*) platform='linux/';
		      mongodb_file='mongodb-linux-x86_64-3.6.4.tgz';
		      mongodb_path='mongodb-linux-x86_64-3.6.4';;
	    (*darwin*) platform='osx/';
		       mongodb_file='mongodb-osx-ssl-x86_64-3.6.4.tgz';
		       mongodb_path='mongodb-osx-x86_64-3.6.4';;
	    (*) echo "error: unsupported platform $uname.";
		exit 2;;
	esac;

	mongo_url='https://fastdl.mongodb.org/'
	echo "Downloading MongoDB $mongo_url$platform$mongodb_file..."

	wget $mongo_url$platform$mongodb_file
	tar -zxvf $mongodb_file && cp -R -n $mongodb_path/ mongodb

	echo "Cleaning download files..."
	rm -r $mongodb_path/ && rm $mongodb_file

	cd mongodb/ && export PATH=$PWD:$PATH && cd .. && echo "Setting PATH..."
    
    file='./mongodb/bin/mongod'
    if [ -f "$file" ]
    then
        echo "Install MongoDB Successfuly!"
    else
        echo "Install MongoDB Failed, please install this manualy!"
        exit 2
    fi
}

function install_IPProxy() {
	echo "Installing requirements of IPProxy..."
	case "$OSTYPE" in
	    (*linux-gnu*) sudo apt-get install sqlite3 python-lxml;;
	    (*darwin*) echo "Skip this cause Mac already has built-in sqllite3.";
		       sudo pip install lxml -i https://pypi.tuna.tsinghua.edu.cn/simple;;
	    (*) echo 'error: unsupported platform.';
		exit 2;;
	esac;
	sudo pip install requests chardet web.py sqlalchemy gevent psutil -i https://pypi.tuna.tsinghua.edu.cn/simple

	echo "Downloading IPProxy from https://github.com/qiyeboy/IPProxyPool/archive/master.zip..."
	wget https://github.com/qiyeboy/IPProxyPool/archive/master.zip
	unzip master.zip
	echo "Cleaning download files..."
    rm master.zip

    file='./IPProxyPool-master/IPProxy.py'
    if [ -f "$file" ] 
    then
        echo "Install IPProxy sucessful!"
    else
        echo "Install IPProxy failed, please install manualy!"
        exit 2
    fi
}

function install_PIP_deps() {
	echo "Installing Pip Dependencies..."
	sudo pip install websocket websocket-client==0.37.0 termcolor ChatterBot -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo "Finished intall Pip dependencies."
}

if_parm=0

while getopts "miph" name
do
    case $name in
        m)  echo "Installing MongoDB...";
            sudo echo "Please run as sudo.";
            install_mongodb && if_parm+=1;;

        i)  echo "Installing IPProxy...";
            sudo echo "Please run as sudo.";
            install_IPProxy && if_parm+=1;;

        p)  echo "Installing Pip dependencies...";
            sudo echo "Please run as sudo.";
            install_PIP_deps && if_parm+=1;;
        
        h)  echo -e "Installer Usage:\n";
            echo "./install_dependencies.sh -options";
            echo "      -m  Install MongoDB database only.";
            echo "      -i  Install IPProxy only.";
            echo "      -p  Install Pip dependencies only.";
            echo "      -h  Help";
            exit 2;;
        
        ?)  echo "Unknown parameter";
            exit 2;;
    esac
done

if [ $if_parm -eq '0' ]; then
    sudo echo "Default installing...";
    install_mongodb && install_IPProxy &&install_PIP_deps && echo "Finished installation!";
fi

