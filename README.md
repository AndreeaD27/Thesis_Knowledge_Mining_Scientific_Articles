# Thesis 2022 - Knowledge Mining in Scientific Articles

This is the code base for the Bachelor's Thesis 2022 - Knowledge Mining in Scientific Articles done by Andreea-Ioana Dan at the University of Groningen in partnership with Microsoft Netherlands.

To find the written thesis, please access the folder `thesis_docs`. 

To find the articles used as data source, please access the folder `thesis_docs/articles`.

To run the venv:
From the parent folder -> `thesis_venv/Scripts/activate`  <-- in terminal (to activate it for the terminal)

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

Before running the pipeline, ensure that there are files already located in the Blob container. 

The pipeline starts by running the main file `cognitive_search.py`. Then, it will continue to ingest the documents from the Blob Storage in the cloud and it will apply the Cognitive Search to extract the content. In the file `language_analytics_health.py`, the Cognitive Service Text Analytics for Health is applied and sent over to the `graph_helper.py` in order to reflect the data in the CosmosDB graph. 

In the folder `section_identifier`, we can find the code and setting for the section identification custom Azure function. 

More details about the inner workings of the pipeline can be found in the actual thesis document. 