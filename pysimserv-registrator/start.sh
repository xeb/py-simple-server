#!/bin/sh
while test $# -gt 0; do
        case "$1" in
                --interface*)
                        export INTERFACE=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                *)
                        break
                        ;;
        esac
done

export HOSTIP=$(ifconfig `echo $INTERFACE` | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
echo "Running..."
echo "/bin/registrator -ip=$HOSTIP $1"
/bin/registrator -ip=$HOSTIP $1
