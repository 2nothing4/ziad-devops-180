output "container_id" {
  description = "ID of the created container"
  value       = docker_container.nginx.id
}

output "container_name" {
  description = "Name of the created container"
  value       = docker_container.nginx.name
}
