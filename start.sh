#!/bin/bash

echo -e "\033[31mStarting proxy pool... \033[0m"

while getopts "p" option;do
    case $option in
    p)
        file='./IPProxyPool-master/IPProxy.py'
        if [ -f "$file" ]
        then
            nohup python -u ./IPProxyPool-master/IPProxy.py >proxy.log 2>&1 &
            echo -e "\033[31mStarting IPProxy successful! \033[0m";
        else
            echo -e "\033[31mStarting IPProxy failed! Making sure you disable proxy in ./src/config.py\033[0m";
        fi;;
    *)
        echo "Wrong parameter."
        exit 2;;
    esac
done

file='./mongodb/bin/mongod'
if [ -f "$file" ]
then
    echo -e "\033[31mMaking new dir for mongodb database... \033[0m"
    mkdir db
    export PATH=./mongodb/bin:$PATH

    echo -e '\033[31mStarting database...\033[0m'
    if mongod --dbpath ./db/ --logpath ./db.log --fork ;then
      echo -e "\033[31mStarting mongodb successful! \033[0m";
      export PYTHONIOENCODING=utf-8
      #nohup python -u ./src/main.py > out.log 2>&1 &
      cd src/
      python main.py
    else
      echo -e "\033[31mStarting mongofb failed! \033[0m";
      exit 2
    fi
else
   echo -e "\033[31mCan't find MongoDB!\033[0m"; 
fi


