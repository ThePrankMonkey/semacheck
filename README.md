# semacheck
Polls SemaConnect for open spaces, using Selenium.

## bash_profile

Add the following to `~/.bash_profile` to allow you to execute this script with `evcheck`.

### Variables

export SEMAUSER='<EMAIL>'
export SEMAPASS='<PASS>'
export SEMASEARCH='"<ADDRESS>"'

### Aliases

alias evcheck="/Path/To/semacheck.py --username $SEMAUSER --password $SEMAPASS --search $SEMASEARCH"
