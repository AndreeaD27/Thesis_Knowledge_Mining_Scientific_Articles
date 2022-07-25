# Reference: Az.CosmosDB | https://docs.microsoft.com/powershell/module/az.cosmosdb
# --------------------------------------------------
# Purpose
# Create Cosmos Gremlin API account, database, and graph
# with dedicated throughput and conflict resolution policy
# with last writer wins and custom resolver path
# --------------------------------------------------

param([string] $graphName)
# --------------------------------------------------
# --------------------------------------------------
# Variables - ***** SUBSTITUTE YOUR VALUES *****
$resourceGroupName = "thesis" # Resource Group must already exist
$accountName = "th-cosmos-gremlin" # Must be all lower case
$databaseName = "article-database-cosmos"
$graphName = $graphName
$graphRUs = 400
$partitionKeys = @("/pk")
# --------------------------------------------------

Remove-AzCosmosDBGremlinGraph -ResourceGroupName $resourceGroupName -AccountName $accountName -DatabaseName $databaseName -Name $graphName