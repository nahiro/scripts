#!/bin/bash

if [ -d .svn ] ; then
  svn status
elif [ -d .git ] ; then
  git status
else
  echo "Neither .svn nor .git"
fi
