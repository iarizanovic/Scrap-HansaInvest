# Scrap HansaInvest
The service download first 200 fund data (PDF fund documents) once a day from HansaInvest website and save them to a file.
It will be repeated every day in specified time, which can be changed in *config.py* file.
The metadata of the downloaded files will be saved as CSV data file.

## Usage
Start the *main.py* file:
```
python .\main.py
```

## Configuration
*config.py* file contain all configuration variables, which can be edited:

| Variable           | Description                                                                                    |
|--------------------|------------------------------------------------------------------------------------------------|
| debug_mode         | Print debug information and warnings (by default False)                                        |
| execution_time     | Print Execution time (by default False)                                                        |
| summary            | Print summary information (by default True)                                                    |
| max_entries        | Max number of read data (by default 200)                                                       |
| start_time_str     | Time when first iteration will be started. Format: "\<hour\>:\<minutes\>" (by default "12:00") |
| repeating_period   | Repeating period in seconds                                                                    |
| root_disk_location | Root disk location for scraped data (by default "c:\\Projects")                                |

## Dependencies
Following dependencies are required (*requirements.txt* file contains all of them):
- requests
- pandas
- selenium

## Description
WEB Data source:
https://fondswelt.hansainvest.com/de/downloads-und-formulare/download-center

Physical data structure (folder view):
```{root disk location}\FundDatabase\{DataSource}\{ISIN}\{pdf file document name}```

Example:
```c:\Projects\FundDatabase\Hansainvest\DE000A3CNGL5\JB-BIT-Global-Crypto-Leaders-08-2022.pdf```

Logical structure/model that is recorded in a file (meta data):
- File name: ```fundDatabase.csv```
- Location: ```c:\Projects\FundDatabase\fundDatabase.csv```

Model structure:
```ISIN,DocumentType,EffectiveDate,DownloadDate,DownloadUrl,FilePath,MD5Hash,FileSize```

| Name          | Description                                                                                                                                                                                                      |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ISIN          | International Securities Identification Number.<br/>It’s in the first column of the data table together with the name of the fund.                                                                               |
| DocumentType  | PDF document type. It can have the following values:<br/>- Verkaufsprospekt (prospectus) second column<br/>- Jahresbericht (annual report) third column<br/>- Halbjahresbericht (semiannualreport) fourth column |
| EffectiveDate | Represents the date of validity of a particular type of document and is found as data in the column of the corresponding type of document                                                                        |
| DownloadDate  | Date of document download                                                                                                                                                                                        |
| DownloadUrl   | Document download link url                                                                                                                                                                                       |
| FilePath      | The path of the downloaded file on the disk                                                                                                                                                                      |
| MD5Hash       | Hash code of the downloaded pdf file                                                                                                                                                                             |
| FileSize      | Size of the downloaded file                                                                                                                                                                                      |

The service analyzes the web data source once a day and download the first 200 fund data described by the model above. 
Data that has already been downloaded in one of the previous fetches should not be downloaded again.

## Example of scraped data
Examples of scraped data can be found in *FundDatabase_example* directory.

## Author
Ivan Arizanovic <ivanarizanovic@yahoo.com>
