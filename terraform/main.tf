terraform {
    required_providers {
        digitalocean = {
            source = "digitalocean/digitalocean"
            version = "~> 2.0"
        }
    }
}

variable "do_token" {}

# Configuring the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "app_server" {
    image = "ubuntu-22-04-x64"
    name = "demo-dia-programador"
    region = "nyc1"
    size = "s-1vcpu-1gb"
}