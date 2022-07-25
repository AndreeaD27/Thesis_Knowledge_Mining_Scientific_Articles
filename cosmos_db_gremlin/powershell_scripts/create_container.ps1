# Reference: Az.CosmosDB | https://docs.microsoft.com/powershell/module/az.cosmosdb
# --------------------------------------------------
# Purpose
# Create a new graph in a database in CosmosDB
# --------------------------------------------------

param([string] $graphName)
# --------------------------------------------------
# --------------------------------------------------
# Variables
$resourceGroupName = "Thesis" # Resource Group must already exist
$accountName = "cosmosdbgremlinstudent" # Must be all lower case
$databaseName = "article-database-cosmos"
$graphName = "BLA"
$graphRUs = 400
$partitionKeys = @("/pk")
# --------------------------------------------------
$database = Get-AzCosmosDBGremlinDatabase -ResourceGroupName $resourceGroupName -AccountName $accountName -Name $databaseName


Write-Host "Creating graph $graphName"
New-AzCosmosDBGremlinGraph -ParentObject $database `
    -Name $graphName -Throughput $graphRUs `
    -PartitionKeyKind Hash -PartitionKeyPath $partitionKeys 
