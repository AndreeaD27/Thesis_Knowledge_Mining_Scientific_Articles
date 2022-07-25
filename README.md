# Thesis 2022 - Knowledge Mining in Scientific Articles

This is the code base for the Bachelor's Thesis 2022 - Knowledge Mining in Scientific Articles done by Andreea-Ioana Dan at the University of Groningen in partnership with Microsoft Netherlands.

To find the written thesis, please access the folder `thesis_docs`. 

To find the articles used as data source, please access the folder `thesis_docs/articles`.

To run the venv:
From the parent folder -> thesis_venv/Scripts/activate  <-- in terminal (to activate it for the terminal)

## Possible requirementes for installation: 
If these are already installed, skip this.

`pip install azure-ai-textanalytics`\
`pip install azure-core`\
`pip install gremlinpython --user`\
`pip install gremlinpython==3.4.13 --user Install-Module -Name Az.CosmosDB > 1400 RU`

Installing AZ:  
https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?view=azps-8.0.0

To update powershell:  \
`iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI"`\
-> 
`Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force -AllowClobber` <-- in terminal

Sign in:\
 `Connect-AzAccount`  -> opens a new window -> sign in into azure

`Uninstall-AzureRm` <-- from older version of PowerShell

## Code

*Disclaimer: in the file `.env`, the environment variables that contain the names and keys for the services should be valid in order for the code to work. Currently, due to privacy concerns, the keys and names of the used services have been removed. Please populate the fields with your personal ones.*