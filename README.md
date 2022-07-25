# Thesis
To run the venv:
From the parent folder -> thesis_venv/Scripts/activate  <-- in terminal (to activate it for the terminal)

install:
pip install azure-ai-textanalytics
pip install azure-core
pip install gremlinpython --user

pip install gremlinpython==3.4.13 --user
Install-Module -Name Az.CosmosDB
> 1400 RU

Installing AZ: 
https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?view=azps-8.0.0

To update powershell:  iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI"
-> 
Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force -AllowClobber <-- in terminal

Sign in: Connect-AzAccount  -> opens a new window -> sign in into azure

Uninstall-AzureRm <-- from older version of PowerShelll

To redeploy functions: 
https://docs.microsoft.com/en-us/azure/developer/javascript/how-to/with-web-app/azure-function-resource-group-management/add-delete-functions-redeploy

Fix charmap error:
https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters

Regex expressions:  
https://www.w3schools.com/python/python_regex.asp

### AZURE:
Create custom skill
https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface
https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-python


Use Text Summarization
https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/text-summarization/quickstart?pivots=programming-language-python

Cognitive Search 
in python: https://docs.microsoft.com/en-us/python/api/overview/azure/search-documents-readme?view=azure-python
REST API: https://docs.microsoft.com/en-us/rest/api/searchservice/search-documents

Tutorial, search from blobs: https://docs.microsoft.com/en-us/azure/search/cognitive-search-tutorial-blob-python

Index overview: https://docs.microsoft.com/en-us/azure/search/search-what-is-an-index

Text analytics: https://docs.microsoft.com/en-in/azure/cognitive-services/language-service/text-analytics-for-health/how-to/call-api?tabs=assertion-detection

Language: https://docs.microsoft.com/en-in/azure/cognitive-services/language-service/overview

Cogn Serv + Machine Learning: https://docs.microsoft.com/en-in/azure/cognitive-services/cognitive-services-and-machine-learning

Cogn Serv + Big Data: https://docs.microsoft.com/en-in/azure/cognitive-services/big-data/cognitive-services-for-big-data

Improve Model Performance: https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/custom-classification/how-to/improve-model

Cogn Search in Jupyter: https://docs.microsoft.com/en-us/azure/search/search-get-started-python

Microsoft Academic: https://www.microsoft.com/en-us/research/project/academic/