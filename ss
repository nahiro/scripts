#!/bin/bash

if [ -d .svn ] ; then
  echo "SVN" >&2
  svn status
elif [ -d .git ] ; then
  echo "GIT" >&2
  git status
else
  echo "Neither .svn nor .git"
fi
