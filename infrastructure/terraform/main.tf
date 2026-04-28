provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "devex" {
  name     = "rg-${var.project_name}-devex-${var.environment}"
  location = var.location
}

# --- Developer Hub Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "devex_k8s" {
  name                = "aks-devex-iq-${var.environment}"
  location            = azurerm_resource_group.devex.location
  resource_group_name = azurerm_resource_group.devex.name
  dns_prefix          = "devex-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Effectiveness Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-devex-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.devex.name
  location               = azurerm_resource_group.devex.location
  version                = "13"
  administrator_login    = "devexadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Search & Discovery (OpenSearch / Elastic - Optional) ---

resource "azurerm_search_service" "discovery" {
  name                = "search-devex-discovery-${var.environment}"
  resource_group_name = azurerm_resource_group.devex.name
  location            = azurerm_resource_group.devex.location
  sku                 = "standard"
}

# --- Multi-Cloud Resilience (AWS S3 Telemetry Sink) ---

resource "aws_s3_bucket" "telemetry" {
  bucket = "db-devex-telemetry-sink-${var.environment}"
}
