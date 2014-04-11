#!/bin/bash
kill -9 $(ps aux | grep python | awk '{print $2}')
