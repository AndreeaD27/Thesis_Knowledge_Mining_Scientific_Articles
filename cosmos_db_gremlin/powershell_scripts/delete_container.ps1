# Reference: Az.CosmosDB | https://docs.microsoft.com/powershell/module/az.cosmosdb
# --------------------------------------------------
# Purpose
# Delete a graph from a database in CosmosDB
# --------------------------------------------------
param([string] $graphName)
# --------------------------------------------------
# --------------------------------------------------
# Variables - ***** SUBSTITUTE YOUR VALUES *****
$resourceGroupName = "Thesis" # Resource Group must already exist
$accountName = "cosmosdbgremlinstudent" # Must be all lower case
$databaseName = "article-database-cosmos"
$graphName = $graphName
# --------------------------------------------------
Remove-AzCosmosDBGremlinGraph -ResourceGroupName $resourceGroupName -AccountName $accountName -DatabaseName $databaseName -Name $graphName