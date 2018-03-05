#!/bin/bash

if [ -d .svn ] ; then
  echo "SVN"
  svn status
elif [ -d .git ] ; then
  echo "GIT"
  git status
else
  echo "Neither .svn nor .git"
fi
