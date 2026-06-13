variable "image_name" {
  description = "Docker image to deploy"
  type        = string
  default     = "nginx:latest"
}

variable "container_name" {
  description = "Name of the container"
  type        = string
  default     = "ziad-nginx"
}

variable "external_port" {
  description = "External port to expose"
  type        = number
  default     = 8080
}
