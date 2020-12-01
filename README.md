This is Group 10's project submission for ADC F2020.

The script "scan.py" awaits input from a PDF417 scanner to read the PDF417 codes on the backs of driver's licenses.
Then the script works on the data, then either writes the specific data to either a .csv file or a .db file.
If written to the .db file, run "server.py", which hosts a local Flask webserver on the device (for me it was a Raspberry Pi 4)
and displays the .db file in a table format.

In order for new scans to appear on the web server, you must refresh the page each time you expect to see new entries. The server does not automatically refresh to see new  entries.

ON THE TODO LIST:
Add a remove button on the web server to be able to remove foul entries.
Add sorting buttons to be able to sort the table.
Add a manual entry form in case of a fouled PDF417 bar code that is unable to be read.
