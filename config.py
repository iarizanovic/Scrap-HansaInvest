######################################################
# Author: Ivan Arizanovic <ivanarizanovic@yahoo.com> #
######################################################

debug_mode: bool = False                  # Print debug information and warnings
execution_time: bool = False              # Print Execution time
summary: bool = True                      # Print summary information
max_entries: int = 200                    # Max number of read data
start_time_str: str = "12:00"             # Time when first iteration will be started. Format: <hour>:<minutes>
repeating_period: int = 24 * 60 * 60      # Repeating period in seconds
root_disk_location: str = "c:\\Projects"  # Root disk location for scraped data
